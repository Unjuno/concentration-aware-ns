import importlib
import importlib.util

from flint import acb, arb


def test_fourier_gradient_l1_bound_is_sharp_for_a_single_cosine_mode():
    spec = importlib.util.find_spec("tools.audit_openfoam_trig_supremum")
    assert spec is not None, "continuous trigonometric reconstruction bound is not implemented"
    module = importlib.import_module("tools.audit_openfoam_trig_supremum")
    coefficients = [
        (1, 0, 0, (acb(arb("0.5")), acb(0), acb(0))),
        (-1, 0, 0, (acb(arb("0.5")), acb(0), acb(0))),
    ]
    bound = module.fourier_gradient_l1_bound(coefficients)
    assert arb("0.999999") < bound < arb("1.000001")


def test_nyquist_real_sine_alias_keeps_the_same_l1_derivative_bound():
    module = importlib.import_module("tools.audit_openfoam_trig_supremum")
    unsplit = module.fourier_gradient_l1_bound([
        (-8, 0, 0, (acb(1), acb(0), acb(0))),
    ])
    split = module.fourier_gradient_l1_bound([
        (-8, 0, 0, (acb(arb("0.5")), acb(0), acb(0))),
        (8, 0, 0, (acb(arb("0.5")), acb(0), acb(0))),
    ])
    assert unsplit < arb("8.000001") and unsplit > arb("7.999999")
    assert split < arb("8.000001") and split > arb("7.999999")


def test_archived_reconstruction_bounds_are_interval_enclosed_and_scoped():
    spec = importlib.util.find_spec("tools.audit_openfoam_trig_supremum")
    assert spec is not None, "continuous trigonometric reconstruction bound is not implemented"
    module = importlib.import_module("tools.audit_openfoam_trig_supremum")
    result = module.audit()
    rows = {row["n"]: row for row in result["cases"]}
    assert set(rows) == {16, 32, 64}
    assert arb(rows[16]["gradient_relative_supremum_upper_fraction"]) > arb("0.05")
    assert arb(rows[16]["vorticity_relative_supremum_upper_fraction"]) > arb("0.05")
    assert arb(rows[32]["gradient_relative_supremum_upper_fraction"]) < arb("0.05")
    assert arb(rows[32]["vorticity_relative_supremum_upper_fraction"]) < arb("0.05")
    assert arb(rows[64]["gradient_relative_supremum_upper_fraction"]) < arb("0.05")
    assert arb(rows[64]["vorticity_relative_supremum_upper_fraction"]) < arb("0.05")
    assert result["finite_volume_field_certified"] is False
