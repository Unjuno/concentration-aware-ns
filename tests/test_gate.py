import copy
import hashlib
from pathlib import Path
import tempfile
import unittest
from tools.acceptance_gate import evaluate, exit_code, REQUIRED

class GateTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
        (self.root/'review.txt').write_text('Synthetic reviewed test fixture, not scientific evidence.')
        ref={'path':'review.txt','sha256':hashlib.sha256((self.root/'review.txt').read_bytes()).hexdigest()}
        self.report={'schema_version':2,'standard_acceptance':'PASS','evidence':dict.fromkeys(REQUIRED,True),
                     'artifacts':{k:dict(ref) for k in REQUIRED},
                     'metrics':[{'name':n,'error_lower':.02,'error_upper':.03,'tolerance':.01} for n in ('max_gradient','max_vorticity')]}
    def evaluate(self):return evaluate(self.report,self.root)
    def test_missing_evidence_never_reproduces(self):
        for key in REQUIRED:
            r=copy.deepcopy(self.report);del r['evidence'][key]
            self.assertEqual(evaluate(r,self.root)['hypothesis'],'UNCERTAIN')
    def test_valid_discrepancy(self):self.assertEqual(self.evaluate()['hypothesis'],'REPRODUCED')
    def test_standard_failure_is_not_missed_acceptance(self):
        self.report['standard_acceptance']='FAIL';self.assertEqual(self.evaluate()['hypothesis'],'UNCERTAIN')
    def test_invalid_bounds(self):
        for value in (True,-1,float('nan'),float('inf'),'0.1'):
            self.report['metrics'][0]['error_lower']=value
            self.assertEqual(self.evaluate()['local_quality'],'UNCERTAIN')
    def test_passing_intervals(self):
        for m in self.report['metrics']:m.update(error_lower=0,error_upper=.005)
        self.assertEqual(self.evaluate()['hypothesis'],'NOT_OBSERVED')
    def test_missing_required_metric(self):
        self.report['metrics'].pop();self.assertEqual(self.evaluate()['local_quality'],'UNCERTAIN')
    def test_straddling_threshold_is_uncertain(self):
        for m in self.report['metrics']:m.update(error_lower=.005,error_upper=.015)
        self.assertEqual(self.evaluate()['local_quality'],'UNCERTAIN')
    def test_one_sided_bound_can_fail_but_cannot_pass(self):
        for m in self.report['metrics']:m['error_upper']=None
        self.assertEqual(self.evaluate()['local_quality'],'FAIL')
        for m in self.report['metrics']:m['error_lower']=0
        self.assertEqual(self.evaluate()['local_quality'],'UNCERTAIN')
    def test_changed_artifact_invalidates_review(self):
        (self.root/'review.txt').write_text('changed');self.assertEqual(self.evaluate()['hypothesis'],'UNCERTAIN')
    def test_outside_root_rejected(self):
        self.report['artifacts'][REQUIRED[0]]['path']='../review.txt'
        self.assertEqual(self.evaluate()['local_quality'],'UNCERTAIN')
    def test_cli_status_requires_both_acceptances(self):
        self.assertEqual(exit_code(dict(local_quality='PASS',standard_acceptance='UNCERTAIN')),2)
        self.assertEqual(exit_code(dict(local_quality='PASS',standard_acceptance='FAIL')),1)
    def test_legacy_flags_are_insufficient(self):
        del self.report['schema_version'];self.assertEqual(self.evaluate()['local_quality'],'UNCERTAIN')
