import numpy as np
import pytest

from tools.physicsnemo_validation_v2 import (
    quality_verdict,
    sampled_quality_metrics,
    validation_grid,
)
from tools.reference import fields


THRESHOLDS = {
    "velocity_relative_l2": 0.02,
    "energy_relative_error": 0.02,
    "gradient_peak_relative_error_samples": 0.05,
    "vorticity_peak_relative_error_samples": 0.05,
    "shell_spectrum_relative_l1": 0.05,
    "divergence_peak_normalized": 0.05,
}


def test_quality_verdict_passes_at_inclusive_thresholds():
    assert quality_verdict(THRESHOLDS, THRESHOLDS) == "PASS"


def test_quality_verdict_fails_if_any_metric_exceeds_threshold():
    metrics = dict(THRESHOLDS, gradient_peak_relative_error_samples=0.050001)
    assert quality_verdict(metrics, THRESHOLDS) == "FAIL"


def test_quality_verdict_rejects_missing_or_nonfinite_metrics():
    with pytest.raises(ValueError, match="missing metrics"):
        quality_verdict({"velocity_relative_l2": 0.01}, THRESHOLDS)
    metrics = dict(THRESHOLDS, energy_relative_error=float("nan"))
    with pytest.raises(ValueError, match="finite nonnegative"):
        quality_verdict(metrics, THRESHOLDS)


def test_validation_grid_is_deterministic_and_disjoint_from_old_half_cell_grid():
    first = validation_grid(8, 0.618034)
    second = validation_grid(8, 0.618034)
    old = validation_grid(8, 0.37)
    assert np.array_equal(first, second)
    assert first.shape == (8**3, 3)
    assert not np.array_equal(first, old)
    assert not np.isclose(first[:, 0], old[:, 0, None]).any()


def test_exact_mms_samples_pass_every_prospective_quality_metric():
    n = 4
    xyz = validation_grid(n, 0.618034)
    exact = fields(xyz, time=0.05)
    metrics = sampled_quality_metrics(
        exact["u"], exact["grad_u"], exact["u"], exact["grad_u"],
        exact["vorticity"], (n, n, n),
    )
    assert metrics["velocity_relative_l2"] == 0
    assert metrics["energy_relative_error"] == 0
    assert metrics["gradient_peak_relative_error_samples"] == 0
    assert metrics["vorticity_peak_relative_error_samples"] == 0
    assert metrics["shell_spectrum_relative_l1"] == 0
    assert metrics["divergence_peak_normalized"] < 1e-12
    assert quality_verdict(metrics, THRESHOLDS) == "PASS"
