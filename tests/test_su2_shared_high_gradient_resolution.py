import unittest

from tools.audit_su2_high_gradient_resolution import audit


class Su2SharedHighGradientResolutionTests(unittest.TestCase):
    def test_exact_vertex_samples_separate_coarse_floor_from_n64(self):
        result = audit("protocols/su2-shared-high-gradient-v1.json")
        rows = result["rows"]
        self.assertEqual([row["n"] for row in rows], [16, 32, 64])
        self.assertEqual([row["operator_floor"] for row in rows], ["FAIL", "FAIL", "PASS"])
        self.assertLess(rows[2]["gradient_peak_relative_error_floor"], .05)
        self.assertLess(rows[2]["vorticity_peak_relative_error_floor"], .05)


if __name__ == "__main__":
    unittest.main()
