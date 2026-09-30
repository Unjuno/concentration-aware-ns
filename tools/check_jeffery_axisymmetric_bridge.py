"""Check a conditional Jeffery-director / continuum tangent-map identity.

This checks algebra under the explicitly stated ideal axisymmetric strain model.
It does not establish that a finite particle follows the OpenAI PDE flow.
"""
import json
from fractions import Fraction
import math
from pathlib import Path

import sympy as sp


def derive():
    beta, gamma, kappa, t, t0, C = sp.symbols(
        "beta gamma kappa t t0 C", positive=True, finite=True
    )
    # E = diag(2 gamma, -gamma, -gamma); axial rigid rotation has zero x component.
    p = sp.Matrix([sp.cos(beta), sp.sin(beta), sp.Integer(0)])
    E = sp.diag(2 * gamma, -gamma, -gamma)
    jeffery = kappa * (E * p - (p.dot(E * p)) * p)
    beta_dot = sp.simplify(-jeffery[0] / sp.sin(beta))
    expected_beta_dot = -3 * kappa * gamma * sp.sin(beta) * sp.cos(beta)
    assert sp.simplify(beta_dot - expected_beta_dot) == 0

    # d(log(tan(beta)))/dt = beta_dot / (sin(beta) cos(beta)).
    log_tan_rate = sp.simplify(beta_dot / (sp.sin(beta) * sp.cos(beta)))
    assert sp.simplify(log_tan_rate + 3 * kappa * gamma) == 0

    # Integrate the hypothesized strain gamma(t)=C/(2(1-t)).
    s = sp.symbols("s", real=True)
    integrated_strain = C * sp.log((1 - t0) / (1 - t)) / 2
    assert sp.simplify(sp.diff(integrated_strain, t) - C / (2 * (1 - t))) == 0
    assert sp.simplify(integrated_strain.subs(t, t0)) == 0
    Q = (1 - t) / (1 - t0)
    expected_ratio = Q ** (sp.Rational(3, 2) * kappa * C)
    resulting_log_rate = sp.simplify(sp.diff(sp.log(expected_ratio), t))
    assert sp.simplify(resulting_log_rate + 3 * kappa * C / (2 * (1 - t))) == 0

    tan_target = sp.symbols("tan_target", positive=True, finite=True)
    q = sp.symbols("q", positive=True, finite=True)
    a = q ** (sp.Rational(3, 2) * kappa * C)
    mu_threshold = a / sp.sqrt(a**2 + tan_target**2)
    orientation_probability = 1 - mu_threshold
    # For isotropic unoriented initial directors, mu=|cos(beta0)| is U[0,1].
    assert sp.simplify((a * sp.sqrt(1 - mu_threshold**2) / mu_threshold) - tan_target) == 0
    assert sp.limit(orientation_probability, q, 0, dir="+") == 1

    # Compare the shape factor for aspect ratios reported in arXiv:2607.14298v2.
    shape_factors = {}
    for ar in (10, 100):
        value = Fraction(ar * ar - 1, ar * ar + 1)
        shape_factors[str(ar)] = {
            "aspect_ratio": ar,
            "kappa_exact": f"{value.numerator}/{value.denominator}",
            "kappa_decimal": float(value),
            "rate_fraction_of_slender_limit": float(value),
        }
    density_kg_m3 = 1059.0
    dynamic_viscosity_pa_s = 1.79e-3
    kinematic_viscosity_m2_s = dynamic_viscosity_pa_s / density_kg_m3
    strain_rates_s = [115.0, 150.0]
    core_radii_m = [math.sqrt(2 * kinematic_viscosity_m2_s / gamma) for gamma in strain_rates_s]
    core_radius_min_m, core_radius_max_m = min(core_radii_m), max(core_radii_m)
    fiber_length_min_m, fiber_length_max_m = 40e-6, 500e-6
    length_to_core_range = [
        fiber_length_min_m / core_radius_max_m,
        fiber_length_max_m / core_radius_min_m,
    ]
    return {
        "status": "ALGEBRA_IDENTITIES_PASS",
        "scope": "Jeffery director in prescribed spatially uniform axisymmetric extensional strain; no finite-particle transfer theorem",
        "velocity_strain_tensor": ["2*gamma", "-gamma", "-gamma"],
        "jeffery_equation": "dp/dt = Omega*p + kappa*(E*p - (p.E.p)*p)",
        "polar_angle_ode": "d beta/dt = -3*kappa*gamma*sin(beta)*cos(beta)",
        "angle_ratio_general": "tan(beta(t))/tan(beta(t0)) = exp(-3*kappa*integral(gamma ds))",
        "assumed_strain_history": "gamma(t) = C/(2*(1-t))",
        "resulting_angle_ratio": "Q^(3*kappa*C/2), Q=(1-t)/(1-t0)",
        "continuum_tangent_map_ratio": "Q^(3*C/2)",
        "slender_limit_match": "kappa -> 1",
        "isotropic_initial_director_probability": "1 - a/sqrt(a^2 + tan(theta_star)^2), a=Q^(3*kappa*C/2), for isotropic unoriented initial directions and kappa>0",
        "probability_scope": "orientation event of an ideal Jeffery director only; no absolute-position distribution",
        "shape_factors": shape_factors,
        "source_reported_fiber_scale_estimate": {
            "density_kg_m3": density_kg_m3,
            "dynamic_viscosity_pa_s": dynamic_viscosity_pa_s,
            "kinematic_viscosity_m2_s": kinematic_viscosity_m2_s,
            "strain_rate_range_s_inverse": [115, 150],
            "fiber_length_range_m": [fiber_length_min_m, fiber_length_max_m],
            "burgers_core_radius_range_m": [core_radius_min_m, core_radius_max_m],
            "fiber_length_to_core_radius_range": length_to_core_range,
            "interpretation": "approximate scale ratio from reported ranges; not a universal Jeffery-breakdown threshold",
        },
        "assumptions_and_missing_bridge": [
            "rigid prolate Jeffery particle with aspect-ratio shape factor kappa",
            "velocity gradient is spatially uniform across the particle",
            "axisymmetric strain eigendirections persist along the particle path",
            "particle inertia, Brownian rotation, flexibility, and particle-flow feedback are neglected",
            "the OpenAI construction only supplies a local continuum flow derivative; no fixed-size endpoint tube is established",
        ],
    }


def main():
    result = derive()
    output = Path("evidence/tests/jeffery-axisymmetric-bridge.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
