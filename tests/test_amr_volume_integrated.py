import unittest

import numpy as np

from tools.compare_amr_resolution_volume_integrated import (
    COMMON_MARGIN,
    LENGTH,
    _cell_widths_and_validate,
    _integrated_relative_errors,
    _quadrature_offsets,
)
from tools.analyze_amr_gauss_gradient import least_squares_gradient_from_internal_faces
from tools.high_gradient_reference import fields


class AmrVolumeIntegratedTests(unittest.TestCase):
    def test_tensor_rule_integrates_polynomials_through_degree_eleven(self):
        points, weights = _quadrature_offsets(6)
        self.assertAlmostEqual(float(weights.sum()), 1.0, places=14)
        self.assertAlmostEqual(float(np.sum(weights * points[:, 0] ** 10)),
                               1 / 11, places=14)
        self.assertAlmostEqual(float(np.sum(
            weights * points[:, 0] ** 2 * points[:, 1] ** 4)),
            1 / 15, places=14)

    def test_amr_geometry_accepts_only_aligned_cubic_levels(self):
        base = LENGTH / 16
        widths = np.array([base, base / 2])
        centers = np.array([
            [base / 2, base / 2, base / 2],
            [3 * base / 4, 3 * base / 4, 3 * base / 4],
        ])
        actual = _cell_widths_and_validate(centers, widths ** 3, 16)
        np.testing.assert_allclose(actual, widths, rtol=0, atol=1e-14)
        with self.assertRaises(ValueError):
            _cell_widths_and_validate(centers[:1], np.array([(base * 0.9) ** 3]), 16)
        misaligned = centers[:1].copy()
        misaligned[0, 0] += 1e-3
        with self.assertRaises(ValueError):
            _cell_widths_and_validate(misaligned, widths[:1] ** 3, 16)

    def test_mms_cell_integral_is_stable_under_order_eight_to_ten(self):
        n = 16
        width = LENGTH / n
        centers = np.array([[5.5 * width, 6.5 * width, 7.5 * width]])
        volumes = np.array([width ** 3])
        mask = np.all(np.minimum(centers, LENGTH - centers) > COMMON_MARGIN, axis=1)
        exact_center = fields(centers, N=4, nu=0.01, time=0.002)
        values = []
        for order in (8, 10):
            values.append(_integrated_relative_errors(
                centers, np.array([width]), volumes, mask,
                exact_center["grad_u"], 4, 0.002, order=order,
            ))
        self.assertLess(abs(
            values[0]["integrated_cellwise_constant_gradient_relative_l2"]
            - values[1]["integrated_cellwise_constant_gradient_relative_l2"]
        ), 1e-11)
        self.assertLess(abs(
            values[0]["integrated_cellwise_constant_curl_relative_l2"]
            - values[1]["integrated_cellwise_constant_curl_relative_l2"]
        ), 1e-11)

    def test_face_neighbor_least_squares_recovers_affine_vector_gradient(self):
        centers = np.array([
            [x + 0.5, y + 0.5, z + 0.5]
            for x in range(2) for y in range(2) for z in range(2)
        ])
        owner, neighbour = [], []
        for i, point in enumerate(centers):
            for j in range(i + 1, len(centers)):
                if np.count_nonzero(np.abs(centers[j] - point) > 0) == 1:
                    owner.append(i)
                    neighbour.append(j)
        exact_gradient = np.array([
            [1.0, 2.0, -0.5],
            [-3.0, 0.25, 4.0],
            [0.0, -2.0, 0.75],
        ])
        velocity = centers @ exact_gradient.T
        gradient, diagnostics = least_squares_gradient_from_internal_faces(
            centers, velocity, owner, neighbour, periodic_length=10.0
        )
        np.testing.assert_allclose(
            gradient, np.broadcast_to(exact_gradient, gradient.shape),
            rtol=0, atol=1e-14,
        )
        self.assertEqual(diagnostics["cells"], 8)

    def test_face_neighbor_least_squares_rejects_rank_deficiency(self):
        centers = np.array([[0.5, 0.5, 0.5], [1.5, 0.5, 0.5]])
        velocity = centers.copy()
        with self.assertRaises(ValueError):
            least_squares_gradient_from_internal_faces(
                centers, velocity, [0], [1], periodic_length=10.0
            )


if __name__ == "__main__":
    unittest.main()
