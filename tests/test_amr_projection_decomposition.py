import unittest

import numpy as np
from numpy.polynomial.legendre import leggauss

from tools.amr_projection_decomposition import (
    decompose_p0_error,
    exact_cell_mean_square_gradient,
    exact_mms_mean_square_velocity,
    exact_mms_mean_square_gradient,
)
from tools.high_gradient_reference import fields


class AmrProjectionDecompositionTests(unittest.TestCase):
    def test_orthogonal_error_decomposition(self):
        result = decompose_p0_error(10, 6, 1)
        self.assertAlmostEqual(result["mean_dof_mismatch_relative_l2"], np.sqrt(.1))
        self.assertAlmostEqual(result["unresolved_projection_relative_l2"], np.sqrt(.4))
        self.assertAlmostEqual(result["p0_total_relative_l2"], np.sqrt(.5))
        self.assertAlmostEqual(result["projection_energy_fraction"], .6)
        self.assertEqual(result["orthogonality_identity_residual"], 0)

    def test_exact_mms_norm_matches_independent_tensor_gauss_integral(self):
        time = .003
        nodes, weights = leggauss(32)
        axis = np.pi*(nodes+1)
        z, y, x = np.meshgrid(axis, axis, axis, indexing="ij")
        points = np.stack((x, y, z), axis=-1)
        u = fields(points, N=4, time=time)["u"]
        w = weights[:, None, None]*weights[None, :, None]*weights[None, None, :]
        direct = float(np.sum(w*np.sum(u*u, axis=-1))/8)
        self.assertAlmostEqual(
            exact_mms_mean_square_velocity(time), direct, places=14)

    def test_exact_gradient_energy_matches_domain_and_cellwise_gauss(self):
        time, h = .003, 2*np.pi/16
        nodes, weights = leggauss(32)
        axis = np.pi*(nodes+1)
        z, y, x = np.meshgrid(axis, axis, axis, indexing="ij")
        points = np.stack((x, y, z), axis=-1)
        gradient = fields(points, N=4, time=time)["grad_u"]
        w = weights[:, None, None]*weights[None, :, None]*weights[None, None, :]
        direct_domain = float(np.sum(w*np.sum(gradient*gradient, axis=(-2, -1)))/8)
        self.assertAlmostEqual(exact_mms_mean_square_gradient(time), direct_domain, places=14)

        centers = np.array([[.2, .4, .8], [1.1, 3.2, 5.4], [5.8, .1, 2.6]])
        exact_cell = exact_cell_mean_square_gradient(
            centers, np.full(len(centers), h), time)
        nodes, weights = leggauss(16)
        direct_cells = np.zeros(len(centers))
        for i, wi in zip(nodes, weights):
            for j, wj in zip(nodes, weights):
                for k, wk in zip(nodes, weights):
                    point = centers+np.array([i, j, k])[None, :]*h/2
                    g = fields(point, N=4, time=time)["grad_u"]
                    direct_cells += wi*wj*wk/8*np.sum(g*g, axis=(-2, -1))
        np.testing.assert_allclose(exact_cell, direct_cells, atol=2e-13, rtol=2e-12)

    def test_invalid_decomposition_is_rejected(self):
        for args in ((0, 0, 0), (1, 2, 0), (1, -1, 0), (1, 0, -1)):
            with self.assertRaises(ValueError):
                decompose_p0_error(*args)


if __name__ == "__main__":
    unittest.main()
