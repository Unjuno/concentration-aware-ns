import unittest

import numpy as np

from tools.su2_local_derivative_audit import (
    audit_derivative_fields,
    centered_gradient,
    curl_from_gradient,
)


class Su2LocalDerivativeAuditTests(unittest.TestCase):
    def test_centered_gradient_uses_periodic_axes(self):
        n = 16
        axis = 2*np.pi*np.arange(n)/n
        x, y, z = np.meshgrid(axis, axis, axis, indexing="ij")
        field = np.zeros((n, n, n, 3))
        field[..., 0] = np.sin(x)
        gradient = centered_gradient(field)
        np.testing.assert_allclose(
            gradient[..., 0, 0], np.cos(x)*np.sin(2*np.pi/n)/(2*np.pi/n),
            atol=1e-14)
        np.testing.assert_allclose(gradient[..., 0, 1:], 0, atol=0)

    def test_curl_convention(self):
        gradient = np.zeros((4, 4, 4, 3, 3))
        gradient[..., 2, 1] = 1
        gradient[..., 1, 2] = -1
        expected = np.zeros((4, 4, 4, 3))
        expected[..., 0] = 2
        np.testing.assert_allclose(curl_from_gradient(gradient), expected)

    def test_error_enrichment_locates_error_in_high_gradient_region(self):
        exact = np.zeros((4, 4, 4, 3, 3))
        exact[0, 0, 0, 0, 1] = 10
        sampled_fd = exact.copy()
        actual_fd = exact.copy()
        actual_fd[0, 0, 0, 0, 1] += 1
        result = audit_derivative_fields(actual_fd, sampled_fd, exact)
        gradient = result["gradient_solver_fd_vs_reference_fd"]
        self.assertEqual(gradient["top_concentration_fraction"], 7/64)
        self.assertAlmostEqual(gradient["error_energy_fraction_in_top_concentration"], 1)
        self.assertGreater(gradient["top_concentration_error_enrichment"], 8)

    def test_invalid_grid_is_rejected(self):
        with self.assertRaises(ValueError):
            centered_gradient(np.zeros((3, 4, 4, 3)))


if __name__ == "__main__":
    unittest.main()
