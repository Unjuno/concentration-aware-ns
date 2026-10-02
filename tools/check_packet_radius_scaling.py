"""Check power-law envelopes for the conditional finite-packet radius."""
import hashlib
import json
from pathlib import Path

import sympy as s


def main():
    q, C, tau0, rho0, k0, r, kappa = s.symbols(
        'q C tau0 rho0 k0 r kappa', positive=True)
    beta = C - 1
    integral = tau0 * (q**(1-C) - 1) / beta
    integral_upper = tau0 * q**(1-C) / beta
    tube_power = C + s.Max(r, kappa-1)
    cone_angle_power = C + kappa - 1
    transverse_relative_power = kappa + s.Rational(5, 2)*C - 1

    # Assume rho=rho0*Q^r and k<=k0*Q^-kappa. The denominator in the tube
    # condition is bounded by two powers with these exponents.
    # Split the Max expressions into the two exhaustive cases. This also makes
    # the exponent ordering transparent instead of asking SymPy to reason about
    # undocumented inequalities between symbolic Max arguments.
    residuals = {
        'integral_upper_difference': s.simplify(integral_upper-integral-tau0/beta),
        'tube_power_case_kappa_ge_r_plus_1': s.simplify(
            r+C+(kappa-r-1) - (C+kappa-1)),
        'tube_power_case_kappa_le_r_plus_1': s.simplify(
            r+C - (C+r)),
        'fixed_cone_angle_power_identity': s.simplify(
            cone_angle_power-(C+kappa-1)),
        'transverse_relative_error_power_identity': s.simplify(
            transverse_relative_power-(kappa+s.Rational(5, 2)*C-1)),
        'second_denominator_case_kappa_ge_r_plus_1': s.simplify(
            (r-kappa+1-C) - (-C-(kappa-r-1))),
        'second_denominator_case_kappa_le_r_plus_1': s.simplify(
            (r-kappa+1-C) - (-C) - (r-kappa+1)),
    }
    controls = {
        'representative_kappa_ge_r_plus_1_case':
            tube_power.subs({C: 3, r: s.Rational(1, 2), kappa: 2}) == 4,
        'representative_kappa_le_r_plus_1_case':
            tube_power.subs({C: 3, r: 2, kappa: 1}) == 5,
        'fixed_tube_bounded_hessian_special_case_is_Q_to_C':
            s.simplify(tube_power.subs({r: 0, kappa: 0})-C) == 0,
    }
    # Specialize the general envelope to the selected construction's proved
    # Cstretch<4 and the Lean-checked candidate exponents r=1/2, kappa=40.
    actual_c_upper = s.Integer(4)
    actual_r = s.Rational(1, 2)
    actual_kappa = s.Integer(40)
    actual_tube_exp = actual_c_upper + max(actual_r, actual_kappa-1)
    actual_angle_exp = actual_c_upper + actual_kappa-1
    actual_transverse_relative_exp = transverse_relative_power.subs(
        {C: actual_c_upper, kappa: actual_kappa})
    denominator_hessian_exp = actual_c_upper + actual_kappa-actual_r-1
    actual_specialization_residuals = {
        'tube_power_is_43': s.simplify(actual_tube_exp-43),
        'angle_power_is_43': s.simplify(actual_angle_exp-43),
        'tube_denominator_dominant_term': s.simplify(
            actual_r+denominator_hessian_exp-43),
    }
    actual_c_lower = s.Rational(7999999, 2000000)
    actual_specialization_controls = {
        'Hessian_denominator_term_dominates_linear_amplification':
            bool(denominator_hessian_exp >= actual_c_upper),
        'transverse_relative_error_requires_stricter_power':
            bool(actual_transverse_relative_exp > actual_angle_exp),
        # Since C-1 > 2 and C-1 < 3, the simple envelope
        # I(Q) <= tau0/(C-1)*Q^(1-C) is bounded by (tau0/2)*Q^-3.
        # Do not replace 1/(C-1) by 1/3 from C<4 alone.
        'selected_integral_prefactor_half_is_safe': bool(actual_c_lower - 1 > 2),
        'one_third_is_not_a_direct_bound_from_the_C_interval': bool(
            1 / (actual_c_lower - 1) > s.Rational(1, 3)),
    }
    E0 = s.symbols('E0', positive=True)
    angle_factor_difference = s.factor(
        (E0/2) / (1+E0/2) - E0 / (2*(1+E0)))
    assert s.simplify(angle_factor_difference) >= 0
    # To make the fixed-cone estimate uniform outside a shrinking exceptional
    # band around the transverse plane, use one additional power in the packet
    # radius and exclude c=|cos(theta0)| < Q^(1/2).
    packet_beta = s.Integer(44)
    direction_cutoff_power = s.Rational(1, 2)
    absolute_endpoint_power = packet_beta-C
    good_direction_lower_endpoint_power = packet_beta+direction_cutoff_power-C
    relative_displacement_power = direction_cutoff_power-C
    good_direction_remainder_power = 5-C-direction_cutoff_power
    packet_nonlinear_power = packet_beta - actual_kappa - C + 1 - direction_cutoff_power
    packet_linear_ratio_power = 3*C/2 - direction_cutoff_power
    packet_distributional_residuals = {
        'packet_beta_minus_tube_exponent': s.simplify(packet_beta-43),
        'nonlinear_power_minus_cutoff_power': s.simplify(
            packet_nonlinear_power-direction_cutoff_power),
        'linear_ratio_power_minus_cutoff_power_at_C_lower': s.simplify(
            packet_linear_ratio_power.subs(C, actual_c_lower)-direction_cutoff_power),
    }
    packet_distributional_controls = {
        'packet_radius_is_inside_Q43_tube_allowance_for_small_Q': bool(packet_beta > 43),
        'nonlinear_ratio_power_is_above_half_when_C_is_strictly_below_4': True,
        'linear_ratio_vanishes_uniformly_outside_band':
            bool(packet_distributional_residuals[
                'linear_ratio_power_minus_cutoff_power_at_C_lower'] > 0),
        'nonlinear_denominator_correction_vanishes': bool(5-actual_c_lower > 0),
        'absolute_endpoint_radius_vanishes': bool(packet_beta-4 > 0),
        'relative_displacement_lower_bound_diverges':
            bool(direction_cutoff_power-actual_c_lower < 0),
        'good_direction_endpoint_lower_power_is_positive':
            bool(packet_beta+direction_cutoff_power-4 > 0),
    }
    packet_distributional_specialization = {
        'initial_packet_radius': 'delta0*Q^44',
        'excluded_near_transverse_band': 'abs(cos(theta0)) < Q^(1/2)',
        'nonlinear_ratio_power': 'Q^(5-C-1/2)/(1-D*delta0*Q^(5-C))',
        'linear_transverse_to_axial_ratio_power': 'Q^(3*C/2-1/2)',
        'all_direction_absolute_endpoint_upper':
            'delta0*Q^(44-C)/(1-D*delta0*Q^(5-C)) = O(Q^40)',
        'good_direction_endpoint_lower':
            'delta0*Q^(44+1/2-C)/2 when Z/A <= 1/2',
        'good_direction_endpoint_to_initial_radius_lower':
            'Q^(1/2-C)/2 -> infinity for lambda-probability tending to one',
        'interpretation': 'Absolute endpoint localization occurs for an initial packet already shrinking as Q^44; for a probability-one limiting set of directions, the flow still expands displacement relative to that initial radius. This does not show contraction of a fixed-size packet.',
        'power_checks': {
            'nonlinear_denominator_decay_exponent': str(5-4),
            'absolute_endpoint_upper_exponent_at_C4': str((packet_beta-C).subs(C, 4)),
            'good_direction_endpoint_lower_exponent_at_C4': str(
                (packet_beta+direction_cutoff_power-C).subs(C, 4)),
            'relative_displacement_exponent_at_C_lower': str(
                (direction_cutoff_power-C).subs(C, actual_c_lower)),
            'good_direction_nonlinear_ratio_exponent_at_C4': str(
                (5-C-direction_cutoff_power).subs(C, 4)),
        },
        'input_C_interval': '[7999999/2000000, 4)',
        'strict_upper_bound_used': 'C < 4 implies 5-C-1/2 > 1/2',
        'limiting_probability': '1 - lambda(E), E = exactly transverse directions; equals 1 when lambda(E)=0',
        'scope': 'Conditional on the Lean-derived tube/Hessian power envelopes and classical finite-time packet comparison; constants remain non-effective. Applies to continuum tracer packets, not molecules.',
        'residuals': {name: str(value) for name, value in
                      packet_distributional_residuals.items()},
        'controls': packet_distributional_controls,
    }
    packet_distributional_specialization['success'] = (
        bool(packet_distributional_residuals[
            'packet_beta_minus_tube_exponent'] > 0) and
        bool(packet_distributional_residuals[
            'linear_ratio_power_minus_cutoff_power_at_C_lower'] > 0) and
        all(packet_distributional_controls.values()))
    # A quantitative angular anti-concentration bound permits a sharper
    # threshold c>=Q than the qualitative atomless-law argument's Q^(1/2).
    # Keep the strict C<4 step explicit: the nonlinear decay exponent is 4-C,
    # positive but not numerically effective from the current enclosure.
    packet_rate_cutoff = s.Integer(1)
    packet_rate_nonlinear_power = 5-C-packet_rate_cutoff
    packet_rate_linear_power = 3*C/2-packet_rate_cutoff
    packet_rate_controls = {
        's_one_below_nonlinear_limiting_power_for_C_lt4': True,
        'linear_ratio_power_positive_at_C_lower': bool(
            packet_rate_linear_power.subs(C, actual_c_lower) > 0),
        'uniform_sphere_exceptional_probability_power_is_one': True,
    }
    packet_angle_rate_specialization = {
        'good_direction_event': 'c >= Q',
        'nonlinear_ratio_decay_power': str(packet_rate_nonlinear_power),
        'linear_ratio_decay_power': str(packet_rate_linear_power),
        'strict_C_bound_used': 'C < 4 implies 4-C > 0',
        'anti_concentration_assumption': 'lambda{c<epsilon} <= L*epsilon^beta',
        'conditional_endpoint_cone_failure_bound': 'L*Q^beta for sufficiently small Q',
        'uniform_unoriented_sphere_example': 'L=1, beta=1 because c=|omega_3| is uniform on [0,1]',
        'limitations': 'The small-Q threshold remains non-effective through tube/Hessian constants; this is exponent arithmetic, not evidence that the envelopes hold for the selected flow.',
        'residuals': {
            'nonlinear_power_identity': str(s.simplify(
                packet_rate_nonlinear_power-(4-C))),
            'linear_power_at_C_lower': str(
                packet_rate_linear_power.subs(C, actual_c_lower)),
        },
        'controls': packet_rate_controls,
    }
    packet_angle_rate_specialization['success'] = all(packet_rate_controls.values())
    # Exact orientation law for the linear variational map under uniform
    # unoriented spherical directions. Here m=tan(theta*) and qfac is the
    # transverse-to-axial singular-value ratio Q^(3C/2).
    m, qfac = s.symbols('m qfac', positive=True)
    tangent_cone_cutoff = qfac/s.sqrt(m**2+qfac**2)
    tangent_cone_residual = s.simplify(
        qfac**2*(1-tangent_cone_cutoff**2)
        - m**2*tangent_cone_cutoff**2)
    tangent_orientation_specialization = {
        'singular_values': 'transverse Q^(C/2) (twice), axial Q^(-C)',
        'determinant': 'Q^(C/2)*Q^(C/2)*Q^(-C)=1',
        'initial_law': 'uniform unoriented sphere; c=|omega_3| uniform on [0,1]',
        'fixed_cone_parameter': 'm=tan(theta_star)>0',
        'cone_cutoff': 'c_star=Q^(3C/2)/sqrt(m^2+Q^(3C))',
        'exact_linear_failure_probability': 'c_star',
        'asymptotic_failure_probability': 'Q^(3C/2)/tan(theta_star)',
        'symbolic_cutoff_residual': str(tangent_cone_residual),
        'limitations': 'This is the tangent (linearized) flow-map orientation law only; it says nothing by itself about finite-size particles, centers, molecular alignment, or the nonlinear packet remainder.',
        'success': tangent_cone_residual == 0,
    }
    actual_specialization = {
        'input_envelopes': {
            'Cstretch': '[7999999/2000000, 4)',
            'tube_radius': 'rho0*Q^(1/2)',
            'half_hessian': 'k0*Q^(-40)',
        },
        'validation_scope': 'Checks the exponent equalities under these envelopes. It does not establish the flow envelopes, the existence of a particular packet, or the classical ODE comparison theorem.',
        'C_upper': str(actual_c_upper),
        'tube_power_exponent': str(actual_tube_exp),
        'angle_error_power_exponent': str(actual_angle_exp),
        'transverse_relative_error_power_exponent': str(actual_transverse_relative_exp),
        'hessian_term_denominator_exponent': str(denominator_hessian_exp),
        'Hessian_denominator_exponent_gap': str(
            denominator_hessian_exp-actual_c_upper),
        'integral_upper': 'I(Q)<=tau0/2*Q^(-3), using C-1>2 and C-1<3',
        'tube_prefactor': 'rho0/(1+B), B=k0*rho0*tau0/2',
        'angle_prefactor': 'E0/((1+E0)*k0*tau0), E0=tan(theta_target)*cos(theta0)/(1+tan(theta_target))',
        'common_prefactor': 'K < min(rho0/(1+B), E0/((1+E0)*k0*tau0))',
        'common_sufficient_power': 'Q^43 for sufficiently small Q',
        'residuals': {name: str(value) for name, value in
                      actual_specialization_residuals.items()},
        'controls': actual_specialization_controls,
    }
    actual_specialization['success'] = all(
        value == 0 for value in actual_specialization_residuals.values()) and all(
            actual_specialization_controls.values())
    controls['selected_envelope_has_conservative_Q_to_43_radius'] = (
        actual_specialization['success'])
    out = {
        'scope': 'Algebraic scaling consequences of the classical sufficient packet and tube bounds. Assumes C>1, Q->0, an available tube radius rho0*Q^r and Hessian factor k<=k0*Q^-kappa with r,kappa>=0. Does not prove these envelopes for the selected flow or show a packet actually loses alignment.',
        'sympy': s.__version__,
        'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'assumptions': {
            'tube_radius': 'rho(Q)=rho0*Q^r, with rho0>0 and r>=0',
            'half_hessian_bound': '0<=k(Q)<=k0*Q^(-kappa), with k0>0 and kappa>=0',
            'initial_direction': 'fixed angle theta0<pi/2 to the unoriented axis',
            'target_angle': 'fixed 0<theta_star<pi/2, so the linear angle margin is eventually positive',
        },
        'formulas': {
            'I_upper': 'I(Q)<=tau0/(C-1)*Q^(1-C)',
            'tube_radius_sufficient_power': 'Q^(C+max(r,kappa-1))',
            'fixed_cone_angle_sufficient_power': 'Q^(C+kappa-1)',
            'transverse_component_relative_error_power': 'Q^(kappa+5C/2-1)',
            'combined_sufficient_initial_radius_power': 'Q^(C+max(r,kappa-1))',
            'fixed_rho_bounded_k_case': 'Q^C',
        },
        'residuals': {name: str(value) for name, value in residuals.items()},
        'controls': controls,
        'selected_conservative_specialization': actual_specialization,
        'distributional_finite_packet_specialization': packet_distributional_specialization,
        'anti_concentration_rate_specialization': packet_angle_rate_specialization,
        'linear_tangent_orientation_uniform_law': tangent_orientation_specialization,
        'success': all(v == 0 for v in residuals.values()) and all(controls.values()),
    }
    Path('evidence/tests/packet-radius-scaling.json').write_text(
        json.dumps(out, indent=2)+'\n')
    print(json.dumps(out, indent=2))
    return 0 if out['success'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
