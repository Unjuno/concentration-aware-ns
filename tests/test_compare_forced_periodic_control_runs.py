import math

from tools.compare_forced_periodic_control_runs import compare


METRICS = [
    "velocity_relative_l2", "pressure_relative_l2_gauge_invariant",
    "energy_relative_error_cell_samples", "shell_spectrum_relative_l1_error",
    "gradient_peak_relative_error_cell_samples", "vorticity_peak_relative_error_cell_samples",
]


def metric_values(velocity=0.01):
    return {metric: velocity for metric in METRICS}


def replay(image, cases):
    return {
        "status": "ARCHIVE_AND_DIAGNOSTIC_REPLAY_PASS",
        "source_commit": "commit-a",
        "image_inspect": f"{image} linux/arm64",
        "run_protocol_sha256": "protocol-hash",
        "cases": [
            {"name": name, "metrics": metrics, "archive_sha256": archive,
             "standard_acceptance_recheck": {"status": "PASS"}}
            for name, metrics, archive in cases
        ],
        "spatial_velocity_observed_orders": [2.0],
        "spatial_pressure_observed_orders": [2.0],
    }


def test_compares_replayed_metric_values_separately_from_archive_and_image_identity():
    old = replay("image-old", [("case", metric_values(), "archive-old")])
    new = replay("image-new", [("case", metric_values(), "archive-new")])

    result = compare(old, new)

    assert result["all_metric_values_exactly_equal"] is True
    assert result["all_archive_hashes_equal"] is False
    assert result["image_ids_differ"] is True
    assert result["case_count"] == 1
    assert result["maximum_absolute_metric_difference"] == 0.0


def test_refuses_to_call_metric_replays_equal_when_one_value_changes():
    old = replay("image-old", [("case", metric_values(0.01), "archive-old")])
    new = replay("image-new", [("case", metric_values(0.0100000001), "archive-new")])

    result = compare(old, new)

    assert result["all_metric_values_exactly_equal"] is False
    assert math.isclose(result["maximum_absolute_metric_difference"], 1e-10, rel_tol=1e-8)
