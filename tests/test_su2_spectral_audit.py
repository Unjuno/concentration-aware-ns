import unittest

import numpy as np

from tools.su2_spectral_audit import compare_shell_spectra


class Su2SpectralAuditTests(unittest.TestCase):
    def test_zero_padding_and_three_way_decomposition(self):
        result = compare_shell_spectra([1.0, 2.0], [1.0], [1.0, 1.0, 1.0], 4.0)
        self.assertAlmostEqual(result["solver_samples_vs_analytic_samples_l1"], .5)
        self.assertAlmostEqual(result["analytic_samples_vs_continuum_l1"], .5)
        self.assertAlmostEqual(result["solver_samples_vs_continuum_l1"], .5)
        self.assertGreaterEqual(result["triangle_residual"], 0)

    def test_identical_spectra_have_zero_contrast(self):
        result = compare_shell_spectra([0.2, 0.8], [0.2, 0.8], [0.2, 0.8], 1)
        self.assertEqual(result["solver_samples_vs_analytic_samples_l1"], 0)
        self.assertEqual(result["analytic_samples_vs_continuum_l1"], 0)
        self.assertEqual(result["solver_samples_vs_continuum_l1"], 0)

    def test_invalid_inputs_are_rejected(self):
        for args in (
            ([-1], [0], [0], 1),
            ([np.nan], [0], [0], 1),
            ([0], [0], [0], 0),
            ([[0]], [0], [0], 1),
        ):
            with self.assertRaises(ValueError):
                compare_shell_spectra(*args)


if __name__ == "__main__":
    unittest.main()
