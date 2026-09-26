"""Exact algebra supporting the classical variational uniqueness proof.

Run with the pinned requirements-verification.txt environment. This is not
Lean verification or proof of differentiability of a nonlinear flow map.
"""
import hashlib
import json
from pathlib import Path

import sympy as sp


def reduced(matrix):
    return matrix.applyfunc(lambda x: sp.simplify(sp.trigsimp(x)))


def main():
    r, z = sp.symbols('r z', positive=True)
    theta, g, omega = sp.symbols('theta g omega', real=True)
    y = sp.Matrix(sp.symbols('y0:3', real=True))
    rotation = sp.Matrix([[sp.cos(theta), -sp.sin(theta), 0],
                          [sp.sin(theta), sp.cos(theta), 0], [0, 0, 1]])
    F = rotation * sp.diag(r, r, z)
    # Construct the proposed inverse independently of Matrix.inv().
    J = sp.diag(1/r, 1/r, 1/z) * rotation.T
    G = sp.Matrix([[-g/2, -omega, 0], [omega, -g/2, 0], [0, 0, g]])

    def dt(matrix):
        return (matrix.diff(r)*(-g*r/2) + matrix.diff(z)*(g*z)
                + matrix.diff(theta)*omega)

    residuals = {
        'left_inverse': reduced(J*F-sp.eye(3)),
        'right_inverse': reduced(F*J-sp.eye(3)),
        'fundamental_ode': reduced(dt(F)-G*F),
        'inverse_ode': reduced(dt(J)+J*G),
        'conserved_initial_vector': reduced(dt(J)*y+J*G*y),
        'gram_matrix': reduced(F.T*F-sp.diag(r*r, r*r, z*z)),
        'determinant': reduced(sp.Matrix([F.det()-r*r*z])),
        'volume_rate': reduced(sp.Matrix([dt(sp.Matrix([r*r*z]))[0]])),
    }
    results = {name: value == sp.zeros(*value.shape)
               for name, value in residuals.items()}

    # Adversarial controls: the same checks must reject convention/rate errors.
    wrong_rotation = G.copy()
    wrong_rotation[0, 1] = omega
    wrong_axial = G.copy()
    wrong_axial[2, 2] = -g
    wrong_transverse = G.copy()
    wrong_transverse[0, 0] = -g
    controls = {
        'wrong_rotation_sign_rejected': reduced(dt(F)-wrong_rotation*F) != sp.zeros(3),
        'wrong_axial_rate_rejected': reduced(dt(F)-wrong_axial*F) != sp.zeros(3),
        'missing_transverse_half_rejected': reduced(dt(F)-wrong_transverse*F) != sp.zeros(3),
    }
    source = Path(__file__)
    output = {
        'scope': 'Exact symbolic matrix identities for the classical proof in '
                 'docs/axis-variational-uniqueness.md. Not a Lean check, PDE '
                 'solution construction, finite-packet bound or viscosity law.',
        'sympy': sp.__version__,
        'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
        'assumptions': ['r > 0', 'z > 0', 'theta, g, omega real',
                        "r\u2032 = -g*r/2", "z\u2032 = g*z", "theta\u2032 = omega"],
        'identities': results,
        'residuals': {name: str(value) for name, value in residuals.items()},
        'negative_controls': controls,
        'success': all(results.values()) and all(controls.values()),
    }
    target = Path('evidence/tests/axis-deformation.json')
    target.write_text(json.dumps(output, indent=2)+'\n')
    print(json.dumps(output, indent=2))
    return 0 if output['success'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
