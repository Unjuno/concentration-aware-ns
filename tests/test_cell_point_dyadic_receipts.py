import json,unittest
from fractions import Fraction
from pathlib import Path
from tools.check_cell_point_dyadic_receipts import check,check_bounds

ROOT=Path(__file__).resolve().parents[1]
class DyadicReceiptControls(unittest.TestCase):
    def fixture(self):
        old=json.loads((ROOT/'evidence/cell-point-uniform-ball-error-v1/n32/analysis.json').read_text())
        new=json.loads((ROOT/'evidence/cell-point-uniform-ball-error-v2/n32/analysis.json').read_text())
        spec=json.loads((ROOT/'protocols/of13-cell-point-matrix-query-n32-v1.json').read_text())
        w=json.loads((ROOT/spec['witness_path']).read_text())['witness']
        return old,new,w
    def mutate_point(self,new,key,delta):
        q=Fraction(new[key]['lower_rational'])+delta
        new[key]['lower_rational']=new[key]['upper_rational']=str(q)
    def test_all_published_cases(self):
        self.assertEqual(len(check(ROOT)['results']),3)
    def test_absolute_upward_grid_step_rejected(self):
        old,new,w=self.fixture();self.mutate_point(new,'gradient_error_lower',Fraction(1,2**32))
        with self.assertRaisesRegex(ValueError,'conservative'):check_bounds(old,new,w)
    def test_relative_upward_grid_step_rejected(self):
        old,new,w=self.fixture();self.mutate_point(new,'curl_relative_reference_peak_error_lower',Fraction(1,2**32))
        with self.assertRaisesRegex(ValueError,'unsupported'):check_bounds(old,new,w)
    def test_non_grid_assertion_rejected(self):
        old,new,w=self.fixture();self.mutate_point(new,'gradient_error_lower',Fraction(1,2**40))
        with self.assertRaisesRegex(ValueError,'non-dyadic'):check_bounds(old,new,w)
    def test_non_point_assertion_rejected(self):
        old,new,w=self.fixture();new['gradient_error_lower']['upper_rational']='1'
        with self.assertRaisesRegex(ValueError,'exact rational'):check_bounds(old,new,w)
