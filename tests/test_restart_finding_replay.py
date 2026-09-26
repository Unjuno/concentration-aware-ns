import copy
import json
from pathlib import Path
import unittest
from tools.replay_su2_restart_findings import reproduced

class FindingReplayTests(unittest.TestCase):
    def setUp(self):
        self.result=json.loads(Path('evidence/su2-restart-time-pilot-v1/replay-review.json').read_text())
        self.protocol=json.loads(Path('protocols/su2-restart-time-pilot-v1.json').read_text())
    def test_recorded_specific_failure(self):
        self.assertTrue(reproduced(self.result,1,self.protocol))
    def test_other_exit_codes_rejected(self):
        for code in [0,2,-9]:self.assertFalse(reproduced(self.result,code,self.protocol))
    def test_missing_row_rejected(self):
        self.result['history'].pop();self.assertFalse(reproduced(self.result,1,self.protocol))
    def test_wrong_time_rejected(self):
        self.result['history'][1]['times'][0]=.2;self.assertFalse(reproduced(self.result,1,self.protocol))
    def test_nonfinite_or_large_field_error_rejected(self):
        for value in [float('nan'),float('inf'),1.0]:
            r=copy.deepcopy(self.result);r['comparisons'][0]['max_differences']['Pressure']=value
            self.assertFalse(reproduced(r,1,self.protocol))
