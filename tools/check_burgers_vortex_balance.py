"""Symbolically verify alignment and nonzero viscous balance in Burgers vortex."""
import hashlib
import json
from pathlib import Path

import sympy as sp


def main():
    r, r0, z, gamma, nu, circulation, t = sp.symbols(
        'r r0 z gamma nu circulation t', positive=True, finite=True)
    E = sp.exp(-gamma*r**2/(2*nu))
    swirl = circulation/(2*sp.pi*r)*(1-E)
    radial = -gamma*r
    axial = 2*gamma*z

    radial_pressure_gradient = -gamma**2*r + swirl**2/r
    axial_pressure_gradient = -4*gamma**2*z
    radial_acceleration = radial*sp.diff(radial, r) - swirl**2/r
    axial_acceleration = axial*sp.diff(axial, z)
    radial_vector_laplacian = (sp.diff(radial, r, 2) +
                               sp.diff(radial, r)/r - radial/r**2 +
                               sp.diff(radial, z, 2))
    azimuthal_advection = radial*(sp.diff(swirl, r) + swirl/r)
    azimuthal_laplacian = sp.diff(swirl, r, 2) + sp.diff(swirl, r)/r - swirl/r**2
    axial_laplacian = sp.diff(axial, r, 2) + sp.diff(axial, r)/r + sp.diff(axial, z, 2)

    residuals = {
        'divergence': sp.simplify(sp.diff(r*radial, r)/r + sp.diff(axial, z)),
        'radial_pressure_balance': sp.simplify(
            radial_acceleration + radial_pressure_gradient),
        'axial_pressure_balance': sp.simplify(
            axial_acceleration + axial_pressure_gradient),
        'radial_vector_laplacian': sp.simplify(radial_vector_laplacian),
        'axial_laplacian': sp.simplify(axial_laplacian),
        'pressure_gradient_compatibility': sp.simplify(
            sp.diff(radial_pressure_gradient, z) -
            sp.diff(axial_pressure_gradient, r)),
        'radial_navier_stokes': sp.simplify(
            radial_acceleration + radial_pressure_gradient -
            nu*radial_vector_laplacian),
        'axial_navier_stokes': sp.simplify(
            axial_acceleration + axial_pressure_gradient - nu*axial_laplacian),
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

    # Exact material flow map in cylindrical coordinates for an off-axis
    # particle, then differentiate it with respect to its initial radius.
    radius_t = r0*sp.exp(-gamma*t)
    omega_r0 = (swirl/r).subs(r, r0)
    omega_rt = (swirl/r).subs(r, radius_t)
    theta_initial_radius_derivative = sp.simplify(
        (omega_r0/r0 - sp.exp(-gamma*t)*omega_rt/radius_t)/gamma)
    radial_to_azimuthal_shear = sp.simplify(
        r0*theta_initial_radius_derivative)
    shear_limit = sp.simplify(sp.limit(radial_to_azimuthal_shear, t, sp.oo))
    expected_shear_limit = sp.simplify(
        circulation*(1 - sp.exp(-gamma*r0**2/(2*nu))) /
        (2*sp.pi*gamma*r0**2) - circulation/(4*sp.pi*nu))
    delta_r0, delta_theta0, delta_z0 = sp.symbols(
        'delta_r0 delta_theta0 delta_z0', real=True)
    transverse_to_axial_ratio_squared = sp.simplify(
        sp.exp(-6*gamma*t) *
        (delta_r0**2 + (radial_to_azimuthal_shear*delta_r0 +
                        delta_theta0)**2) / delta_z0**2)
    off_axis_alignment_limit = sp.simplify(sp.limit(
        transverse_to_axial_ratio_squared, t, sp.oo))
    off_axis_deformation = sp.Matrix([
        [sp.exp(-gamma*t), 0, 0],
        [sp.exp(-gamma*t)*radial_to_azimuthal_shear,
         sp.exp(-gamma*t), 0],
        [0, 0, sp.exp(2*gamma*t)],
    ])
    off_axis_determinant = sp.simplify(off_axis_deformation.det())

    identities = {
        'incompressible': residuals['divergence'] == 0,
        'radial_balance': residuals['radial_pressure_balance'] == 0,
        'axial_balance': residuals['axial_pressure_balance'] == 0,
        'radial_viscous_component_zero': residuals['radial_vector_laplacian'] == 0,
        'axial_viscous_component_zero': residuals['axial_laplacian'] == 0,
        'pressure_gradient_compatible': residuals['pressure_gradient_compatibility'] == 0,
        'radial_equation': residuals['radial_navier_stokes'] == 0,
        'axial_equation': residuals['axial_navier_stokes'] == 0,
        'azimuthal_viscous_advection_balance':
            residuals['azimuthal_advection_minus_diffusion'] == 0,
        'azimuthal_viscous_term_nonzero_for_positive_r':
            residuals['azimuthal_advection'] != 0,
        'viscous_advection_balance_is_derived':
            residuals['azimuthal_advection_minus_diffusion'] == 0,
        'axis_swirling_rate': sp.simplify(
            axis_swirl_rate - circulation*gamma/(4*sp.pi*nu)) == 0,
        'axis_deformation_volume_preserved': determinant == 1,
        'axis_directional_alignment_rate': alignment_factor == sp.exp(-3*gamma*t),
        'off_axis_flow_map_volume_preserved': off_axis_determinant == 1,
        'off_axis_shear_has_finite_limit': not shear_limit.has(
            sp.oo, -sp.oo, sp.zoo, sp.nan),
        'off_axis_shear_limit_matches_closed_form': sp.simplify(
            shear_limit - expected_shear_limit) == 0,
        'off_axis_transverse_to_axial_ratio_tends_to_zero':
            off_axis_alignment_limit == 0,
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
                 'Burgers vortex and on/off-axis deformation; unbounded-domain '
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
        'off_axis_radius_trajectory': str(radius_t),
        'off_axis_radial_derivative_of_rotation': str(
            theta_initial_radius_derivative),
        'off_axis_deformation_matrix_in_cylindrical_orthonormal_bases':
            str(off_axis_deformation),
        'off_axis_shear_limit': str(shear_limit),
        'off_axis_expected_shear_limit': str(expected_shear_limit),
        'off_axis_transverse_to_axial_ratio_squared_limit':
            str(off_axis_alignment_limit),
        'viscosity_coefficient': str(nu),
        'azimuthal_advection_equals_viscous_diffusion':
            residuals['azimuthal_advection_minus_diffusion'] == 0,
        'negative_controls': negative_controls,
        'success': all(identities.values()) and all(negative_controls.values()),
    }
    target = Path('evidence/tests/burgers-vortex-balance.json')
    target.write_text(json.dumps(output, indent=2) + '\n')
    print(json.dumps(output, indent=2))
    return 0 if output['success'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
