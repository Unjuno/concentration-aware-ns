import math
import unittest
import numpy as np

from tools.amr_p0_spectrum import voxel_fft, fft_coefficients, direct_cube_coefficients, reference_coefficients, spectrum
from tools.amr_projection_decomposition import exact_mms_mean_square_velocity
from tools.high_gradient_cell_average import exact_cell_average_velocity


def mixed_cells(n=4):
    h=2*np.pi/n
    centers=np.stack(np.meshgrid(*[(np.arange(n)+.5)*h]*3,indexing='ij'),axis=-1).reshape(-1,3)
    offsets=np.stack(np.meshgrid(*[np.array([-.25,.25])*h]*3,indexing='ij'),axis=-1).reshape(-1,3)
    children=centers[:1]+offsets
    return np.concatenate((children,centers[1:])),np.concatenate((np.full(8,(h/2)**3),np.full(n**3-1,h**3)))


class AmrP0SpectrumTests(unittest.TestCase):
    def test_mixed_mesh_fft_integrals_match_direct_cubes_including_alias_modes(self):
        c,v=mixed_cells();u=np.random.default_rng(197).normal(size=c.shape)
        f,norm=voxel_fft(c,v,u,4)
        modes=np.array([(0,0,0),(1,-2,3),(-3,2,-1),(4,0,0),(9,-10,3),(8,0,0)])
        direct=direct_cube_coefficients(c,np.cbrt(v),v,u,modes)
        np.testing.assert_allclose(fft_coefficients(f,modes),direct,atol=2e-15,rtol=2e-13)
        self.assertAlmostEqual(norm['voxel_mean_square'],np.sum(v*np.sum(u*u,axis=1))/(2*np.pi)**3,places=13)
        np.testing.assert_allclose(fft_coefficients(f,[(8,0,0)]),0,atol=1e-15)

    def test_parent_copy_preserves_coefficients_and_total_norm(self):
        n=4;h=2*np.pi/n
        c=np.stack(np.meshgrid(*[(np.arange(n)+.5)*h]*3,indexing='ij'),axis=-1).reshape(-1,3)
        u=np.random.default_rng(51).normal(size=c.shape)
        f,norm=voxel_fft(c,np.full(n**3,h**3),u,n)
        cc,v=mixed_cells(n);cu=np.concatenate((np.repeat(u[:1],8,axis=0),u[1:]))
        g,other=voxel_fft(cc,v,cu,n)
        np.testing.assert_array_equal(f,g)
        self.assertEqual(norm['voxel_mean_square'],other['voxel_mean_square'])

    def test_reference_coefficients_match_independent_realspace_gauss_integrals(self):
        nodes,weights=np.polynomial.legendre.leggauss(64)
        q=np.pi*(nodes+1);w=weights/2
        envelope=((1+np.cos(q))/2)**4
        derivative=-2*np.sin(q)*((1+np.cos(q))/2)**3
        time=.137
        for n in (3,7):
            modes=np.array([(n,0,0),(-n,1,-4),(n,-3,2),(n,5,0),(0,0,0)])
            expected=[]
            for kx,ky,kz in modes:
                ix=np.sum(w*np.sin(n*q)*np.exp(-1j*kx*q))
                cx=np.sum(w*np.cos(n*q)*np.exp(-1j*kx*q))
                dy=np.sum(w*derivative*np.exp(-1j*ky*q))
                gy=np.sum(w*envelope*np.exp(-1j*ky*q))
                gz=np.sum(w*envelope*np.exp(-1j*kz*q))
                expected.append(np.exp(-time)*np.array([ix*dy*gz/n**2,-cx*gy*gz/n,0]))
            np.testing.assert_allclose(reference_coefficients(modes,n,time),expected,atol=2e-15,rtol=2e-12)
            all_modes=np.array([(x,y,z) for x in (-n,n) for y in range(-4,5) for z in range(-4,5)])
            energy=np.sum(np.abs(reference_coefficients(all_modes,n,time))**2)
            self.assertAlmostEqual(energy,exact_mms_mean_square_velocity(time,n),places=16)

    def test_parseval_tail_recovers_full_spatial_error_and_cannot_disappear(self):
        n=8;h=2*np.pi/n
        c=np.stack(np.meshgrid(*[(np.arange(n)+.5)*h]*3,indexing='ij'),axis=-1).reshape(-1,3)
        v=np.full(n**3,h**3);time=.05
        means=exact_cell_average_velocity(c,h,time,3)
        f,norm=voxel_fft(c,v,means,n)
        result,*_=spectrum(f,norm['voxel_mean_square'],3,time,7)
        expected=1-norm['voxel_mean_square']/exact_mms_mean_square_velocity(time,3)
        self.assertAlmostEqual(result['p0_global_error_relative_l2']**2,expected,places=13)
        self.assertGreater(result['outside_cube_mean_square'],0)
        self.assertTrue(result['shells'][7]['complete_integer_shell'])
        self.assertFalse(result['shells'][8]['complete_integer_shell'])

    def test_invalid_coverage_nonfinite_fields_or_truncated_reference_are_rejected(self):
        c,v=mixed_cells();u=np.ones(c.shape)
        bad=c.copy();bad[1]=bad[0]
        with self.assertRaisesRegex(ValueError,'overlaps or holes'):voxel_fft(bad,v,u,4)
        u[0,0]=np.nan
        with self.assertRaises(ValueError):voxel_fft(c,v,u,4)
        for modes in ([(1.5,0,0)],[(float('nan'),0,0)],[(True,False,False)]):
            with self.assertRaises(ValueError):reference_coefficients(modes,3,.05)
        with self.assertRaises(ValueError):spectrum(np.zeros((16,16,16,3)),0,3,.05,2)
        with self.assertRaises(ValueError):spectrum(np.zeros((16,16,16,3)),0,3,.05,8)


if __name__ == '__main__':unittest.main()
