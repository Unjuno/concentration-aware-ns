from tools.check_shrinking_core_mass_bound import derive


def test_shrinking_core_volume_and_mass_probability_scaling():
    result = derive()
    assert result["status"] == "PASS_SYMBOLIC_CORE_ENCLOSURE_AND_MASS_SCALING"
    assert all(result["checks"].values())
