"""Independently replay archived Foundation 13 exact-control cases."""

import argparse
import hashlib
import json
import math
import tarfile
import tempfile
from pathlib import Path

from tools.analyze_openfoam import analyze
from tools.high_gradient_acceptance import standard_acceptance


METRICS = (
    "velocity_relative_l2",
    "pressure_relative_l2_gauge_invariant",
    "energy_relative_error_cell_samples",
    "shell_spectrum_relative_l1_error",
    "gradient_peak_relative_error_cell_samples",
    "vorticity_peak_relative_error_cell_samples",
)


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def observed_order(coarse, fine, ratio=2):
    if coarse <= 0 or fine <= 0 or ratio <= 1:
        raise ValueError("errors and refinement ratio must be positive")
    return math.log(coarse / fine) / math.log(ratio)


def verify(run_root, acceptance_protocol_path="protocols/high-gradient-of13-v2.json"):
    run_root = Path(run_root)
    manifest_path = run_root / "manifest.json"
    protocol_path = run_root / "protocol.json"
    manifest = json.loads(manifest_path.read_text())
    protocol = json.loads(protocol_path.read_text())
    if manifest.get("status") != "COMPLETE_WITH_DIAGNOSTICS":
        raise ValueError("run manifest is not complete")
    if sha256(protocol_path) != manifest.get("protocol_sha256"):
        raise ValueError("protocol hash does not match run manifest")
    acceptance_protocol_path = Path(acceptance_protocol_path)
    acceptance = json.loads(acceptance_protocol_path.read_text())["standard_acceptance"]
    tolerance = acceptance["outer_corrector_residual_absolute"]
    max_outer = acceptance["maximum_outer_correctors"]
    archived_rows = manifest["cases"]
    if len(archived_rows) != 6:
        raise ValueError("expected the frozen six-case matrix")

    verified_rows = []
    with tempfile.TemporaryDirectory(prefix="forced-periodic-openfoam-replay-") as temp:
        temp_root = Path(temp)
        for row in archived_rows:
            archive_path = run_root / row["archive"]
            archive_hash = sha256(archive_path)
            if archive_hash != row["archive_sha256"]:
                raise ValueError(f"archive digest mismatch: {row['name']}")
            case_parent = temp_root / row["name"]
            case_parent.mkdir()
            with tarfile.open(archive_path, "r:gz") as archive:
                members = archive.getmembers()
                if not members or any(Path(item.name).is_absolute() or ".." in Path(item.name).parts
                                      for item in members):
                    raise ValueError(f"unsafe or empty archive: {row['name']}")
                archive.extractall(case_parent, filter="data")
            case = case_parent / row["name"]
            exit_receipt = json.loads((case / "exit.json").read_text())
            params = json.loads((case / "parameters.json").read_text())
            if exit_receipt["exit_code"] != 0:
                raise ValueError(f"nonzero solver exit in {row['name']}")
            if exit_receipt["observed_time_steps"] != row["steps"]:
                raise ValueError(f"logged step count differs for {row['name']}")
            if params["n"] != row["n"] or params["dt"] != row["dt"] or params["end"] != row["end"]:
                raise ValueError(f"case inputs differ from run manifest for {row['name']}")

            replay = analyze(case)
            saved = row["diagnostics"]
            for metric in METRICS:
                if not math.isclose(replay[metric], saved[metric], rel_tol=0, abs_tol=1e-14):
                    raise ValueError(f"diagnostic replay mismatch for {row['name']}:{metric}")
            for name, expected_hash in replay["sha256"].items():
                if sha256(case / name) != expected_hash:
                    raise ValueError(f"field or input digest mismatch for {row['name']}:{name}")
            standard = standard_acceptance(
                (case / "log.foamRun").read_text(), row["end"], row["dt"], tolerance,
                max_outer, (case / "system/fvSolution").read_text(),
            )
            verified_rows.append({
                "name": row["name"], "group": row["group"], "n": row["n"],
                "dt": row["dt"], "expected_and_observed_steps": row["steps"],
                "archive_sha256": archive_hash,
                "diagnostics_replayed": True,
                "standard_acceptance_recheck": standard,
                "metrics": {key: replay[key] for key in METRICS},
            })

    spatial = sorted((item for item in verified_rows if item["group"] == "spatial"),
                     key=lambda item: item["n"])
    temporal = sorted((item for item in verified_rows if item["group"] == "temporal"),
                      key=lambda item: item["dt"], reverse=True)
    result = {
        "status": "ARCHIVE_AND_DIAGNOSTIC_REPLAY_PASS",
        "source_commit": manifest["source_commit"],
        "image_inspect": manifest["image_inspect"],
        "run_protocol_sha256": manifest["protocol_sha256"],
        "acceptance_recheck_source": str(acceptance_protocol_path),
        "acceptance_recheck_source_sha256": sha256(acceptance_protocol_path),
        "acceptance_recheck_scope": "Applied after execution from the repository's existing Foundation 13 standard gate; not a claim that this threshold was frozen in the archived v1 run protocol.",
        "cases": verified_rows,
        "spatial_velocity_observed_orders": [
            observed_order(spatial[i]["metrics"]["velocity_relative_l2"],
                           spatial[i + 1]["metrics"]["velocity_relative_l2"])
            for i in range(len(spatial) - 1)
        ],
        "spatial_pressure_observed_orders": [
            observed_order(spatial[i]["metrics"]["pressure_relative_l2_gauge_invariant"],
                           spatial[i + 1]["metrics"]["pressure_relative_l2_gauge_invariant"])
            for i in range(len(spatial) - 1)
        ],
        "temporal_velocity_total_error_differences": [
            abs(temporal[i]["metrics"]["velocity_relative_l2"]-
                temporal[i + 1]["metrics"]["velocity_relative_l2"])
            for i in range(len(temporal) - 1)
        ],
        "temporal_pressure_total_error_differences": [
            abs(temporal[i]["metrics"]["pressure_relative_l2_gauge_invariant"]-
                temporal[i + 1]["metrics"]["pressure_relative_l2_gauge_invariant"])
            for i in range(len(temporal) - 1)
        ],
        "temporal_convergence_assessment": "UNCERTAIN: total-error differences do not isolate the time-discretization error from the fixed-grid spatial floor; the matrix is a completed step-size comparison but not a resolved temporal-order estimate.",
        "limits": manifest["limitations"],
    }
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("run_root", help="directory containing manifest.json, protocol.json, and archives/")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    result = verify(args.run_root)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
    print(json.dumps({"status": result["status"], "output": str(output),
                      "cases": len(result["cases"]),
                      "spatial_velocity_observed_orders": result["spatial_velocity_observed_orders"],
                      "spatial_pressure_observed_orders": result["spatial_pressure_observed_orders"],
                      "temporal_convergence_assessment": result["temporal_convergence_assessment"]},
                     indent=2, allow_nan=False))
