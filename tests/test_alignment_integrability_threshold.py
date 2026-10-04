"""Adversarial check: a diverging strain rate need not align a director."""
import sympy as sp


def test_integrable_blowup_of_strain_has_finite_jeffery_angle_limit():
    t, alpha, gamma0, kappa, tau0 = sp.symbols(
        "t alpha gamma0 kappa tau0", positive=True
    )
    tau = 1-t
    gamma = gamma0*tau**(-alpha)
    accumulated = gamma0*(tau0**(1-alpha)-tau**(1-alpha))/(1-alpha)
    assert sp.simplify(sp.diff(accumulated, t)-gamma) == 0
    assert sp.simplify(accumulated.subs(t, 1-tau0)) == 0
    assert sp.limit(gamma, t, 1, dir="-") == sp.oo
    terminal_strain = sp.simplify(
        sp.limit(accumulated.subs(alpha, sp.Rational(1, 2)), t, 1, dir="-")
    )
    assert terminal_strain == 2*gamma0*sp.sqrt(tau0)
    terminal_angle_factor = sp.exp(-3*kappa*terminal_strain)
    assert terminal_angle_factor.is_positive


def test_reciprocal_time_rate_is_the_alignment_integrability_threshold():
    t, alpha, gamma0, tau0 = sp.symbols(
        "t alpha gamma0 tau0", positive=True
    )
    tau = 1-t
    critical_integral = gamma0*sp.log(tau0/tau)
    assert sp.limit(critical_integral, t, 1, dir="-") == sp.oo
    assert sp.limit(sp.exp(-critical_integral), t, 1, dir="-") == 0
    supercritical_integral = gamma0*(tau**(1-alpha)-tau0**(1-alpha))/(alpha-1)
    assert sp.limit(
        supercritical_integral.subs(alpha, 2), t, 1, dir="-"
    ) == sp.oo
