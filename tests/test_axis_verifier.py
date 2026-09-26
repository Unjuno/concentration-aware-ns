"""Fault-injection checks of the verification gate, not Lean theorem tests."""
import contextlib
import io
import json
import os
from pathlib import Path
import runpy
import subprocess
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'tools/verify_axis_sign.py'
LOG = (ROOT / 'evidence/lean-verification/axis-force-sign.log').read_text()


class AxisVerifierGateTests(unittest.TestCase):
    def run_gate(self, log=LOG, returncode=0, mutate=False):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in ('verification', 'runtime/lean-verification', 'evidence/lean-verification'):
                (root / name).mkdir(parents=True)
            source = root / 'verification/AxisForceSign.lean'
            source.write_text('-- isolated test fixture\n')
            (root / 'runtime/lean-verification/check_axis_sign.sh').write_text('# fixture\n')
            def fake_run(*args, **kwargs):
                if mutate:
                    source.write_text('-- changed during verification\n')
                return subprocess.CompletedProcess(args[0], returncode, log, '')
            previous = Path.cwd()
            try:
                os.chdir(root)
                with patch('subprocess.run', side_effect=fake_run), contextlib.redirect_stdout(io.StringIO()):
                    with self.assertRaises(SystemExit) as outcome:
                        runpy.run_path(str(SCRIPT), run_name='__main__')
                result = json.loads((root / 'evidence/lean-verification/axis-force-sign.json').read_text())
                return outcome.exception.code, result
            finally:
                os.chdir(previous)

    def test_recorded_success_is_accepted(self):
        code, result = self.run_gate()
        self.assertEqual(code, 0)
        self.assertTrue(result['success'])

    def test_process_failure_overrides_successful_reports(self):
        code, result = self.run_gate(returncode=1)
        self.assertEqual(code, 1)
        self.assertFalse(result['success'])

    def test_missing_axiom_report_rejected(self):
        log = LOG.replace("'ConcentrationAware.root_pressure_threshold_identity'", "'Other.unrelated'")
        self.assertNotEqual(log, LOG)
        code, result = self.run_gate(log=log)
        self.assertEqual(code, 1)
        self.assertFalse(result['expected_axiom_reports_present'])

    def test_forbidden_axiom_rejected(self):
        log = LOG.replace('propext', 'sorryAx')
        self.assertNotEqual(log, LOG)
        code, result = self.run_gate(log=log)
        self.assertEqual(code, 1)
        self.assertTrue(result['contains_sorryAx'])
        self.assertFalse(result['only_allowed_axioms'])

    def test_source_mutation_rejected(self):
        code, result = self.run_gate(mutate=True)
        self.assertEqual(code, 1)
        self.assertFalse(result['source_unchanged_during_run'])


if __name__ == '__main__':
    unittest.main()
