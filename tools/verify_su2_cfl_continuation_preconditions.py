"""Replay and bind the completed baseline before a same-image control resume."""

import argparse
import csv
import hashlib
import json
import math
from pathlib import Path

from tools.analyze_su2 import analyze
from tools.run_su2_full_horizon_cfl_pair import verify_history


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def verify(protocol_path, baseline_root):
    protocol_path = Path(protocol_path)
    baseline_root = Path(baseline_root)
    protocol = json.loads(protocol_path.read_text())
    baseline = protocol["baseline_evidence"]
    frozen_checks = (
        (baseline["root"] + "/manifest.json", baseline["manifest_sha256"]),
        (baseline["root"] + "/successor-receipt.json", baseline["successor_receipt_sha256"]),
        (protocol["input_protocol"], protocol["input_protocol_sha256"]),
        (protocol["quality_protocol"], protocol["quality_protocol_sha256"]),
        *protocol["runtime"]["recipe_sha256"].items(),
    )
    for relative_path, expected in frozen_checks:
        if sha256(relative_path) != expected:
            raise ValueError(f"frozen continuation input changed: {relative_path}")

    manifest_path = baseline_root / "manifest.json"
    if sha256(manifest_path) != baseline["manifest_sha256"]:
        raise ValueError("baseline run manifest digest mismatch")
    manifest = json.loads(manifest_path.read_text())
    if (manifest.get("status") != "INCOMPLETE"
            or manifest.get("completed_cases") != 1
            or manifest.get("expected_cases") != 2
            or [row.get("case") for row in manifest.get("cases", [])] != ["baseline"]
            or manifest.get("preflight_status") != "SUCCESSOR_ACTUAL_PROBE_VERIFIED"):
        raise ValueError("predecessor artifact does not contain exactly one verified baseline")
    row = manifest["cases"][0]
    if row.get("steps") != 50:
        raise ValueError("completed baseline does not record the frozen 50 updates")

    receipt_path = baseline_root / "successor-receipt.json"
    receipt = json.loads(receipt_path.read_text())
    if sha256(receipt_path) != baseline["successor_receipt_sha256"]:
        raise ValueError("baseline successor-receipt digest mismatch")
    if receipt.get("image_id") != protocol["runtime"]["expected_image_id"]:
        raise ValueError("baseline image differs from the continuation's frozen image")
    if receipt.get("source_commit") != protocol["runtime"]["source_commit"]:
        raise ValueError("baseline source commit differs from the continuation protocol")

    case = baseline_root / "baseline"
    params = json.loads((case / "parameters.json").read_text())
    if (params.get("image_id") != receipt["image_id"]
            or params.get("CFL_NUMBER") != 10
            or params.get("n") != 32
            or params.get("dt") != 0.001
            or params.get("end") != 0.05):
        raise ValueError("baseline case parameters do not match the frozen predecessor")
    if (case / "exit_code").read_text().strip() != "0":
        raise ValueError("baseline solver did not exit zero")
    with (case / "history.csv").open() as stream:
        history = [{k.strip().strip('"'): v for k, v in item.items()}
                   for item in csv.DictReader(stream)]
    clock = verify_history(history)
    saved_diagnostics = json.loads((case / "diagnostics.json").read_text())
    replay = analyze(case)
    if saved_diagnostics.get("steps") != 50 or saved_diagnostics.get("converged_steps") != row.get("converged_steps"):
        raise ValueError("baseline diagnostics differ from the run manifest")
    for name, expected_hash in saved_diagnostics["sha256"].items():
        if sha256(case / name) != expected_hash or replay["sha256"].get(name) != expected_hash:
            raise ValueError(f"baseline raw output replay mismatch: {name}")
    for key in ("velocity_relative_l2", "gradient_peak_relative_error_samples",
                "vorticity_peak_relative_error_samples"):
        if not math.isclose(replay[key], saved_diagnostics[key], rel_tol=0, abs_tol=1e-14):
            raise ValueError(f"baseline diagnostic replay mismatch: {key}")

    return {
        "status": "BASELINE_ARCHIVE_AND_DIAGNOSTIC_REPLAY_PASS",
        "baseline_image_id": receipt["image_id"],
        "baseline_exit_code": 0,
        "physical_updates": clock["steps"],
        "residual_converged_steps": saved_diagnostics["converged_steps"],
        "baseline_quality": saved_diagnostics["quality"],
        "baseline_relative_errors": {
            key: saved_diagnostics[key]
            for key in ("velocity_relative_l2", "gradient_peak_relative_error_samples",
                        "vorticity_peak_relative_error_samples")
        },
        "receipt_sha256": sha256(receipt_path),
        "scope": "Baseline identity and diagnostics replay only; does not validate or pair the not-yet-run control.",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--protocol", type=Path, required=True)
    parser.add_argument("--baseline-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError("preserve previous baseline verification")
    result = verify(args.protocol, args.baseline_root)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
