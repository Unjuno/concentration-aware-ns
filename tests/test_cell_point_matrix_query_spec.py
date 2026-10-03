import copy,json,unittest
from pathlib import Path
from tools.cell_point_matrix_query_spec import validate_spec,verify_query_ball
from tools.run_amr_mean_quality import ROOT

class MatrixQueryControls(unittest.TestCase):
    def spec(self):return json.loads((ROOT/'protocols/of13-cell-point-matrix-query-n32-v1.json').read_text())
    def test_all_frozen_targets_bound(self):
        for p in (ROOT/'protocols').glob('of13-cell-point-matrix-query-*-v1.json'):
            validate_spec(json.loads(p.read_text()))
    def test_wrong_target_rejected(self):
        s=self.spec();s['cell']+=1
        with self.assertRaisesRegex(ValueError,'target differs'):validate_spec(s)
    def test_hash_substitution_rejected(self):
        s=self.spec();s['witness_sha256']='0'*64
        with self.assertRaisesRegex(ValueError,'identity'):validate_spec(s)
    def test_schedule_expansion_rejected(self):
        s=self.spec();s['step_powers']=[8,16,18]
        with self.assertRaisesRegex(ValueError,'schedule'):validate_spec(s)
    def test_exact_ball_interior_and_boundary(self):
        b={'radius':{'lower_rational':'1/4096'},'centre':[{'lower_rational':'0','upper_rational':'0'}]*3}
        self.assertTrue(verify_query_ball([{'x':2.**-14,'y':0.,'z':0.}],b))
        with self.assertRaisesRegex(ValueError,'outside'):
            verify_query_ball([{'x':2.**-12,'y':0.,'z':0.}],b)
    def test_uncertain_centre_conservative_rejection(self):
        b={'radius':{'lower_rational':'1/4096'},'centre':[{'lower_rational':'0','upper_rational':'1'}]*3}
        with self.assertRaisesRegex(ValueError,'outside'):verify_query_ball([{'x':0.,'y':0.,'z':0.}],b)
