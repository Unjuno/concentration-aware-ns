import unittest
import numpy as np
from tools.reference import fields
from tools.reference_energy import mean_energy, periodic_vertex_mean_energy


class ReferenceTests(unittest.TestCase):
    def setUp(self):
        self.x = np.pi + np.random.default_rng(19).uniform(-0.7, 0.7, (24, 3))

    def test_divergence_and_periodicity(self):
        f = fields(self.x)
        np.testing.assert_allclose(np.trace(f['grad_u'], axis1=-2, axis2=-1), 0, atol=1e-13)
        for j in range(3):
            offset = np.eye(3)[j]*2*np.pi
            for key, value in f.items():
                np.testing.assert_allclose(fields(self.x+offset)[key], value, atol=2e-11)

    def test_independent_finite_difference_residual_converges(self):
        # Reconstruct time, convective and viscous terms using u samples only.
        t, nu = 0.2, 0.01
        exact = fields(self.x, t, nu=nu)
        errors = []
        for h in (0.01, 0.005, 0.0025):
            u = exact['u']
            dt = (fields(self.x, t+h)['u']-fields(self.x, t-h)['u'])/(2*h)
            conv = np.zeros_like(u)
            lap = np.zeros_like(u)
            for j in range(3):
                shift = np.eye(3)[j]*h
                plus = fields(self.x+shift, t)['u']
                minus = fields(self.x-shift, t)['u']
                conv += u[:, j, None]*(plus-minus)/(2*h)
                lap += (plus-2*u+minus)/h**2
            errors.append(np.max(np.abs(dt+conv-nu*lap-exact['force'])))
        self.assertGreater(errors[0]/errors[1], 3.8)
        self.assertGreater(errors[1]/errors[2], 3.8)
        self.assertLess(errors[-1], 0.02)

    def test_invalid_width(self):
        with self.assertRaises(ValueError):
            fields(self.x, sigma=0)

    def test_analytic_vertex_energy_matches_direct_field_mean(self):
        for n in (8, 16):
            axis = 2*np.pi*np.arange(n)/n
            xyz = np.stack(np.meshgrid(axis, axis, axis, indexing='ij'), axis=-1)
            u = fields(xyz, time=.05, sigma=.5)['u']
            direct = .5*np.mean(np.sum(u*u, axis=-1))
            self.assertAlmostEqual(periodic_vertex_mean_energy(n, .05, .5), direct, places=14)

    def test_vertex_energy_converges_to_continuum_integral(self):
        exact = mean_energy(.05, .5)
        e16 = periodic_vertex_mean_energy(16, .05, .5)
        e32 = periodic_vertex_mean_energy(32, .05, .5)
        self.assertLess(abs(e32/exact-1), 1e-13)
        self.assertLess(abs(e16/exact-1), 1e-3)

    def test_invalid_vertex_grid(self):
        for n in (0, -1, 2.5, True):
            with self.assertRaises(ValueError):
                periodic_vertex_mean_energy(n)
