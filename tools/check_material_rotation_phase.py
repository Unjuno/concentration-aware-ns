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


def illustrative_table():
    h = 0.01
    f_star = 0.336
    d_star = 1.0
    tau0 = 1.0
    rows = []
    for q in (1e-2, 3e-3, 1e-5, 1e-15):
        angle = (f_star * d_star ** (1 + h) * tau0 ** (-h)
                 * (q ** (-h) - 1) / h)
        rows.append({
            "Q_tau_over_tau0": f"{q:.0e}",
            "angle_radians": angle,
            "turns": angle / (2 * math.pi),
        })
    one_turn_q = (1 + 2 * math.pi * h /
                  (f_star * d_star ** (1 + h) * tau0 ** (-h))) ** (-1 / h)
    return {
        "profile_amplitude_f_star": f_star,
        "amplitude_provenance": "Illustrative only: the independent preprint reports F_0(0)=0.336 for one matched leading-order profile; this is not extracted for OpenAI's selected profile.",
        "h": h,
        "d_star": d_star,
        "tau0": tau0,
        "cumulative_tangent_rotation": rows,
        "one_turn_threshold_Q": one_turn_q,
    }


def result():
    return {
        "schema_version": 1,
        "source_relation": "docs/openai-core-material-trajectory.md gives q=tau/d_star and Omega=q^(-1-h)*f(0,eta_star) along a fixed-eta axis material trajectory.",
        "symbolic": symbolic_identity(),
        "illustration": illustrative_table(),
        "scope": "Cumulative rotation of the infinitesimal transverse tangent frame only. It is conditional on a fixed nonzero f_star, the source path remaining in the core, and its local deformation equation. It is not an off-axis tracer trajectory, winding theorem for a finite curve, or molecular-orientation prediction.",
        "interpretation": "For any fixed h>=0 and nonzero f_star the integrated tangent-frame angle is unbounded as Q tends to zero, although each finite preterminal interval has finite angle. The transverse-to-axial direction ratio still tends to zero because axial stretching dominates; an unbounded transverse phase does not prevent directional alignment. Physical cutoffs in the cited illustrative liquid/gas estimates occur much earlier than the mathematical Q->0 limit.",
    }


if __name__ == "__main__":
    output = result()
    path = Path("evidence/tests/material-rotation-phase.json")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps(output, indent=2))
