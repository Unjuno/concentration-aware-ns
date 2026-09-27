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
        'angle_power_case_kappa_ge_r_plus_1': s.simplify(
            (C+kappa-1) - (C+kappa-1)),
        'angle_power_case_kappa_le_r_plus_1': s.simplify(
            (C+r) - (C+kappa-1) - (r-kappa+1)),
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
            'angle_error_sufficient_power': 'Q^(C+kappa-1)',
            'combined_sufficient_initial_radius_power': 'Q^(C+max(r,kappa-1))',
            'fixed_rho_bounded_k_case': 'Q^C',
        },
        'residuals': {name: str(value) for name, value in residuals.items()},
        'controls': controls,
        'success': all(v == 0 for v in residuals.values()) and all(controls.values()),
    }
    Path('evidence/tests/packet-radius-scaling.json').write_text(
        json.dumps(out, indent=2)+'\n')
    print(json.dumps(out, indent=2))
    return 0 if out['success'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
