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


def test_linearized_ensemble_concentrates_to_axis_but_escapes_bounded_segments():
    result = subprocess.run(
        [sys.executable, "-m", "tools.check_alignment_uncertainty"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    report = json.loads(result.stdout)
    assert report["identities"]["transverse_tube_probability_tends_to_one"]
    assert report["identities"]["bounded_axis_segment_probability_tends_to_zero"]
    assert report["identities"]["bounded_axis_segment_leading_order_is_q_to_C"]
