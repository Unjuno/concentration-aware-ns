"""Check exact exponent and derivative identities for the cusp-tube note.

This is symbolic algebra only. The mean-value inequality, primitive support
instantiation, and assembled-field conclusion are proved or audited separately.
"""
import json
from pathlib import Path

import sympy as sp


def check():
    h, D, q, eta, s = sp.symbols("h D q eta s", real=True)
    D_value = sp.Rational(1, 2) - h
    exponent_identity = sp.simplify(2 * D_value + 2 * h - 1) == 0

    chart_factor_residual = sp.simplify(
        q - eta**2 * q ** (2 * D_value + 2 * h) - q * (1 - eta**2)
    )
    chart_factor_identity = chart_factor_residual == 0

    # After the ordinary product/chain rule, both terms share
    # (1-s^2)^(-D-1); verify the remaining coefficient exactly.
    derivative_coefficient = (1 - s**2) + 2 * D_value * s**2
    derivative_factorization = sp.simplify(
        derivative_coefficient - (1 - 2 * h * s**2)
    ) == 0

    tau_pos, d_pos = sp.symbols("tau_pos d_pos", positive=True)
    tau_power_identity = sp.simplify(
        eta * (tau_pos / d_pos) ** D_value / tau_pos**D_value
        - eta * d_pos ** (-D_value)
    ) == 0

    result = {
        "scope": "Exact symbolic identities only; no support-family instantiation or end-to-end tube theorem.",
        "sympy": sp.__version__,
        "D_equals_half_minus_h": True,
        "2D_plus_2h_equals_one": exponent_identity,
        "similarity_chart_factor_identity": chart_factor_identity,
        "normalized_axis_trajectory_identity": tau_power_identity,
        "F_derivative_factorization": derivative_factorization,
        "derivative_factor": "(1-s^2)^(-D-1) * (1-2*h*s^2)",
        "positive_lower_bound_under_note_assumptions": "1-2*h > 0 for 0<h<1/2 and |s|<1",
    }
    output = Path("evidence/tests/support-hole-tube-geometry.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    if not all((exponent_identity, chart_factor_identity, tau_power_identity, derivative_factorization)):
        raise SystemExit(1)


if __name__ == "__main__":
    check()
