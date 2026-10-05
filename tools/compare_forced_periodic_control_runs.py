"""Compare independently replayed forced-periodic control matrices."""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

METRICS = (
    "velocity_relative_l2",
    "pressure_relative_l2_gauge_invariant",
    "energy_relative_error_cell_samples",
    "shell_spectrum_relative_l1_error",
    "gradient_peak_relative_error_cell_samples",
    "vorticity_peak_relative_error_cell_samples",
)


def compare(old: dict, new: dict) -> dict:
    for label, result in (("old", old), ("new", new)):
        if result.get("status") != "ARCHIVE_AND_DIAGNOSTIC_REPLAY_PASS":
            raise ValueError(f"{label} replay did not pass archive and diagnostic checks")
    if old.get("run_protocol_sha256") != new.get("run_protocol_sha256"):
        raise ValueError("run protocol hashes differ")

    old_cases = {row["name"]: row for row in old["cases"]}
    new_cases = {row["name"]: row for row in new["cases"]}
    if len(old_cases) != len(old["cases"]) or len(new_cases) != len(new["cases"]):
        raise ValueError("duplicate case name in a replay")
    if set(old_cases) != set(new_cases):
        raise ValueError("run matrices do not contain the same cases")

    rows = []
    differences = []
    exact = True
    for name in sorted(old_cases):
        left, right = old_cases[name], new_cases[name]
        metrics = {}
        if set(left["metrics"]) != set(right["metrics"]):
            raise ValueError(f"metric sets differ for {name}")
        for metric in METRICS:
            a, b = left["metrics"][metric], right["metrics"][metric]
            if not (math.isfinite(a) and math.isfinite(b)):
                raise ValueError(f"nonfinite metric in {name}:{metric}")
            delta = abs(a - b)
            metrics[metric] = {"old": a, "new": b, "absolute_difference": delta,
                               "exactly_equal": a == b}
            differences.append(delta)
            exact = exact and a == b
        rows.append({
            "case": name,
            "old_archive_sha256": left.get("archive_sha256"),
            "new_archive_sha256": right.get("archive_sha256"),
            "archive_hash_equal": left.get("archive_sha256") == right.get("archive_sha256"),
            "all_metrics_exactly_equal": all(v["exactly_equal"] for v in metrics.values()),
            "metrics": metrics,
        })

    old_image = old.get("image_inspect", "").split()[0]
    new_image = new.get("image_inspect", "").split()[0]
    old_acceptance = {
        row["name"]: row["standard_acceptance_recheck"]["status"] for row in old["cases"]
    }
    new_acceptance = {
        row["name"]: row["standard_acceptance_recheck"]["status"] for row in new["cases"]
    }
    return {
        "schema": "forced-periodic-control-run-comparison/v1",
        "same_protocol": True,
        "protocol_sha256": old["run_protocol_sha256"],
        "old_source_commit": old.get("source_commit"),
        "new_source_commit": new.get("source_commit"),
        "old_image_id": old_image,
        "new_image_id": new_image,
        "image_ids_differ": old_image != new_image,
        "case_count": len(rows),
        "all_metric_values_exactly_equal": exact,
        "maximum_absolute_metric_difference": max(differences, default=0.0),
        "all_archive_hashes_equal": all(row["archive_hash_equal"] for row in rows),
        "standard_recheck_statuses_equal": old_acceptance == new_acceptance,
        "standard_recheck_statuses": new_acceptance,
        "old_spatial_velocity_observed_orders": old.get("spatial_velocity_observed_orders"),
        "new_spatial_velocity_observed_orders": new.get("spatial_velocity_observed_orders"),
        "old_spatial_pressure_observed_orders": old.get("spatial_pressure_observed_orders"),
        "new_spatial_pressure_observed_orders": new.get("spatial_pressure_observed_orders"),
        "cases": rows,
        "interpretation": (
            "Exact equality means equality of the six replayed scalar diagnostics, not identity "
            "of raw archives or proof that the solver field's continuous extrema are bounded."
        ),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("old_replay", type=Path)
    parser.add_argument("new_replay", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = compare(json.loads(args.old_replay.read_text()), json.loads(args.new_replay.read_text()))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
    print(json.dumps({k: result[k] for k in (
        "schema", "case_count", "all_metric_values_exactly_equal",
        "maximum_absolute_metric_difference", "image_ids_differ", "all_archive_hashes_equal",
    )}, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
