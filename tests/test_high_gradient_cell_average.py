import unittest

import numpy as np
from numpy.polynomial.legendre import leggauss

from tools.high_gradient_cell_average import exact_cell_average_velocity
from tools.high_gradient_reference import fields


class HighGradientCellAverageTests(unittest.TestCase):
    def test_closed_form_matches_independent_tensor_quadrature(self):
        centers = np.array([
            [0.03, 2*np.pi - 0.02, 0.01],
            [np.pi/4, np.pi/2, 3*np.pi/4],
            [2*np.pi - 0.04, 0.07, 2*np.pi - 0.03],
        ])
        widths = np.array([0.13, 0.41, 0.22])
        time = 0.173
        exact = exact_cell_average_velocity(centers, widths, time)

        nodes, weights = leggauss(12)
        numerical = np.zeros_like(exact)
        for i, wi in zip(nodes, weights):
            for j, wj in zip(nodes, weights):
                for k, wk in zip(nodes, weights):
                    offsets = np.column_stack((i*widths, j*widths, k*widths))/2
                    numerical += (wi*wj*wk/8) * fields(
                        centers + offsets, N=4, nu=0.01, time=time
                    )["u"]
        self.assertLess(float(np.max(np.abs(exact-numerical))), 3e-15)

    def test_scalar_width_and_explicit_frequency(self):
        centers = np.array([[0.4, 1.2, 2.1], [2.2, 3.0, 4.4]])
        average = exact_cell_average_velocity(
            centers, 0.2, 0.31, frequency=3
        )
        self.assertEqual(average.shape, (2, 3))
        self.assertTrue(np.isfinite(average).all())
        self.assertTrue(np.array_equal(average[:, 2], np.zeros(2)))

    def test_rejects_invalid_widths_and_geometry(self):
        centers = np.zeros((2, 3))
        with self.assertRaisesRegex(ValueError, "positive"):
            exact_cell_average_velocity(centers, [0.1, 0.0], 0.0)
        with self.assertRaisesRegex(ValueError, "one value per center"):
            exact_cell_average_velocity(centers, [0.1, 0.2, 0.3], 0.0)
        with self.assertRaisesRegex(ValueError, "shape"):
            exact_cell_average_velocity(np.zeros((3, 2)), 0.1, 0.0)


if __name__ == "__main__":
    unittest.main()
