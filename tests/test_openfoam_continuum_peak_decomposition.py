import math

from tools.compare_openfoam_peaks_to_continuum import row_from_diagnostics


def test_peak_decomposition_keeps_reference_sampling_stencil_and_solver_levels_distinct():
    diagnostics = {
        "parameters": {"n": 64, "dt": 0.001, "end": 0.05, "frequency": 4},
        "reference_gradient_peak_cell_samples": 0.97,
        "reference_vorticity_peak_cell_samples": 0.97,
        "reference_sampled_fd2": {"max_gradient_fd2": 0.95, "max_vorticity_fd2": 0.94},
        "computed": {"max_gradient_fd2": 0.949, "max_vorticity_fd2": 0.941},
    }

    row = row_from_diagnostics("n64-dt0.001", diagnostics)

    assert row["n"] == 64
    assert math.isclose(
        row["reference_exact_gradient_sample_fraction"],
        0.97 / (math.sqrt(65) / 8 * math.exp(-0.05)),
    )
    assert math.isclose(
        row["reference_fd2_gradient_fraction"],
        0.95 / (math.sqrt(65) / 8 * math.exp(-0.05)),
    )
    assert math.isclose(
        row["solver_fd2_gradient_fraction"],
        0.949 / (math.sqrt(65) / 8 * math.exp(-0.05)),
    )


def test_peak_decomposition_refuses_unproven_reference_frequency():
    diagnostics = {
        "parameters": {"n": 64, "dt": 0.001, "end": 0.05, "frequency": 8},
        "reference_gradient_peak_cell_samples": 0.97,
        "reference_vorticity_peak_cell_samples": 0.97,
        "reference_sampled_fd2": {"max_gradient_fd2": 0.95, "max_vorticity_fd2": 0.94},
        "computed": {"max_gradient_fd2": 0.949, "max_vorticity_fd2": 0.941},
    }

    try:
        row_from_diagnostics("n64-dt0.001", diagnostics)
    except ValueError as error:
        assert "N=4" in str(error)
    else:
        raise AssertionError("unsupported frequency must not be compared to the N=4 certificate")
