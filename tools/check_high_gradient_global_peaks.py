"""Certify the exact continuous local peaks of the N=4 Fourier MMS.

The solver is not used. Trigonometric dependence is reduced to two variables
in [0, 1], then exact Bernstein coefficients certify each global upper bound.
"""
from __future__ import annotations

import json
import hashlib
from math import comb
from pathlib import Path
import platform

import sympy as sp


def _bernstein_coefficients(polynomial: sp.Expr, s: sp.Symbol, r: sp.Symbol):
    """Return the exact tensor Bernstein coefficients on [0,1]^2."""
    poly = sp.Poly(sp.expand(polynomial), s, r)
    degree_s, degree_r = poly.degree(s), poly.degree(r)
    power = {monomial: coefficient for monomial, coefficient in poly.terms()}
    coefficients = []
    for i in range(degree_s + 1):
        for j in range(degree_r + 1):
            value = sum((
                power.get((k, ell), sp.Integer(0))
                * sp.Rational(comb(i, k), comb(degree_s, k))
                * sp.Rational(comb(j, ell), comb(degree_r, ell))
                for k in range(i + 1) for ell in range(j + 1)
            ), sp.Integer(0))
            coefficients.append(sp.factor(value))
    return [degree_s, degree_r], coefficients


def certify_global_peaks() -> dict:
    s, r = sp.symbols("s r", real=True)
    N = 4
    envelope = lambda q: (1 - q) ** 4
    envelope_first_sq = lambda q: 16 * q * (1 - q) ** 7
    envelope_second = lambda q: 2 * (1 - q) ** 3 * (8 * q - 1)

    # Verify these derivative reductions from s=sin(y/2)^2 and ds/dy.
    q = sp.symbols("q", real=True)
    g = (1 - q) ** 4
    g_prime = sp.diff(g, q)
    g_second = sp.diff(g, q, 2)
    first_square_identity = sp.expand(
        g_prime**2 * q * (1 - q) - envelope_first_sq(q)
    ) == 0
    second_identity = sp.expand(
        g_second * q * (1 - q) + g_prime * (1 - 2 * q) / 2
        - envelope_second(q)
    ) == 0
    if not (first_square_identity and second_identity):
        raise AssertionError("envelope derivative reduction failed")

    chi = envelope(s) * envelope(r)
    chi_y_squared = envelope_first_sq(s) * envelope(r) ** 2
    chi_z_squared = envelope_first_sq(r) * envelope(s) ** 2
    chi_yy = envelope_second(s) * envelope(r)
    chi_yz_squared = envelope_first_sq(s) * envelope_first_sq(r)

    gradient_sin = sp.expand(
        chi**2 + (chi_yy**2 + chi_yz_squared) / N**4
    )
    gradient_cos = sp.expand(
        (2 * chi_y_squared + chi_z_squared) / N**2
    )
    vorticity_sin = sp.expand(
        (chi - chi_yy / N**2) ** 2 + chi_yz_squared / N**4
    )
    vorticity_cos = sp.expand(chi_z_squared / N**2)

    squared_peaks = {
        "gradient_sin_branch": sp.Rational(65, 64),
        "gradient_cos_branch": sp.Rational(65, 64),
        "vorticity_sin_branch": sp.Rational(81, 64),
        "vorticity_cos_branch": sp.Rational(81, 64),
    }
    branches = {
        "gradient_sin_branch": gradient_sin,
        "gradient_cos_branch": gradient_cos,
        "vorticity_sin_branch": vorticity_sin,
        "vorticity_cos_branch": vorticity_cos,
    }

    certificates = {}
    for name, branch in branches.items():
        degree, coefficients = _bernstein_coefficients(
            squared_peaks[name] - branch, s, r
        )
        if not all(coefficient.is_nonnegative for coefficient in coefficients):
            raise AssertionError(f"negative Bernstein coefficient in {name}")
        certificates[name] = {
            "degree": degree,
            "gap_bernstein_coefficients": [sp.sstr(c) for c in coefficients],
            "all_nonnegative": True,
        }

    if sp.simplify(gradient_sin.subs({s: 0, r: 0}) - sp.Rational(65, 64)) != 0:
        raise AssertionError("gradient peak is not attained at the claimed point")
    if sp.simplify(vorticity_sin.subs({s: 0, r: 0}) - sp.Rational(81, 64)) != 0:
        raise AssertionError("vorticity peak is not attained at the claimed point")

    return {
        "schema": "high-gradient-global-peaks/v1",
        "scope": (
            "Exact global continuum peaks for the frozen N=4 Fourier-envelope "
            "MMS; no CFD solver or sampled field is used."
        ),
        "reduction": {
            "variables": "s=sin(y/2)^2, r=sin(z/2)^2 in [0,1]",
            "x_dependence": "Each squared norm is a*sin(N*x)^2+b*cos(N*x)^2, so its global x maximum is max(a,b).",
            "bernstein_basis": "Tensor Bernstein basis of bidegree (8,8); coefficients are exact rationals.",
        },
        "peaks_at_time_zero": {
            "gradient_frobenius": "sqrt(65)/8",
            "vorticity": "9/8",
        },
        "time_dependence": "Both peaks are multiplied by exp(-t).",
        "attainment_point": {"x": "pi/(2*N)", "y": "0", "z": "0", "N": N},
        "envelope_derivative_identities": {
            "first_derivative_square": first_square_identity,
            "second_derivative": second_identity,
        },
        "bernstein_certificate_degrees": {
            name: certificate["degree"] for name, certificate in certificates.items()
        },
        "all_gap_bernstein_coefficients_nonnegative": all(
            certificate["all_nonnegative"] for certificate in certificates.values()
        ),
        "provenance": {
            "command": "python -m tools.check_high_gradient_global_peaks",
            "python_version": platform.python_version(),
            "sympy_version": sp.__version__,
            "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "reference_evaluator_sha256": hashlib.sha256(
                Path(__file__).with_name("high_gradient_reference.py").read_bytes()
            ).hexdigest(),
        },
        "branches": {
            name: {
                "squared_upper_bound": sp.sstr(squared_peaks[name]),
                **certificate,
            }
            for name, certificate in certificates.items()
        },
        "limitations": [
            "The certificate applies to the exact analytic reference, not any solver or learned field.",
            "It certifies the N=4 shared MMS only; other N values require their own coefficients and certificates.",
            "It does not certify temporal or spatial convergence or the solver's within-cell reconstruction.",
        ],
    }


def run(output: Path = Path("evidence/tests/high-gradient-global-peaks.json")) -> dict:
    result = certify_global_peaks()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    return result


if __name__ == "__main__":
    run()
