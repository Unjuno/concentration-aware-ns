import unittest

from tools.verify_openfoam_high_gradient_matrix import verify_matrix


class OpenFoamHighGradientMatrixReplayTests(unittest.TestCase):
    def test_current_six_case_index_replays_from_published_archives(self):
        result = verify_matrix()
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["case_count"], 6)
        self.assertEqual(result["matrix_reproduction"], "NOT_OBSERVED")
        self.assertEqual(
            [case["observed_steps"] for case in result["cases"]],
            [50, 50, 50, 50, 100, 200],
        )
        self.assertEqual(
            [case["standard_acceptance"] for case in result["cases"]],
            ["PASS"] * 6,
        )
        self.assertEqual(
            [case["local_quality"] for case in result["cases"]],
            ["FAIL", "FAIL", "PASS", "PASS", "PASS", "PASS"],
        )


if __name__ == "__main__":
    unittest.main()
