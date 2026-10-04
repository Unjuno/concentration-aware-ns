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
from tools.su2_case import generate


class Su2SharedHighGradientReplayTests(unittest.TestCase):
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
