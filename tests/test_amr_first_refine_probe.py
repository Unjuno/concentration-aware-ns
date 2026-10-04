import json
from pathlib import Path

import pytest

from tools.analyze_amr_first_refine_probe import difference_in_differences


def test_predeclared_excess_growth_contrast():
    amr = {"0.001": 0.02, "0.002": 0.04, "0.003": 0.17}
    uniform = {"0.001": 0.03, "0.002": 0.05, "0.003": 0.07}
    assert difference_in_differences(amr, uniform) == pytest.approx(0.11)


def test_protocol_scopes_post_refinement_checkpoint_as_one_step_later():
    protocol = json.loads(Path(
        "protocols/high-gradient-of13-amr-first-refinement-v1.json"
    ).read_text())
    interpretation = protocol["predeclared_comparison"]["logical_boundary"]
    assert "one solved timestep after remapping" in interpretation
    assert "not isolate interpolation" in interpretation
    assert protocol["acceptance"]["quality_gate"].startswith("No new acceptance threshold")
