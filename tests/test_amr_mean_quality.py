import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

import numpy as np

from tools.summarize_amr_mean_quality import summarize
from tools.amr_derivative_projection import derivative_moments
from tools.high_gradient_acceptance import local_quality
from tools.high_gradient_cell_average import exact_cell_average_velocity
from tools.analyze_amr_mean_quality import stage_metrics, verify_cube_coverage
from tools.run_amr_mean_quality import generate_case, PROTOCOL


def uniform_cells(n):
    h = 2*np.pi/n
    axis = (np.arange(n)+.5)*h
    coordinates = np.stack(np.meshgrid(axis, axis, axis, indexing="ij"), axis=-1).reshape(-1, 3)
    return coordinates, np.full(n**3, h**3), h


class AmrMeanQualityTests(unittest.TestCase):
    def setUp(self):
        self.spec = json.loads(PROTOCOL.read_text())

    def test_new_protocol_has_three_grids_common_map_time_and_distinct_time_control(self):
        cases = self.spec["cases"]
        self.assertEqual([c["n"] for c in cases[:3]], [16, 32, 64])
        self.assertEqual(self.spec["model"]["frequency"], 3)
        self.assertEqual(self.spec["model"]["end"], .05)
        self.assertEqual({c["refine_interval"]*c["dt"] for c in cases}, {.002})
        self.assertEqual([(c["n"], c["dt"]) for c in cases if c["dt"] != .001], [(32, .0005)])
        self.assertEqual(self.spec["quality"]["gradient_mean_mismatch_relative_l2"], .05)
        self.assertEqual([c["id"] for c in cases if c["capture_disabled_control"]], ["n16-dt0.001"])

    def test_cube_coverage_rejects_equal_volume_overlap_and_hole(self):
        c, v, h = uniform_cells(8)
        widths = np.full(len(v), h)
        self.assertEqual(verify_cube_coverage(c, widths, 8)["finest_voxels"], 16**3)
        c[1] = c[0]  # Total volume and cell counts remain unchanged.
        with self.assertRaisesRegex(ValueError, "overlaps or holes"):
            verify_cube_coverage(c, widths, 8)

    def test_exact_means_pass_named_gate_despite_large_p0_floor(self):
        c, v, h = uniform_cells(8)
        u = exact_cell_average_velocity(c, h, .05, 3)
        g = derivative_moments(c, np.full(len(v), h), .05, 3)["gradient_mean"]
        result = stage_metrics(c, v, u, g, g, 8, .05, 3)
        self.assertEqual(local_quality(result["metrics"], self.spec["quality"])["status"], "PASS")
        self.assertGreater(result["derivative_decomposition"]["gradient"]["projection_floor_relative_l2"], .5)
        self.assertEqual(result["continuous_extrema"], "NOT_CERTIFIED_FOR_THE_NUMERICAL_FIELD")
        self.assertEqual(result["spectrum"], "UNAVAILABLE_PENDING_VALIDATED_NONUNIFORM_RECONSTRUCTION")

    def test_known_mean_error_fails_without_changing_representation_floor(self):
        c, v, h = uniform_cells(8)
        u = exact_cell_average_velocity(c, h, .05, 3)
        g = derivative_moments(c, np.full(len(v), h), .05, 3)["gradient_mean"]
        oracle = stage_metrics(c, v, u, g, g, 8, .05, 3)
        reference_energy = oracle["derivative_decomposition"]["gradient"]["exact_reference_integrated_energy"]
        shifted = g.copy(); shifted[:, 1, 0] += .06*np.sqrt(reference_energy/v.sum())
        result = stage_metrics(c, v, u, shifted, g, 8, .05, 3)
        self.assertAlmostEqual(result["metrics"]["gradient_mean_mismatch_relative_l2"], .06, places=13)
        self.assertEqual(local_quality(result["metrics"], self.spec["quality"])["status"], "FAIL")
        self.assertEqual(result["derivative_decomposition"]["gradient"]["projection_floor_relative_l2"],
                         oracle["derivative_decomposition"]["gradient"]["projection_floor_relative_l2"])

    def test_nan_tensor_cannot_become_quality_pass(self):
        c, v, h = uniform_cells(8)
        u = exact_cell_average_velocity(c, h, .05, 3)
        g = derivative_moments(c, np.full(len(v), h), .05, 3)["gradient_mean"]
        for array in (u, g):
            with self.subTest(shape=array.shape):
                bad = array.copy(); bad.flat[-1] = np.nan
                with self.assertRaises(ValueError):
                    stage_metrics(c, v, bad if array is u else u,
                                  bad if array is g else g, g, 8, .05, 3)

    def test_matrix_missing_control_underresolution_and_mixed_results_stay_uncertain(self):
        results = [{"status": "COMPLETE_SPECIFIED_MEAN_GATE_ANALYSIS", "case_id": c["id"],
            "case": c, "model": self.spec["model"], "source_commit": "a"*40,
            "protocol_sha256": "frozen", "standard_acceptance": {"status": "PASS"},
            "instrumentation_control": "BYTE_IDENTICAL_FINAL_U_AND_P" if c["capture_disabled_control"] else "separate",
            "stages": [{"stage": stage, "time": time, "reference_operator_quality": {"status": "PASS"},
                        "local_mean_quality": {"status": "FAIL"}} for stage, time in
                       self.spec["measurements"]["state_times"].items()]} for c in self.spec["cases"]]
        self.assertEqual(summarize(results, self.spec, "frozen")["status"], "REPRODUCED_SPECIFIED_MEAN_GATE_DISCREPANCY")
        self.assertEqual(summarize(results[:-1], self.spec, "frozen")["status"], "UNCERTAIN")
        for mutation in ("control", "reference", "mixed", "source", "protocol", "time", "standard"):
            broken = copy.deepcopy(results)
            if mutation == "control": broken[0]["instrumentation_control"] = "UNVERIFIED"
            if mutation == "reference": broken[1]["stages"][0]["reference_operator_quality"]["status"] = "FAIL"
            if mutation == "mixed": broken[1]["stages"][-1]["local_mean_quality"]["status"] = "PASS"
            if mutation == "source": broken[1]["source_commit"] = "b"*40
            if mutation == "protocol": broken[1]["protocol_sha256"] = "changed"
            if mutation == "time": broken[1]["stages"][0]["time"] = .004
            if mutation == "standard": broken[3]["standard_acceptance"]["status"] = "FAIL"
            with self.subTest(mutation=mutation):
                self.assertEqual(summarize(broken, self.spec, "frozen")["status"], "UNCERTAIN")
        for row in results:
            for stage in row["stages"]: stage["local_mean_quality"]["status"] = "PASS"
        self.assertEqual(summarize(results, self.spec, "frozen")["status"], "NOT_OBSERVED")
        with self.assertRaisesRegex(ValueError, "duplicate"):
            summarize(results+results[:1], self.spec, "frozen")

    def test_disabled_control_has_identical_input_bytes_and_n3_model(self):
        case = self.spec["cases"][0]
        with tempfile.TemporaryDirectory() as temp:
            a, b = Path(temp)/"main", Path(temp)/"control"
            first, second = generate_case(a, case, self.spec), generate_case(b, case, self.spec)
            self.assertEqual(first, second)
            params = json.loads((a/"parameters.json").read_text())
            self.assertEqual(params["frequency"], 3)
            self.assertEqual(params["n"], 16)
            self.assertEqual(params["nu"], .01)
            self.assertIn("const scalar frequency = 3.0;", (a/"constant/fvModels").read_text())
            self.assertEqual(first["system/fvSolution"], hashlib.sha256((a/"system/fvSolution").read_bytes()).hexdigest())
            with self.assertRaises(ValueError):
                generate_case(a, case, self.spec)


if __name__ == "__main__":
    unittest.main()
