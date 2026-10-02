import math
import unittest

import numpy as np
from mpmath import iv

from tools.reference import fields


class PhysicsNeMoLocalIntervalProbeTests(unittest.TestCase):
    def test_interval_gradient_contains_exact_point_error(self):
        try:
            from tools.physicsnemo_local_interval_probe import gradient_error_enclosure
        except ImportError as exc:
            self.fail(f"local interval enclosure is not implemented: {exc}")

        hidden_layers = [
            ([[1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0]], [0.0]),
            ([[1.0]], [0.0]),
            ([[1.0]], [0.0]),
        ]
        output_layer = ([[1.0], [0.0], [0.0]], [0.0, 0.0, 0.0])
        point = np.array([0.23, 0.41, 0.72])
        radius = 1e-5
        box = [(float(x - radius), float(x + radius)) for x in point]
        enclosure = gradient_error_enclosure(
            hidden_layers, output_layer, box, time=0.05, sigma=0.5, dps=50
        )

        z1 = math.tanh(math.sin(point[0]) + math.cos(point[0]))
        z2 = math.tanh(z1)
        z3 = math.tanh(z2)
        mlp_dx = ((1-z1*z1)*(1-z2*z2)*(1-z3*z3)
                  * (math.cos(point[0])-math.sin(point[0])))
        reference_grad = fields(point, time=0.0, sigma=0.5)["grad_u"][0, 0]
        expected = 0.05*mlp_dx + (1-math.exp(-0.05))*reference_grad

        interval = enclosure[0][0]
        self.assertLessEqual(float(interval.a), expected)
        self.assertGreaterEqual(float(interval.b), expected)

    def test_point_boxes_contain_reference_only_gradient_at_multiple_points(self):
        from tools.physicsnemo_local_interval_probe import gradient_error_enclosure

        zero_layers = [([[0.0] * 7], [0.0]), ([[0.0]], [0.0]), ([[0.0]], [0.0])]
        output = ([[0.0], [0.0], [0.0]], [0.0, 0.0, 0.0])
        for point in (np.array([0.23, 0.41, 0.72]), np.array([4.8, 2.4, 5.1])):
            result = gradient_error_enclosure(
                zero_layers, output, [(float(x), float(x)) for x in point],
                time=0.05, sigma=0.5, dps=60,
            )
            reference = fields(point, time=0.0, sigma=0.5)["grad_u"]
            for component in range(3):
                for axis in range(3):
                    expected = (1-math.exp(-0.05)) * float(reference[component, axis])
                    enclosure = result[component][axis]
                    midpoint = (float(enclosure.a) + float(enclosure.b)) / 2
                    self.assertAlmostEqual(midpoint, expected, delta=1e-10)

    def test_box_refinement_tightens_at_a_fixed_point(self):
        from tools.physicsnemo_local_interval_probe import gradient_error_enclosure

        zero_layers = [([[0.0] * 7], [0.0]), ([[0.0]], [0.0]), ([[0.0]], [0.0])]
        output = ([[0.0], [0.0], [0.0]], [0.0, 0.0, 0.0])
        point = np.array([0.83, 1.27, 2.08])
        widths = []
        for radius in (1e-2, 1e-4, 1e-6):
            result = gradient_error_enclosure(
                zero_layers, output,
                [(float(x-radius), float(x+radius)) for x in point],
                time=0.05, sigma=0.5, dps=60,
            )
            interval = result[0][1]
            widths.append(float(interval.delta))
        self.assertGreater(widths[0], widths[1])
        self.assertGreater(widths[1], widths[2])

    def test_validation_restores_interval_precision(self):
        from tools.physicsnemo_local_interval_probe import gradient_error_enclosure

        zero_layers = [([[0.0] * 7], [0.0]), ([[0.0]], [0.0]), ([[0.0]], [0.0])]
        output = ([[0.0], [0.0], [0.0]], [0.0, 0.0, 0.0])
        old_dps = iv.dps
        with self.assertRaises(ValueError):
            gradient_error_enclosure(zero_layers, output, [(0.0, 1.0)] * 3,
                                     time=0.06, sigma=0.5, endpoint=0.05)
        self.assertEqual(iv.dps, old_dps)


if __name__ == "__main__":
    unittest.main()
