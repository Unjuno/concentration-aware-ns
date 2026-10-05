"""Exact incompressible-interface compatibility and planar Couette FV controls.

This solves a specified scalar resistance chain analytically, not OpenFOAM.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path("evidence/upstream-refresh/openfoam-interface-diffusion-source-2026-10-03.json")


def normal_dev2_jump(normal, normal_derivative_jump):
    normal, b = sp.Matrix(normal), sp.Matrix(normal_derivative_jump)
    jump = b * normal.T  # mathematical gradient convention: dU_i/dx_j
    return sp.simplify(normal.T * (jump - sp.Rational(2, 3) * sp.trace(jump) * sp.eye(3)))


def couette_chain(n, mu_left, mu_right, traction=1, harmonic=False):
    if n < 2 or n % 2:
        raise ValueError("an even grid count of at least two is required")
    left, right, tau = map(sp.sympify, (mu_left, mu_right, traction))
    if left.is_positive is not True or right.is_positive is not True:
        raise ValueError("positive viscosities are required")
    if tau.is_zero is not False:
        raise ValueError("nonzero traction is required for relative errors")
    h = sp.Rational(2, n)
    interface = 2 * left * right / (left + right) if harmonic else (left + right) / 2
    resistance = [h / (2 * left)]
    for face in range(1, n):
        mu = left if face < n // 2 else right if face > n // 2 else interface
        resistance.append(h / mu)
    resistance.append(h / (2 * right))
    boundary_left, boundary_right = -tau / left, tau / right
    flux = sp.simplify((boundary_right - boundary_left) / sum(resistance))
    points = [-1 + (sp.Rational(1, 2) + i) * h for i in range(n)]
    exact = [tau * x / (left if x < 0 else right) for x in points]
    cumulative = sp.Integer(0)
    values = []
    for segment in resistance[:-1]:
        cumulative += segment
        values.append(sp.simplify(boundary_left + flux * cumulative))
    error_squared = sp.simplify(sum((a-b)**2 for a,b in zip(values,exact)) / sum(x*x for x in exact))
    return {"h": h, "flux": flux, "values": values, "reference": exact,
            "relative_velocity_L2_squared": error_squared,
            "relative_flux_error": sp.simplify(flux / tau - 1)}


def derive():
    n = sp.Matrix(sp.symbols("n_x n_y n_z", real=True))
    b = sp.Matrix(sp.symbols("b_x b_y b_z", real=True))
    tangent_seed = sp.Matrix(sp.symbols("q_x q_y q_z", real=True))
    tangent = n.cross(tangent_seed)
    jump = b * n.T
    contraction = normal_dev2_jump(n, b)
    expected = sp.Rational(1, 3) * b.dot(n) * n.T
    checks = {
        "rank_one_jump_annihilates_tangent_directions": all(sp.simplify(x) == 0 for x in jump * tangent),
        "normal_dev2_contraction_is_one_third_divergence_jump": all(sp.simplify(x) == 0 for x in contraction - expected),
        "incompressible_tangent_jump_contraction_zero": all(x == 0 for x in normal_dev2_jump(n, tangent)),
    }
    left, right, tau = sp.symbols("mu_left mu_right tau", positive=True)
    normal = sp.Matrix([1, 0, 0])
    gradients = [sp.Matrix([[0,0,0],[tau/mu,0,0],[0,0,0]]) for mu in (left,right)]
    checks["compatible_shear_explicit_transpose_correction_zero"] = all(
        x == 0 for gradient in gradients for x in normal.T * gradient)
    checks["compatible_shear_total_traction_constant"] = all(
        sp.simplify(mu * gradient * normal - sp.Matrix([0,tau,0])) == sp.zeros(3,1)
        for mu,gradient in zip((left,right),gradients))
    ratio = sp.factor((left + right) / 2 * (1 / left + 1 / right) / 2)
    checks["exact_nodal_arithmetic_interface_ratio"] = sp.simplify(
        ratio - (1 + (left-right)**2 / (4*left*right))) == 0
    h = sp.symbols("h", positive=True)
    resistance = (1-h/2)*(1/left+1/right) + 2*h/(left+right)
    solved_ratio = sp.factor((1/left+1/right)/resistance)
    expected_ratio = 1 / (1 - h/2 * ((right-left)/(right+left))**2)
    checks["solved_chain_flux_ratio"] = sp.simplify(solved_ratio - expected_ratio) == 0
    leading = sp.simplify(sp.limit((solved_ratio-1)/h,h,0))
    checks["solved_flux_error_is_first_order"] = sp.simplify(leading - (right-left)**2/(2*(right+left)**2)) == 0

    rows = []
    for count in (16,32,64):
        arithmetic = couette_chain(count,1,100)
        harmonic = couette_chain(count,1,100,harmonic=True)
        assert harmonic["flux"] == 1 and harmonic["relative_velocity_L2_squared"] == 0
        rows.append({"n":count,"h":str(arithmetic["h"]),
                     "arithmetic_flux_exact":str(arithmetic["flux"]),
                     "arithmetic_relative_flux_error_exact":str(arithmetic["relative_flux_error"]),
                     "arithmetic_relative_flux_error":float(arithmetic["relative_flux_error"]),
                     "arithmetic_relative_velocity_L2_squared_exact":str(arithmetic["relative_velocity_L2_squared"]),
                     "harmonic_flux_exact":str(harmonic["flux"]),
                     "harmonic_cell_value_error_exact":"0"})
    checks["three_grid_harmonic_exact_cell_values"] = all(row["harmonic_cell_value_error_exact"] == "0" for row in rows)
    checks["arithmetic_solved_flux_error_decreases"] = all(
        sp.Rational(rows[i]["arithmetic_relative_flux_error_exact"])
        > sp.Rational(rows[i+1]["arithmetic_relative_flux_error_exact"]) > 0
        for i in range(2))
    assert all(checks.values()), checks
    source = (ROOT / SOURCE).read_bytes()
    manifest = json.loads(source)
    assert manifest["source_commit"] == "18870c24d21c6b982e2cdec27b2f59738cca5f90"
    assert manifest["all_match_local_tree"]
    return {
        "status":"PASS_COMPATIBILITY_AND_EXACT_RESISTANCE_CHAIN_ONLY",
        "checker":"tools/check_interface_stress_compatibility.py",
        "checker_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "source_manifest":str(SOURCE),"source_manifest_sha256":hashlib.sha256(source).hexdigest(),
        "source_commit":manifest["source_commit"],
        "symbolic_backend":f"SymPy {sp.__version__}","checks":checks,
        "compatibility":{"premises":"C0 velocity with a common C1 tangential trace on a planar interface, piecewise C1 one-sided velocity gradients, divergence zero on both sides, matching interface normal and tensor convention.",
                         "gradient_jump":"[A]=b outer n; b dot n=0",
                         "explicit_contracted_jump":"n.T*dev2([A])=(b dot n)*n.T/3=0",
                         "bounded_piecewise_C2_sample_consequence":"Across adjacent normal samples, contracted tensor difference is O(h); with bounded coefficient jump and common linear weights, correction density is O(1), volume L1 is O(h), volume L2 squared is O(h). This excludes the fixed nonzero-contracted-jump scaling for this compatible continuum class."},
        "couette":{"domain":"x in [-1,1]; interface x=0; rho=1; U=(0,tau*x/mu_side,0); p=constant; forcing=0; stationary material interface; mu_side>0; tau!=0 for relative metrics",
                   "discretization":"Even uniform cell-centered Cartesian grid; specified orthogonal uncorrected scalar-coefficient FV diffusion; fixed-value wall velocities; coefficient arithmetic or harmonic at the aligned interface.",
                   "explicit_correction_flux":"0 on both sides for exact shear gradients",
                   "exact_nodal_arithmetic_face_flux_ratio":str(ratio),
                   "ratio_contrast_100":str(ratio.subs({left:1,right:100})),
                   "solved_arithmetic_flux_ratio":str(expected_ratio),
                   "relative_flux_error_over_h_limit":str(leading),
                   "all_discrete_cell_flux_balances":"0 by constant chain flux; independent stiffness-matrix tests verify the chain solution.",
                   "grids":rows},
        "scope_limits":[
            "The rank-one compatibility is conditional on shared differentiable velocity traces and one-sided incompressibility. Discontinuous/slip traces and inaccurate discrete gradients are outside it.",
            "The resistance chain is an exact analysis of a specified stationary orthogonal FV stencil; no OpenFOAM binary, VoF interface transport, pressure coupling, nonorthogonal mesh or upstream reproducer was executed.",
            "The observed face interpolation mismatch is a coefficient-interface discretization control. It is not a violated implementation contract or a new issue report.",
            "Viscosity is prescribed and unchanged; no speed-dependent viscosity, particle alignment, phase transition or continuum blow-up follows.",
        ],
    }


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",type=Path,default=Path("evidence/tests/interface-stress-compatibility-2026-10-03.json"))
    args=parser.parse_args();result=derive();encoded=json.dumps(result,indent=2)+"\n"
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(encoded);print(encoded,end="")


if __name__ == "__main__":
    main()
