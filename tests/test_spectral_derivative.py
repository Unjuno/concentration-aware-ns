import unittest
import numpy as np
from tools.spectral_derivative import gradient


class SpectralDerivativeTest(unittest.TestCase):
    def test_resolved_modes_rectangular_shifted_grid(self):
        lengths = (3., 5., 7.)
        axes = [(np.arange(n)+.37)*L/n for n,L in zip((12,15,18),lengths)]
        x,y,z = np.meshgrid(*axes,indexing='ij')
        u = np.stack((np.sin(4*np.pi*y/5),np.cos(6*np.pi*z/7),np.sin(2*np.pi*x/3)),axis=-1)
        exact = np.zeros(u.shape+(3,))
        exact[...,0,1] = 4*np.pi/5*np.cos(4*np.pi*y/5)
        exact[...,1,2] = -6*np.pi/7*np.sin(6*np.pi*z/7)
        exact[...,2,0] = 2*np.pi/3*np.cos(2*np.pi*x/3)
        np.testing.assert_allclose(gradient(u,lengths),exact,atol=2e-14,rtol=0)

    def test_even_nyquist_convention(self):
        u = np.zeros((8,8,8,3));u[...,0] = (-1.)**np.arange(8)[:,None,None]
        np.testing.assert_allclose(gradient(u),0,atol=1e-14)

    def test_reject_nonfinite(self):
        u=np.zeros((4,4,4,3));u[0,0,0,0]=np.nan
        with self.assertRaises(ValueError):gradient(u)
