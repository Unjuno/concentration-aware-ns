import unittest
from fractions import Fraction

from tools.physicsnemo_global_hessian_bound import (
    best_case_uniform_grid_nodes,
    network_hessian_entry_bound,
    total_error_hessian_entry_bound,
    network_hessian_vector_norm_bound,
    spectral_total_error_hessian_entry_bound,
)


class PhysicsNeMoGlobalHessianBoundTests(unittest.TestCase):
    def test_vector_norm_bound_is_rational_and_zero_for_constant_network(self):
        hidden = [[[0] * 7], [[0]], [[0]]]
        output = [[0], [0], [0]]
        bound = network_hessian_vector_norm_bound(hidden, output)
        self.assertEqual(bound, Fraction(0))
        self.assertEqual(spectral_total_error_hessian_entry_bound(bound), Fraction(29))

    def test_vector_norm_bound_ignores_spatially_constant_time_feature(self):
        hidden = [[[0, 0, 0, 0, 0, 0, 100]], [[1]], [[1]]]
        output = [[1], [0], [0]]
        self.assertEqual(network_hessian_vector_norm_bound(hidden, output), Fraction(0))

    def test_zero_network_has_zero_spatial_hessian(self):
        hidden = [[[0] * 7], [[0]], [[0]]]
        output = [[0], [0], [0]]
        self.assertEqual(network_hessian_entry_bound(hidden, output), 0)
        self.assertEqual(total_error_hessian_entry_bound(Fraction(0)), 29)

    def test_exact_second_derivative_propagation(self):
        # Frozen input order is sin(x), sin(y), sin(z), cos(x), cos(y),
        # cos(z), t/end. The sin(x)+cos(x) pair shares the x derivative:
        # D1<=2, input D2<=2, then each later tanh adds at most D1^2=4.
        hidden = [[[1, 0, 0, 1, 0, 0, 0]], [[1]], [[1]]]
        output = [[1], [0], [0]]
        self.assertEqual(network_hessian_entry_bound(hidden, output), Fraction(7, 10))

    def test_cover_cost_is_integer_and_grows_with_bound(self):
        small = best_case_uniform_grid_nodes(Fraction(580))
        large = best_case_uniform_grid_nodes(Fraction(1200))
        self.assertIsInstance(small, int)
        self.assertGreater(large, small)
        self.assertGreater(large**3, 10**12)

    def test_optimistic_floor_uses_strict_inequality_rounding(self):
        # At this value the rational comparison quotient is exactly one, but
        # pi>3 and peak<21 imply the true required node count is strictly >1.
        self.assertEqual(
            best_case_uniform_grid_nodes(Fraction(21, 540)),
            2,
        )

    def test_rejects_wrong_hidden_depth_and_input_width(self):
        with self.assertRaises(ValueError):
            network_hessian_entry_bound([[[0] * 7]], [[0], [0], [0]])
        with self.assertRaises(ValueError):
            network_hessian_entry_bound([[[0] * 6], [[1]], [[1]]], [[1], [0], [0]])


if __name__ == "__main__":
    unittest.main()
