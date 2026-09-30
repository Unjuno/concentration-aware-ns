"""Regression check for exact tracer-position probability calculations."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'tools/check_burgers_vortex_tracer_probability.py'


class BurgersVortexTracerProbabilityTests(unittest.TestCase):
    def test_geometry_dependent_probability_and_volume_conservation(self):
        with tempfile.TemporaryDirectory() as directory:
            evidence = Path(directory) / 'evidence/tests'
            evidence.mkdir(parents=True)
            result = subprocess.run(
                [sys.executable, str(SCRIPT)], cwd=directory, env=dict(os.environ),
                capture_output=True, text=True, check=False)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            report = json.loads(
                (evidence / 'burgers-vortex-tracer-probability.json').read_text())

        self.assertEqual(report['source_sha256'], hashlib.sha256(SCRIPT.read_bytes()).hexdigest())
        self.assertTrue(report['success'])
        self.assertTrue(all(report['identities'].values()))
        self.assertEqual(report['physical_flow_jacobian'], '1')
        self.assertEqual(report['cylindrical_coordinate_jacobian'], 'exp(gamma*t)')
        self.assertEqual(report['covariance_determinant'], 'sigma**6')
        self.assertEqual(report['finite_cylinder_scaled_limit'],
                         'sqrt(2)*half_length/(sqrt(pi)*sigma)')
        self.assertIn('exp(2*gamma*t)', report['infinite_axis_tube_probability'])
        self.assertIn('exp(-2*gamma*t)', report['finite_cylinder_probability'])


if __name__ == '__main__':
    unittest.main()
