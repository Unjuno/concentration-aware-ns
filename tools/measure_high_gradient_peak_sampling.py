"""Measure cell-center sampling loss against the certified N=4 continuum peaks."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np

from tools.high_gradient_reference import fields


def measure(resolutions=(16, 32, 64, 128), time=0.05) -> dict:
    resolutions = tuple(resolutions)
    if not np.isfinite(time) or time < 0:
        raise ValueError("time must be finite and nonnegative")
    if any(not isinstance(n, int) or n < 1 for n in resolutions):
        raise ValueError("resolutions must be positive integers")

    continuum_gradient = np.sqrt(65) / 8 * np.exp(-time)
    continuum_vorticity = 9 / 8 * np.exp(-time)
    rows = []
    for n in resolutions:
        axis = (np.arange(n) + 0.5) * 2 * np.pi / n
        z, y, x = np.meshgrid(axis, axis, axis, indexing="ij")
        centers = np.stack((x, y, z), axis=-1).reshape(-1, 3)
        reference = fields(centers, N=4, time=time)
        sampled_gradient = float(np.linalg.norm(reference["grad_u"], axis=(-2, -1)).max())
        sampled_vorticity = float(np.linalg.norm(reference["vorticity"], axis=-1).max())
        rows.append({
            "n": n,
            "sampled_gradient_peak": sampled_gradient,
            "certified_continuum_gradient_peak": float(continuum_gradient),
            "gradient_fraction": float(sampled_gradient / continuum_gradient),
            "sampled_vorticity_peak": sampled_vorticity,
            "certified_continuum_vorticity_peak": float(continuum_vorticity),
            "vorticity_fraction": float(sampled_vorticity / continuum_vorticity),
        })

    reference_path = Path(__file__).with_name("high_gradient_reference.py")
    certificate_path = (
        Path(__file__).resolve().parent.parent / "evidence/tests/high-gradient-global-peaks.json"
    )
    return {
        "schema": "high-gradient-cell-center-peak-sampling/v1",
        "scope": (
            "Reference-field sampling only: exact analytic derivatives sampled on periodic "
            "uniform-grid cell centers, divided by certified N=4 continuum peaks."
        ),
        "parameters": {"N": 4, "time": float(time), "resolutions": list(resolutions)},
        "interpretation": (
            "Fractions quantify reference peak undersampling only. They do not measure solver "
            "error, bound a numerical field between cells, or alter an acceptance gate."
        ),
        "rows": rows,
        "provenance": {
            "measurement_tool_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "reference_evaluator_sha256": hashlib.sha256(reference_path.read_bytes()).hexdigest(),
            "continuum_certificate_sha256": (
                hashlib.sha256(certificate_path.read_bytes()).hexdigest()
                if certificate_path.exists() else None
            ),
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    parser.add_argument("--time", type=float, default=0.05)
    args = parser.parse_args()
    result = measure(time=args.time)
    serialized = json.dumps(result, indent=2, allow_nan=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(serialized)
    print(serialized, end="")


if __name__ == "__main__":
    main()
