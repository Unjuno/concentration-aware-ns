"""Compare the frozen n=64 high-gradient endpoint triplet across temporal steps."""
import hashlib
import json
import math
from pathlib import Path, PurePosixPath
import tarfile
import tempfile

import numpy as np

from tools.analyze_openfoam import vectors
from tools.archive_high_gradient_openfoam import completion_check
from tools.high_gradient_reference import fields


CASES = [
    ("n64-dt0.001", Path("evidence/of13-high-gradient-v2/n64-dt0.001.tar.gz")),
    ("n64-dt0.0005", Path("evidence/of13-high-gradient-v2-temporal-addendum/n64-dt0.0005.tar.gz")),
    ("n64-dt0.00025", Path("evidence/of13-high-gradient-v2-temporal-addendum/n64-dt0.00025.tar.gz")),
]
CURRENT = Path("evidence/of13-high-gradient-v2/manifest-current-2026-09-30.json")


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def extract_case_archive(archive_path, destination, case_name):
    """Safely extract one frozen case archive into a fresh parent directory."""
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=True)
    if any(destination.iterdir()):
        raise ValueError(f"case archive destination is not empty: {destination}")
    with tarfile.open(archive_path, "r:gz") as archive:
        members = archive.getmembers()
        if not members:
            raise ValueError(f"empty case archive: {archive_path}")
        seen = set()
        for member in members:
            path = PurePosixPath(member.name)
            if (path.is_absolute() or ".." in path.parts or not path.parts
                    or path.parts[0] != case_name or member.name in seen):
                raise ValueError(f"unsafe or unexpected archive member: {member.name}")
            seen.add(member.name)
        archive.extractall(destination, members=members, filter="data")
    case = destination / case_name
    if not case.is_dir():
        raise ValueError(f"case directory is missing from archive: {case_name}")
    return case


def compare():
    status = json.loads(CURRENT.read_text())
    listed = {row["case"]: row for row in status["completed_cases"]}
    if not all(name in listed for name, _ in CASES):
        raise ValueError("current cross-run manifest does not list all three temporal cases")
    arrays, centers, errors, records, static_inputs = [], [], [], [], []
    with tempfile.TemporaryDirectory(prefix="cans-of13-temporal-") as temporary:
        for index, (name, archive_path) in enumerate(CASES):
            row = listed[name]
            archive_path = Path(archive_path)
            if sha256(archive_path) != row["archive_sha256"]:
                raise ValueError(f"archive hash mismatch: {name}")
            case = extract_case_archive(
                archive_path, Path(temporary) / f"case-{index}", name
            )
            result = completion_check(case, 0.05)
            if result is None or result["diagnostics"]["standard_acceptance"]["status"] != "PASS":
                raise ValueError(f"case is not complete and standard-accepted: {name}")
            expected_log = row.get("source_log_sha256", row.get("log_sha256"))
            if expected_log and result["log_sha256"] != expected_log:
                raise ValueError(f"source log hash mismatch: {name}")
            params = result["diagnostics"]["parameters"]
            if (params["n"], params["end"], params["nu"], params["profile"], params["frequency"]) != (64, 0.05, 0.01, "high-gradient", 4):
                raise ValueError(f"incompatible manufactured-solution case: {name}")
            u = vectors(case / "0.05/U", 64**3)
            c = vectors(case / "0.05/C", 64**3)
            ref = fields(c, N=4, nu=0.01, time=0.05)["u"]
            arrays.append(u)
            centers.append(c)
            errors.append(float(np.linalg.norm(u - ref) / np.linalg.norm(ref)))
            input_hashes = json.loads((case / "input-hashes.json").read_text())
            static_inputs.append({key: value for key, value in input_hashes.items()
                                  if key not in {"parameters.json", "system/controlDict"}})
            records.append({
                "case": name,
                "dt": params["dt"],
                "archive_sha256": row["archive_sha256"],
                "source_log_sha256": result["log_sha256"],
                "steps": result["time_steps"],
                "converged_steps": result["converged_steps"],
                "standard_acceptance": result["diagnostics"]["standard_acceptance"]["status"],
                "local_quality": result["diagnostics"].get("local_quality", {}).get("status", "UNCERTAIN"),
                "velocity_error_to_exact": errors[-1],
            })
    if not (np.array_equal(centers[0], centers[1]) and np.array_equal(centers[1], centers[2])):
        raise ValueError("cell-center correspondence differs across temporal cases")
    if not (static_inputs[0] == static_inputs[1] == static_inputs[2]):
        raise ValueError("non-time input hashes differ across cases")
    d01 = float(np.linalg.norm(arrays[0] - arrays[1]) / np.linalg.norm(arrays[2]))
    d12 = float(np.linalg.norm(arrays[1] - arrays[2]) / np.linalg.norm(arrays[2]))
    order = math.log2(d01 / d12) if d01 > 0 and d12 > 0 else None
    e01 = math.log2(errors[0] / errors[1]) if errors[0] > 0 and errors[1] > 0 else None
    e12 = math.log2(errors[1] / errors[2]) if errors[1] > 0 and errors[2] > 0 else None
    from tools.high_gradient_acceptance import matrix_reproduction
    base_manifest = json.loads(Path("evidence/of13-high-gradient-v2/manifest.json").read_text())
    base_cases = []
    for row in base_manifest["completed_cases"]:
        n = int(row["case"].split("-")[0][1:])
        current_row = listed.get(row["case"])
        if (current_row is None
                or current_row["archive_sha256"] != row["archive_sha256"]
                or current_row["standard_acceptance"] != row["standard_acceptance"]
                or current_row["local_quality"] != row["local_quality"]):
            raise ValueError(f"base and current manifest disagree: {row['case']}")
        base_cases.append({
            "parameters": {"n": n, "dt": 0.001},
            "standard_acceptance": {"status": row["standard_acceptance"]},
            "local_quality": {"status": row["local_quality"]},
        })
    matrix = matrix_reproduction(base_cases)
    return {
        "cases": records,
        "relative_endpoint_differences_normalized_by_finest": [d01, d12],
        "observed_order_of_endpoint_differences": order,
        "observed_orders_of_exact_velocity_error": [e01, e12],
        "static_input_hashes_match": True,
        "cell_centers_match_exactly": True,
        "temporal_error_certified": False,
        "matrix_reproduction": matrix,
        "scope": "Fixed n=64 endpoint comparison with exact MMS reference. Orders are descriptive; a three-point finite-resolution trend is not an asymptotic temporal error certificate or a solver defect claim.",
    }


def main():
    result = compare()
    output = Path("evidence/tests/high-gradient-of13-v2-temporal-comparison-2026-09-30.json")
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
