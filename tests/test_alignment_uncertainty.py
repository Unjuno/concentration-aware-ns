import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_linearized_alignment_does_not_imply_positional_certainty():
    result = subprocess.run(
        [sys.executable, "-m", "tools.check_alignment_uncertainty"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    report = json.loads(result.stdout)
    assert report["success"]
    assert all(report["identities"].values())
    assert all(report["negative_controls"].values())
    assert "not a finite-packet theorem" in report["scope"]
