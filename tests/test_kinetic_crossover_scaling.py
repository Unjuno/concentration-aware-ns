import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools/check_kinetic_crossover_scaling.py"


def test_conditional_kinetic_and_knudsen_power_laws():
    with tempfile.TemporaryDirectory() as tmp:
        result = subprocess.run([sys.executable, str(SCRIPT)], cwd=tmp,
                                capture_output=True, text=True, check=False)
        assert result.returncode == 0, result.stdout + result.stderr
        receipt = json.loads((Path(tmp) /
            "evidence/analytic-checks/kinetic-crossover-scaling-2026-10-04.json").read_text())
    assert receipt["source_sha256"] == hashlib.sha256(SCRIPT.read_bytes()).hexdigest()
    assert receipt["success"]
    assert all(receipt["controls"].values())
    assert receipt["derived"]["chi_power_in_s"] == "alpha - 1"
    assert receipt["derived"]["knudsen_power_in_s"] == "beta - 1/2"
