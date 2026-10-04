import json
import unittest
from pathlib import Path

from tools.audit_high_gradient_width_sweep import audit


class HighGradientWidthSweepTests(unittest.TestCase):
    def test_default_sweep_spans_broad_to_concentrated_envelopes(self):
        result = audit(n_values=(16, 32))
        self.assertEqual([row["envelope_power"] for row in result["widths"]],
                         [1, 2, 4, 8, 16, 32])
        narrow = result["widths"][-1]
        self.assertEqual(narrow["rows"][0]["cells_per_highest_envelope_wavelength"],
                         0.5)

    def test_power_four_rows_reproduce_the_frozen_fd2_floor(self):
        frozen = json.loads(Path(
            "evidence/tests/high-gradient-fd2-resolution-floor.json"
        ).read_text())
        result = audit(envelope_powers=(4,), n_values=(16, 32, 64, 128))
        observed = {row["n"]: row for row in result["widths"][0]["rows"]}
        self.assertEqual(result["status"], "ANALYTIC_REFERENCE_ONLY")
        self.assertEqual(result["scope"], frozen["scope"])
        for row in frozen["rows"]:
            current = observed[row["n"]]
            self.assertEqual(current["gradient_stencil_floor_relative_error"],
                             row["exact_solution_fd2_gradient_peak_relative_error"])
            self.assertEqual(current["vorticity_stencil_floor_relative_error"],
                             row["exact_solution_fd2_vorticity_peak_relative_error"])

    def test_frozen_width_protocol_has_two_reference_resolved_fine_grids(self):
        protocol_path = Path("protocols/high-gradient-of13-width-v1.json")
        protocol = json.loads(protocol_path.read_text())
        result = audit(tuple(protocol["envelope_powers"]),
                       tuple(protocol["spatial_matrix"]["cell_counts"]),
                       str(protocol_path))
        self.assertEqual([row["envelope_power"] for row in result["widths"]],
                         [1, 2, 4])
        required = set(protocol["reference_resolution_gate"][
            "required_fine_grid_counts"])
        for width in result["widths"]:
            by_n = {row["n"]: row for row in width["rows"]}
            self.assertTrue(all(by_n[n]["gradient_floor_within_threshold"]
                                and by_n[n]["vorticity_floor_within_threshold"]
                                for n in required))
            self.assertFalse(by_n[32]["gradient_floor_within_threshold"])
            self.assertFalse(by_n[32]["vorticity_floor_within_threshold"])
        self.assertFalse(protocol["reference_resolution_gate"][
            "continuous_extrema_certified"])
        self.assertEqual(protocol["expected_unique_cases"], 15)

    def test_coarse_reference_floor_is_reported_without_assuming_monotonicity(self):
        result = audit(envelope_powers=(2, 4, 8), n_values=(16, 32))
        by_power = {row["envelope_power"]: row for row in result["widths"]}
        self.assertGreater(by_power[2]["near_peak_equivalent_gaussian_sigma"],
                           by_power[4]["near_peak_equivalent_gaussian_sigma"])
        self.assertGreater(by_power[4]["near_peak_equivalent_gaussian_sigma"],
                           by_power[8]["near_peak_equivalent_gaussian_sigma"])
        for width in by_power.values():
            for row in width["rows"]:
                self.assertGreater(row["gradient_stencil_floor_relative_error"],
                                   row["gradient_threshold"])
                self.assertGreater(row["vorticity_stencil_floor_relative_error"],
                                   row["vorticity_threshold"])
        self.assertEqual(result["continuous_extrema"], "NOT_CERTIFIED")


if __name__ == "__main__":
    unittest.main()
