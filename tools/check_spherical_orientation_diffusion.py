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
    subcritical_decay = sp.symbols("subcritical_decay", positive=True)
    total_diffusion_subcritical = sp.simplify(
        sp.integrate(expected_clock.subs(delta, sp.Rational(1, 2)), (s, 0, sp.oo))
    )
    total_diffusion_general = D0 * tau0 ** (1 - delta) / (1 - delta)
    x_drift = a * x * (1 - x**2)
    lyapunov_derivative = sp.factor(2 * x * x_drift)
    scalar_sphere_laplacian_x = sp.simplify((1-x**2)*sp.diff(x,x,2)-2*x*sp.diff(x,x))
    scalar_ito_drift = sp.simplify(x_drift + D*scalar_sphere_laplacian_x)
    scalar_ito_drift_decomposed = (a-2*D)*x - a*x**3
    scalar_noise_variance = 2*D*(1-x**2)
    theta = sp.symbols("theta", real=True)
    theta_drift = a*sp.sin(theta)*sp.cos(theta) - D*sp.tan(theta)
    theta_drift_derivative = sp.diff(theta_drift, theta)
    theta_drift_expected_derivative = a*sp.cos(2*theta) - D/sp.cos(theta)**2
    scalar_drift_theta_chart = ((a-2*D)*sp.sin(theta)-a*sp.sin(theta)**3)/sp.cos(theta)
    scalar_ito_theta_correction = D*sp.sin(theta)/sp.cos(theta)
    theta_ito_transform_residual = sp.trigsimp(
        scalar_drift_theta_chart + scalar_ito_theta_correction - theta_drift
    )
    pole_drifts = (scalar_ito_drift_decomposed.subs(x, 1), scalar_ito_drift_decomposed.subs(x, -1))
    total_diffusion_from_decay_rate = sp.integrate(
        D0 * tau0 ** (1-delta) * sp.exp(-subcritical_decay*s), (s, 0, sp.oo)
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
    identity_checks = [
        lap_x2 == 2 - 6*x**2,
        div_drift == a*(1 - 3*x**2),
        zero_flux_residual == 0,
        clock_transform_residual == 0,
        total_diffusion_subcritical == 2*D0*sp.sqrt(tau0),
        sp.simplify(total_diffusion_from_decay_rate - D0*tau0**(1-delta)/subcritical_decay) == 0,
        sp.simplify(total_diffusion_from_decay_rate.subs(subcritical_decay, 1-delta)-total_diffusion_general) == 0,
        sp.simplify(lyapunov_derivative - 2*a*x**2*(1-x**2)) == 0,
        scalar_sphere_laplacian_x == -2*x,
        sp.simplify(scalar_ito_drift - scalar_ito_drift_decomposed) == 0,
        sp.simplify(scalar_noise_variance - 2*D*(1-x**2)) == 0,
        sp.simplify(theta_drift_derivative-theta_drift_expected_derivative) == 0,
        theta_ito_transform_residual == 0,
        pole_drifts == (-2*D, 2*D),
        sp.limit(cone_probability_erfi, chi, 0, dir="+") == 1-cutoff,
        isotropic_probability == isotropic_cone_probability,
    ]

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
        "delta_lt_one_total_diffusion_general": "D0*tau0^(1-delta)/(1-delta), finite for delta<1",
        "deterministic_polar_coordinate_ode": "d(p_z)/ds=a*p_z*(1-p_z^2)",
        "strict_lyapunov_quantity": "V(p)=p_z^2; dV/ds=2*a*p_z^2*(1-p_z^2), zero only on the equator and the two poles",
        "scalar_ito_reduction": "dx=[(a-2*d(s))*x-a*x^3]ds+sqrt(2*d(s)*(1-x^2))dW_s; for d(s)>0 the scalar Ito drift points inward at both poles, so they are not absorbing",
        "scalar_pole_ito_drifts": str(pole_drifts),
        "equatorial_theta_sde": "dtheta=[a*sin(theta)*cos(theta)-d(s)*tan(theta)]ds+sqrt(2*d(s))*dW_s, x=sin(theta), |theta|<pi/2",
        "equatorial_theta_drift_derivative": "a*cos(2*theta)-d(s)/cos(theta)^2",
        "theta_ito_transform_residual": str(theta_ito_transform_residual),
        "equator_avoidance_argument": "For any r<pi/4, at sufficiently late deterministic S the theta drift derivative is uniformly positive on [-r,r], since d(s)->0. For a fixed future Brownian path, differences of two additive-noise solutions satisfy D'=b_s(theta1)-b_s(theta2); two distinct paths that both converge to zero would eventually be in this band and their difference would grow exponentially, a contradiction. Thus at most one theta_S can converge to zero for each future noise path. At any positive deterministic S, ellipticity of the sphere SDE gives an absolutely continuous state law, hence theta_S has no atoms; independence of future Brownian increments and conditioning/Fubini imply zero probability of equator convergence. This uses the standard pathwise uniqueness/order-preserving flow on the interior; endpoint nonattainment is required.",
        "scalar_linearization_near_equator": "dx=(a-2*d(s))*x ds + sqrt(2*d(s))dW_s after dropping cubic drift and O(x^2) noise corrections; its integrating-factor terminal amplitude has a nondegenerate Gaussian law, but this alone does not prove equator avoidance for the nonlinear SDE",
        "subcritical_stochastic_limit_set": "Finite integrated diffusion makes the sphere-valued SDE an asymptotic pseudotrajectory of the deterministic Jeffery flow. The compact limit set is internally chain transitive; the strict Lyapunov function restricts it to the equator (V=0) or a pole (V=1). The separate additive-noise theta argument recorded here excludes equator convergence almost surely, conditional on the stated interior flow and ellipticity facts; therefore the ideal director converges to a pole almost surely.",
        "delta_eq_one_stationary_density_relative_to_surface_area": "rho_inf(p)=Z^(-1)*exp(chi*p_z^2), chi=a/(2*D0)",
        "stationarity_method": "The drift is (a/2)*grad_S(p_z^2); this density has zero probability current. For D0>0, ellipticity on compact connected S^2 gives the unique invariant density.",
        "unoriented_target_cone_probability": "integral_c^1 exp(chi*x^2) dx / integral_0^1 exp(chi*x^2) dx, c=cos(beta_star)",
        "target_cone_probability_erfi_form": str(cone_probability_erfi),
        "target_cone_probability_isotropic_limit": str(isotropic_cone_probability),
        "delta_gt_one_limit": "The transformed diffusivity grows exponentially. The mean-zero density obeys a Poincare energy inequality Y' <= -lambda*D(s)*Y + K/D(s) for sufficiently large D(s), hence rho converges to the uniform surface density in L2(S^2).",
        "identity_checks": identity_checks,
        "identities_pass": all(identity_checks),
        "limitations": [
            "No finite-particle strain-uniformity premise is established by the continuum flow proof.",
            "D_r divergence as tau approaches zero is a prescribed mathematical law, not a measured molecular constitutive law.",
            "The delta>1 limit is an asymptotic full-sphere model result; it does not imply unbounded physical variance.",
            "The delta<1 pole-convergence conclusion additionally uses standard interior nonattainment, elliptic smoothing, future-increment independence, and pathwise uniqueness/order preservation; the symbolic checker verifies only algebra, not those probabilistic theorems.",
            "No particle-position determinism, intermolecular ordering, phase transition, or viscosity change is established.",
        ],
    }
    return checks


def main():
    result = derive()
    output = Path("evidence/tests/spherical-orientation-diffusion-equator-avoidance-2026-10-03.json")
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    if not result["identities_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
