"""Check exact passive-tracer probabilities in the Burgers-vortex flow map."""
import hashlib
import json
from pathlib import Path

import sympy as sp


def main():
    gamma, t, sigma, radius, half_length = sp.symbols(
        'gamma t sigma radius half_length', positive=True, finite=True)
    radial_sq, z = sp.symbols('radial_sq z', real=True)
    initial_density = (sp.exp(-(radial_sq + z**2)/(2*sigma**2)) /
                       ((2*sp.pi*sigma**2)**sp.Rational(3, 2)))
    inverse_density = sp.simplify(initial_density.subs({
        radial_sq: sp.exp(2*gamma*t)*radial_sq,
        z: sp.exp(-2*gamma*t)*z,
    }, simultaneous=True))

    covariance = sp.diag(sigma**2*sp.exp(-2*gamma*t),
                         sigma**2*sp.exp(-2*gamma*t),
                         sigma**2*sp.exp(4*gamma*t))
    covariance_determinant = sp.simplify(covariance.det())
    theta_radial_shear = sp.symbols('theta_radial_shear', real=True)
    coordinate_flow_jacobian = sp.Matrix([
        [sp.exp(-gamma*t), 0, 0],
        [theta_radial_shear, 1, 0],
        [0, 0, sp.exp(2*gamma*t)],
    ])
    cylindrical_coordinate_jacobian = sp.simplify(coordinate_flow_jacobian.det())
    physical_flow_jacobian = sp.simplify(
        sp.exp(-gamma*t)*cylindrical_coordinate_jacobian)
    tube_probability = 1 - sp.exp(-radius**2*sp.exp(2*gamma*t)/(2*sigma**2))
    cylinder_probability = tube_probability * sp.erf(
        half_length*sp.exp(-2*gamma*t)/(sp.sqrt(2)*sigma))
    cylinder_asymptotic_coefficient = sp.simplify(sp.limit(
        cylinder_probability*sp.exp(2*gamma*t), t, sp.oo))

    expected_density = (sp.exp(-(
        sp.exp(2*gamma*t)*radial_sq + sp.exp(-4*gamma*t)*z**2)/(2*sigma**2)) /
        ((2*sp.pi*sigma**2)**sp.Rational(3, 2)))
    identities = {
        'inverse_flow_density_is_anisotropic_gaussian':
            sp.simplify(inverse_density - expected_density) == 0,
        'flow_map_preserves_volume': physical_flow_jacobian == 1,
        'cylindrical_jacobian_matches_flow':
            cylindrical_coordinate_jacobian == sp.exp(gamma*t),
        'covariance_determinant_preserved': covariance_determinant == sigma**6,
        'gaussian_differential_entropy_preserved': sp.simplify(
            sp.log(covariance_determinant/sigma**6)) == 0,
        'peak_density_preserved': sp.simplify(
            expected_density.subs({radial_sq: 0, z: 0}) -
            initial_density.subs({radial_sq: 0, z: 0})) == 0,
        'infinite_axis_tube_probability_tends_to_one':
            sp.simplify(sp.limit(tube_probability, t, sp.oo)) == 1,
        'finite_cylinder_probability_tends_to_zero':
            sp.simplify(sp.limit(cylinder_probability, t, sp.oo)) == 0,
        'finite_cylinder_asymptotic_coefficient': sp.simplify(
            cylinder_asymptotic_coefficient -
            sp.sqrt(2/sp.pi)*half_length/sigma) == 0,
    }
    source = Path(__file__)
    output = {
        'scope': 'Exact passive-tracer pushforward of an isotropic Gaussian under '
                 'the classical Burgers-vortex flow map; it is an imposed '
                 'ensemble, not a molecular model or selected OpenAI-profile result.',
        'sympy': sp.__version__,
        'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
        'assumptions': ['gamma > 0', 'sigma > 0', 'radius > 0',
                        'half_length > 0', 't >= 0'],
        'flow_map': {'r_t': 'r0*exp(-gamma*t)',
                     'z_t': 'z0*exp(2*gamma*t)',
                     'theta_t': 'theta0 + integral_0^t u_theta(r_s)/r_s ds'},
        'density': str(expected_density),
        'covariance': str(covariance),
        'covariance_determinant': str(covariance_determinant),
        'cylindrical_coordinate_jacobian': str(cylindrical_coordinate_jacobian),
        'coordinate_flow_jacobian_matrix': str(coordinate_flow_jacobian),
        'physical_flow_jacobian': str(physical_flow_jacobian),
        'infinite_axis_tube_probability': str(tube_probability),
        'finite_cylinder_probability': str(cylinder_probability),
        'finite_cylinder_scaled_limit': str(cylinder_asymptotic_coefficient),
        'identities': identities,
        'success': all(identities.values()),
    }
    target = Path('evidence/tests/burgers-vortex-tracer-probability.json')
    target.write_text(json.dumps(output, indent=2) + '\n')
    print(json.dumps(output, indent=2))
    return 0 if output['success'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
