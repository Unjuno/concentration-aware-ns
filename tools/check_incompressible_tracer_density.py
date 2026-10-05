"""Symbolically verify the finite-dimensional Liouville determinant identity.

This checks the algebra used in docs/incompressible-tracer-density-invariant.md;
the smooth-flow and change-of-variables hypotheses remain analytic premises.
"""
import hashlib
import json
from pathlib import Path

import sympy as sp


def check():
    f = sp.Matrix(3, 3, lambda i, j: sp.Symbol(f"F{i}{j}"))
    grad = sp.Matrix(3, 3, lambda i, j: sp.Symbol(f"A{i}{j}"))
    directional_derivative = sum(
        sp.diff(f.det(), f[i, j]) * (grad * f)[i, j]
        for i in range(3) for j in range(3)
    )
    liouville_residual = sp.factor(directional_derivative - sp.trace(grad) * f.det())

    lam1, lam2, lam3, sigma = sp.symbols(
        "lambda_1 lambda_2 lambda_3 sigma", positive=True
    )
    diagonal_f = sp.diag(lam1, lam2, lam3)
    covariance = sp.simplify(diagonal_f * (sigma**2 * sp.eye(3)) * diagonal_f.T)
    peak_ratio = sp.simplify(1 / sp.Abs(diagonal_f.det()))
    covariance_volume_ratio = sp.simplify(sp.sqrt(covariance.det()) / sigma**3)
    controls = {
        "generic_liouville_identity": liouville_residual == 0,
        "unit_determinant_peak_density_invariant":
            sp.simplify(peak_ratio.subs(lam3, 1 / (lam1 * lam2)) - 1) == 0,
        "unit_determinant_covariance_volume_invariant":
            sp.simplify(covariance_volume_ratio.subs(lam3, 1 / (lam1 * lam2)) - 1) == 0,
    }
    return {
        "scope": "Symbolic algebra for Liouville's determinant identity and a diagonal affine Gaussian example; smooth-flow and change-of-variables theorems are analytic assumptions, not established by this script.",
        "sympy": sp.__version__,
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "identities": {
            "flow_gradient_equation": "dF/dt = (D_x u)(t,X) F",
            "determinant_evolution": "d(det F)/dt = tr(D_x u)(t,X) det F",
            "density_transport": "rho_t(x)=rho_0(X_t^{-1}(x)) when div u=0 and X_t is a diffeomorphism",
            "affine_gaussian_covariance": [
                "sigma^2*lambda_1^2", "sigma^2*lambda_2^2", "sigma^2*lambda_3^2"
            ],
            "condition_for_volume_preserving_diagonal_map": "lambda_1*lambda_2*lambda_3=1",
        },
        "liouville_residual": str(liouville_residual),
        "controls": controls,
        "success": all(controls.values()),
    }


def main():
    result = check()
    path = Path("evidence/tests/incompressible-tracer-density-invariant.json")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    return 0 if result["success"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
