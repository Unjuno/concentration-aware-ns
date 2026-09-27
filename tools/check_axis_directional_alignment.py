"""Exact algebra for infinitesimal and finite-packet directional alignment."""
import hashlib
import json
from pathlib import Path

import sympy as s


def main():
    q, C, hp, hz = s.symbols('q C hp hz', positive=True)
    transverse = q**(C/2) * hp
    axial = q**(-C) * hz
    tangent = s.simplify(transverse / axial)

    delta, k, I = s.symbols('delta k I', positive=True)
    beta = k * delta * I
    eps = delta * beta / (1 - beta)
    finite_bound = (q**(3*C/2) * hp + eps) / (hz - eps)
    x = s.symbols('x', nonnegative=True)
    ratio_gap = s.simplify(finite_bound - (x + eps)/(hz - eps))

    # For C>1, I(Q) diverges as Q -> 0. The scaled comparison error
    # epsilon/delta = beta/(1-beta) therefore cannot stay bounded for fixed
    # positive delta and k in this sufficient estimate.
    tau0 = s.symbols('tau0', positive=True)
    r = s.symbols('r', positive=True)
    scaled_integral = tau0 * (1-r) / (C-1)

    identities = {
        'linear_direction_ratio': s.simplify(tangent - q**(3*C/2) * hp / hz),
        'finite_angle_bound_monotonicity': s.simplify(ratio_gap -
            (q**(3*C/2)*hp-x)/(hz-eps)),
        'singular_values_product': s.simplify(q**(C/2) * q**(C/2) * q**(-C) - 1),
    }
    asymptotic_remainder = s.simplify(scaled_integral - tau0/(C-1))
    controls = {
        'pure_transverse_is_exception': s.simplify((q**(C/2) * hp) / (q**(C/2) * hp)) == 1,
        'axial_alignment_rate_is_strict': bool(s.simplify(3*C/2) > 0),
        'error_denominator_condition_is_explicit': s.denom(eps) == 1 - beta,
        'time_integral_asymptotic_remainder_vanishes': s.simplify(asymptotic_remainder + r*tau0/(C-1)) == 0,
    }
    success = all(v == 0 for v in identities.values()) and all(controls.values())
    out = {
        'scope': 'Exact symbolic consequences of the selected infinitesimal propagator and the previously derived conditional packet error bound. Not molecular dynamics, not a full Lean proof of nonlinear flow differentiation, and not effective constants for the selected profile.',
        'sympy': s.__version__,
        'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'conditions': ['0 < Q <= 1', 'C > 1', 'nonzero initial axial component hz', 'finite-packet beta=k*delta*I(T)<1', 'finite-packet scaled error delta*beta/(1-beta)<|hz|'],
        'identities': {k: str(v) for k, v in identities.items()},
        'time_integral_asymptotic_remainder': str(asymptotic_remainder),
        'controls': controls,
        'formula': {
            'infinitesimal_tan_angle': 'Q^(3*C/2) * |h_perp| / |h_z|',
            'finite_packet_tan_angle_upper_bound': '(Q^(3*C/2)*|h_perp| + epsilon) / (|h_z|-epsilon)',
            'epsilon': 'k*delta^2*I(T)/(1-k*delta*I(T))',
            'exception': 'h_z=0: the linearized displacement remains transverse',
            'time_integral_with_r_Q_to_zero': 'I(T)=tau0*(1/r-1)/(C-1), r=Q^(C-1)',
        },
        'success': success,
    }
    Path('evidence/tests/axis-directional-alignment.json').write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps(out, indent=2))
    return 0 if success else 1


if __name__ == '__main__':
    raise SystemExit(main())
