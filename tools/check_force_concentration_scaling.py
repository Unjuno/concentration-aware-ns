"""Check exact scaling consequences of the localized force rescaling.

This is a change-of-variables audit of arXiv:2609.10262v4, not an actuator
model or a verification of the paper's blowup theorem.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import sys
from pathlib import Path

import sympy as sp


def check() -> dict[str, object]:
    q, s = sp.symbols("q s", positive=True, real=True)
    k, ell = sp.symbols("k ell", nonnegative=True, integer=True)
    spatial_exponent = sp.simplify(-3 + sp.Rational(3, 2) - s)
    mixed_exponent = sp.simplify(sp.Rational(2, 1) / q + spatial_exponent)
    derivative_exponent = -3 - k - 2 * ell

    assert spatial_exponent == -sp.Rational(3, 2) - s
    assert mixed_exponent.subs(q, 1) == sp.Rational(1, 2) - s
    assert mixed_exponent.subs(q, 2) == -sp.Rational(1, 2) - s
    assert derivative_exponent.subs({k: 0, ell: 0}) == -3
    assert derivative_exponent.subs({k: 1, ell: 0}) == -4
    assert derivative_exponent.subs({k: 0, ell: 1}) == -5

    return {
        "status": "PASS",
        "tool": "SymPy exact scaling algebra",
        "sympy_version": sp.__version__,
        "python_version": platform.python_version(),
        "platform": platform.platform(),
        "interpreter": sys.executable,
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "source": "Cao-Chi-Nie, arXiv:2609.10262v4, equations (20) and force scaling after Theorem 1.1",
        "rescaling": "F_epsilon(x,t)=epsilon^-3 F((x-x0)/epsilon,(t-t_epsilon)/epsilon^2)",
        "Lq_homogeneous_Hs_exponent": "2/q-3/2-s",
        "thresholds": {
            "q1": "1/2-s; vanishes for s<1/2",
            "q2": "-1/2-s; vanishes for s<-1/2",
        },
        "pointwise_derivative_exponents": {
            "force_amplitude": "epsilon^-3",
            "one_spatial_derivative": "epsilon^-4",
            "one_time_derivative": "epsilon^-5",
            "general_k_spatial_ell_time": "epsilon^(-3-k-2*ell)",
        },
        "scope": (
            "Exact scaling of a fixed nonzero smooth compactly supported force. "
            "Weak force-norm smallness does not give uniform pointwise amplitude "
            "or derivative bounds. This is not an actuator-feasibility theorem "
            "and does not validate the underlying blowup construction."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("evidence/tests/force-concentration-scaling-2026-10-03.json"),
    )
    args = parser.parse_args()
    result = json.dumps(check(), indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(result, encoding="utf-8")
    else:
        print(result, end="")


if __name__ == "__main__":
    main()
