import unittest
import numpy as np

from tools.amr_band_reconstruction import diagnostics, derivative_coefficients, sampled_peak_bounds, validate
from tools.amr_p0_spectrum import reference_coefficients


class BandReconstructionTests(unittest.TestCase):
    def test_shear_derivatives_and_continuum_peak_enclosure(self):
        modes = np.array([[-3,0,0],[3,0,0]])
        # v=(0,sin(3*x),0); derivative and curl have exact peak 3.
        coefficients = np.array([[0,.5j,0],[0,-.5j,0]])
        grad = derivative_coefficients(modes, coefficients, 'gradient')
        curl = derivative_coefficients(modes, coefficients, 'curl')
        self.assertEqual(np.count_nonzero(grad), 2)
        np.testing.assert_allclose(curl[:,2], grad[:,3])
        for grid in (16,32):
            bounds = sampled_peak_bounds(modes, grad, grid)
            self.assertLessEqual(bounds['sampled_peak_lower'], 3+1e-14)
            self.assertGreaterEqual(bounds['analytic_peak_upper'], 3)
            self.assertAlmostEqual(bounds['parseval_mean_square'], 4.5)
            self.assertAlmostEqual(bounds['grid_mean_square'], 4.5)
        self.assertLess(sampled_peak_bounds(modes,grad,32)['analytic_peak_upper'],
                        sampled_peak_bounds(modes,grad,16)['analytic_peak_upper'])

    def test_derivatives_match_direct_physical_polynomial_at_non_grid_points(self):
        modes = np.array([[-2,1,3],[2,-1,-3]])
        vector = np.array([.1+.2j,-.3j,.4])
        coefficients = np.array([vector.conj(),vector])
        points = np.array([[.37,1.21,2.18],[3.15,.78,5.3]])
        grad = derivative_coefficients(modes,coefficients,'gradient').reshape(2,3,3)
        phase = np.exp(1j*(points@modes.T))
        actual = np.einsum('pk,kij->pij',phase,grad).real
        expected = np.stack([-2*np.outer(np.imag(vector*np.exp(1j*(point@modes[1]))),modes[1]) for point in points])
        np.testing.assert_allclose(actual,expected,atol=2e-15)

    def test_longitudinal_error_has_zero_curl_and_orthogonal_projection(self):
        modes = np.array([[-3,1,0],[3,-1,0]])
        ref = reference_coefficients(modes,3,.05)
        perturbation = modes.astype(complex)*.007
        actual = ref+perturbation*1j
        result = diagnostics(modes,actual,ref,32)
        self.assertLess(result['curl']['relative_l2'],1e-15)
        self.assertGreater(result['gradient']['relative_l2'],.1)
        self.assertLess(result['helmholtz']['divergence_free_band_error_relative_l2'],1e-14)
        self.assertAlmostEqual(result['helmholtz']['orthogonal_error_identity_residual'],0,places=15)

    def test_invalid_modes_symmetry_aliasing_and_nan_rejected(self):
        modes=np.array([[-1,0,0],[1,0,0]]); good=np.ones((2,3),complex)
        with self.assertRaises(ValueError):validate(modes[:1],good[:1])
        with self.assertRaises(ValueError):validate(np.zeros((2,3),int),good)
        bad=good.copy();bad[0,0]=np.nan
        with self.assertRaises(ValueError):validate(modes,bad)
        with self.assertRaises(ValueError):sampled_peak_bounds(modes,good,2)
        with self.assertRaises(ValueError):derivative_coefficients(modes,good,'unknown')


if __name__ == '__main__': unittest.main()
