"""Check the analytic enclosure and probability scaling for the OpenAI core."""

import hashlib
import json
from pathlib import Path

import sympy as sp


def derive():
    tau, h, eta_c, X_c, K = sp.symbols(
        "tau h eta_c X_c K", positive=True
    )
    D = sp.Rational(1, 2) - h
    # Similarity coordinates: tau=q(1-eta^2), r^2=2Xq, z=q^D eta.
    q_upper = tau / (1 - eta_c**2)
    radial_radius_sq = 2 * X_c * q_upper
    axial_half_length = eta_c * q_upper**D
    cylinder_volume_upper = sp.simplify(
        sp.pi * radial_radius_sq * 2 * axial_half_length
    )
    expected_volume_upper = (
        4 * sp.pi * X_c * eta_c
        * tau ** (sp.Rational(3, 2) - h)
        / (1 - eta_c**2) ** (sp.Rational(3, 2) - h)
    )
    checks = {
        "similarity_coordinate_cylinder_volume_identity":
            sp.simplify(sp.powsimp(
                cylinder_volume_upper / expected_volume_upper, force=True
            ) - 1) == 0,
        "axial_similarity_exponent_lower_endpoint":
            D.subs(h, sp.Rational(1, 100)) == sp.Rational(49, 100),
        "axial_similarity_exponent_decreases_with_h":
            sp.diff(D, h) == -1,
        "core_volume_exponent_lower_endpoint":
            (sp.Rational(3, 2) - h).subs(h, sp.Rational(1, 100))
            == sp.Rational(149, 100),
        "core_volume_exponent_upper_endpoint":
            (sp.Rational(3, 2) - h).subs(h, 0) == sp.Rational(3, 2),
        "core_volume_exponent_decreases_with_h":
            sp.diff(sp.Rational(3, 2) - h, h) == -1,
        "probability_bound_vanishes_for_fixed_finite_density":
            sp.limit(K * expected_volume_upper.subs(h, sp.Rational(1, 200)),
                     tau, 0, dir="+") == 0,
        "uniform_lower_exponent_bound_vanishes":
            sp.limit(K * 4 * sp.pi * X_c * eta_c
                     / (1 - eta_c**2) ** sp.Rational(3, 2)
                     * tau ** sp.Rational(149, 100),
                     tau, 0, dir="+") == 0,
    }
    checks = {name: bool(value) for name, value in checks.items()}
    return {
        "status": "PASS_SYMBOLIC_CORE_ENCLOSURE_AND_MASS_SCALING"
        if all(checks.values()) else "FAIL",
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "primary_source": "OpenAI, Finite Time Blowup for Navier–Stokes, Section 2.1, similarity coordinates (3.2) and core definition (2.1)",
        "assumptions": [
            "0 < tau <= 1", "0 < h < 1/100", "X_c > 0 and 0 < eta_c < 1 are fixed",
            "the preterminal classical flow preserves volume",
            "the initial passive-tracer position density is bounded by fixed K",
        ],
        "formulas": {
            "D": "1/2-h",
            "similarity_relations": ["tau=q(1-eta^2)", "r^2=2Xq", "z=q^D eta"],
            "enclosing_cylinder_radius_squared_upper": "2*X_c*tau/(1-eta_c^2)",
            "enclosing_cylinder_axial_half_length_upper": "eta_c*(tau/(1-eta_c^2))^(1/2-h)",
            "core_volume_upper": str(sp.simplify(expected_volume_upper)),
            "core_mass_probability_upper": "K*core_volume_upper",
            "asymptotic_probability_order": "O(tau^(3/2-h))",
            "exponent_range": "149/100 < 3/2-h < 3/2",
        },
        "checks": checks,
        "interpretation": [
            "Bounds a bounded-density passive-tracer ensemble's occupancy of the time-dependent Eulerian core, not an individual trajectory.",
            "Point-mass laws, unbounded densities, finite-size or inertial particles, and molecular interactions are outside scope.",
            "Infinitesimal direction alignment can coexist with vanishing core occupancy because the observables differ.",
        ],
    }


if __name__ == "__main__":
    result = derive()
    Path("evidence/tests/shrinking-core-mass-bound.json").write_text(
        json.dumps(result, indent=2) + "\n"
    )
    print(json.dumps(result, indent=2))
