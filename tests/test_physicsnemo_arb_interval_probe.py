import unittest
import itertools
import importlib.util

import numpy as np

from tools.reference import fields


class PhysicsNeMoArbIntervalProbeTests(unittest.TestCase):
    def test_trigonometric_and_tanh_analytic_ranges_are_enforced(self):
        from flint import arb
        from tools.physicsnemo_arb_interval_probe import (
            _unit_range,
            _tanh_first_derivative_range,
            _tanh_second_derivative_range,
            _monotone_tanh_range,
        )

        for interval in (arb(-1).union(1), arb(-4).union(4)):
            self.assertLessEqual(float(_unit_range(interval.tanh()).abs_upper()), 1.0 + 1e-7)
        broad = arb(-1).union(1)
        tight = _monotone_tanh_range(broad)
        self.assertLess(float(tight.abs_upper()), 0.77)
        for sample in (-1.0, -0.5, 0.0, 0.5, 1.0):
            self.assertTrue(tight.contains(arb(sample).tanh()))
        self.assertLessEqual(float(_unit_range(arb(-4).union(4).sin()).abs_upper()), 1.0 + 1e-7)
        self.assertGreaterEqual(float(_tanh_first_derivative_range(arb(-2).union(2)).lower()), -1e-7)
        self.assertLessEqual(float(_tanh_first_derivative_range(arb(-2).union(2)).upper()), 1.0 + 1e-7)
        self.assertLessEqual(float(_tanh_second_derivative_range(arb(-2).union(2)).abs_upper()), 0.8 + 1e-7)

    def test_centered_form_contains_point_interval_evaluations(self):
        from tools.physicsnemo_arb_interval_probe import (
            centered_gradient_error_enclosure,
            gradient_error_enclosure,
        )

        hidden = [
            ([[0.1, -0.2, 0.3, 0.4, -0.1, 0.2, 0.0]], [0.05]),
            ([[0.7]], [-0.1]),
            ([[-0.6]], [0.02]),
        ]
        output = ([[0.8], [-0.4], [0.2]], [0.0, 0.0, 0.0])
        box = [(0.7, 0.71), (1.1, 1.11), (2.0, 2.01)]
        centered = centered_gradient_error_enclosure(
            hidden, output, box, time=0.05, sigma=0.5, dps=80
        )
        for point in itertools.product(*[(lo, (lo+hi)/2, hi) for lo, hi in box]):
            direct_point = gradient_error_enclosure(
                hidden, output, [(x, x) for x in point], time=0.05, sigma=0.5, dps=80
            )
            for i in range(3):
                for j in range(3):
                    self.assertTrue(centered[i][j].contains(direct_point[i][j]))

    def test_centered_form_tightens_over_direct_form_for_small_box(self):
        from tools.physicsnemo_arb_interval_probe import (
            centered_gradient_error_enclosure,
            gradient_error_enclosure,
        )

        hidden = [
            ([[0.1, -0.2, 0.3, 0.4, -0.1, 0.2, 0.0]], [0.05]),
            ([[0.7]], [-0.1]),
            ([[-0.6]], [0.02]),
        ]
        output = ([[0.8], [-0.4], [0.2]], [0.0, 0.0, 0.0])
        box = [(0.7, 0.71), (1.1, 1.11), (2.0, 2.01)]
        direct = gradient_error_enclosure(hidden, output, box, time=0.05, sigma=0.5)
        centered = centered_gradient_error_enclosure(
            hidden, output, box, time=0.05, sigma=0.5, dps=80
        )
        direct_radius = max(float(direct[i][j].rad().upper()) for i in range(3) for j in range(3))
        centered_radius = max(float(centered[i][j].rad().upper()) for i in range(3) for j in range(3))
        self.assertLess(centered_radius, direct_radius)

    def test_quadratic_taylor_remainder_contains_sampled_point_enclosures(self):
        from tools.physicsnemo_arb_interval_probe import (
            gradient_error_enclosure,
            centered_gradient_error_enclosure,
            quadratic_taylor_gradient_error_enclosure,
        )

        hidden = [
            ([[0.1, -0.2, 0.3, 0.4, -0.1, 0.2, 0.0]], [0.05]),
            ([[0.7]], [-0.1]),
            ([[-0.6]], [0.02]),
        ]
        output = ([[0.8], [-0.4], [0.2]], [0.0, 0.0, 0.0])
        box = [(0.7, 0.71), (1.1, 1.11), (2.0, 2.01)]
        centered = centered_gradient_error_enclosure(
            hidden, output, box, time=0.05, sigma=0.5, dps=70
        )
        taylor = quadratic_taylor_gradient_error_enclosure(
            hidden, output, box, time=0.05, sigma=0.5, dps=70
        )
        self.assertLess(
            max(float(taylor[i][j].rad().upper()) for i in range(3) for j in range(3)),
            max(float(centered[i][j].rad().upper()) for i in range(3) for j in range(3)),
        )
        for point in itertools.product(*[(lo, (lo+hi)/2, hi) for lo, hi in box]):
            direct = gradient_error_enclosure(
                hidden, output, [(x, x) for x in point], time=0.05, sigma=0.5, dps=70
            )
            for i in range(3):
                for j in range(3):
                    self.assertTrue(taylor[i][j].contains(direct[i][j]))

    @unittest.skipUnless(importlib.util.find_spec("torch"), "optional torch check")
    def test_third_spatial_jets_match_autograd_and_reference_finite_difference(self):
        import torch
        from flint import arb
        from tools.physicsnemo_arb_interval_probe import _network_jet, _reference_jet

        torch.set_default_dtype(torch.float64)
        hidden = [
            ([[0.1, -0.2, 0.3, 0.4, -0.1, 0.2, 0.0]], [0.05]),
            ([[0.7]], [-0.1]),
            ([[-0.6]], [0.02]),
        ]
        output = ([[0.8], [-0.4], [0.2]], [0.0, 0.0, 0.0])
        point = np.array([0.83, 1.27, 2.08])
        _, _, _, network_third = _network_jet(
            hidden, output, [arb(float(x)) for x in point], 0.05, 0.05,
            include_third=True,
        )
        x = torch.tensor(point, requires_grad=True)
        features = torch.cat((torch.sin(x), torch.cos(x), torch.ones(1)))
        value = features
        for weights, biases in hidden:
            value = torch.tanh(torch.nn.functional.linear(
                value, torch.tensor(weights), torch.tensor(biases)
            ))
        predicted = torch.nn.functional.linear(value, torch.tensor(output[0]),
                                                torch.tensor(output[1]))
        for component in range(3):
            for a in range(3):
                for b in range(3):
                    for c in range(3):
                        first = torch.autograd.grad(predicted[component], x, create_graph=True, retain_graph=True)[0][a]
                        second = torch.autograd.grad(first, x, create_graph=True, retain_graph=True)[0][b]
                        third = torch.autograd.grad(second, x, retain_graph=True)[0][c]
                        self.assertAlmostEqual(float(network_third[component][a][b][c].mid()),
                                               float(third), delta=2e-12)

        _, _, reference_third = _reference_jet(
            [arb(float(x)) for x in point], 0.5, include_fourth=True
        )
        step = 2e-3
        for i, j, axis in ((2, 1, 1), (1, 2, 0)):
            offset = np.zeros(3)
            offset[axis] = 2 * step
            f_plus = fields(point + offset, time=0.0, sigma=0.5)["grad_u"][i, j]
            f_center = fields(point, time=0.0, sigma=0.5)["grad_u"][i, j]
            f_minus = fields(point - offset, time=0.0, sigma=0.5)["grad_u"][i, j]
            finite = (f_plus - 2*f_center + f_minus) / (4*step*step)
            self.assertAlmostEqual(float(reference_third[i][j][axis][axis].mid()),
                                   float(finite), delta=2e-6)

    def test_invalid_box_is_rejected(self):
        from tools.physicsnemo_arb_interval_probe import gradient_error_enclosure

        hidden = [([[0.0] * 7], [0.0]), ([[0.0]], [0.0]), ([[0.0]], [0.0])]
        output = ([[0.0], [0.0], [0.0]], [0.0, 0.0, 0.0])
        with self.assertRaises(ValueError):
            gradient_error_enclosure(hidden, output, [(1.0, 0.0), (0.0, 0.0), (0.0, 0.0)],
                                     time=0.05, sigma=0.5)

    def test_reference_hessian_matches_independent_finite_difference(self):
        from flint import arb
        from tools.physicsnemo_arb_interval_probe import _reference_jet

        point = np.array([0.83, 1.27, 2.08])
        _, hessian = _reference_jet([arb(float(x)) for x in point], 0.5)
        step = 2e-4
        for derivative_axis in range(3):
            offset = np.zeros(3)
            offset[derivative_axis] = step
            plus = fields(point + offset, time=0.0, sigma=0.5)["grad_u"]
            minus = fields(point - offset, time=0.0, sigma=0.5)["grad_u"]
            finite_difference = (plus - minus) / (2 * step)
            for component in range(3):
                for jacobian_axis in range(3):
                    analytic = float(hessian[component][jacobian_axis][derivative_axis])
                    self.assertAlmostEqual(
                        analytic, finite_difference[component, jacobian_axis], delta=2e-7
                    )


if __name__ == "__main__":
    unittest.main()
