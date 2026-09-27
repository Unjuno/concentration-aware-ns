import unittest
import numpy as np
from tools.compare_openfoam_iteration_sensitivity import alignment, completed_times


class IterationComparisonTests(unittest.TestCase):
    def test_dimensional_time_and_exponent(self):
        self.assertEqual(completed_times('Time = 1e-3s\nExecutionTime = 9 s\nTime = 0.05s\n'), [.001, .05])

    def test_plain_time(self):
        self.assertEqual(completed_times('Time = 0.001\nTime = 0.05\n'), [.001, .05])

    def test_exact_first_order_vector(self):
        base = np.array([[2., 3., 4.]])
        error = np.array([[1., -2., 1.]])
        result = alignment([base+h*error for h in [1., .5, .25]])
        self.assertAlmostEqual(result['norm_order'], 1)
        self.assertAlmostEqual(result['cosine'], 1)
        self.assertAlmostEqual(result['best_fit_scale'], 2)
        self.assertAlmostEqual(result['first_order_defect'], 0)

    def test_direction_change(self):
        result = alignment([np.array([2., 2.]), np.array([1., 2.]), np.array([1., 1.])])
        self.assertAlmostEqual(result['cosine'], 0)
        self.assertGreater(result['first_order_defect'], 1)


if __name__ == '__main__':
    unittest.main()
