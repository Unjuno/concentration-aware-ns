import unittest
from fractions import Fraction

from tools.physicsnemo_global_hessian_bound import (
    best_case_uniform_grid_nodes,
    network_hessian_entry_bound,
    total_error_hessian_entry_bound,
)


class PhysicsNeMoGlobalHessianBoundTests(unittest.TestCase):
    def test_zero_network_has_zero_spatial_hessian(self):
        hidden = [[[0] * 7], [[0]], [[0]]]
        output = [[0], [0], [0]]
        self.assertEqual(network_hessian_entry_bound(hidden, output), 0)
        self.assertEqual(total_error_hessian_entry_bound(Fraction(0)), 580)

    def test_exact_second_derivative_propagation(self):
        # For the first unit, |D(sin(2x+cos x))| <= 3 and the input
        # second-derivative envelope is 3. Each tanh adds at most D1^2=9.
        hidden = [[[2, 1, 0, 0, 0, 0, 0]], [[1]], [[1]]]
        output = [[1], [0], [0]]
        self.assertEqual(network_hessian_entry_bound(hidden, output), Fraction(3, 2))

    def test_cover_cost_is_integer_and_grows_with_bound(self):
        small = best_case_uniform_grid_nodes(Fraction(580))
        large = best_case_uniform_grid_nodes(Fraction(1200))
        self.assertIsInstance(small, int)
        self.assertGreater(large, small)
        self.assertGreater(large**3, 10**12)

    def test_rejects_wrong_hidden_depth_and_input_width(self):
        with self.assertRaises(ValueError):
            network_hessian_entry_bound([[[0] * 7]], [[0], [0], [0]])
        with self.assertRaises(ValueError):
            network_hessian_entry_bound([[[0] * 6], [[1]], [[1]]], [[1], [0], [0]])


if __name__ == "__main__":
    unittest.main()
