import copy
import hashlib
import unittest
from tools.audit_comparator_result import audit


class ComparatorResultAudit(unittest.TestCase):
    def setUp(self):
        self.inputs = {'source_commit': 'fixed-pin', 'configuration': {
            'theorem_names': ['Euler.first', 'Euler.second'],
            'permitted_axioms': ['propext', 'Quot.sound', 'Classical.choice'],
            'enable_nanoda': True}}
        self.log = ("'Euler.first' depends on axioms: [propext, Classical.choice]\n"
                    "'Euler.second' depends on axioms: [Quot.sound]\n"
                    'nanoda kernel accepts the solution\n'
                    'Lean default kernel accepts the solution\n'
                    'Your solution is okay!\n').encode()
        self.result = {'exit_code': 0, 'upstream_commit': 'fixed-pin',
                       'log_sha256': hashlib.sha256(self.log).hexdigest()}

    def check_log(self, log):
        result = dict(self.result, log_sha256=hashlib.sha256(log).hexdigest())
        return audit(result, self.inputs, log)['success']

    def test_complete_record(self):
        self.assertTrue(audit(self.result, self.inputs, self.log)['success'])

    def test_failed_exit_despite_success_text(self):
        self.assertFalse(audit(dict(self.result, exit_code=1), self.inputs, self.log)['success'])

    def test_missing_each_acceptance(self):
        for line in self.log.splitlines(keepends=True):
            with self.subTest(line=line):
                self.assertFalse(self.check_log(self.log.replace(line, b'')))

    def test_forbidden_axiom(self):
        self.assertFalse(self.check_log(self.log.replace(b'Quot.sound', b'sorryAx')))

    def test_altered_log(self):
        self.assertFalse(audit(self.result, self.inputs, self.log+b'\n')['success'])

    def test_wrong_source(self):
        self.assertFalse(audit(dict(self.result, upstream_commit='other'), self.inputs, self.log)['success'])

    def test_duplicate_or_empty_targets(self):
        for names in [[], ['Euler.first', 'Euler.first']]:
            inputs = copy.deepcopy(self.inputs)
            inputs['configuration']['theorem_names'] = names
            self.assertFalse(audit(self.result, inputs, self.log)['success'])

    def test_trailing_failure(self):
        self.assertFalse(self.check_log(self.log+b'failure after apparent success\n'))

    def test_nanoda_disabled(self):
        self.inputs['configuration']['enable_nanoda'] = False
        self.assertFalse(audit(self.result, self.inputs, self.log)['success'])
