"""Regression check for the analytic Burgers-vortex counterexample."""
import json
import hashlib
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'tools/check_burgers_vortex_balance.py'


class BurgersVortexBalanceTests(unittest.TestCase):
    def test_full_equations_and_off_axis_alignment_are_checked(self):
        with tempfile.TemporaryDirectory() as directory:
            evidence = Path(directory) / 'evidence/tests'
            evidence.mkdir(parents=True)
            env = dict(os.environ)
            result = subprocess.run(
                [sys.executable, str(SCRIPT)], cwd=directory, env=env,
                capture_output=True, text=True, check=False)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            report = json.loads((evidence / 'burgers-vortex-balance.json').read_text())

        self.assertTrue(report['success'])
        self.assertEqual(report['source_sha256'], hashlib.sha256(SCRIPT.read_bytes()).hexdigest())
        self.assertTrue(all(report['identities'].values()))
        self.assertTrue(all(report['negative_controls'].values()))
        self.assertEqual(report['residuals']['azimuthal_advection_minus_diffusion'], '0')
        self.assertEqual(report['residuals']['radial_navier_stokes'], '0')
        self.assertEqual(report['residuals']['axial_navier_stokes'], '0')
        self.assertNotEqual(report['residuals']['kinematic_diffusion'], '0')
        self.assertEqual(report['axis_variational_residual'],
                         'Matrix([[0, 0, 0], [0, 0, 0], [0, 0, 0]])')
        self.assertEqual(report['axis_transverse_to_axial_ratio_squared_limit'], '0')
        self.assertEqual(report['off_axis_transverse_to_axial_ratio_squared_limit'], '0')
        self.assertEqual(report['off_axis_shear_limit'], report['off_axis_expected_shear_limit'])
        self.assertTrue(report['azimuthal_advection_equals_viscous_diffusion'])


if __name__ == '__main__':
    unittest.main()
