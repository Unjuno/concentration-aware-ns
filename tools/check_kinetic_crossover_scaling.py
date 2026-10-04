"""Check the conditional power laws in the kinetic crossover audit.

This is an algebra check, not a kinetic or Navier--Stokes simulation.
"""
import hashlib
import json
from pathlib import Path

import sympy as sp


def check():
    s, alpha, beta = sp.symbols("s alpha beta", positive=True)
    tau0, t_ref, kappa, lambda0, length0 = sp.symbols(
        "tau0 t_ref kappa lambda0 length0", positive=True
    )
    tau_rel = tau0 * s**alpha
    gamma_core = kappa / (t_ref * s)
    chi = sp.simplify(tau_rel * gamma_core)
    lambda_local = lambda0 * s**beta
    ell_r = length0 * sp.sqrt(s)
    kn = sp.simplify(lambda_local / ell_r)
    chi_cross = sp.solve(sp.Eq(chi.subs(alpha, 0), 1), s)[0]
    kn_cross = sp.solve(sp.Eq(kn.subs(beta, 0), 1), s)[0]
    # d(log y)/d(log s) = s * d(log y)/ds.
    chi_power = sp.simplify(s * sp.diff(sp.log(chi), s))
    kn_power = sp.simplify(s * sp.diff(sp.log(kn), s))
    controls = {
        "fixed_relaxation_chi_power_is_minus_one":
            sp.simplify(chi_power.subs(alpha, 0) + 1) == 0,
        "variable_relaxation_chi_power_is_alpha_minus_one":
            sp.simplify(chi_power - (alpha - 1)) == 0,
        "fixed_mean_free_path_kn_power_is_minus_one_half":
            sp.simplify(kn_power.subs(beta, 0) + sp.Rational(1, 2)) == 0,
        "variable_mean_free_path_kn_power_is_beta_minus_one_half":
            sp.simplify(kn_power - (beta - sp.Rational(1, 2))) == 0,
        "fixed_relaxation_crossing":
            sp.simplify(chi_cross - kappa * tau0 / t_ref) == 0,
        "fixed_mean_free_path_crossing":
            sp.simplify(kn_cross - (lambda0 / length0)**2) == 0,
    }
    return {
        "scope": "Symbolic power-law and dimensional algebra only; no kinetic closure failure, material state, or physical transition is established.",
        "sympy": sp.__version__,
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "definitions": {
            "remaining_time": "s=(T-t)/t_ref",
            "core_rate": "Gamma_core=kappa/(t_ref*s)",
            "relaxation_time": "tau_rel=tau0*s**alpha",
            "strain_collision_indicator": "chi=tau_rel*Gamma_core",
            "radial_core_scale": "ell_r=length0*s**(1/2)",
            "mean_free_path": "lambda=lambda0*s**beta",
            "local_knudsen": "Kn_r=lambda/ell_r",
        },
        "derived": {
            "chi": str(chi),
            "chi_power_in_s": str(chi_power),
            "fixed_relaxation_order_one_crossing": str(chi_cross),
            "knudsen_ratio": str(kn),
            "knudsen_power_in_s": str(kn_power),
            "fixed_mean_free_path_order_one_crossing": str(kn_cross),
            "BGK_relaxation_model": "tau_rel=mu/p_thermodynamic only under the stated BGK kinetic model; not inferred from incompressible constraint pressure",
        },
        "controls": controls,
        "success": all(controls.values()),
    }


def main():
    result = check()
    target = Path("evidence/analytic-checks/kinetic-crossover-scaling-2026-10-04.json")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    return 0 if result["success"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
