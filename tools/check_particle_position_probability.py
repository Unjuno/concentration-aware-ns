"""Exact symbolic checks separating directional alignment from spatial concentration."""
import hashlib
import json
from pathlib import Path

import sympy as s


def main():
    q, C, m, mu, alpha, radius, half_length, zscale = s.symbols(
        'q C m mu alpha radius half_length zscale', positive=True)
    # For the selected infinitesimal propagator, transverse/axial ratios
    # acquire the factor a=q^(3C/2). For isotropic directions, |cos(theta0)|
    # is uniform on [0,1].
    a = q**(3*C/2)
    ratio_factor = s.simplify(q**(C/2) / q**(-C))
    threshold = alpha / s.sqrt(m**2 + alpha**2)
    probability = 1 - threshold
    stretch = s.diag(q**(C/2), q**(C/2), q**(-C))
    covariance = s.simplify(stretch * stretch.T)
    covariance_det = s.simplify(covariance.det())
    gaussian_peak_ratio = s.simplify(1 / s.Abs(stretch.det()))
    # Set zscale=Q^C so the CAS need not infer positivity through a symbolic
    # exponent when taking the singular-time limit.
    transverse_tube_probability = 1 - s.exp(-radius**2 / (2*zscale))
    axial_window_probability = s.erf(half_length*zscale / s.sqrt(2))
    finite_cylinder_probability = s.simplify(
        transverse_tube_probability * axial_window_probability)

    # The event theta_t <= theta_* is equivalent to |cos(theta0)| >= threshold.
    event_residual = s.simplify(
        (alpha**2 * (1-mu**2) - m**2 * mu**2) -
        (alpha**2 - (alpha**2+m**2)*mu**2)
    )
    # A concrete exact case: at Q=1, the unoriented spherical cap probability
    # is 1-cos(theta_*); at a=1/2 and tan(theta_*)=1 it is 1-1/sqrt(5).
    controls = {
        'deformation_is_volume_preserving': s.simplify(stretch.det() - 1) == 0,
        'pushforward_gaussian_peak_unchanged': s.simplify(gaussian_peak_ratio - 1) == 0,
        'position_covariance_volume_unchanged': s.simplify(covariance_det - 1) == 0,
        'angle_ratio_factor_matches_selected_deformation':
            s.simplify(ratio_factor-a) == 0,
        'infinite_axis_tube_probability_limit':
            s.limit(transverse_tube_probability, zscale, 0, dir='+') == 1,
        'bounded_axial_window_probability_limit':
            s.limit(axial_window_probability, zscale, 0, dir='+') == 0,
        'finite_cylinder_probability_limit':
            s.limit(finite_cylinder_probability, zscale, 0, dir='+') == 0,
        'finite_cylinder_leading_order':
            s.simplify(s.limit(finite_cylinder_probability/zscale, zscale, 0, dir='+') -
                       s.sqrt(2/s.pi)*half_length) == 0,
        'angular_event_boundary_identity': event_residual == 0,
        'uniform_direction_probability_integral':
            s.simplify(s.integrate(1, (mu, threshold, 1)) - probability) == 0,
        'q_one_probability_is_unoriented_spherical_cap':
            s.simplify(probability.subs(alpha, 1) - (1 - 1/s.sqrt(1+m**2))) == 0,
        'alignment_probability_limit': s.limit(probability, alpha, 0, dir='+') == 1,
        'example_probability_exact':
            s.simplify((1-alpha/s.sqrt(1+alpha**2)).subs(alpha, s.Rational(1, 2)) -
                       (1-1/s.sqrt(5))) == 0,
    }
    out = {
        'scope': 'Exact algebra for the selected local flow derivative and for a separate global affine tangent-map toy ensemble. The actual nonlinear flow theorem does not establish that the unbounded Gaussian lies within a linearization neighborhood; no molecular or finite-packet result is claimed.',
        'sympy': s.__version__,
        'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'conditions': ['0 < Q <= 1', 'C > 0', '0 < theta_target < pi/2',
                       'initial separation directions uniform on the sphere',
                       'local flow derivative applies to infinitesimal separations'],
        'formulas': {
            'deformation_singular_values': ['Q^(C/2)', 'Q^(C/2)', 'Q^(-C)'],
            'determinant': '1',
            'position_pushforward_density': 'rho_t(x)=rho_0(F^{-1}x)/|det F|',
            'isotropic_gaussian_covariance_eigenvalues': ['Q^C', 'Q^C', 'Q^(-2C)'],
            'gaussian_peak_density_ratio': '1',
            'probability_inside_infinite_axis_tube_radius_r':
                '1-exp(-r^2/(2*Q^C))',
            'probability_inside_finite_cylinder_radius_r_half_length_L':
                '(1-exp(-r^2/(2*Q^C)))*erf(L*Q^C/sqrt(2))',
            'finite_cylinder_asymptotic': 'sqrt(2/pi)*L*Q^C as Q tends to 0',
            'angular_probability': 'P(theta_t <= theta_target)=1-a/sqrt(a^2+tan(theta_target)^2), a=Q^(3C/2)',
            'alignment_limit': '1 as Q tends to 0 for every fixed positive target angle',
        },
        'identity_checks': {
            'covariance': [str(x) for x in covariance.diagonal()],
            'probability_at_Q_1': str(s.simplify(probability.subs(alpha, 1))),
            'probability_as_alpha_tends_to_zero': str(s.limit(probability, alpha, 0, dir='+')),
            'infinite_axis_tube_probability_limit': str(
                s.limit(transverse_tube_probability, zscale, 0, dir='+')),
            'bounded_axial_window_probability_limit': str(
                s.limit(axial_window_probability, zscale, 0, dir='+')),
            'finite_cylinder_probability_limit': str(
                s.limit(finite_cylinder_probability, zscale, 0, dir='+')),
            'example_a_half_target_45_degrees': '1-1/sqrt(5)',
        },
        'controls': controls,
        'success': all(controls.values()),
    }
    Path('evidence/tests/particle-position-probability.json').write_text(
        json.dumps(out, indent=2) + '\n')
    print(json.dumps(out, indent=2))
    return 0 if out['success'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
