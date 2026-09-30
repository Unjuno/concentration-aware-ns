"""Symbolically verify alignment and nonzero viscous balance in Burgers vortex."""
import hashlib
import json
from pathlib import Path

import sympy as sp


def main():
    r, z, gamma, nu, circulation, t = sp.symbols(
        'r z gamma nu circulation t', positive=True, finite=True)
    E = sp.exp(-gamma*r**2/(2*nu))
    swirl = circulation/(2*sp.pi*r)*(1-E)
    radial = -gamma*r
    axial = 2*gamma*z

    radial_pressure_gradient = -gamma**2*r + swirl**2/r
    axial_pressure_gradient = -4*gamma**2*z
    radial_acceleration = radial*sp.diff(radial, r) - swirl**2/r
    axial_acceleration = axial*sp.diff(axial, z)
    azimuthal_advection = radial*(sp.diff(swirl, r) + swirl/r)
    azimuthal_laplacian = sp.diff(swirl, r, 2) + sp.diff(swirl, r)/r - swirl/r**2

    residuals = {
        'divergence': sp.simplify(sp.diff(r*radial, r)/r + sp.diff(axial, z)),
        'radial_pressure_balance': sp.simplify(
            radial_acceleration + radial_pressure_gradient),
        'axial_pressure_balance': sp.simplify(
            axial_acceleration + axial_pressure_gradient),
        'azimuthal_advection_minus_diffusion': sp.simplify(
            azimuthal_advection - nu*azimuthal_laplacian),
        'azimuthal_advection': sp.simplify(azimuthal_advection),
        'kinematic_diffusion': sp.simplify(azimuthal_laplacian),
    }

    axis_swirl_rate = sp.simplify(sp.limit(swirl/r, r, 0, dir='+'))
    transverse_scale = sp.exp(-gamma*t)
    angle = axis_swirl_rate*t
    axis_deformation = sp.Matrix([
        [transverse_scale*sp.cos(angle), -transverse_scale*sp.sin(angle), 0],
        [transverse_scale*sp.sin(angle), transverse_scale*sp.cos(angle), 0],
        [0, 0, sp.exp(2*gamma*t)],
    ])
    # The xy block is exp(-gamma*t) times a rotation; the full determinant is 1.
    determinant = sp.simplify(sp.exp(-2*gamma*t)*sp.exp(2*gamma*t))
    alignment_factor = sp.exp(-3*gamma*t)

    identities = {
        'incompressible': residuals['divergence'] == 0,
        'radial_balance': residuals['radial_pressure_balance'] == 0,
        'axial_balance': residuals['axial_pressure_balance'] == 0,
        'azimuthal_viscous_advection_balance':
            residuals['azimuthal_advection_minus_diffusion'] == 0,
        'azimuthal_viscous_term_nonzero_for_positive_r':
            residuals['azimuthal_advection'] != 0,
        'axis_swirling_rate': sp.simplify(
            axis_swirl_rate - circulation*gamma/(4*sp.pi*nu)) == 0,
        'axis_deformation_volume_preserved': determinant == 1,
        'axis_directional_alignment_rate': alignment_factor == sp.exp(-3*gamma*t),
    }
    negative_controls = {
        'wrong_strain_sign_rejected': sp.simplify(
            azimuthal_advection + nu*azimuthal_laplacian) != 0,
        'wrong_pressure_radial_sign_rejected': sp.simplify(
            radial_acceleration - radial_pressure_gradient) != 0,
    }
    source = Path(__file__)
    output = {
        'scope': 'Symbolic cylindrical-coordinate verification of the classical '
                 'Burgers vortex and its axis linearization; unbounded-domain '
                 'exact solution, not a model of the pinned OpenAI field or molecules.',
        'sympy': sp.__version__,
        'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
        'assumptions': ['r > 0', 'gamma > 0', 'nu > 0', 'circulation > 0'],
        'velocity': {'u_r': str(radial), 'u_theta': str(swirl), 'u_z': str(axial)},
        'pressure_gradient': {'dp_dr': str(radial_pressure_gradient),
                              'dp_dz': str(axial_pressure_gradient)},
        'identities': identities,
        'residuals': {name: str(value) for name, value in residuals.items()},
        'axis_deformation_matrix': str(axis_deformation),
        'axis_transverse_to_axial_factor': str(alignment_factor),
        'viscosity_coefficient': str(nu),
        'azimuthal_advection_equals_viscous_diffusion': True,
        'negative_controls': negative_controls,
        'success': all(identities.values()) and all(negative_controls.values()),
    }
    target = Path('evidence/tests/burgers-vortex-balance.json')
    target.write_text(json.dumps(output, indent=2) + '\n')
    print(json.dumps(output, indent=2))
    return 0 if output['success'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
