import unittest

from tools.check_high_gradient_global_peaks import certify_global_peaks


class HighGradientGlobalPeakTests(unittest.TestCase):
    def test_n4_continuum_gradient_and_vorticity_peaks_have_exact_global_certificates(self):
        result = certify_global_peaks()

        self.assertEqual(result["peaks_at_time_zero"], {
            "gradient_frobenius": "sqrt(65)/8",
            "vorticity": "9/8",
        })
        self.assertEqual(result["attainment_point"], {
            "x": "pi/(2*N)", "y": "0", "z": "0", "N": 4,
        })
        self.assertEqual(
            result["bernstein_certificate_degrees"],
            {"gradient_sin_branch": [8, 8],
             "gradient_cos_branch": [8, 8],
             "vorticity_sin_branch": [8, 8],
             "vorticity_cos_branch": [8, 8]},
        )
        self.assertEqual(result["all_gap_bernstein_coefficients_nonnegative"], True)
        self.assertEqual(result["envelope_derivative_identities"], {
            "first_derivative_square": True,
            "second_derivative": True,
        })


if __name__ == "__main__":
    unittest.main()
