import copy
import unittest
from fractions import Fraction
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.extract_finite_cutoff_schedule import extract_schedule


def sample_input():
    return {
        "schema_version": 1,
        "bound_provenance": "synthetic test values only; not source bounds",
        "h_lower": "1/2",
        "q_min": "1/8",
        "initial_scale_lower_bound": 1,
        "coefficient_upper_bounds": {
            str(j): {str(m): "1" for m in range(j + 3)}
            for j in range(1, 8)
        },
    }


class FiniteCutoffScheduleTests(unittest.TestCase):
    def test_exact_schedule_and_terminal_zero_prefix(self):
        result = extract_schedule(sample_input())
        rows = result["schedule"]
        self.assertEqual([row["schedule_scale"] for row in rows],
                         [1, 4, 8, 16])
        self.assertEqual(result["terminal_zero_from_stage"], 3)
        self.assertEqual(result["finite_prefix_last_stage"], 2)
        self.assertEqual(Fraction(1, 8) * rows[-1]["schedule_scale"], 2)
        self.assertTrue(all(row.get("all_jet_bounds_verified", True)
                            for row in rows))

    def test_fractional_coefficient_uses_exact_integer_arithmetic(self):
        data = sample_input()
        data["coefficient_upper_bounds"]["1"] = {
            "0": "3/2", "1": "3/2", "2": "3/2", "3": "3/2"
        }
        result = extract_schedule(data)
        # For j=1 and h_lower=1/2, a >= 4*(3/2)^2 = 9 exactly.
        self.assertEqual(result["schedule"][1]["stage_threshold"], 9)

    def test_rejects_missing_certificate_metadata(self):
        data = sample_input()
        data["bound_provenance"] = ""
        with self.assertRaisesRegex(ValueError, "bound_provenance"):
            extract_schedule(data)

    def test_rejects_missing_jet_order(self):
        data = sample_input()
        del data["coefficient_upper_bounds"]["2"]["4"]
        with self.assertRaisesRegex(ValueError, "jet orders"):
            extract_schedule(data)

    def test_rejects_noncanonical_jet_order(self):
        data = sample_input()
        value = data["coefficient_upper_bounds"]["1"].pop("0")
        data["coefficient_upper_bounds"]["1"]["00"] = value
        with self.assertRaisesRegex(ValueError, "canonical"):
            extract_schedule(data)

    def test_rejects_incomplete_stage_prefix(self):
        data = sample_input()
        del data["coefficient_upper_bounds"]["2"]
        with self.assertRaisesRegex(ValueError, "missing certified"):
            extract_schedule(data)


if __name__ == "__main__":
    unittest.main()
