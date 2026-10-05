import unittest
from flint import arb,ctx
from tools.audit_cell_point_affine_divergence import certificate

class AffineDivergenceControls(unittest.TestCase):
    def setUp(self):
        self.old=ctx.prec;ctx.prec=128
        self.v=[[0.,0.,0.],[1.,0.,0.],[0.,1.,0.],[0.,0.,1.]]
    def tearDown(self):ctx.prec=self.old
    def test_isotropic_gradient_has_exact_trace(self):
        r=certificate(self.v,self.v)
        self.assertEqual(r['signed_divergence']['lower_rational'],'3')
        self.assertTrue(1.7<r['distance_to_trace_free_gradient_lower']['display_lower']<1.733)
    def test_rigid_rotation_not_a_divergence_violation(self):
        r=certificate(self.v,[[y,-x,0.] for x,y,z in self.v])
        self.assertEqual(r['status'],'NONZERO_DIVERGENCE_NOT_CERTIFIED')
        self.assertEqual(r['absolute_divergence_lower']['lower_rational'],'0')
    def test_divergence_sign_does_not_change_distance(self):
        a=certificate(self.v,self.v);b=certificate(self.v,[[-x,-y,-z] for x,y,z in self.v])
        self.assertEqual(a['distance_to_trace_free_gradient_lower'],b['distance_to_trace_free_gradient_lower'])
    def test_degenerate_geometry_rejected(self):
        with self.assertRaisesRegex(ValueError,'nondegenerate'):
            certificate([[0.,0.,0.]]*4,[[0.,0.,0.]]*4)
