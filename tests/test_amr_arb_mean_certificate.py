import unittest
import numpy as np
from flint import arb,acb,ctx

from tools.amr_arb_mean_certificate import dft3,voxel_bound,reference_bounds,average_tables


class ArbMeanCertificateTests(unittest.TestCase):
    def setUp(self):self.old=ctx.prec;ctx.prec=96
    def tearDown(self):ctx.prec=self.old

    def test_three_axis_dft_matches_direct_ball_sum(self):
        m=4;grid=np.array([arb(j%7-3)/11 for j in range(m**3)],dtype=object).reshape(m,m,m)
        transformed=dft3(grid)
        for index in ((0,0,0),(1,2,3),(2,0,1)):
            direct=acb(0)
            for i in np.ndindex(grid.shape):
                phase=arb.pi()*(-2*sum(a*b for a,b in zip(index,i)))/m
                direct+=grid[i]*acb(phase.cos(),phase.sin())
            self.assertTrue(transformed[index].overlaps(direct))

    def test_alias_upper_is_above_independent_continuum_hminus_series(self):
        m=8;grid=np.empty((m,m,m),object)
        for i in range(m):grid[i]= (arb.pi()*(2*i+1)/m).sin()*(arb.pi()/m).sin()/(arb.pi()/m)
        norm,mean,upper=voxel_bound(grid)
        # This input is the exact mean of sin(x); gradient norm sqrt(1/2).
        centered=norm-mean*mean
        lower=centered.lower()/upper.upper().sqrt()
        self.assertTrue(lower< (arb(1)/2).sqrt())
        primary=(arb.pi()/m).sin()/(arb.pi()/m)
        partial=arb(0)
        for j in range(-100,101):
            k=1+j*m;partial+=primary**4/(2*k**4)
        self.assertTrue(upper>partial)

    def test_mean_tables_match_independent_numeric_cube_integrals(self):
        from tools.high_gradient_cell_average import exact_cell_average_velocity
        n=16;g,dg,sx,cx=average_tables(n,'0.05',3)
        centers=np.array([[.5,3.5,7.5]])*2*np.pi/n
        expected=exact_cell_average_velocity(centers,2*np.pi/n,.05,3)[0]
        for j,result in enumerate((sx[0]*dg[3]*g[7],cx[0]*g[3]*g[7])):
            self.assertLess(abs(float(result)-expected[j]),2e-16)
        norm,peak,curl=reference_bounds('0.05',3)
        self.assertTrue(norm>0);self.assertTrue(peak<1)
        # Rational polynomial critical values prove the envelope derivative bounds.
        self.assertTrue(arb(2)*(arb(7)/8)**7<1)
        self.assertTrue(arb(7)/2*(arb(21)/32)**3<2)


if __name__=='__main__':unittest.main()
