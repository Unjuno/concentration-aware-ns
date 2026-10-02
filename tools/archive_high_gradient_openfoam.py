"""Preserve the frozen OpenFOAM high-gradient campaign, including partial runs."""
import hashlib
import argparse
import io
import json
import math
import shutil
import tarfile
from datetime import datetime, timezone
from pathlib import Path


WORK = Path("work/of13-high-gradient-v2")
EVIDENCE = Path("evidence/of13-high-gradient-v2")
REQUIRED_CASES = (
    "n16-dt0.001",
    "n32-dt0.001",
    "n64-dt0.001",
    "n64-dt0.0005",
    "n64-dt0.00025",
)
EXTRA_CASES = ("n128-dt0.001",)
AMR_CASES = ("amr-cap4096", "amr-cap5000", "amr-cap100000")


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def inspect_case(name):
    case = WORK / name
    if not case.is_dir():
        return {"case": name, "status": "NOT_STARTED", "files": []}

    files = sorted(path for path in case.rglob("*") if path.is_file())
    file_hashes = [
        {"path": str(path.relative_to(case)), "sha256": sha256(path)}
        for path in files
    ]
    params_path = case / "parameters.json"
    params = json.loads(params_path.read_text()) if params_path.exists() else {}
    log_path = case / "log.foamRun"
    log_ends_normally = log_path.exists() and log_path.read_text().rstrip().endswith("End")
    exit_path = case / "exit.json"
    exit_code = json.loads(exit_path.read_text()).get("exit_code") if exit_path.exists() else None
    end_time = params.get("end")
    has_end_output = bool(
        end_time is not None
        and any(
            folder.is_dir()
            and _numeric_name_equals(folder.name, end_time)
            and (folder / "U").is_file()
            for folder in case.iterdir()
        )
    )
    complete = (
        exit_code == 0
        and log_ends_normally
        and has_end_output
        and (case / "diagnostics.json").is_file()
    )
    return {
        "case": name,
        "status": "COMPLETE" if complete else "INCOMPLETE",
        "exit_code": exit_code,
        "log_ends_normally": bool(log_ends_normally),
        "end_time_output_present": has_end_output,
        "diagnostics_present": (case / "diagnostics.json").is_file(),
        "files": file_hashes,
    }


def _numeric_name_equals(name, expected):
    try:
        return math.isclose(float(name), float(expected), rel_tol=0, abs_tol=1e-12)
    except ValueError:
        return False


def archive_case(name):
    case = WORK / name
    destination = EVIDENCE / f"{name}.tar.gz"
    if destination.exists():
        raise FileExistsError(f"refusing to replace preserved evidence: {destination}")
    selected = _review_archive_paths(case)
    with tarfile.open(destination, "w:gz") as archive:
        for path in selected:
            arcname = str(Path(name) / path.relative_to(case))
            if path.name == "command.json":
                payload = json.dumps(_redact_host_mount(path), indent=2).encode() + b"\n"
                info = tarfile.TarInfo(arcname)
                info.size = len(payload)
                archive.addfile(info, io.BytesIO(payload))
            else:
                archive.add(path, arcname=arcname)
    return {"sha256": sha256(destination),
            "paths": [str(path.relative_to(case)) for path in selected],
            "sanitized_paths": ["command.json"] if any(p.name == "command.json" for p in selected) else []}


def _redact_host_mount(path):
    command = json.loads(Path(path).read_text())
    for index, argument in enumerate(command):
        if isinstance(argument, str) and argument.endswith(":/case") and "/" in argument:
            command[index] = "<HOST_CASE_DIR>:/case"
    return command


def _review_archive_paths(case):
    """Select inputs, logs, and fields needed to audit/replay reported metrics.

    The complete ignored work directory remains untouched. Generated mesh and
    redundant cell-centre component fields are reproducible from blockMeshDict;
    their raw hashes remain in the manifest/input-hashes file.
    """
    name = Path(case).name
    fixed = [
        case / "command.json", case / "input-hashes.json", case / "parameters.json",
        case / "log.blockMesh", case / "log.container", case / "log.foamRun",
        case / "0/U", case / "0/p",
        case / "system/blockMeshDict", case / "system/controlDict",
        case / "system/fvSchemes", case / "system/fvSolution",
        case / "constant/fvModels", case / "constant/momentumTransport",
        case / "constant/physicalProperties",
        case / "dynamicCode/mmsForce/codedFvModelTemplate.C",
        case / "dynamicCode/mmsForce/codedFvModelTemplate.H",
    ]
    if name in AMR_CASES:
        fixed.append(case / "constant/dynamicMeshDict")
    optional = [case / "diagnostics.json", case / "exit.json", case / "log.centres"]
    if name in AMR_CASES:
        optional.extend((case / "log.volumes", case / "log.gradient"))
    params = json.loads((case / "parameters.json").read_text())
    output = next((path for path in case.iterdir()
                   if path.is_dir() and _numeric_name_equals(path.name, params["end"])), None)
    if output is not None:
        optional.extend(output / field for field in ("C", "U", "p"))
        if name in AMR_CASES:
            optional.extend(output / field for field in ("Vc", "grad(U)", "cellLevel"))
        time_state = output / "uniform/time"
        optional.append(time_state)
    missing = [path for path in fixed if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"required review archive inputs missing: {missing}")
    return fixed + [path for path in optional if path.is_file()]


def repack_existing_campaign():
    """Replace bulky full-case tarballs with hashed, audit-focused tarballs.

    The original tarballs and manifest are moved into the ignored work tree
    before any replacement. Their hashes remain recorded in the new manifest.
    """
    manifest_path = EVIDENCE / "matrix-manifest.json"
    manifest = json.loads(manifest_path.read_text())
    manifest["last_repacked_utc"] = datetime.now(timezone.utc).isoformat()
    manifest["container_liveness"] = {
        "observed_utc": datetime.now(timezone.utc).isoformat(),
        "host_solver_process": "NOT_OBSERVED",
        "container_daemon_state": "UNVERIFIED",
        "method": "host process-list scan only; no successful Docker/OrbStack inspect was available",
    }
    originals = WORK / "preserved-review-archives"
    originals.mkdir(parents=True, exist_ok=True)
    shutil.copy2(manifest_path, originals / "matrix-manifest-before-redaction.json")
    for row in manifest["cases"]:
        if row["status"] == "NOT_STARTED":
            continue
        name = row["case"]
        old = EVIDENCE / f"{name}.tar.gz"
        if sha256(old) != row["archive_sha256"]:
            raise ValueError(f"existing archive hash mismatch: {old}")
        original_sha = row["archive_sha256"]
        preserved = originals / old.name
        if preserved.exists():
            raise FileExistsError(f"refusing to replace preserved archive: {preserved}")
        old.rename(preserved)
        archive_info = archive_case(name)
        row["superseded_review_archive_sha256"] = original_sha
        row["archive_sha256"] = archive_info["sha256"]
        row["archive_paths"] = archive_info["paths"]
        row["archive_sanitized_paths"] = archive_info["sanitized_paths"]
        row["archive_scope"] = "inputs-logs-diagnostics-and-end-time-U-p-C"
    manifest["notes"] = [
        "Review tarballs preserve original conditions/settings, generated force source, logs, diagnostics when available, and end-time U/p/C when available.",
        "Per-file hashes describe the full ignored case tree, including omitted derived output and generated mesh.",
        "Generated mesh and redundant cell-centre component fields are excluded from tarballs; blockMeshDict and input hashes record the reproducible geometry.",
        "command.json redacts the user-specific host mount path; the original file hash remains in the full case-tree hashes.",
        "Original full-case tarballs remain in the ignored work tree; their hashes are recorded per case.",
        "Archives preserve both complete and partial work; an archive is not a PASS.",
        "AMR is required by the frozen protocol and has not been run in this matrix.",
        "The n64-dt0.00025 temporal case is required and remains NOT_STARTED.",
    ]
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    return manifest


def archive_campaign():
    run_environment = WORK / "run-environment.json"
    if not run_environment.is_file():
        raise FileNotFoundError(run_environment)
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    environment_copy = EVIDENCE / "run-environment.json"
    if environment_copy.exists() and environment_copy.read_bytes() != run_environment.read_bytes():
        raise FileExistsError(f"run environment evidence differs: {environment_copy}")
    environment_copy.write_bytes(run_environment.read_bytes())

    names = (*REQUIRED_CASES, *EXTRA_CASES)
    rows = [inspect_case(name) for name in names]
    for row in rows:
        case = WORK / row["case"]
        if case.is_dir():
            archive_info = archive_case(row["case"])
            row["archive_sha256"] = archive_info["sha256"]
            row["archive_paths"] = archive_info["paths"]
            row["archive_sanitized_paths"] = archive_info["sanitized_paths"]

    required_complete = all(
        next(row for row in rows if row["case"] == name)["status"] == "COMPLETE"
        for name in REQUIRED_CASES
    )
    manifest = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "protocol": "protocols/high-gradient-of13-v1.json",
        "required_cases": list(REQUIRED_CASES),
        "additional_cases": list(EXTRA_CASES),
        "amr_required_by_protocol": True,
        "amr_status": "NOT_STARTED",
        "run_environment_sha256": sha256(environment_copy),
        "cases": rows,
        "campaign_status": "INCOMPLETE" if not required_complete else "UNASSESSED_AMR_REQUIRED",
        "quality_verdict": "UNCERTAIN",
        "notes": [
            "Archives preserve both complete and partial work; an archive is not a PASS.",
            "Per-file hashes describe the full ignored case tree; review tarballs contain required inputs, logs and U/p/C outputs.",
            "command.json redacts the user-specific host mount path; the original file hash remains in the full case-tree hashes.",
            "Generated mesh and redundant cell-centre component fields are excluded from tarballs and remain hash-recorded; blockMeshDict regenerates the mesh.",
            "AMR is required by the frozen protocol and has not been run in this matrix.",
            "The n64-dt0.00025 temporal case is a required case and remains NOT_STARTED when absent.",
        ],
    }
    manifest_path = EVIDENCE / "matrix-manifest.json"
    if manifest_path.exists():
        raise FileExistsError(f"refusing to replace preserved manifest: {manifest_path}")
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    return manifest


def append_case_to_manifest(name, replaces=None):
    """Append one preserved rerun/AMR case without replacing earlier evidence."""
    manifest_path = EVIDENCE / "matrix-manifest.json"
    manifest = json.loads(manifest_path.read_text())
    if any(row["case"] == name for row in manifest["cases"]):
        raise FileExistsError(f"case already recorded in manifest: {name}")
    row = inspect_case(name)
    if row["status"] == "NOT_STARTED":
        raise FileNotFoundError(WORK / name)
    archive_info = archive_case(name)
    row.update(
        archive_sha256=archive_info["sha256"],
        archive_paths=archive_info["paths"],
        archive_sanitized_paths=archive_info["sanitized_paths"],
        archive_scope=(
            "inputs-logs-diagnostics-and-end-time-U-p-C-Vc-gradU-cellLevel"
            if name in AMR_CASES else "inputs-logs-diagnostics-and-end-time-U-p-C"
        ),
    )
    if replaces:
        row["replaces_incomplete_attempt"] = replaces
    manifest["cases"].append(row)
    if name not in manifest["additional_cases"]:
        manifest["additional_cases"].append(name)
    if name in AMR_CASES:
        manifest["notes"] = [
            note for note in manifest.get("notes", [])
            if "AMR is required by the frozen protocol and has not been run" not in note
        ]
    manifest.setdefault("notes", []).append(
        f"Additional case {name} was appended without replacing earlier evidence."
    )
    required_complete = all(
        any(
            case["status"] == "COMPLETE"
            and (case["case"] == required
                 or case.get("replaces_incomplete_attempt") == required)
            for case in manifest["cases"]
        )
        for required in REQUIRED_CASES
    )
    amr_complete = all(
        any(case["case"] == amr_case and case["status"] == "COMPLETE"
            for case in manifest["cases"])
        for amr_case in AMR_CASES
    )
    if any(row["case"] in AMR_CASES for row in manifest["cases"]):
        manifest["amr_status"] = "COMPLETE" if amr_complete else "INCOMPLETE"
    manifest["campaign_status"] = (
        "INCOMPLETE" if not required_complete or not amr_complete
        else "UNASSESSED_QUALITY"
    )
    manifest["quality_verdict"] = "UNCERTAIN"
    manifest["container_liveness"] = {
        "observed_utc": datetime.now(timezone.utc).isoformat(),
        "host_solver_process": "NOT_OBSERVED",
        "container_daemon_state": "RESPONSIVE_NO_NAMED_CASE_CONTAINERS",
        "method": "docker context orbstack; docker ps -a and inspect for five temporal/AMR names succeeded",
    }
    manifest["last_updated_utc"] = datetime.now(timezone.utc).isoformat()
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    return row


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--repack-existing", action="store_true",
                        help="preserve old full-case tarballs locally and repack evidence")
    parser.add_argument("--append-case",
                        help="append an additional completed or partial case to an existing manifest")
    parser.add_argument("--replaces",
                        help="required-case name whose incomplete attempt this rerun replaces")
    args = parser.parse_args()
    if args.append_case:
        result = append_case_to_manifest(args.append_case, args.replaces)
    else:
        result = repack_existing_campaign() if args.repack_existing else archive_campaign()
    print(json.dumps(result, indent=2))
