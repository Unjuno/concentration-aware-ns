import unittest
from flint import arb,ctx
from tools.cell_point_local_neighborhood import unique_neighborhood


class LocalNeighborhoodControls(unittest.TestCase):
    def setUp(self):
        self.old=ctx.prec;ctx.prec=128
        self.a=[[0.,0.,0.],[1.,0.,0.],[0.,1.,0.],[0.,0.,1.]]
        self.c=[arb(1)/4]*3
    def tearDown(self):ctx.prec=self.old

    def test_disjoint_candidate_and_small_ball(self):
        b=[[x+3,y,z] for x,y,z in self.a]
        r=unique_neighborhood([self.a,b],0,self.c,arb(1)/128)
        self.assertEqual(r['status'],'UNIQUE_IDEALIZED_PIECE_ON_ENCLOSED_BALL')

    def test_overlapping_candidate_not_certified(self):
        r=unique_neighborhood([self.a,self.a],0,self.c,arb(1)/128)
        self.assertEqual(r['status'],'LOCAL_UNIQUENESS_NOT_CERTIFIED')

    def test_ball_crossing_face_not_certified(self):
        r=unique_neighborhood([self.a],0,self.c,arb(1))
        self.assertEqual(r['status'],'LOCAL_UNIQUENESS_NOT_CERTIFIED')

    def test_degenerate_candidate_rejected(self):
        with self.assertRaisesRegex(ValueError,'degenerate'):unique_neighborhood([[[0.,0.,0.]]*4],0,self.c,arb(1)/128)
