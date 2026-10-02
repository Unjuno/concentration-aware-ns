"""Check when an unbounded ideal strain actually forces Jeffery alignment.

This is a kinematic director-model calculation, not an OpenAI-flow or
finite-particle transfer theorem.
"""
import json
import math
from pathlib import Path

import sympy as sp


def derive():
    t, alpha, gamma0, kappa, tau0 = sp.symbols(
        "t alpha gamma0 kappa tau0", positive=True
    )
    tau = 1 - t
    gamma = gamma0 * tau ** (-alpha)
    assert sp.limit(gamma, t, 1, dir="-") == sp.oo

    # For 0 < alpha < 1, the pointwise rate diverges but its time integral
    # converges. The Jeffery director depends on this integral, not gamma(t)
    # alone.
    integral_subcritical = gamma0 * (tau0 ** (1-alpha) - tau ** (1-alpha)) / (1-alpha)
    assert sp.simplify(sp.diff(integral_subcritical, t) - gamma) == 0
    assert sp.simplify(integral_subcritical.subs(t, 1-tau0)) == 0
    integral_half_power = sp.simplify(
        sp.limit(integral_subcritical.subs(alpha, sp.Rational(1, 2)),
                 t, 1, dir="-")
    )
    assert integral_half_power == 2*gamma0*sp.sqrt(tau0)

    # At and above the reciprocal-time scale the accumulated strain diverges.
    integral_critical = gamma0 * sp.log(tau0 / tau)
    assert sp.simplify(sp.diff(integral_critical, t) - gamma0/tau) == 0
    assert sp.simplify(integral_critical.subs(t, 1-tau0)) == 0
    assert sp.limit(integral_critical, t, 1, dir="-") == sp.oo
    integral_supercritical = gamma0 * (tau ** (1-alpha) - tau0 ** (1-alpha)) / (alpha-1)
    assert sp.simplify(sp.diff(integral_supercritical, t) - gamma) == 0
    assert sp.simplify(integral_supercritical.subs(t, 1-tau0)) == 0
    assert sp.limit(integral_supercritical.subs(alpha, 2), t, 1, dir="-") == sp.oo

    angle0 = sp.symbols("tan_beta0", positive=True)
    angle_factor_subcritical = sp.exp(-3*kappa*integral_half_power)
    angle_limit_subcritical = angle0 * angle_factor_subcritical
    assert angle_factor_subcritical.is_positive
    angle_factor_critical = sp.exp(-3*kappa*integral_critical)
    assert sp.limit(angle_factor_critical, t, 1, dir="-") == 0

    # Concrete dimensionless example: unbounded gamma, finite integrated
    # strain, and an isotropic director ensemble that does not collapse into
    # an arbitrary fixed cone with probability one.
    alpha_num = sp.Rational(1, 2)
    gamma0_num = sp.Rational(1, 10)
    kappa_num = sp.Rational(3, 4)
    t0_num = sp.Integer(0)
    integrated_num = sp.simplify(integral_half_power.subs({
        gamma0: gamma0_num, tau0: 1-t0_num
    }))
    factor_num = sp.simplify(sp.exp(-3*kappa_num*integrated_num))
    target_degrees = 10
    tangent_target = sp.tan(sp.pi*target_degrees/180)
    isotropic_cone_probability = sp.simplify(
        1-factor_num/sp.sqrt(factor_num**2+tangent_target**2)
    )
    probability_numeric = float(isotropic_cone_probability.evalf(17))
    assert integrated_num == sp.Rational(1, 5)
    assert 0 < probability_numeric < 1

    return {
        "status": "ALGEBRA_IDENTITIES_PASS",
        "scope": "Jeffery director under prescribed spatially uniform axisymmetric strain; kinematic counterexample to inferring complete alignment from pointwise rate blow-up alone.",
        "general_angle_law": "tan(beta(t))/tan(beta(t0)) = exp(-3*kappa*integral_[t0,t](gamma(s) ds))",
        "rate_family": "gamma(t)=gamma0*(1-t)^(-alpha), gamma0>0, alpha>0, t0<1",
        "pointwise_strain_diverges_for": "every alpha>0",
        "integrated_strain_finite_for": "0<alpha<1",
        "integrated_strain_diverges_for": "alpha>=1",
        "subcritical_integral_limit": "gamma0*(1-t0)^(1-alpha)/(1-alpha), valid for 0<alpha<1 by direct integration",
        "subcritical_tangent_ratio_limit": "exp(-3*kappa*gamma0*(1-t0)^(1-alpha)/(1-alpha)) > 0",
        "critical_rate": "alpha=1 gives logarithmically divergent integrated strain and ideal alignment for kappa>0",
        "openai_ideal_rate_comparison": "gamma=C/(2*(1-t)) has alpha=1; under the assumed Jeffery model it is on the nonintegrable side.",
        "counterexample": {
            "alpha": str(alpha_num),
            "gamma0": str(gamma0_num),
            "kappa": str(kappa_num),
            "initial_time": str(t0_num),
            "strain_rate": "(1/10)/sqrt(1-t), which diverges as t approaches 1",
            "integrated_strain": str(integrated_num),
            "tangent_ratio_for_any_initial_direction": str(factor_num),
            "initial_director_law": "isotropic unoriented directors",
            "target_cone_half_angle_degrees": target_degrees,
            "limiting_target_cone_probability": probability_numeric,
            "probability_is_strictly_below_one": True,
        },
        "limits": [
            "No finite-particle uniformity or trajectory premise is supplied by a pointwise velocity-gradient estimate.",
            "This prescribed strain is not asserted to solve Navier-Stokes or to equal the OpenAI selected profile.",
            "It does not model molecules, Brownian rotation, interactions, stress, viscosity, or a physical cutoff.",
        ],
    }


def main():
    result = derive()
    path = Path("evidence/tests/alignment-integrability-threshold.json")
    path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
