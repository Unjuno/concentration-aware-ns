"""Check a homogeneous exact reduction of a recent visco-morphoelastic model.

The calculation is an internal-strain tensor example, not a molecule model or
a consequence of the OpenAI Navier–Stokes construction.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import sympy as sp


def derive() -> dict[str, object]:
    t, alpha, beta, shear_rate, mu1, lam = sp.symbols(
        "t alpha beta shear_rate mu1 lam", positive=True, real=True
    )
    identity = sp.eye(3)
    D = sp.diag(shear_rate, -shear_rate, 0)
    W = sp.zeros(3)
    qstar = 3 * beta / alpha
    decay = 1 - sp.exp(-alpha * t)

    # Model equation: E_t + E W - W E + (tr(E)-1)D = -alpha E + beta I.
    # For q(0)=3 beta/alpha and div(v)=tr(D)=0, the trace remains qstar.
    trace_residual = sp.simplify(-alpha * qstar + 3 * beta)
    assert trace_residual == 0

    Fxx = sp.simplify(-(qstar - 1) * shear_rate * decay / alpha)
    F = sp.diag(Fxx, -Fxx, 0)
    F_rhs = -alpha * F - (qstar - 1) * D
    F_residual = sp.simplify(F.diff(t) - F_rhs)
    assert F_residual == sp.zeros(3)
    assert sp.simplify(sp.trace(F)) == 0
    assert F == F.T

    # The Kelvin–Voigt law contains a fixed viscous part mu1*D plus elastic
    # strain stress lam*F; the latter can change the projected total ratio.
    stress_deviator = sp.simplify(mu1 * D + lam * F)
    projected_total = sp.factor(stress_deviator[0, 0] / shear_rate)
    expected = sp.factor(mu1 - lam * (3 * beta - alpha) * decay / alpha**2)
    assert sp.simplify(projected_total - expected) == 0

    return {
        "status": "PASS",
        "tool": "SymPy exact homogeneous reduction",
        "sympy_version": sp.__version__,
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "source": "Banerjee et al., arXiv:2610.01487v1, equations (1.1), (1.2), (3.2)",
        "assumptions": [
            "smooth homogeneous incompressible extension v=(shear_rate*x,-shear_rate*y,0)",
            "constant positive alpha and lambda; beta >= 0",
            "trace initialized at q(0)=3*beta/alpha",
            "initial deviatoric effective strain F(0)=0",
            "no spatial dependence, so transport and strain diffusion vanish",
        ],
        "D": "diag(shear_rate,-shear_rate,0)",
        "W": "zero",
        "trace_equation": "q'=-alpha*q+3*beta",
        "trace_solution": "q=3*beta/alpha",
        "F_xx": sp.sstr(Fxx),
        "F_yy": sp.sstr(sp.simplify(-Fxx)),
        "F_zz": "0",
        "F_is_symmetric_trace_free": True,
        "F_eigenvectors": "coordinate axes, which are the extension/compression axes",
        "constitutive_viscous_coefficient": "mu1",
        "elastic_stress_coefficient_symbol": "lam",
        "projected_total_stress_coefficient": sp.sstr(projected_total),
        "weak_limit_note": (
            "The paper's vanishing-diffusion weak limit may contain a Jaumann "
            "commutator defect; strong convergence of F in L-infinity L2 or "
            "of grad(v) in L2 is sufficient for its disappearance."
        ),
        "scope": (
            "Exact homogeneous tensor ODE for one visco-morphoelastic Kelvin–Voigt "
            "model. Tensor principal axes follow the imposed extension; this is "
            "not particle alignment, positional certainty, a Newtonian viscosity "
            "law, a singularity result, or evidence about OpenAI's flow. The "
            "projected total stress coefficient includes elastic memory stress "
            "and must not be mislabeled as the fixed constitutive viscous coefficient."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("evidence/tests/visco-morphoelastic-internal-state-2026-10-03.json"),
    )
    args = parser.parse_args()
    result = json.dumps(derive(), indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(result, encoding="utf-8")
    else:
        print(result, end="")


if __name__ == "__main__":
    main()
