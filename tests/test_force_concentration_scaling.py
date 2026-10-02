from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools/check_force_concentration_scaling.py"


class ForceConcentrationScalingTests(unittest.TestCase):
    def test_exact_rescaling_and_scope_are_recorded(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "scaling.json"
            run = subprocess.run(
                [sys.executable, str(SCRIPT), "--output", str(output)],
                cwd=directory,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
            result = json.loads(output.read_text(encoding="utf-8"))

        self.assertEqual(result["status"], "PASS")
        self.assertNotIn("interpreter", result)
        self.assertEqual(result["python_implementation"], "cpython")
        self.assertEqual(
            result["source_sha256"], hashlib.sha256(SCRIPT.read_bytes()).hexdigest()
        )
        self.assertEqual(result["Lq_homogeneous_Hs_exponent"], "2/q-3/2-s")
        self.assertEqual(result["pointwise_derivative_exponents"]["force_amplitude"], "epsilon^-3")
        self.assertEqual(result["pointwise_derivative_exponents"]["one_spatial_derivative"], "epsilon^-4")
        self.assertIn("not an actuator-feasibility theorem", result["scope"])


if __name__ == "__main__":
    unittest.main()
