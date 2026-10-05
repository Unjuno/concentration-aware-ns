import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools/check_incompressible_tracer_density.py"


class IncompressibleTracerDensityTests(unittest.TestCase):
    def test_general_liouville_identity_and_affine_controls(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run([sys.executable, str(SCRIPT)], cwd=tmp,
                                    capture_output=True, text=True, check=False)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            evidence = json.loads((Path(tmp) /
                "evidence/tests/incompressible-tracer-density-invariant.json").read_text())
        self.assertEqual(evidence["source_sha256"], hashlib.sha256(SCRIPT.read_bytes()).hexdigest())
        self.assertEqual(evidence["liouville_residual"], "0")
        self.assertTrue(evidence["success"])
        self.assertTrue(all(evidence["controls"].values()))


if __name__ == "__main__":
    unittest.main()
