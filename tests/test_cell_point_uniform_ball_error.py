import unittest
from flint import arb,ctx
from tools.audit_cell_point_uniform_ball_error import norm_lower

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
