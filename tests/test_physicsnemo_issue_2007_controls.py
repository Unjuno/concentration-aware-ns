"""Adversarial controls for the focused upstream fix verdict, without Torch."""
from copy import deepcopy
import pytest
from tools.reproduce_physicsnemo_issue_2007 import classify_controls


def healthy():
    peak = {"index": 1, "power": 1.0, "bins": [0.0, 1.0]}
    return {n: {"height_wave_peak": deepcopy(peak),
                "width_wave_peak": deepcopy(peak),
                "height_vs_width_peak_equal": True,
                "height_vs_width_spectrum_allclose": True} for n in ("32", "33")} | {
        "transpose_controls": {"odd_33x33_max_abs_difference": 0.0,
                               "even_32x32_max_abs_difference": 0.0,
                               "odd_33x33_allclose": True, "even_32x32_allclose": True}}


def test_fixed_symmetry_and_original_asymmetry_are_distinct():
    r = healthy()
    assert classify_controls(r) == (False, True)
    r["33"]["height_vs_width_peak_equal"] = False
    r["33"]["height_vs_width_spectrum_allclose"] = False
    r["transpose_controls"]["odd_33x33_allclose"] = False
    assert classify_controls(r) == (True, False)
    # The former `not reproduced` rule incorrectly called this broken control fixed.
    r["32"]["height_vs_width_spectrum_allclose"] = False
    assert classify_controls(r) == (False, False)


@pytest.mark.parametrize("case,key", [("32", "height_vs_width_peak_equal"),
    ("32", "height_vs_width_spectrum_allclose"), ("33", "height_vs_width_peak_equal"),
    ("33", "height_vs_width_spectrum_allclose"),
    ("transpose_controls", "odd_33x33_allclose"),
    ("transpose_controls", "even_32x32_allclose")])
def test_any_failed_required_symmetry_rejects_fixed(case, key):
    r = healthy(); r[case][key] = False
    assert not classify_controls(r)[1]


@pytest.mark.parametrize("value", [0.0, float("nan"), float("inf"), -1.0])
def test_degenerate_or_invalid_spectra_reject_fix(value):
    r = healthy()
    r["33"]["width_wave_peak"].update(power=value, bins=[value])
    assert classify_controls(r) == (False, False)
