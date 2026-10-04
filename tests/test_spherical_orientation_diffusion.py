"""Exact identities for the global Jeffery--Smoluchowski audit model."""

from tools.check_spherical_orientation_diffusion import derive


def test_global_orientation_checker_proves_stationary_density_and_diffusion_clock():
    result = derive()
    assert result["identities_pass"]
    assert result["surface_divergence_of_drift"] == "a*(1 - 3*x**2)"
    assert result["delta_eq_one_stationary_density_relative_to_surface_area"] == (
        "rho_inf(p)=Z^(-1)*exp(chi*p_z^2), chi=a/(2*D0)"
    )


def test_full_sphere_diffusion_limit_isotropic_cone_probability_is_bounded():
    result = derive()
    assert result["target_cone_probability_isotropic_limit"] == "1 - cutoff"
    assert "uniform surface density in L2(S^2)" in result["delta_gt_one_limit"]
    assert any("does not imply unbounded physical variance" in item for item in result["limitations"])


def test_subcritical_integrable_diffusion_excludes_equator_under_documented_sde_argument():
    result = derive()
    assert result["delta_lt_one_total_diffusion_general"] == (
        "D0*tau0^(1-delta)/(1-delta), finite for delta<1"
    )
    assert result["strict_lyapunov_quantity"].endswith(
        "zero only on the equator and the two poles"
    )
    assert "excludes equator convergence almost surely" in result["subcritical_stochastic_limit_set"]
    assert "conditioning/Fubini imply zero probability" in result["equator_avoidance_argument"]


def test_equatorial_coordinate_reduction_and_poles_are_corrected():
    result = derive()
    assert result["scalar_ito_reduction"].startswith(
        "dx=[(a-2*d(s))*x-a*x^3]ds"
    )
    assert result["scalar_pole_ito_drifts"] == "(-2*D, 2*D)"
    assert "not absorbing" in result["scalar_ito_reduction"]
    assert "sqrt(2*d(s))*dW_s" in result["equatorial_theta_sde"]
    assert result["identities_pass"]
