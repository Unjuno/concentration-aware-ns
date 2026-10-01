"""Check the fixed-cone packet estimate and distinguish its error scale."""

import sympy as sp


def test_remainder_threshold_preserves_a_fixed_axis_cone():
    q, C, delta, k, integral = sp.symbols(
        "q C delta k integral", positive=True
    )
    theta, target_tangent = sp.symbols("theta target_tangent", positive=True)
    cosine = sp.cos(theta)
    axial = q**(-C) * delta * cosine
    transverse = q**(C / 2) * delta * sp.sin(theta)
    eta = (target_tangent - q**(3 * C / 2) * sp.tan(theta)) / (1 + target_tangent)
    E = cosine * eta
    threshold = E / ((1 + E) * k * integral)
    remainder = q**(-C) * k * delta**2 * integral / (1 - k * delta * integral)

    # At the sufficient threshold, the remainder/axial ratio is exactly the
    # allowance obtained by rearranging (B+Z)/(A-Z) <= tan(theta_target).
    normalized_remainder = sp.simplify(
        (remainder / axial).subs(delta, threshold)
    )
    assert sp.simplify(normalized_remainder - eta) == 0
    assert sp.simplify(
        transverse + eta * axial - target_tangent * (axial - eta * axial)
    ) == 0
    assert sp.simplify(
        (transverse / axial) - q ** (3 * C / 2) * sp.tan(theta)
    ) == 0


def test_fixed_cone_and_transverse_relative_error_have_different_powers():
    C, kappa = sp.symbols("C kappa", positive=True)
    fixed_cone_power = C + kappa - 1
    transverse_relative_power = kappa + sp.Rational(5, 2) * C - 1

    assert sp.simplify(transverse_relative_power - fixed_cone_power - sp.Rational(3, 2) * C) == 0
    assert fixed_cone_power.subs({C: 4, kappa: 40}) == 43
    assert transverse_relative_power.subs({C: 4, kappa: 40}) == 49
