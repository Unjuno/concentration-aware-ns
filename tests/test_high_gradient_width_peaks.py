import unittest
from fractions import Fraction

import numpy as np
import sympy as sp

from tools.check_high_gradient_width_peaks import certify_width_peaks, _width_branches
from tools.high_gradient_reference import fields


class HighGradientWidthPeakTests(unittest.TestCase):
    def test_frozen_widths_have_exact_continuum_peak_certificates(self):
        result = certify_width_peaks()

        self.assertEqual(result["envelope_powers"], [1, 2, 4])
        self.assertEqual(result["frequency_N"], 4)
        expected = {
            "1": {"gradient_frobenius_squared": "1025/1024", "vorticity_squared": "1089/1024"},
            "2": {"gradient_frobenius_squared": "257/256", "vorticity_squared": "289/256"},
            "4": {"gradient_frobenius_squared": "65/64", "vorticity_squared": "81/64"},
        }
        for power, peaks in expected.items():
            with self.subTest(power=power):
                self.assertEqual(result["peaks_squared_at_time_zero"][power], peaks)
                self.assertTrue(result["width_certificates"][power]["all_gap_bernstein_coefficients_nonnegative"])
                self.assertTrue(result["width_certificates"][power]["attained_at_center"])

    def test_width_certificate_contains_exact_branch_gaps(self):
        result = certify_width_peaks()
        for power in ("1", "2", "4"):
            with self.subTest(power=power):
                branches = result["width_certificates"][power]["branches"]
                self.assertEqual(set(branches), {
                    "gradient_sin_branch", "gradient_cos_branch",
                    "vorticity_sin_branch", "vorticity_cos_branch",
                })
                self.assertTrue(all(branch["all_nonnegative"] for branch in branches.values()))
                self.assertTrue(all(
                    all(Fraction(value) >= 0 for value in branch["gap_bernstein_coefficients"])
                    for branch in branches.values()
                ))

    def test_symbolic_branch_formulas_match_independent_field_evaluator(self):
        s, r = sp.symbols("s r", real=True)
        points = np.array([
            [0.13, -1.1, 0.25],
            [0.43, 0.7, -0.9],
            [0.88, 1.4, 2.1],
        ])
        for power in (1, 2, 4):
            branches = _width_branches(power, s, r)
            evaluate = {
                name: sp.lambdify((s, r), expr, "numpy")
                for name, expr in branches.items()
            }
            exact = fields(points, N=4, time=0.17, envelope_power=power)
            for point, gradient, vorticity in zip(
                points, exact["grad_u"], exact["vorticity"]
            ):
                sv, rv = np.sin(point[1] / 2) ** 2, np.sin(point[2] / 2) ** 2
                sine2, cosine2 = np.sin(4 * point[0]) ** 2, np.cos(4 * point[0]) ** 2
                predicted_gradient2 = np.exp(-0.34) * (
                    evaluate["gradient_sin_branch"](sv, rv) * sine2
                    + evaluate["gradient_cos_branch"](sv, rv) * cosine2
                )
                predicted_vorticity2 = np.exp(-0.34) * (
                    evaluate["vorticity_sin_branch"](sv, rv) * sine2
                    + evaluate["vorticity_cos_branch"](sv, rv) * cosine2
                )
                self.assertAlmostEqual(np.sum(gradient**2), predicted_gradient2, places=12)
                self.assertAlmostEqual(np.sum(vorticity**2), predicted_vorticity2, places=12)


if __name__ == "__main__":
    unittest.main()
