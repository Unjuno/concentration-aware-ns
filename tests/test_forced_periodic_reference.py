import numpy as np

from tools.forced_periodic_reference import fields


def test_closed_form_reference_matches_independent_sample_values():
    result = fields(
        np.array([[0.2, 1.1, 2.2]]),
        time=0.3,
        nu=0.07,
    )

    # These values were independently evaluated from equations (5.1), (5.4),
    # and Theorem 4.1 of arXiv:2609.38210v1 with exact rational inputs.
    np.testing.assert_allclose(
        result["u"][0], [0.58028674067734352, -0.086189213050850511, 0.13785447382484954],
        rtol=2e-14,
        atol=2e-14,
    )
    np.testing.assert_allclose(
        result["grad_u"][0],
        [
            [0.67338036599328154, -0.83751766388541632, -0.11210829620779582],
            [0.83751766388541632, 0.58931385439243017, -0.35164711332865045],
            [0.11210829620779582, 0.35164711332865045, -1.2626942203857117],
        ],
        rtol=2e-14,
        atol=2e-14,
    )
    np.testing.assert_allclose(result["pressure"], [0.11996817184290715], rtol=2e-14, atol=2e-14)
    np.testing.assert_allclose(
        result["force"][0], [0.38960084990349693, 0.47346752302568024, -0.021221753851800013],
        rtol=2e-14,
        atol=2e-14,
    )


def test_reference_is_periodic_and_incompressible_at_sampled_points():
    points = np.array([[0.3, 0.7, 1.1], [2.4, 3.1, 5.2]])
    shifted = points + np.array([2 * np.pi, -4 * np.pi, 6 * np.pi])
    base = fields(points, time=0.41, nu=0.023)
    translated = fields(shifted, time=0.41, nu=0.023)

    for key in ("u", "grad_u", "vorticity", "pressure", "grad_pressure", "force"):
        np.testing.assert_allclose(translated[key], base[key], rtol=2e-13, atol=2e-13)
    np.testing.assert_allclose(np.trace(base["grad_u"], axis1=-2, axis2=-1), 0.0, atol=2e-15)
