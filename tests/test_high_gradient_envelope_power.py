import math
import unittest

import numpy as np
import sympy as sp

from tools.high_gradient_reference import envelope_derivatives, fields


class HighGradientEnvelopePowerTests(unittest.TestCase):
    def test_envelope_derivatives_match_direct_power_differentiation(self):
        q_values = np.array([-2.4, -0.7, 0.0, 0.9, 2.1, math.pi])
        q = sp.symbols("q", real=True)
        base = (1 + sp.cos(q)) / 2
        for power in (1, 2, 4, 8, 16, 32):
            exact = [sp.lambdify(q, sp.diff(base**power, q, order), "numpy")
                     for order in range(4)]
            observed = envelope_derivatives(q_values, power=power)
            for order in range(4):
                np.testing.assert_allclose(observed[order], exact[order](q_values),
                                           rtol=2e-13, atol=2e-13)

    def test_width_parameter_preserves_solenoidality_and_force_shapes(self):
        points = np.array([[0.2, 0.7, 1.1], [2.3, -0.4, 2.8], [5.1, 1.8, -2.0]])
        for power in (1, 2, 4, 8, 16, 32):
            result = fields(points, N=4, envelope_power=power)
            self.assertEqual(result["u"].shape, (3, 3))
            self.assertEqual(result["grad_u"].shape, (3, 3, 3))
            self.assertEqual(result["force"].shape, (3, 3))
            np.testing.assert_allclose(np.trace(result["grad_u"], axis1=-2, axis2=-1),
                                       0.0, rtol=0.0, atol=2e-15)

    def test_default_envelope_is_the_original_power_four_case(self):
        points = np.array([[0.2, 0.7, 1.1], [2.3, -0.4, 2.8]])
        implicit = fields(points, N=4)
        explicit = fields(points, N=4, envelope_power=4)
        for name in ("u", "grad_u", "vorticity", "force"):
            np.testing.assert_array_equal(implicit[name], explicit[name])


if __name__ == "__main__":
    unittest.main()
