"""Check an exact affine NS flow separating alignment from viscosity."""
import hashlib
import json
from pathlib import Path

import sympy as sp


def main():
    x, y, z, a, nu, t = sp.symbols('x y z a nu t', real=True)
    coordinates = sp.Matrix([x, y, z])
    A = sp.diag(-a, -a, 2*a)
    velocity = A * coordinates
    pressure = -sp.Rational(1, 2) * (coordinates.T * A**2 * coordinates)[0]
    acceleration = A**2 * coordinates
    pressure_force = -sp.Matrix([sp.diff(pressure, q) for q in coordinates])
    laplacian = sp.Matrix([sum(sp.diff(component, q, 2)
                               for q in coordinates)
                           for component in velocity])
    residuals = {
        'incompressibility': sp.simplify(sp.trace(A)),
        'steady_material_acceleration_matches_pressure': sp.simplify(
            acceleration - pressure_force),
        'viscous_laplacian': sp.simplify(laplacian),
        'navier_stokes_residual': sp.simplify(
            acceleration + sp.Matrix([sp.diff(pressure, q) for q in coordinates])
            - nu*laplacian),
    }
    flow = sp.diag(sp.exp(-a*t), sp.exp(-a*t), sp.exp(2*a*t))
    deformation = {
        'determinant': sp.simplify(flow.det()),
        'transverse_to_axial_ratio_factor': sp.exp(-3*a*t),
        'viscosity_coefficient': nu,
        'viscous_force': sp.simplify(nu*laplacian),
    }
    identities = {
        'incompressibility_zero': residuals['incompressibility'] == 0,
        'pressure_balances_acceleration': residuals[
            'steady_material_acceleration_matches_pressure'] == sp.zeros(3, 1),
        'viscous_laplacian_zero': residuals['viscous_laplacian'] == sp.zeros(3, 1),
        'full_equation_zero': residuals['navier_stokes_residual'] == sp.zeros(3, 1),
        'volume_preserved': deformation['determinant'] == 1,
    }
    controls = {
        'wrong_pressure_sign_rejected': sp.simplify(
            acceleration + pressure_force) != sp.zeros(3, 1),
        'nonzero_laplacian_control_rejected': sp.simplify(
            nu*sp.Matrix([sp.diff(x**2, q, 2) for q in coordinates]))
            != sp.zeros(3, 1),
    }
    source = Path(__file__)
    output = {
        'scope': 'Exact symbolic counterexample on R^3 with prescribed affine '
                 'flow; not finite-energy, periodic, molecular, or a claim about '
                 'the pinned OpenAI construction.',
        'sympy': sp.__version__,
        'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
        'assumptions': ['a > 0', 'nu >= 0', 'x,y,z,t real'],
        'field': {'velocity': str(velocity), 'pressure': str(pressure),
                  'deformation': str(flow)},
        'identities': identities,
        'residuals': {name: str(value) for name, value in residuals.items()},
        'deformation_facts': {name: str(value)
                              for name, value in deformation.items()},
        'negative_controls': controls,
        'success': all(identities.values()) and all(controls.values()),
    }
    target = Path('evidence/tests/affine-alignment-counterexample.json')
    target.write_text(json.dumps(output, indent=2) + '\n')
    print(json.dumps(output, indent=2))
    return 0 if output['success'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
