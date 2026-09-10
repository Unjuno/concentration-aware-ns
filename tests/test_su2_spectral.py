import unittest
import numpy as np
from tools.compare_su2_spectral import vertex_grid
from tools.spectral_derivative import gradient


class SU2SpectralGridTests(unittest.TestCase):
    def fixture(self):
        axis = np.arange(9)*2*np.pi/8
        x, y, z = np.meshgrid(axis, axis, axis, indexing='ij')
        xyz = np.stack((x, y, z), axis=-1).reshape(-1, 3)
        u = np.stack((np.sin(y), np.cos(z), np.sin(x)), axis=-1).reshape(-1, 3)
        return xyz, u

    def test_shuffled_grid_preserves_components_and_derivative_axes(self):
        xyz, u = self.fixture()
        order = np.random.default_rng(518).permutation(len(xyz))
        points, field, mismatch = vertex_grid(xyz[order], u[order], 8)
        expected = np.zeros(field.shape+(3,))
        expected[..., 0, 1] = np.cos(points[..., 1])
        expected[..., 1, 2] = -np.sin(points[..., 2])
        expected[..., 2, 0] = np.cos(points[..., 0])
        np.testing.assert_allclose(gradient(field), expected, atol=2e-14, rtol=0)
        self.assertLess(mismatch, 1e-14)

    def test_missing_coordinate_replaced_by_duplicate_rejected(self):
        xyz, u = self.fixture()
        xyz[0] = xyz[1]
        with self.assertRaisesRegex(ValueError, 'complete vertex lattice'):
            vertex_grid(xyz, u, 8)

    def test_periodic_endpoint_discrepancy_is_reported(self):
        xyz, u = self.fixture()
        u[-1, 0] += 1
        _, _, mismatch = vertex_grid(xyz, u, 8)
        self.assertAlmostEqual(mismatch, 1)
