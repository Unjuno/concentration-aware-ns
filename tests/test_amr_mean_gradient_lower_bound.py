import unittest
import numpy as np

from tools.amr_mean_gradient_lower_bound import bound
from tools.amr_p0_spectrum import voxel_fft


class MeanGradientLowerBoundTests(unittest.TestCase):
    def test_known_smooth_error_satisfies_bound_and_more_modes_tighten_it(self):
        n=8;h=2*np.pi/n
        c=np.stack(np.meshgrid(*[(np.arange(n)+.5)*h]*3,indexing='ij'),axis=-1).reshape(-1,3)
        values=np.zeros_like(c);values[:,1]=np.sin(2*c[:,0])*np.sinc(2/n)
        f,norm=voxel_fft(c,np.full(n**3,h**3),values,n)
        records=[bound(f,norm['voxel_mean_square'],cutoff) for cutoff in (3,7,15,31)]
        known_gradient_norm=np.sqrt(2.)
        for q in records:
            self.assertLessEqual(q['gradient_mean_norm_lower'],known_gradient_norm*(1+1e-13))
            self.assertGreater(q['gradient_mean_norm_lower'],0)
        lower=[r['gradient_mean_norm_lower'] for r in records]
        self.assertEqual(lower,sorted(lower))
        # Independent scalar H-1 series for this uniform projected sine:
        # only k=+/-2 modulo n occur, with coefficient magnitudes
        # sinc(2/n)^2 * 2/(2+l*n) / 2 (up to harmless phases).
        modes=2+np.arange(-50000,50001)*n
        hminus=np.sum((np.sinc(2/n)**2/modes)**2/modes**2)*2
        self.assertLessEqual(records[-1]['partial_hminus_mean_square'],hminus*(1+1e-13))
        self.assertGreaterEqual(records[-1]['upper_hminus_mean_square'],hminus*(1-1e-13))

    def test_constant_mean_is_removed_and_zero_error_has_zero_lower_bound(self):
        m=8;f=np.zeros((m,m,m,3),complex);f[0,0,0]=[1,2,3]
        result=bound(f,14.,7)
        self.assertEqual(result['constant_mode_mean_square'],14.)
        self.assertEqual(result['gradient_mean_norm_lower'],0.)
        self.assertEqual(bound(np.zeros_like(f),0.,7)['gradient_mean_norm_lower'],0.)

    def test_invalid_norm_and_cutoff_are_rejected(self):
        f=np.zeros((8,8,8,3),complex);f[0,0,0,0]=1
        for cutoff in (0,64,True):
            with self.assertRaises(ValueError):bound(f,1,cutoff)
        with self.assertRaises(ValueError):bound(f,float('nan'),7)
        with self.assertRaises(ValueError):bound(f,.1,7)


if __name__=='__main__':unittest.main()
