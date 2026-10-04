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


def test_selected_q43_prefactors_use_integral_ordering_from_the_source_interval():
    C_lower = sp.Rational(7999999, 2000000)
    C_upper = sp.Integer(4)
    # The selected source enclosure gives 0 < b=C-1 < 3. With L=-log(Q),
    # the exact integral is integral_0^L exp(b*s) ds, bounded by its b=3 case.
    assert C_lower - 1 > 0
    assert C_upper - 1 == 3
    beta, length, s = sp.symbols("beta length s", positive=True)
    exact_integral = (sp.exp(beta * length) - 1) / beta
    integral_representation = sp.integrate(sp.exp(beta * s), (s, 0, length))
    assert sp.simplify(exact_integral - integral_representation) == 0
    pointwise_difference = sp.simplify(
        sp.exp(3 * s) - sp.exp(beta * s)
        - sp.exp(beta * s) * (sp.exp((3 - beta) * s) - 1)
    )
    assert pointwise_difference == 0
    upper_integral = (sp.exp(3 * length) - 1) / 3
    assert sp.simplify(
        upper_integral - sp.integrate(sp.exp(3 * s), (s, 0, length))
    ) == 0

    E0 = sp.symbols("E0", positive=True)
    angle_factor = sp.simplify(
        (E0 / 2) / (1 + E0 / 2) - E0 / (2 * (1 + E0))
    )
    expected = E0**2 / (4 * (1 + E0 / 2) * (1 + E0))
    assert sp.simplify(angle_factor - expected) == 0
    assert angle_factor.is_positive


def test_shrinking_packet_absolute_localization_coexists_with_relative_stretch():
    C = sp.symbols("C", positive=True)
    initial_power = sp.Integer(44)
    # With delta=delta0*Q^44, a(Q)<=Q^-4, and k*I=O(Q^-(C+39)),
    # the nonlinear denominator is 1-O(Q^(5-C)).
    denominator_decay_power = 5 - C
    absolute_endpoint_power = initial_power - C
    good_direction_lower_endpoint_power = initial_power + sp.Rational(1, 2) - C
    relative_displacement_power = sp.Rational(1, 2) - C
    good_direction_nonlinear_ratio_power = sp.Rational(9, 2) - C

    # The source enclosure 7999999/2000000 <= C < 4 makes the denominator
    # correction vanish, the absolute endpoint radius O(Q^40), and the
    # good-direction displacement/initial-radius lower bound diverge.
    C_lower = sp.Rational(7999999, 2000000)
    assert sp.simplify(denominator_decay_power.subs(C, 4)) == 1
    assert sp.simplify(absolute_endpoint_power.subs(C, 4)) == 40
    assert sp.simplify(good_direction_lower_endpoint_power.subs(C, 4)) == sp.Rational(81, 2)
    assert sp.simplify(relative_displacement_power.subs(C, C_lower)) < 0
    assert sp.simplify(good_direction_nonlinear_ratio_power.subs(C, 4)) == sp.Rational(1, 2)


def test_uniform_sphere_tangent_map_cone_failure_probability():
    q, C, m = sp.symbols("q C m", positive=True)
    transverse_to_axial = q ** (sp.Rational(3, 2) * C)
    cutoff = transverse_to_axial / sp.sqrt(m**2 + transverse_to_axial**2)

    # For uniform spherical directions z=omega_3 has constant density 1/2
    # on [-1,1], so c=|z| is uniform on [0,1]. The cone condition is exactly
    # c >= cutoff; its failure probability is therefore the cutoff itself.
    z = sp.symbols("z", real=True)
    x = sp.symbols("x", nonnegative=True)
    band_probability = sp.integrate(sp.Rational(1, 2), (z, -x, x))
    cone_identity = sp.simplify(
        transverse_to_axial**2 * (1 - cutoff**2) - m**2 * cutoff**2
    )
    asymptotic_coefficient = sp.limit(cutoff / transverse_to_axial, q, 0)

    assert sp.simplify(band_probability - x) == 0
    assert cone_identity == 0
    assert asymptotic_coefficient == 1 / m
    assert sp.simplify(
        sp.Rational(3, 2) * sp.Rational(7999999, 2000000) - 1
    ) > 0
