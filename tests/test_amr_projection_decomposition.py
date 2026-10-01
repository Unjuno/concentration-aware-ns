import unittest

import numpy as np
from numpy.polynomial.legendre import leggauss

from tools.amr_projection_decomposition import (
    decompose_p0_error,
    exact_mms_mean_square_velocity,
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

    def test_invalid_decomposition_is_rejected(self):
        for args in ((0, 0, 0), (1, 2, 0), (1, -1, 0), (1, 0, -1)):
            with self.assertRaises(ValueError):
                decompose_p0_error(*args)


if __name__ == "__main__":
    unittest.main()
