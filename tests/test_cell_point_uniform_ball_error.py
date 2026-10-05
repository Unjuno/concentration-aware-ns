import unittest
from flint import arb,ctx
from tools.audit_cell_point_uniform_ball_error import norm_lower,dyadic_lower

class UniformErrorControls(unittest.TestCase):
    def test_exact_vector_norm(self):
        x=norm_lower([arb(3),arb(-4),arb(0)])
        self.assertTrue(x<=5 and x>arb('4.99999'))
    def test_zero_crossing_must_contribute_zero(self):
        self.assertEqual(norm_lower([arb(0,1)]),0)
    def test_componentwise_minima(self):
        r=norm_lower([arb(4,1),arb(-5,1)])
        self.assertTrue(r<=5 and r>arb('4.99999'))
    def test_broad_intervals_cannot_show_positive_error(self):
        self.assertEqual(norm_lower([arb(2,3),arb(-2,3)]),0)

    def test_downward_rounding_never_increases_bound(self):
        from fractions import Fraction
        from tools.amr_arb_mean_certificate import endpoints
        for text in ('0.1','-0.1','0','1/3'):
            v=arb(text) if '/' not in text else arb(1)/3
            out=dyadic_lower(v,8)
            q=Fraction(endpoints(out)['lower_rational'])
            lo=Fraction(endpoints(v.lower())['lower_rational'])
            self.assertTrue(q<=lo and lo-q<Fraction(1,256))
    def test_interval_lower_endpoint_not_midpoint(self):
        self.assertTrue(dyadic_lower(arb(1,1)/2)<=0)
    def test_exact_dyadic_value_unchanged(self):
        self.assertEqual(dyadic_lower(arb(3)/8,8),arb(3)/8)
    def test_invalid_grid_rejected(self):
        with self.assertRaises(ValueError):dyadic_lower(arb(1),0)
