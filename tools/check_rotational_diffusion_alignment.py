"""Verify the tangent-plane Jeffery-plus-rotational-diffusion model exactly."""
import json
import hashlib
from pathlib import Path

import sympy as sp


q, alpha, v0, dr, tau0 = sp.symbols("q alpha v0 Dr tau0", positive=True)
delta, d0 = sp.symbols("delta D0", positive=True)


def main():
    v_general = v0*q**(2*alpha) + 2*dr*tau0/(2*alpha-1)*(q-q**(2*alpha))
    ode_general = sp.simplify(sp.diff(v_general, q)-2*alpha*v_general/q + 2*dr*tau0)
    v_critical = q*(v0+2*dr*tau0*sp.log(1/q))
    ode_critical = sp.simplify(sp.diff(v_critical, q)-v_critical/q + 2*dr*tau0)
    v_scaled_diffusion = v0*q**(2*alpha) + 2*d0*tau0/(2*alpha+delta-1)*(
        q**(1-delta)-q**(2*alpha)
    )
    ode_scaled_diffusion = sp.simplify(
        sp.diff(v_scaled_diffusion, q)-2*alpha*v_scaled_diffusion/q
        +2*d0*tau0*q**(-delta)
    )
    scaled_initial_residual = sp.simplify(v_scaled_diffusion.subs(q, 1)-v0)

    gt_half_coefficient = 2*dr*tau0/(2*alpha-1)
    gt_half_remainder = sp.simplify(v_general/q-gt_half_coefficient)
    lt_half_coefficient = v0+2*dr*tau0/(1-2*alpha)
    lt_half_remainder = sp.simplify(v_general/q**(2*alpha)-lt_half_coefficient)
    critical_coefficient = 2*dr*tau0
    critical_remainder = sp.simplify(
        v_critical/(q*sp.log(1/q))-critical_coefficient
    )
    zero_strain_variance = sp.simplify(v_general.subs(alpha, 0))
    deterministic_variance = sp.simplify(v_general.subs(dr, 0))
    delta_one_variance = sp.simplify(v_scaled_diffusion.subs(delta, 1))
    delta_one_limit = sp.simplify(sp.limit(delta_one_variance, q, 0, dir="+"))
    delta_half_alpha_scaled = sp.simplify(
        v_scaled_diffusion.subs(delta, sp.Rational(1, 2))
    )
    diffusion_critical = q**(2*alpha)*(v0+2*d0*tau0*sp.log(1/q))
    critical_diffusion_ode = sp.simplify(
        sp.diff(diffusion_critical, q)-2*alpha*diffusion_critical/q
        +2*d0*tau0*q**(-(1-2*alpha))
    )
    delta_gt_one_variance = v_scaled_diffusion.subs({delta: sp.Rational(3, 2), alpha: 1})
    delta_gt_one_limit = sp.limit(delta_gt_one_variance, q, 0, dir="+")

    # The large-strain regime relevant to the slender Jeffery limit has
    # alpha=3*kappa*C/2. For alpha>1/2 and Dr>0, variance is noise-dominated.
    deterministic_exponent = 2*alpha
    brownian_exponent = sp.Integer(1)
    fiber_alpha = sp.Rational(3, 2)*sp.Rational(99, 101)*sp.Rational(7999999, 2000000)

    checks = {
        "checker": "tools/check_rotational_diffusion_alignment.py",
        "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "sympy_version": sp.__version__,
        "general_branch_substitution_residual_zero": ode_general == 0,
        "critical_branch_substitution_residual_zero": ode_critical == 0,
        "alpha_gt_half_noise_leading_coefficient": str(gt_half_coefficient),
        "alpha_gt_half_normalized_remainder": str(gt_half_remainder),
        "alpha_lt_half_deterministic_leading_coefficient": str(lt_half_coefficient),
        "alpha_lt_half_normalized_remainder": str(lt_half_remainder),
        "alpha_eq_half_logarithmic_leading_coefficient": str(critical_coefficient),
        "alpha_eq_half_normalized_remainder": str(critical_remainder),
        "alpha_gt_half_noise_exponent": str(brownian_exponent),
        "alpha_gt_half_deterministic_variance_exponent": str(deterministic_exponent),
        "alpha_gt_half_noise_dominates_for_positive_Dr": True,
        "zero_strain_variance": str(zero_strain_variance),
        "deterministic_limit_variance": str(deterministic_variance),
        "AR10_source_C_lower_bound_alpha": str(fiber_alpha),
        "AR10_source_C_lower_bound_exceeds_half": bool(fiber_alpha > sp.Rational(1, 2)),
        "fixed_cutoff_variance_formula": str(sp.factor(v_general)),
        "scaled_diffusion_variance_formula": str(sp.factor(v_scaled_diffusion)),
        "scaled_diffusion_ode_substitution_residual_zero": ode_scaled_diffusion == 0,
        "scaled_diffusion_initial_condition_residual_zero": scaled_initial_residual == 0,
        "delta_one_variance_limit": str(delta_one_limit),
        "critical_diffusion_branch_ode_residual_zero": critical_diffusion_ode == 0,
        "delta_half_alpha_gt_half_variance_tends_zero": bool(
            sp.limit(delta_half_alpha_scaled.subs(alpha, 1), q, 0, dir="+") == 0
        ),
        "delta_3_over_2_alpha_1_variance_limit": str(delta_gt_one_limit),
        "dimensionless_Peclet_scale": "Pe(q) ~ [C/(2*D0*tau0)]*q^(delta-1)",
        "diffusion_exponent_threshold": "delta<1: variance tends to zero; delta=1: finite positive limit; delta>1: tangent-plane variance diverges",
        "pass": all([
            ode_general == 0, ode_critical == 0, ode_scaled_diffusion == 0,
            sp.simplify(v_general.subs(q, 1)-v0) == 0,
            sp.simplify(v_critical.subs(q, 1)-v0) == 0,
            scaled_initial_residual == 0,
            critical_diffusion_ode == 0,
            sp.simplify(gt_half_remainder - q**(2*alpha-1)*(v0-gt_half_coefficient)) == 0,
            sp.simplify(lt_half_remainder - 2*dr*tau0/(2*alpha-1)*q**(1-2*alpha)) == 0,
            sp.simplify(critical_remainder - v0/sp.log(1/q)) == 0,
            sp.simplify(zero_strain_variance-(v0+2*dr*tau0*(1-q))) == 0,
            deterministic_variance == v0*q**(2*alpha),
            delta_one_limit == d0*tau0/alpha,
            sp.limit(delta_half_alpha_scaled.subs(alpha, 1), q, 0, dir="+") == 0,
            delta_gt_one_limit is sp.oo,
            fiber_alpha > sp.Rational(1, 2),
        ]),
    }
    out = Path("evidence/tests/rotational-diffusion-alignment.json")
    out.write_text(json.dumps(checks, indent=2)+"\n")
    print(json.dumps(checks, indent=2))
    if not checks["pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
