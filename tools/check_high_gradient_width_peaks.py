"""Exact continuum-peak certificates for the frozen N=4 width profiles.

This checker uses only symbolic polynomials and rational Bernstein bounds; it
does not load a CFD solver, archived run, or sampled field.
"""
from __future__ import annotations

import hashlib
import json
from math import comb
from pathlib import Path
import platform

import sympy as sp


WIDTHS = (1, 2, 4)
N = 4


def _bernstein_coefficients(polynomial: sp.Expr, s: sp.Symbol, r: sp.Symbol):
    """Return exact tensor Bernstein coefficients on the unit square."""
    poly = sp.Poly(sp.expand(polynomial), s, r)
    ds, dr = poly.degree(s), poly.degree(r)
    power = dict(poly.terms())
    coefficients = []
    for i in range(ds + 1):
        for j in range(dr + 1):
            value = sum((
                power.get((k, ell), sp.Integer(0))
                * sp.Rational(comb(i, k), comb(ds, k))
                * sp.Rational(comb(j, ell), comb(dr, ell))
                for k in range(i + 1) for ell in range(j + 1)
            ), sp.Integer(0))
            coefficients.append(sp.factor(value))
    return [ds, dr], coefficients


def _width_branches(power: int, s: sp.Symbol, r: sp.Symbol) -> dict[str, sp.Expr]:
    q = sp.symbols("q", real=True)
    g = lambda x: (1 - x) ** power
    gp, gpp = sp.diff(g(q), q), sp.diff(g(q), q, 2)
    gy2 = sp.expand(gp.subs(q, s) ** 2 * s * (1 - s))
    gz2 = sp.expand(gp.subs(q, r) ** 2 * r * (1 - r))
    gyy = sp.expand(gpp.subs(q, s) * s * (1 - s) + gp.subs(q, s) * (1 - 2 * s) / 2)

    chi = g(s) * g(r)
    chi_y2 = gy2 * g(r) ** 2
    chi_z2 = gz2 * g(s) ** 2
    chi_yy = gyy * g(r)
    chi_yz2 = gy2 * gz2
    return {
        "gradient_sin_branch": sp.expand(chi**2 + (chi_yy**2 + chi_yz2) / N**4),
        "gradient_cos_branch": sp.expand((2 * chi_y2 + chi_z2) / N**2),
        "vorticity_sin_branch": sp.expand((chi - chi_yy / N**2) ** 2 + chi_yz2 / N**4),
        "vorticity_cos_branch": sp.expand(chi_z2 / N**2),
    }


def _certify_width(power: int) -> dict:
    s, r = sp.symbols("s r", real=True)
    branches = _width_branches(power, s, r)
    peak_gradient_sq = sp.Rational(1) + sp.Rational(power**2, 1024)
    peak_vorticity_sq = (sp.Rational(1) + sp.Rational(power, 32)) ** 2
    upper = {
        "gradient_sin_branch": peak_gradient_sq,
        "gradient_cos_branch": peak_gradient_sq,
        "vorticity_sin_branch": peak_vorticity_sq,
        "vorticity_cos_branch": peak_vorticity_sq,
    }
    certs = {}
    for name, branch in branches.items():
        degree, coeffs = _bernstein_coefficients(upper[name] - branch, s, r)
        if not all(c.is_nonnegative for c in coeffs):
            raise AssertionError(f"width {power}: negative exact Bernstein coefficient in {name}")
        certs[name] = {
            "degree": degree,
            "gap_bernstein_coefficients": [sp.sstr(c) for c in coeffs],
            "all_nonnegative": True,
        }

    attained = (
        sp.simplify(branches["gradient_sin_branch"].subs({s: 0, r: 0}) - peak_gradient_sq) == 0
        and sp.simplify(branches["vorticity_sin_branch"].subs({s: 0, r: 0}) - peak_vorticity_sq) == 0
    )
    if not attained:
        raise AssertionError(f"width {power}: center does not attain both claimed peaks")
    return {
        "all_gap_bernstein_coefficients_nonnegative": True,
        "attained_at_center": True,
        "bernstein_certificate_degrees": {k: v["degree"] for k, v in certs.items()},
        "branches": {
            name: {"squared_upper_bound": sp.sstr(upper[name]), **cert}
            for name, cert in certs.items()
        },
    }


def certify_width_peaks() -> dict:
    results = {str(power): _certify_width(power) for power in WIDTHS}
    peaks = {
        str(power): {
            "gradient_frobenius_squared": sp.sstr(sp.Rational(1) + sp.Rational(power**2, 1024)),
            "vorticity_squared": sp.sstr((sp.Rational(1) + sp.Rational(power, 32)) ** 2),
        }
        for power in WIDTHS
    }
    return {
        "schema": "high-gradient-width-global-peaks/v1",
        "scope": "Exact continuum extrema of the frozen width-v1 analytic reference only; no solver or simulation is used.",
        "frequency_N": N,
        "envelope_powers": list(WIDTHS),
        "reduction": {
            "variables": "s=sin(y/2)^2 and r=sin(z/2)^2 in [0,1]",
            "envelope": "g_m(q)=(1-q)^m",
            "branch_rule": "Each squared norm is a*sin(N*x)^2+b*cos(N*x)^2; certify both branches separately.",
            "basis": "Exact tensor Bernstein basis on [0,1]^2 at each polynomial's exact bidegree.",
        },
        "peaks_squared_at_time_zero": peaks,
        "peaks_at_time_zero": {
            str(power): {
                "gradient_frobenius": sp.sstr(sp.sqrt(sp.Rational(1) + sp.Rational(power**2, 1024))),
                "vorticity": sp.sstr(sp.Rational(1) + sp.Rational(power, 32)),
            }
            for power in WIDTHS
        },
        "time_dependence": "Both norms scale by exp(-t); their squares scale by exp(-2*t).",
        "attainment_point": {"x": "pi/(2*N)", "y": "0", "z": "0", "N": N},
        "width_certificates": results,
        "provenance": {
            "command": "python -m tools.check_high_gradient_width_peaks",
            "python_version": platform.python_version(),
            "sympy_version": sp.__version__,
            "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "reference_evaluator_sha256": hashlib.sha256(
                Path(__file__).with_name("high_gradient_reference.py").read_bytes()
            ).hexdigest(),
        },
        "limitations": [
            "The certificates apply to the exact analytic reference, not a CFD or learned field.",
            "They certify N=4 and width powers 1, 2, and 4 only.",
            "They do not establish solver convergence, within-cell extrema, molecular alignment, a phase transition, viscosity collapse, or blow-up.",
            "Existing solver acceptance denominators and historical classifications are unchanged.",
        ],
    }


def run(output: Path = Path("evidence/tests/high-gradient-width-global-peaks.json")) -> dict:
    result = certify_width_peaks()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    return result


if __name__ == "__main__":
    run()
