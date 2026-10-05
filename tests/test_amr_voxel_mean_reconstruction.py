import unittest
import numpy as np

from tools.amr_voxel_mean_reconstruction import reconstruct, recovered_voxel_averages, cube_averages, errors
from tools.high_gradient_cell_average import exact_cell_average_velocity


class VoxelMeanReconstructionTests(unittest.TestCase):
    def test_arbitrary_means_and_nyquist_signs_preserved(self):
        m=8;values=np.random.default_rng(510).normal(size=(m,m,m,3))
        transform=np.fft.fftn(values,axes=(0,1,2))/m**3
        axis,coefficients,meta=reconstruct(transform)
        recovered,imaginary=recovered_voxel_averages(axis,coefficients)
        np.testing.assert_allclose(recovered,values,atol=2e-15)
        self.assertLess(imaginary,1e-15)
        h=2*np.pi/m
        centers=np.array([[.5,.5,.5],[2.5,4.5,7.5]])*h
        means=cube_averages(axis,coefficients,centers,h)
        np.testing.assert_allclose(means.real,np.array([values[0,0,0],values[2,4,7]]),atol=4e-15)
        self.assertLess(np.max(np.abs(means.imag)),2e-15)
        self.assertEqual(meta['mode_count'],9**3)

    def test_resolved_exact_mms_voxel_means_recover_velocity_and_derivatives(self):
        for m in (16,32):
            h=2*np.pi/m
            centers=np.stack(np.meshgrid(*[(np.arange(m)+.5)*h]*3,indexing='ij'),axis=-1)
            values=exact_cell_average_velocity(centers.reshape(-1,3),h,.05,3).reshape(m,m,m,3)
            axis,coefficients,_=reconstruct(np.fft.fftn(values,axes=(0,1,2))/m**3)
            result=errors(axis,coefficients,3,.05)
            for value in result['relative_l2'].values():self.assertLess(value,8e-14)

    def test_parent_copy_adds_nonvanishing_derivative_error_for_exact_shear(self):
        # u=(0,sin(x),0). Native coarse means are exact, but copying each mean
        # to two fine voxels adds a high-frequency alias to the interpolant.
        for n in (16,32,64):
            coarse=np.sin((np.arange(n)+.5)*2*np.pi/n)*np.sinc(1/n)
            # This control is one-dimensional; replicate on a cubic grid.
            m=2*n;values=np.zeros((m,m,m,3));values[...,1]=np.repeat(coarse,2)[:,None,None]
            axis,coefficients,_=reconstruct(np.fft.fftn(values,axes=(0,1,2))/m**3)
            line=coefficients[:,m//2,m//2,1]
            alpha=np.pi/(2*n)
            # Low sine amplitude cos^2(alpha); alias sin((n-1)*x) amplitude
            # (n-1)*sin^2(alpha), with the sign fixed by cell integration.
            low=2*abs(line[np.flatnonzero(axis==1)[0]])
            high=2*abs(line[np.flatnonzero(axis==n-1)[0]])
            self.assertAlmostEqual(low,np.cos(alpha)**2,places=13)
            self.assertAlmostEqual(high,(n-1)*np.sin(alpha)**2,places=13)
            derivative_error=np.sqrt((low-1)**2+((n-1)*high)**2)
            self.assertGreater(derivative_error,2.)
            self.assertLess(derivative_error,np.pi**2/4)

    def test_invalid_shape_nonfinite_or_unresolved_reference_rejected(self):
        with self.assertRaises(ValueError):reconstruct(np.zeros((5,5,5,3)))
        bad=np.zeros((8,8,8,3),complex);bad[0,0,0]=np.nan
        with self.assertRaises(ValueError):reconstruct(bad)
        axis,coefs,_=reconstruct(np.zeros((8,8,8,3)))
        with self.assertRaises(ValueError):errors(axis,coefs,3,.05)


if __name__=='__main__':unittest.main()
