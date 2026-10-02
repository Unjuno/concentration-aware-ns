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
