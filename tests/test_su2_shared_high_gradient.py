import csv
import json
import tempfile
import unittest
from pathlib import Path

import numpy as np

from tools.analyze_su2 import analyze
from tools.high_gradient_reference import fields
from tools.su2_case import generate
from tools.run_su2_high_gradient_study import case_pairs


class Su2SharedHighGradientTests(unittest.TestCase):
    def test_protocol_deduplicates_shared_spatial_temporal_case(self):
        protocol = {"cases": {"spatial": [[16, .001], [64, .001]],
                              "temporal": [[64, .001], [64, .0005]]}}
        self.assertEqual(case_pairs(protocol), [(16, .001), (64, .001), (64, .0005)])

    def test_case_records_vertex_sampled_shared_mms(self):
        with tempfile.TemporaryDirectory() as temp:
            case = Path(temp) / "case"
            generate(case, n=4, dt=.05, end=.05, inner=2,
                     profile="high-gradient", frequency=4)
            params = json.loads((case / "parameters.json").read_text())
            self.assertEqual(params["profile"], "high-gradient")
            self.assertEqual(params["frequency"], 4)
            self.assertIn("MARKER_PERIODIC=", (case / "case.cfg").read_text())
            self.assertEqual((case / "mesh.su2").read_text().splitlines()[0], "NDIME= 3")

    def test_case_rejects_frequency_different_from_frozen_adapter(self):
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaisesRegex(ValueError, "compiled adapter frequency"):
                generate(Path(temp) / "case", n=4, profile="high-gradient", frequency=8)

    def test_analyzer_uses_shared_mms_at_completed_solution_time(self):
        n, end = 4, .05
        with tempfile.TemporaryDirectory() as temp:
            case = Path(temp) / "case"
            generate(case, n=n, dt=end, end=end, inner=2,
                     profile="high-gradient", frequency=4)
            params = json.loads((case / "parameters.json").read_text())
            params["quality_thresholds"] = {
                "velocity_relative_l2": .02, "energy_relative_error": .02,
                "max_gradient_relative_error_samples": .05,
                "max_vorticity_relative_error_samples": .05,
                "shell_spectrum_relative_l1": .05}
            (case / "parameters.json").write_text(json.dumps(params))
            (case / "exit_code").write_text("0\n")
            (case / "solver.log").write_text("Exit Success (SU2_CFD)\n")
            with (case / "history.csv").open("w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Time_Iter", "Cur_Time", "rms[P]", "rms[U]", "rms[V]", "rms[W]"])
                writer.writerow([0, 0, -11, -11, -11, -11])
            axis = np.linspace(0, 2*np.pi, n+1)
            xyz = np.array(np.meshgrid(axis, axis, axis, indexing="ij")).reshape(3, -1).T
            velocity = fields(xyz, N=4, nu=.01, time=end)["u"]
            data = np.column_stack((xyz, velocity))
            np.savetxt(case / "restart_00000.csv", data, delimiter=",",
                       header="x,y,z,Velocity_x,Velocity_y,Velocity_z", comments="")
            result = analyze(case)
            self.assertEqual(result["mms_profile"], "high-gradient")
            self.assertAlmostEqual(result["updated_solution_time"], .05)
            self.assertAlmostEqual(result["expected_last_source_time"], 0.0)
            self.assertAlmostEqual(result["reported_history_time"], 0.0)
            self.assertLess(result["velocity_relative_l2"], 1e-14)
            self.assertLess(result["energy_relative_error"], 1e-14)
            self.assertEqual(result["quality_sampled"], "FAIL")


if __name__ == "__main__":
    unittest.main()
