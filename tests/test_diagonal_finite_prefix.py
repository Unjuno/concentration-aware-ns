import unittest

from tools.check_diagonal_finite_prefix import audit, diagonal_sum, stage


class DiagonalFinitePrefixTests(unittest.TestCase):
    def test_each_fixed_stage_decays_but_growing_sum_stays_bounded_away_from_zero(self):
        for j in (1, 2, 8, 32):
            self.assertEqual(stage(j, 1 / 512), 1 / 512)
            self.assertEqual(stage(j, 1 / 2048), 1 / 2048)
        for n in (8, 16, 32, 64, 128):
            self.assertGreaterEqual(diagonal_sum(1 / n), 1)
            self.assertLessEqual(diagonal_sum(1 / n), 2)

    def test_audit_record_passes(self):
        self.assertTrue(audit()["success"])


if __name__ == "__main__":
    unittest.main()
