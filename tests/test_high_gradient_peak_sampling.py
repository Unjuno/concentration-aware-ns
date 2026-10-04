import math

from tools.measure_high_gradient_peak_sampling import measure


def test_cell_center_peak_sampling_is_bounded_by_and_converges_to_exact_peaks():
    result = measure(resolutions=(16, 32, 64, 128), time=0.05)

    assert result["scope"].startswith("Reference-field sampling only")
    assert [row["n"] for row in result["rows"]] == [16, 32, 64, 128]
    for metric in ("gradient_fraction", "vorticity_fraction"):
        fractions = [row[metric] for row in result["rows"]]
        assert all(0 < fraction <= 1 for fraction in fractions)
        assert fractions == sorted(fractions)
    assert math.isclose(result["rows"][0]["gradient_fraction"], 0.663241939338, abs_tol=5e-13)
    assert math.isclose(result["rows"][0]["vorticity_fraction"], 0.652160656630, abs_tol=5e-13)
    assert math.isclose(result["rows"][-1]["gradient_fraction"], 0.993972476262, abs_tol=5e-13)
    assert math.isclose(result["rows"][-1]["vorticity_fraction"], 0.993870577713, abs_tol=5e-13)
