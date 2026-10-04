"""Measure reference-only centered-FD2 peak floors across envelope widths."""
import json
import math
from pathlib import Path

import numpy as np

from tools.high_gradient_reference import fields
from tools.metrics import diagnostics


SCOPE = (
    "Exact MMS samples passed through the benchmark's periodic centered-FD2 "
    "diagnostics; reference-only truncation floor, not solver output or defect evidence."
)


def audit(envelope_powers=(1, 2, 4, 8, 16, 32), n_values=(16, 32, 64, 128),
          protocol_path="protocols/high-gradient-of13-v2.json"):
    """Audit sampled peak floors; no solver output or continuum bound is used."""
    protocol_path = Path(protocol_path)
    spec = json.loads(protocol_path.read_text())
    powers = tuple(envelope_powers)
    counts = tuple(n_values)
    if not powers or any(int(p) != p or p < 1 for p in powers):
        raise ValueError("envelope_powers must contain positive integers")
    if not counts or any(int(n) != n or n < 4 for n in counts):
        raise ValueError("n_values must contain integers >= 4")
    if len(set(powers)) != len(powers) or len(set(counts)) != len(counts):
        raise ValueError("envelope_powers and n_values must not contain duplicates")

    frequency = spec["frequency_N"]
    time = spec["end_time"]
    viscosity = spec["viscosity"]
    thresholds = spec["local_quality_relative_error_thresholds"]
    length = 2 * np.pi
    width_rows = []
    for power in powers:
        rows = []
        for n in counts:
            axis = (np.arange(n) + 0.5) * length / n
            z, y, x = np.meshgrid(axis, axis, axis, indexing="ij")
            points = np.stack((x, y, z), axis=-1).reshape(-1, 3)
            reference = fields(points, N=frequency, nu=viscosity, time=time,
                               envelope_power=power)
            grid = reference["u"].reshape(n, n, n, 3).transpose(2, 1, 0, 3)
            fd2 = diagnostics(grid)
            exact_gradient_peak = float(np.linalg.norm(
                reference["grad_u"], axis=(-2, -1)
            ).max())
            exact_vorticity_peak = float(np.linalg.norm(
                reference["vorticity"], axis=-1
            ).max())
            gradient_floor = abs(fd2["max_gradient_fd2"] - exact_gradient_peak) / exact_gradient_peak
            vorticity_floor = abs(fd2["max_vorticity_fd2"] - exact_vorticity_peak) / exact_vorticity_peak
            rows.append({
                "n": n,
                "cells_per_highest_envelope_wavelength": n / power,
                "gradient_stencil_floor_relative_error": gradient_floor,
                "vorticity_stencil_floor_relative_error": vorticity_floor,
                "gradient_threshold": thresholds["max_gradient"],
                "vorticity_threshold": thresholds["max_vorticity"],
                "gradient_floor_within_threshold": gradient_floor <= thresholds["max_gradient"],
                "vorticity_floor_within_threshold": vorticity_floor <= thresholds["max_vorticity"],
                "reference_sampled_gradient_peak": exact_gradient_peak,
                "reference_sampled_vorticity_peak": exact_vorticity_peak,
                "fd2_gradient_peak": fd2["max_gradient_fd2"],
                "fd2_vorticity_peak": fd2["max_vorticity_fd2"],
            })
        width_rows.append({
            "envelope_power": power,
            "near_peak_equivalent_gaussian_sigma": math.sqrt(2 / power),
            "envelope": "((1+cos(q))/2)^m in each transverse coordinate",
            "rows": rows,
        })
    return {
        "status": "ANALYTIC_REFERENCE_ONLY",
        "protocol": str(protocol_path),
        "scope": SCOPE,
        "frequency_N": frequency,
        "time": time,
        "continuous_extrema": "NOT_CERTIFIED",
        "widths": width_rows,
        "interpretation": (
            "Near-peak equivalent width describes local curvature only. "
            "Each floor compares sampled analytic peaks to the same samples "
            "passed through centered-FD2; it is not a continuous-domain bound."
        ),
    }


if __name__ == "__main__":
    result = audit()
    target = Path("evidence/tests/high-gradient-width-sweep-reference-only.json")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
