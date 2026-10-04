"""Exact algebra for the conditional finite-packet bound; no PDE simulation."""
import hashlib
import json
from pathlib import Path

import sympy as s


def main():
    q, tau0, C = s.symbols('q tau0 C', positive=True)
    a = q**(-C)
    integral = tau0*(1-q**(1-C))/(1-C)
    critical_integral = -tau0*s.log(q)
    I, delta, k, A, rho = s.symbols('I delta k A rho', positive=True)
    b = delta/(1-k*delta*I)
    x, y, z, g, omega = s.symbols('x y z g omega', real=True)
    v = s.Matrix([x, y, z])
    G = s.Matrix([[-g/2, -omega, 0], [omega, -g/2, 0], [0, 0, g]])
    theta0, m = s.symbols('theta0 m', positive=True)
    cosine, sine = s.cos(theta0), s.sin(theta0)
    axial = q**(-C)*delta*cosine
    transverse = q**(C/2)*delta*sine
    remainder = q**(-C)*k*delta**2*I/(1-k*delta*I)
    eta = (m-q**(3*C/2)*s.tan(theta0))/(1+m)
    E = cosine*eta
    delta_cone = E/((1+E)*k*I)
    residuals = {
        'primitive_derivative_C_ne_one': s.simplify(-s.diff(integral, q)/tau0-a),
        'primitive_derivative_C_one': s.simplify(-s.diff(critical_integral, q)/tau0-1/q),
        'primitive_initial_C_ne_one': s.simplify(integral.subs(q, 1)),
        'primitive_initial_C_one': critical_integral.subs(q, 1),
        'comparison_derivative_in_I': s.simplify(s.diff(b, I)-k*b*b),
        'remainder_identity': s.simplify(b-delta-k*delta**2*I/(1-k*delta*I)),
        'tube_threshold_equality': s.simplify((A*b).subs(delta, rho/(A+k*rho*I))-rho),
        'rotation_cancellation': s.expand((v.T*G*v)[0]-g*(z*z-(x*x+y*y)/2)),
        'growth_bound_slack': s.expand(g*(v.dot(v))-(v.T*G*v)[0]-3*g*(x*x+y*y)/2),
        'linear_transverse_to_axial_ratio': s.simplify(transverse/axial-q**(3*C/2)*s.tan(theta0)),
        'cone_boundary_from_component_inequality': s.simplify(
            (transverse+eta*axial)-m*(axial-eta*axial)),
        'remainder_over_axial_amplification': s.simplify(
            remainder.subs(delta, delta_cone)/axial.subs(delta, delta_cone)-eta),
        'cone_radius_threshold_saturates_comparison': s.simplify(
            (k*delta_cone*I)/(cosine*(1-k*delta_cone*I))-eta),
    }
    # Exact rational examples test the sufficient radius, not an actual flow.
    small = (A*b).subs({A: 4, k: 1, I: 1, delta: s.Rational(1, 100)})
    large = (A*b).subs({A: 4, k: 1, I: 1, delta: s.Rational(1, 20)})
    controls = {
        'small_packet_bound_inside_tube': bool(small < s.Rational(1, 10)),
        'large_packet_bound_not_certified': bool(large > s.Rational(1, 10)),
        'failed_sufficient_bound_is_not_an_exit_claim': bool(large > s.Rational(1, 10)),
        'omitting_denominator_is_detected': s.simplify(b-delta-k*delta**2*I) != 0,
    }
    success = all(value == 0 for value in residuals.values()) and all(controls.values())
    out = {
        'scope': 'Symbolic identities and rational controls for docs/axis-packet-bound.md. '
                 'Not a proof of the comparison theorem, certified rho/M estimates, '
                 'a packet simulation, or end-to-end Lean verification.',
        'sympy': s.__version__,
        'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'conditions': ['0 < q <= 1', 'tau0 > 0', 'C > 0', 'k = M/2 >= 0',
                       'delta >= 0', 'k*delta*I < 1', 'A*delta/(1-k*delta*I) < rho'],
        'fixed_cone_alignment': {
            'linear_transverse_over_axial': 'Q^(3C/2)*tan(theta0)',
            'cone_remainder_allowance_ratio': 'eta(Q)=(tan(theta_target)-Q^(3C/2)*tan(theta0))/(1+tan(theta_target))',
            'normalized_remainder_over_axial': 'k*delta*I/(cos(theta0)*(1-k*delta*I))',
            'sufficient_packet_threshold': 'delta<=E(Q)/((1+E(Q))*k*I), E(Q)=cos(theta0)*eta(Q)',
            'asymptotic_power_under_k_and_I_envelopes': 'Q^(C+kappa-1)',
            'scope': 'Keeps a fixed non-transverse initial direction inside a fixed axis cone; it is distinct from relative error against the contracting transverse component.',
        },
        'residuals': {name: str(value) for name, value in residuals.items()},
        'controls': controls,
        'rational_bounds': {'small': str(small), 'large': str(large), 'tube': '1/10'},
        'logical_boundary': {
            'certified_inside': 'the upper comparison bound is strictly below tube radius',
            'not_certified': 'the upper comparison bound exceeds tube radius',
            'not_implied': ['actual trajectory exits the tube', 'finite-packet alignment fails',
                            'molecular alignment changes', 'constitutive viscosity changes'],
        },
        'success': success,
    }
    Path('evidence/tests/axis-packet-bound.json').write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps(out, indent=2))
    return 0 if success else 1


if __name__ == '__main__':
    raise SystemExit(main())
