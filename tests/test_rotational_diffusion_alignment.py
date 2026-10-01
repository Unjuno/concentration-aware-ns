"""Analytic controls for the reduced Jeffery-plus-rotational-diffusion model."""
import sympy as sp


def test_constant_rotational_diffusion_variance_solves_initial_value_problem():
    q, alpha, v0, dr, tau0 = sp.symbols(
        "q alpha v0 Dr tau0", positive=True
    )
    v = v0*q**(2*alpha) + 2*dr*tau0/(2*alpha-1)*(q-q**(2*alpha))
    # q=(1-t)/(1-t0), so dv/dq - 2 alpha v/q = -2 Dr tau0.
    assert sp.simplify(sp.diff(v, q)-2*alpha*v/q+2*dr*tau0) == 0
    assert sp.simplify(v.subs(q, 1)-v0) == 0
    assert sp.simplify(v.subs(dr, 0)-v0*q**(2*alpha)) == 0


def test_diffusion_power_law_has_critical_exponent_one():
    q, alpha, v0, d0, tau0, delta = sp.symbols(
        "q alpha v0 D0 tau0 delta", positive=True
    )
    v = v0*q**(2*alpha) + 2*d0*tau0/(2*alpha+delta-1)*(
        q**(1-delta)-q**(2*alpha)
    )
    residual = sp.diff(v, q)-2*alpha*v/q+2*d0*tau0*q**(-delta)
    assert sp.simplify(residual) == 0
    assert sp.simplify(sp.limit(v.subs(delta, 1), q, 0, dir="+")) == d0*tau0/alpha
    assert sp.limit(v.subs({delta: sp.Rational(1, 2), alpha: 1}), q, 0, dir="+") == 0
    assert sp.limit(v.subs({delta: sp.Rational(3, 2), alpha: 1}), q, 0, dir="+") is sp.oo


def test_brownian_and_flow_rates_have_same_delta_one_boundary():
    q, C, d0, tau0, delta = sp.symbols(
        "q C D0 tau0 delta", positive=True
    )
    gamma = C/(2*tau0*q)
    rotational_diffusion = d0*q**(-delta)
    pe = sp.simplify(gamma/rotational_diffusion)
    assert sp.simplify(pe/(C/(2*d0*tau0)*q**(delta-1))) == 1

