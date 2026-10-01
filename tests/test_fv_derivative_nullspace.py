from tools.check_fv_derivative_nullspace import audit


def test_cell_local_divergence_free_null_sequence_identity():
    result = audit()
    assert result["divergence_identity"] == "identically zero by cancellation of mixed partial derivatives"
    assert result["uniform_velocity_bound"] == "O(k^(-1/2)) for fixed smooth chi"
    assert result["gradient_supremum"].startswith("Theta(k^(1/2))")
    assert "integral over that cell is zero" in result["cell_average_invariance"]
    assert "not an OpenFOAM field reconstruction" in result["scope"]
    assert "or Navier-Stokes solution with the benchmark forcing" in result["scope"]
