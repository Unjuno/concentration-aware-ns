import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools/check_pressure_data_amplitude_countermodel.py"


class PressureDataAmplitudeCountermodelTests(unittest.TestCase):
    def test_exact_pressure_and_signed_derivative(self):
        with tempfile.TemporaryDirectory() as directory:
            run = subprocess.run(
                [sys.executable, str(SCRIPT)], cwd=directory,
                capture_output=True, text=True, check=False)
            self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
            result = json.loads(
                (Path(directory) / "evidence/tests/pressure-data-amplitude-countermodel-2026-10-02.json")
                .read_text(encoding="utf-8"))

        self.assertEqual(result["source_sha256"], hashlib.sha256(SCRIPT.read_bytes()).hexdigest())
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["prefix_mass"], "5*B**2")
        self.assertEqual(result["tail_mass"], "2")
        self.assertEqual(result["pressure_derivative"], "10*B**2*eta/(eta**2 + 1)**3")
        self.assertEqual(result["eta_times_pressure_derivative"], "10*B**2*eta**2/(eta**2 + 1)**3")
        self.assertEqual(result["subthreshold_witness_B"], "1")
        self.assertIn("does not instantiate", result["scope"])


if __name__ == "__main__":
    unittest.main()
