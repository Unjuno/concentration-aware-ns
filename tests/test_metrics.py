import unittest
import numpy as np
from tools.metrics import diagnostics


class MetricsTests(unittest.TestCase):
    def test_known_mode_and_parseval(self):
        n=32
        y=2*np.pi*np.arange(n)/n
        u=np.zeros((n,n,n,3))
        u[...,0]=np.sin(3*y)[None,:,None]
        result=diagnostics(u)
        self.assertAlmostEqual(result['mean_kinetic_energy'],0.25)
        self.assertAlmostEqual(result['spectrum_energy'],0.25)
        self.assertAlmostEqual(result['shell_energy'][3],0.25)
        self.assertAlmostEqual(result['max_divergence_fd2'],0)
        expected=np.sin(3*2*np.pi/n)/(2*np.pi/n)
        self.assertAlmostEqual(result['max_gradient_fd2'],expected)
        self.assertAlmostEqual(result['max_vorticity_fd2'],expected)

    def test_derivative_converges_to_known_peak(self):
        errors=[]
        for n in (16,32,64):
            y=2*np.pi*np.arange(n)/n
            u=np.zeros((4,n,4,3))
            u[...,0]=np.sin(y)[None,:,None]
            errors.append(abs(diagnostics(u)['max_gradient_fd2']-1))
        self.assertGreater(errors[0]/errors[1],3.9)
        self.assertGreater(errors[1]/errors[2],3.9)

    def test_nonfinite_cannot_generate_diagnostics(self):
        u=np.zeros((4,4,4,3)); u[0,0,0,0]=np.nan
        with self.assertRaises(ValueError):
            diagnostics(u)

    def test_constant_velocity_has_only_zero_mode(self):
        r=diagnostics(np.ones((4,6,8,3)))
        self.assertAlmostEqual(r['shell_energy'][0],1.5)
        self.assertAlmostEqual(r['max_gradient_fd2'],0)
        self.assertAlmostEqual(sum(r['shell_energy'][1:]),0)
