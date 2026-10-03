"""Derive the same-weight face-interpolation covariance in a stress flux.

This checks a generic algebraic identity motivated by OpenFOAM Foundation
issue #2. It does not emulate OpenFOAM's complete fvc::dotInterpolate path or
validate the issue's attached CFD case.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import sympy as sp


def derive() -> dict[str, object]:
    w = sp.symbols("w", real=True)
    a_p, a_n, g_p, g_n = sp.symbols("a_P a_N G_P G_N", real=True)
    h, a0, a1, g0, g1, delta_a, delta_g = sp.symbols(
        "h a_0 a_1 G_0 G_1 delta_a delta_G", real=True
    )

    interpolate_product = w * a_p * g_p + (1 - w) * a_n * g_n
    product_of_interpolants = (w * a_p + (1 - w) * a_n) * (
        w * g_p + (1 - w) * g_n
    )
    defect = sp.factor(interpolate_product - product_of_interpolants)
    expected = w * (1 - w) * (a_p - a_n) * (g_p - g_n)

    a_p_smooth, a_n_smooth = a0, a0 + h * a1
    g_p_smooth, g_n_smooth = g0, g0 + h * g1
    smooth_defect = sp.factor(
        defect.subs({a_p: a_p_smooth, a_n: a_n_smooth,
                     g_p: g_p_smooth, g_n: g_n_smooth})
    )
    jump_defect = sp.factor(
        defect.subs({a_p: a0 + delta_a, a_n: a0,
                     g_p: g0 + delta_g, g_n: g0})
    )

    identities_pass = sp.simplify(defect - expected) == 0
    degeneracies_pass = all(
        sp.simplify(expected.subs(substitution)) == 0
        for substitution in (
            {w: 0}, {w: 1}, {a_p: a_n}, {g_p: g_n}
        )
    )
    smooth_leading_term_pass = sp.simplify(
        smooth_defect - w * (1 - w) * h**2 * a1 * g1
    ) == 0
    finite_jump_identity_pass = sp.simplify(
        jump_defect - w * (1 - w) * delta_a * delta_g
    ) == 0

    assert identities_pass
    assert degeneracies_pass
    assert smooth_leading_term_pass
    assert finite_jump_identity_pass

    return {
        "status": "PASS_GENERIC_IDENTITY_ONLY",
        "checker": "tools/audit_openfoam_stress_interpolation_identity.py",
        "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "symbolic_backend": f"SymPy {sp.__version__}",
        "interpolation_convention": "I_w(f)=w*f_P+(1-w)*f_N; identical weight on both factors",
        "identity": "I_w(a*G)-I_w(a)*I_w(G)=w*(1-w)*(a_P-a_N)*(G_P-G_N)",
        "sympy_defect": str(defect),
        "smooth_affine_field_defect": str(smooth_defect),
        "piecewise_constant_jump_defect": str(jump_defect),
        "checks": {
            "product_interpolation_identity": identities_pass,
            "zero_for_endpoint_weights_or_one_constant_factor": degeneracies_pass,
            "smooth_affine_data_defect_is_quadratic_in_cell_spacing": smooth_leading_term_pass,
            "finite_jump_defect_has_no_cell_spacing_factor": finite_jump_identity_pass,
        },
        "interpretation": {
            "smooth_coefficient_and_gradient": "For fixed 0<w<1 and differentiable fields sampled at adjacent cells, the face product defect is O(h^2).",
            "unresolved_interface_jump": "For finite coefficient and gradient jumps, the algebraic face defect can remain O(1) as h shrinks; this says nothing by itself about the assembled operator or solution error.",
            "benchmark_relation": "The primary OpenFOAM MMS uses a smooth single-phase field and constant nu=0.01, so this coefficient-jump mechanism is outside that frozen case.",
            "upstream_issue": "https://github.com/OpenFOAM/OpenFOAM-13/issues/2",
            "upstream_change": "https://github.com/OpenFOAM/OpenFOAM-13/commit/6592798ca0704aa6eaaaaf74ea3cc6a9553317dc",
        },
        "scope_limits": [
            "This is an algebraic identity for a generic same-weight linear interpolation, componentwise for vector or tensor G.",
            "It does not establish that OpenFOAM fvc::dotInterpolate uses this exact equivalent operator in every scheme or mesh geometry.",
            "It does not reproduce the attached OpenFOAM issue case or prove either version's discretization is wrong.",
            "It supports no inference about molecular ordering, physical viscosity reduction, phase transition, or a continuum singularity.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("evidence/tests/openfoam-stress-interpolation-covariance-2026-10-03.json"),
    )
    args = parser.parse_args()
    result = derive()
    encoded = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded, encoding="utf-8")
    print(encoded, end="")


if __name__ == "__main__":
    main()
