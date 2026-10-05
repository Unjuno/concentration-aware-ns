"""Verify SU2 shared-MMS run archives and replay their postprocessor."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import tarfile
import tempfile

from tools.analyze_su2 import analyze
from tools.run_su2_high_gradient_study import case_pairs


REPLAY_ATOL = 1e-12


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def compare(saved, replayed, path="metrics"):
    if isinstance(saved, dict):
        if not isinstance(replayed, dict) or saved.keys() != replayed.keys():
            raise ValueError(f"replay structure mismatch at {path}")
        for key in saved:
            compare(saved[key], replayed[key], f"{path}.{key}")
    elif isinstance(saved, list):
        if not isinstance(replayed, list) or len(saved) != len(replayed):
            raise ValueError(f"replay list mismatch at {path}")
        for i, (a, b) in enumerate(zip(saved, replayed)):
            compare(a, b, f"{path}[{i}]")
    elif isinstance(saved, (int, float)) and not isinstance(saved, bool):
        if not isinstance(replayed, (int, float)) or abs(float(saved)-float(replayed)) > REPLAY_ATOL:
            raise ValueError(f"replay value mismatch at {path}: {saved!r} vs {replayed!r}")
    elif saved != replayed:
        raise ValueError(f"replay value mismatch at {path}: {saved!r} vs {replayed!r}")


def safe_extract_case(archive, label, destination):
    destination.mkdir()
    with tarfile.open(archive, "r:gz") as tar:
        for member in tar.getmembers():
            path = PurePosixPath(member.name)
            if not path.parts or path.parts[0] != label or len(path.parts) > 2:
                raise ValueError(f"unsafe or unexpected archive path: {member.name}")
            if member.issym() or member.islnk() or not (member.isdir() or member.isfile()):
                raise ValueError(f"unexpected archive member type: {member.name}")
            if member.isdir():
                continue
            if len(path.parts) != 2:
                raise ValueError(f"unexpected nested case member: {member.name}")
            stream = tar.extractfile(member)
            if stream is None:
                raise ValueError(f"unreadable archive member: {member.name}")
            (destination / path.parts[1]).write_bytes(stream.read())


def review(root, reference_patch="runtime/su2/high_gradient.patch"):
    root = Path(root)
    summary = json.loads((root / "summary.json").read_text())
    protocol_path = root / "protocol.json"
    protocol = json.loads(protocol_path.read_text())
    protocol_hash = sha256(protocol_path)
    if protocol_hash != summary["protocol_sha256"]:
        raise ValueError("run summary protocol hash mismatch")
    if sha256(root / "high_gradient.patch") != sha256(reference_patch):
        raise ValueError("run adapter patch differs from the checked-in source")
    expected = case_pairs(protocol)
    expected_by_label = {f"n{n}-dt{dt:g}": (n, dt) for n, dt in expected}
    if len(expected) != protocol["cases"]["expected_cases"]:
        raise ValueError("protocol unique-case count is inconsistent")
    if summary["expected_cases"] != len(expected):
        raise ValueError("summary expected-case count mismatch")
    rows = []
    for item in summary["cases"]:
        label = item["case"]
        if label not in expected_by_label or item["case"] in {r["case"] for r in rows}:
            raise ValueError(f"unexpected or repeated case: {label}")
        n, dt = expected_by_label[label]
        if item["n"] != n or abs(item["dt"]-dt) > 1e-15:
            raise ValueError(f"protocol case parameters mismatch: {label}")
        archive = root / f"{label}.tar.gz"
        archive_hash = sha256(archive)
        if archive_hash != item["archive_sha256"]:
            raise ValueError(f"archive hash mismatch: {label}")
        with tempfile.TemporaryDirectory(prefix="su2-shared-replay-") as temp:
            case = Path(temp) / label
            safe_extract_case(archive, label, case)
            if (case / "exit_code").read_text().strip() != str(item["exit_code"]):
                raise ValueError(f"exit-code copy mismatch: {label}")
            parameters = json.loads((case / "parameters.json").read_text())
            if parameters.get("image_id") != summary["image_id"]:
                raise ValueError(f"image identity mismatch: {label}")
            if parameters.get("protocol_sha256") != protocol_hash:
                raise ValueError(f"case protocol hash mismatch: {label}")
            if item["exit_code"] != 0:
                rows.append({"case": label, "archive_sha256": archive_hash,
                             "replay_status": "NOT_RUN_NONZERO_EXIT",
                             "standard_acceptance": item["standard_acceptance"],
                             "quality_sampled": None})
                continue
            if "Exit Success (SU2_CFD)" not in (case / "solver.log").read_text():
                raise ValueError(f"SU2 success marker missing: {label}")
            saved = json.loads((case / "diagnostics.json").read_text())
            for name, digest in saved["sha256"].items():
                if sha256(case / name) != digest:
                    raise ValueError(f"case input/output digest mismatch: {label}/{name}")
            replayed = analyze(case)
            compare(saved, replayed)
            compare(item["metrics"], saved, f"summary.{label}.metrics")
            steps = round(protocol["time"]["end"] / dt)
            standard = "PASS" if (saved["steps"] == steps and saved["converged_steps"] == steps) else "FAIL"
            if item["planned_steps"] != steps or item["standard_acceptance"] != standard:
                raise ValueError(f"standard-gate summary mismatch: {label}")
            if item["quality_sampled"] != saved["quality_sampled"]:
                raise ValueError(f"sampled-quality summary mismatch: {label}")
            rows.append({"case": label, "archive_sha256": archive_hash,
                         "replay_status": "PASS", "standard_acceptance": standard,
                         "quality_sampled": saved["quality_sampled"],
                         "updated_solution_time": saved["updated_solution_time"],
                         "expected_last_source_time": saved["expected_last_source_time"],
                         "reported_history_time": saved["reported_history_time"],
                         "quality_metric_errors": saved["quality_metric_errors"]})
    if len(rows) != summary["attempted_cases"]:
        raise ValueError("attempted-case count does not match summary")
    missing = sorted(set(expected_by_label)-{row["case"] for row in rows})
    return {"study_id": summary["study_id"], "run_status": summary["status"],
            "protocol_sha256": protocol_hash, "image_id": summary["image_id"],
            "expected_cases": summary["expected_cases"], "attempted_cases": len(rows),
            "reviewed_cases": sum(row["replay_status"] == "PASS" for row in rows),
            "missing_cases": missing, "replay_atol": REPLAY_ATOL, "cases": rows,
            "scope": "Archive integrity and rerun of the pinned postprocessor; not an independent solver implementation or continuum-extrema certificate."}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--output", default="evidence/tests/su2-shared-high-gradient-replay.json")
    args = parser.parse_args()
    result = review(args.root)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
