"""Compare hand-coded NumPy fields with direct SymPy differentiation."""
import json
from pathlib import Path

import numpy as np
import sympy as sp

from tools.high_gradient_reference import fields


def check():
    x, y, z = sp.symbols("x y z", real=True)
    nu = sp.Rational(1, 100)
    rng = np.random.default_rng(2741)
    result_cases = []
    for n in (4, 8, 16):
        chi = ((1+sp.cos(y))/2)**4 * ((1+sp.cos(z))/2)**4
        psi = chi * sp.sin(n*x) / n**2
        u = sp.Matrix([sp.diff(psi, y), -sp.diff(psi, x), 0])
        coords = (x, y, z)
        grad = u.jacobian(coords)
        lap = sp.Matrix([sum(sp.diff(u[i], q, 2) for q in coords) for i in range(3)])
        omega = sp.Matrix([grad[2, 1]-grad[1, 2],
                           grad[0, 2]-grad[2, 0],
                           grad[1, 0]-grad[0, 1]])
        force = grad*u - nu*lap
        exprs = {"u": u, "grad_u": grad, "vorticity": omega, "force": force}
        fn = {key: sp.lambdify(coords, expr, "numpy", cse=True)
              for key, expr in exprs.items()}
        points = rng.uniform(0, 2*np.pi, size=(64, 3))
        points = np.vstack((points, [np.pi/(2*n), 0., 0.]))
        errors = {key: 0.0 for key in exprs}
        for point in points:
            reference = fields(point, N=n, nu=float(nu))
            for key, evaluator in fn.items():
                symbolic = np.asarray(evaluator(*point), dtype=float).reshape(reference[key].shape)
                errors[key] = max(errors[key], float(np.max(np.abs(symbolic-reference[key]))))
        result_cases.append({"N": n, "points": len(points), "max_absolute_errors": errors})
    result = {
        "method": "independent hand-coded Fourier derivative evaluator versus direct SymPy differentiation",
        "seed": 2741,
        "sympy": sp.__version__,
        "numpy": np.__version__,
        "cases": result_cases,
        "tolerance": 1e-10,
        "passed": all(error < 1e-10
                       for case in result_cases
                       for error in case["max_absolute_errors"].values()),
        "limitations": "Formula implementation comparison only; no OpenFOAM/SU2/PhysicsNeMo run or solver sign-convention verification.",
    }
    out = Path("evidence/tests/high-gradient-reference.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    if not result["passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    check()
