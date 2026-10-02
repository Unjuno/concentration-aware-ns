"""Check the full-sphere Jeffery--Smoluchowski model used in the audit note.

This is symbolic model algebra, not a simulation or a particle-transfer theorem.
"""

import hashlib
import json
import platform
from pathlib import Path
import sys

import sympy as sp


def derive():
    x, a, D, D0, tau0, s, delta, cutoff, chi = sp.symbols(
        "x a D D0 tau0 s delta cutoff chi", positive=True
    )
    rho = sp.exp(chi * x**2)

    # On S^2, x=p_z is zonal and Delta f=(1-x^2)f''-2*x*f'.
    lap_x2 = sp.simplify((1 - x**2) * sp.diff(x**2, x, 2) - 2 * x * sp.diff(x**2, x))
    div_drift = sp.simplify(a * lap_x2 / 2)
    log_density_derivative = sp.simplify(
        (D * sp.diff(sp.log(rho), x)).subs(chi, a / (2 * D))
    )
    drift_potential_derivative = sp.simplify(a * x)
    zero_flux_residual = sp.simplify(log_density_derivative - drift_potential_derivative)

    tau = tau0 * sp.exp(-s)
    diffusion_clock = sp.simplify(D0 * tau ** (1 - delta))
    expected_clock = D0 * tau0 ** (1 - delta) * sp.exp((delta - 1) * s)
    clock_transform_residual = sp.simplify(diffusion_clock - expected_clock)
    total_diffusion_subcritical = sp.simplify(
        sp.integrate(expected_clock.subs(delta, sp.Rational(1, 2)), (s, 0, sp.oo))
    )

    # A director is unoriented: the target cone contains both poles, hence |x|>=c.
    norm_x = sp.Integral(sp.exp(chi * x**2), (x, 0, 1))
    cone_x = sp.Integral(sp.exp(chi * x**2), (x, cutoff, 1))
    isotropic_probability = sp.simplify(
        sp.limit((cone_x / norm_x).doit(), chi, 0, dir="+")
    )
    cone_probability_erfi = sp.simplify(
        (sp.erfi(sp.sqrt(chi)) - sp.erfi(cutoff * sp.sqrt(chi)))
        / sp.erfi(sp.sqrt(chi))
    )
    isotropic_cone_probability = sp.simplify(1 - cutoff)

    checks = {
        "checker": "tools/check_spherical_orientation_diffusion.py",
        "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "python_version": platform.python_version(),
        "python_implementation": sys.implementation.name,
        "platform": platform.platform(),
        "sympy_version": sp.__version__,
        "scope": "Full unit-sphere Smoluchowski equation for an ideal rigid Jeffery director in spatially uniform axisymmetric extension with prescribed rotational diffusion.",
        "time_change": "s=log(tau0/tau), tau=1-t",
        "strain_rate": "gamma=C/(2*tau)",
        "jeffery_drift_on_sphere": "b(p)=a*(p_z*e_z-p_z^2*p), a=3*kappa*C/2",
        "rotational_diffusion": "D_r(t)=D0*tau^(-delta)",
        "transformed_fokker_planck": "partial_s rho=-div_S(b*rho)+D0*tau0^(1-delta)*exp((delta-1)*s)*Delta_S rho",
        "zonal_laplacian_x2": str(lap_x2),
        "surface_divergence_of_drift": str(div_drift),
        "delta_lt_one_total_diffusion_example_delta_half": str(total_diffusion_subcritical),
        "delta_eq_one_stationary_density_relative_to_surface_area": "rho_inf(p)=Z^(-1)*exp(chi*p_z^2), chi=a/(2*D0)",
        "stationarity_method": "The drift is (a/2)*grad_S(p_z^2); this density has zero probability current. For D0>0, ellipticity on compact connected S^2 gives the unique invariant density.",
        "unoriented_target_cone_probability": "integral_c^1 exp(chi*x^2) dx / integral_0^1 exp(chi*x^2) dx, c=cos(beta_star)",
        "target_cone_probability_erfi_form": str(cone_probability_erfi),
        "target_cone_probability_isotropic_limit": str(isotropic_cone_probability),
        "delta_gt_one_limit": "The transformed diffusivity grows exponentially. The mean-zero density obeys a Poincare energy inequality Y' <= -lambda*D(s)*Y + K/D(s) for sufficiently large D(s), hence rho converges to the uniform surface density in L2(S^2).",
        "identities_pass": all([
            lap_x2 == 2 - 6*x**2,
            div_drift == a*(1 - 3*x**2),
            zero_flux_residual == 0,
            clock_transform_residual == 0,
            total_diffusion_subcritical == 2*D0*sp.sqrt(tau0),
            sp.limit(cone_probability_erfi, chi, 0, dir="+") == 1-cutoff,
            isotropic_probability == isotropic_cone_probability,
        ]),
        "limitations": [
            "No finite-particle strain-uniformity premise is established by the continuum flow proof.",
            "D_r divergence as tau approaches zero is a prescribed mathematical law, not a measured molecular constitutive law.",
            "The delta>1 limit is an asymptotic full-sphere model result; it does not imply unbounded physical variance.",
            "The delta<1 global stochastic convergence-to-poles theorem is not proved by this symbolic checker.",
            "No particle-position determinism, intermolecular ordering, phase transition, or viscosity change is established.",
        ],
    }
    return checks


def main():
    result = derive()
    output = Path("evidence/tests/spherical-orientation-diffusion-2026-10-03.json")
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    if not result["identities_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
