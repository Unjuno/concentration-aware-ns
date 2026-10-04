"""Symbolically check a smooth divergence-free FV-observation null sequence."""
from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


def audit() -> dict:
    x, y, z, k = sp.symbols("x y z k", positive=True)
    chi = sp.Function("chi")(x, y, z)
    az = k ** sp.Rational(-3, 2) * chi * sp.sin(k * y)
    w = sp.Matrix([sp.diff(az, y), -sp.diff(az, x), 0])
    div = sp.simplify(sp.diff(w[0], x) + sp.diff(w[1], y) + sp.diff(w[2], z))

    expected_wx = (
        k ** sp.Rational(-3, 2) * sp.diff(chi, y) * sp.sin(k * y)
        + k ** sp.Rational(-1, 2) * chi * sp.cos(k * y)
    )
    expected_dy_wx = (
        k ** sp.Rational(-3, 2) * sp.diff(chi, y, 2) * sp.sin(k * y)
        + 2 * k ** sp.Rational(-1, 2) * sp.diff(chi, y) * sp.cos(k * y)
        - k ** sp.Rational(1, 2) * chi * sp.sin(k * y)
    )
    assert div == 0
    assert sp.simplify(w[0] - expected_wx) == 0
    assert sp.simplify(sp.diff(w[0], y) - expected_dy_wx) == 0

    return {
        "scope": "Symbolic derivative identity for a conditional smooth compactly supported construction; not an OpenFOAM field reconstruction or Navier-Stokes solution with the benchmark forcing.",
        "vector_potential": "A_k=(0,0,k^(-3/2)*chi(x,y,z)*sin(k*y))",
        "cutoff_assumption": "chi is a nonzero C-infinity function supported strictly inside one cell",
        "curl_x": "k^(-3/2)*chi_y*sin(k*y) + k^(-1/2)*chi*cos(k*y)",
        "curl_y": "-k^(-3/2)*chi_x*sin(k*y)",
        "divergence_identity": "identically zero by cancellation of mixed partial derivatives",
        "uniform_velocity_bound": "O(k^(-1/2)) for fixed smooth chi",
        "gradient_y_component": "-k^(1/2)*chi*sin(k*y) + 2*k^(-1/2)*chi_y*cos(k*y) + k^(-3/2)*chi_yy*sin(k*y)",
        "gradient_supremum": "Theta(k^(1/2)) for nonzero chi; the oscillatory phase attains order-one sine values where |chi| is bounded below",
        "cell_average_invariance": "each curl component is a derivative of a function compactly supported inside the cell, hence its integral over that cell is zero",
        "face_trace_invariance": "the perturbation vanishes in a neighborhood of every cell face",
        "sympy_version": sp.__version__,
    }


def main() -> None:
    result = audit()
    output = Path("evidence/tests/fv-derivative-nullspace.json")
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
