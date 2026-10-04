import csv
import hashlib
import json
import shutil
import tarfile
import tempfile
import unittest
from pathlib import Path

import numpy as np

from tools.analyze_su2 import analyze
from tools.high_gradient_reference import fields
from tools.replay_su2_high_gradient_study import review
from tools.run_su2_high_gradient_study import aggregate_case_artifacts, case_pairs
from tools.su2_case import generate


class Su2SharedHighGradientReplayTests(unittest.TestCase):
    def _write_case_workers(self, root, missing=(), image_ids=None):
        protocol_path = Path("protocols/su2-shared-high-gradient-v1.json")
        protocol = json.loads(protocol_path.read_text())
        labels = [f"n{n}-dt{dt:g}" for n, dt in case_pairs(protocol)]
        image_ids = image_ids or {}
        for index, label in enumerate(labels):
            if label in missing:
                continue
            n, dt = case_pairs(protocol)[index]
            worker = root / f"worker-{label}" / "run"
            worker.mkdir(parents=True)
            shutil.copy2(protocol_path, worker / "protocol.json")
            shutil.copy2("runtime/su2/high_gradient.patch", worker / "high_gradient.patch")
            archive = worker / f"{label}.tar.gz"
            with tarfile.open(archive, "w:gz") as tar:
                payload = root / f"payload-{label}.txt"
                payload.write_text(label)
                tar.add(payload, arcname=f"{label}/payload.txt")
            digest = hashlib.sha256(archive.read_bytes()).hexdigest()
            row = {"case": label, "n": n, "dt": dt, "planned_steps": round(.05/dt),
                   "exit_code": 0,
                   "standard_acceptance": "FAIL" if n == 16 else "PASS",
                   "quality_sampled": "FAIL", "archive_sha256": digest}
            (worker / "summary.json").write_text(json.dumps({
                "study_id": protocol["study_id"], "status": "INCOMPLETE",
                "expected_cases": len(labels), "attempted_cases": 1,
                "protocol_sha256": hashlib.sha256(protocol_path.read_bytes()).hexdigest(),
                "image": "same-image", "image_id": image_ids.get(label, "sha256:identical"),
                "cases": [row],
            }))
        return protocol_path, labels

    def test_parallel_case_aggregation_separates_coverage_from_acceptance(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            workers = root / "workers"
            workers.mkdir()
            protocol_path, labels = self._write_case_workers(workers)
            result = aggregate_case_artifacts(workers, protocol_path, root / "aggregate")

            self.assertEqual(result["status"], "COMPLETE")
            self.assertEqual(result["standard_acceptance"], "FAIL")
            self.assertEqual(result["attempted_cases"], len(labels))
            self.assertEqual(result["missing_cases"], [])
            self.assertTrue((root / "aggregate" / "n64-dt0.00025.tar.gz").is_file())

    def test_parallel_case_aggregation_keeps_missing_cases_incomplete(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            workers = root / "workers"
            workers.mkdir()
            protocol_path, labels = self._write_case_workers(workers, missing={"n64-dt0.001"})
            result = aggregate_case_artifacts(workers, protocol_path, root / "aggregate")

            self.assertEqual(result["status"], "INCOMPLETE")
            self.assertEqual(result["standard_acceptance"], "INCOMPLETE")
            self.assertEqual(result["missing_cases"], ["n64-dt0.001"])
            self.assertEqual(result["attempted_cases"], len(labels) - 1)

    def test_parallel_case_aggregation_rejects_different_solver_images(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            workers = root / "workers"
            workers.mkdir()
            protocol_path, _ = self._write_case_workers(
                workers, image_ids={"n32-dt0.001": "sha256:different"}
            )
            with self.assertRaisesRegex(ValueError, "one shared image"):
                aggregate_case_artifacts(workers, protocol_path, root / "aggregate")

    def test_replay_checks_archive_integrity_and_recomputes_metrics(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "run"
            root.mkdir()
            case_name = "n4-dt0.05"
            protocol = {
                "study_id": "fixture", "status": "frozen before execution",
                "adapter": {"frequency_N": 4},
                "time": {"end": .05},
                "cases": {"spatial": [[4, 0.05]], "temporal": [], "expected_cases": 1}}
            protocol_path = root / "protocol.json"
            protocol_path.write_text(json.dumps(protocol))
            shutil.copy2("runtime/su2/high_gradient.patch", root / "high_gradient.patch")
            case = root / case_name
            generate(case, n=4, dt=.05, end=.05, inner=2,
                     profile="high-gradient", frequency=4)
            params = json.loads((case / "parameters.json").read_text())
            params.update({"study_id": "fixture", "protocol_sha256": hashlib.sha256(protocol_path.read_bytes()).hexdigest(),
                           "image": "fixture-image", "image_id": "sha256:fixture",
                           "nu": .01, "rho": 1.0,
                           "quality_thresholds": {"velocity_relative_l2": .02,
                               "energy_relative_error": .02,
                               "max_gradient_relative_error_samples": .05,
                               "max_vorticity_relative_error_samples": .05,
                               "shell_spectrum_relative_l1": .05}})
            (case / "parameters.json").write_text(json.dumps(params, indent=2))
            (case / "exit_code").write_text("0\n")
            (case / "solver.log").write_text("Exit Success (SU2_CFD)\n")
            with (case / "history.csv").open("w", newline="") as f:
                w = csv.writer(f)
                w.writerow(["Time_Iter", "Cur_Time", "rms[P]", "rms[U]", "rms[V]", "rms[W]"])
                w.writerow([0, 0, -11, -11, -11, -11])
            axis = np.linspace(0, 2*np.pi, 5)
            xyz = np.array(np.meshgrid(axis, axis, axis, indexing="ij")).reshape(3, -1).T
            u = fields(xyz, N=4, nu=.01, time=.05)["u"]
            np.savetxt(case / "restart_00000.csv", np.column_stack((xyz, u)), delimiter=",",
                       header="x,y,z,Velocity_x,Velocity_y,Velocity_z", comments="")
            metrics = analyze(case)
            (case / "diagnostics.json").write_text(json.dumps(metrics, indent=2))
            archive_path = root / f"{case_name}.tar.gz"
            with tarfile.open(archive_path, "w:gz") as tar:
                tar.add(case, arcname=case_name)
            archive_sha = hashlib.sha256(archive_path.read_bytes()).hexdigest()
            (root / "summary.json").write_text(json.dumps({
                "study_id": "fixture", "status": "COMPLETE", "expected_cases": 1,
                "attempted_cases": 1, "protocol_sha256": hashlib.sha256(protocol_path.read_bytes()).hexdigest(),
                "image": "fixture-image", "image_id": "sha256:fixture",
                "cases": [{"case": case_name, "n": 4, "dt": .05, "planned_steps": 1,
                           "exit_code": 0, "standard_acceptance": "PASS",
                           "quality_sampled": metrics["quality_sampled"],
                           "metrics": metrics, "archive_sha256": archive_sha}]}, indent=2))
            result = review(root)
            self.assertEqual(result["reviewed_cases"], 1)
            self.assertEqual(result["cases"][0]["replay_status"], "PASS")


if __name__ == "__main__":
    unittest.main()
