"""Integrate the transverse tangent-frame rotation on the selected axis path.

This checks a hand-derived consequence already recorded in
docs/openai-core-material-trajectory.md. It is not an off-axis particle
trajectory or a molecular model.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import sympy as sp


def symbolic_identity():
    h, d, tau, tau0 = sp.symbols("h d tau tau0", positive=True)
    f = sp.symbols("f", real=True)
    omega_tau = f * (tau / d) ** (-1 - h)
    angle = f * d ** (1 + h) / h * (tau ** (-h) - tau0 ** (-h))
    derivative = sp.diff(angle, tau)
    assert sp.simplify(derivative + omega_tau) == 0
    return {
        "angular_rate": "Omega(t) = f_star * (tau/d_star)^(-1-h)",
        "integrated_angle": "DeltaTheta(Q) = f_star*d_star^(1+h)*tau0^(-h)*(Q^(-h)-1)/h",
        "per_decade_angle": "f_star*d_star^(1+h)*tau0^(-h)*Q^(-h)*(10^h-1)/h",
        "symbolic_derivative_check": "PASS",
        "h_zero_limit": "DeltaTheta = f_star*d_star*log(1/Q)",
    }


def phase_sensitivity():
    rows = []
    unit_scale_thresholds = []
    for h in (0.0, 0.005, 0.0099):
        q_one_turn = (
            math.exp(-2 * math.pi)
            if h == 0
            else (1 + 2 * math.pi * h) ** (-1 / h)
        )
        unit_scale_thresholds.append({
            "h": h,
            "K": 1.0,
            "Q_for_one_turn": q_one_turn,
        })
        for q in (1e-2, 1e-5, 1e-15):
            turns_per_scale = (
                math.log(1 / q) / (2 * math.pi)
                if h == 0
                else (q ** (-h) - 1) / (2 * math.pi * h)
            )
            rows.append({
                "h": h,
                "Q_tau_over_tau0": f"{q:.0e}",
                "turns_per_K": turns_per_scale,
            })
    return {
        "dimensionless_scale": "K = f_star*d_star^(1+h)*tau0^(-h)",
        "interpretation": "Each turns_per_K entry is multiplied by K; no profile coefficient is assumed or imported.",
        "cumulative_tangent_rotation_sensitivity": rows,
        "unit_scale_one_turn_thresholds": unit_scale_thresholds,
    }


def result():
    return {
        "schema_version": 1,
        "source_relation": "docs/openai-core-material-trajectory.md gives q=tau/d_star and Omega=q^(-1-h)*f(0,eta_star) along a fixed-eta axis material trajectory.",
        "symbolic": symbolic_identity(),
        "sensitivity": phase_sensitivity(),
        "sensitivity": phase_sensitivity(),
        "scope": "Cumulative rotation of the infinitesimal transverse tangent frame only. It is conditional on the profile identity, a fixed nonzero f_star, the source path remaining in the core, and its local deformation equation. It is not an off-axis tracer trajectory, winding theorem for a finite curve, or molecular-orientation prediction.",
        "interpretation": "For any fixed h>=0 and nonzero f_star the integrated tangent-frame angle is unbounded as Q tends to zero, although each finite preterminal interval has finite angle. The transverse-to-axial direction ratio still tends to zero because axial stretching dominates; an unbounded transverse phase does not prevent directional alignment. No externally computed profile coefficient is assumed.",
    }


if __name__ == "__main__":
    output = result()
    path = Path("evidence/tests/material-rotation-phase.json")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps(output, indent=2))
