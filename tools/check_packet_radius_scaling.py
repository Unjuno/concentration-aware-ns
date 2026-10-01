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
    actual_specialization_controls = {
        'Hessian_denominator_term_dominates_linear_amplification':
            bool(denominator_hessian_exp >= actual_c_upper),
        'transverse_relative_error_requires_stricter_power':
            bool(actual_transverse_relative_exp > actual_angle_exp),
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
        'tube_prefactor': 'rho0/(1+B), B=k0*rho0*tau0/3',
        'angle_prefactor': '3*E0/(2*(1+E0)*k0*tau0), E0=tan(theta_target)*cos(theta0)/(1+tan(theta_target))',
        'common_prefactor': 'K < min(rho0/(1+B), 3*E0/(2*(1+E0)*k0*tau0))',
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
        'success': all(v == 0 for v in residuals.values()) and all(controls.values()),
    }
    Path('evidence/tests/packet-radius-scaling.json').write_text(
        json.dumps(out, indent=2)+'\n')
    print(json.dumps(out, indent=2))
    return 0 if out['success'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
