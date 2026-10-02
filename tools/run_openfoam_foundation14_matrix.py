"""Run the frozen Foundation 14 five-case successor matrix serially."""
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tarfile
from pathlib import Path

from tools.analyze_openfoam import analyze
from tools.openfoam_case import generate


ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "protocols/high-gradient-of14-v1.json"
IMAGE = "concentration-aware-ns:of14-20260724"
IMAGE_ID = "sha256:13a8802edab29a093c62ab90f063b823536e18985d52c91ab58212a4ac31447d"
BASELINE = ROOT / "evidence/of14-high-gradient-v1/n64-dt0.001.tar.gz"
MAX_ARCHIVE_PART_BYTES = 80_000_000


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def run_checked(command, timeout=10):
    return subprocess.run(command, capture_output=True, text=True, check=True, timeout=timeout)


def expected_cases(spec):
    spatial = spec["spatial_matrix"]
    temporal = spec["temporal_matrix"]
    pairs = [(n, spatial["delta_t"]) for n in spatial["cell_counts"]]
    pairs.extend((temporal["cell_count"], dt) for dt in temporal["delta_t"]
                 if (temporal["cell_count"], dt) not in pairs)
    return [f"n{n}-dt{dt:g}" for n, dt in pairs]


def complete_case(case, end_time):
    required = [case / "exit.json", case / "log.foamRun", case / "diagnostics.json"]
    if not all(path.is_file() for path in required):
        return False
    exit_record = json.loads(required[0].read_text())
    diagnostics = json.loads(required[2].read_text())
    dt = diagnostics.get("parameters", {}).get("dt")
    if not isinstance(dt, (int, float)) or dt <= 0:
        return False
    log = required[1].read_text(errors="replace")
    steps = len(re.findall(r"^Time = ", log, re.MULTILINE))
    endpoint = f"{end_time:g}"
    return (
        exit_record.get("exit_code") == 0
        and round(end_time / dt) == steps
        and log.count("PIMPLE: Converged in") == steps
        and log.rstrip().endswith("End")
        and all((case / endpoint / field).is_file() for field in ("U", "p", "C", "phi"))
    )


def existing_archive_record(case_name, evidence_root):
    archive = evidence_root / f"{case_name}.tar.gz"
    if archive.is_file():
        return {"archive": archive.name, "archive_sha256": sha256(archive),
                "archive_bytes": archive.stat().st_size}
    parts_path = evidence_root / f"{case_name}.tar.gz.parts.json"
    if parts_path.is_file():
        manifest = json.loads(parts_path.read_text())
        aggregate = hashlib.sha256()
        for part in manifest["parts"]:
            path = evidence_root / part["file"]
            if not path.is_file() or sha256(path) != part["sha256"]:
                raise ValueError(f"existing archive part is missing or changed: {path}")
            with path.open("rb") as stream:
                for chunk in iter(lambda: stream.read(1 << 20), b""):
                    aggregate.update(chunk)
        if aggregate.hexdigest() != manifest["archive_sha256"]:
            raise ValueError(f"existing split archive does not reassemble to its recorded hash: {parts_path}")
        return {"archive": parts_path.name, "archive_sha256": manifest["archive_sha256"],
                "archive_bytes": manifest["archive_bytes"], "parts": manifest["parts"]}
    raise FileNotFoundError(f"complete run lacks an archived case: {case_name}")


def compare_completed_replay(first, second):
    first, second = Path(first), Path(second)
    first_diagnostics = json.loads((first / "diagnostics.json").read_text())
    second_diagnostics = json.loads((second / "diagnostics.json").read_text())
    first_log_sha = first_diagnostics.get("sha256", {}).get("log.foamRun")
    second_log_sha = second_diagnostics.get("sha256", {}).get("log.foamRun")
    first_diagnostics.get("sha256", {}).pop("log.foamRun", None)
    second_diagnostics.get("sha256", {}).pop("log.foamRun", None)
    input_hashes_equal = (first / "input-hashes.json").read_bytes() == (second / "input-hashes.json").read_bytes()
    metrics_equal_ignoring_run_log_hash = first_diagnostics == second_diagnostics
    endpoint_fields = {
        field: sha256(first / "0.05" / field) == sha256(second / "0.05" / field)
        for field in ("U", "p", "C", "phi")
    }
    passed = input_hashes_equal and metrics_equal_ignoring_run_log_hash and all(endpoint_fields.values())
    return {
        "status": "PASS" if passed else "FAIL",
        "input_hashes_equal": input_hashes_equal,
        "diagnostics_equal_ignoring_run_log_hash": metrics_equal_ignoring_run_log_hash,
        "endpoint_field_hashes_equal": endpoint_fields,
        "preserved_run_log_sha256": first_log_sha,
        "replay_run_log_sha256": second_log_sha,
    }


def archive_case(case, evidence, name):
    archive_path = evidence / f"{name}.tar.gz"
    temporary = archive_path.with_suffix(".tar.gz.tmp")
    with tarfile.open(temporary, "w:gz") as archive:
        for path in sorted(case.rglob("*")):
            if path.is_file():
                archive.add(path, arcname=f"{name}/{path.relative_to(case)}")
    digest = sha256(temporary)
    if temporary.stat().st_size <= MAX_ARCHIVE_PART_BYTES:
        temporary.replace(archive_path)
        return {"archive": archive_path.name, "archive_sha256": digest,
                "archive_bytes": archive_path.stat().st_size}

    parts = []
    with temporary.open("rb") as source:
        part_index = 0
        while data := source.read(MAX_ARCHIVE_PART_BYTES):
            part = evidence / f"{name}.tar.gz.part-{part_index:02d}"
            part.write_bytes(data)
            parts.append({"file": part.name, "bytes": len(data), "sha256": sha256(part)})
            part_index += 1
    temporary.unlink()
    parts_manifest = evidence / f"{name}.tar.gz.parts.json"
    parts_manifest.write_text(json.dumps({
        "archive": f"{name}.tar.gz", "archive_sha256": digest,
        "archive_bytes": sum(part["bytes"] for part in parts),
        "reassemble": "cat " + " ".join(part["file"] for part in parts)
                       + f" > {name}.tar.gz",
        "parts": parts,
    }, indent=2) + "\n")
    return {"archive": parts_manifest.name, "archive_sha256": digest,
            "archive_bytes": sum(part["bytes"] for part in parts), "parts": parts}


def archive_preserved_attempt(attempt, evidence_root, run_root):
    attempt_path = Path(run_root) / attempt["path"]
    is_complete = attempt["status"] == "COMPLETE_REPLAY_PRESERVED_AFTER_FALSE_INCOMPLETE_CLASSIFICATION"
    destination_dir = Path(evidence_root) / "attempts"
    destination_dir.mkdir(parents=True, exist_ok=True)
    if is_complete:
        paths = [path for path in attempt_path.rglob("*") if path.is_file() or path.is_symlink()]
        excluded = []
    else:
        paths = []
        input_hash_path = attempt_path / "input-hashes.json"
        if input_hash_path.is_file():
            input_hashes = json.loads(input_hash_path.read_text())
            paths.extend(attempt_path / relative for relative in input_hashes)
        for filename in ("parameters.json", "input-hashes.json", "command.json", "exit.json",
                         "log.container", "log.blockMesh", "log.foamRun", "log.centres"):
            path = attempt_path / filename
            if path.is_file():
                paths.append(path)
        excluded = ["generated mesh and partial time directories"]
    destination = destination_dir / f"{attempt_path.name}{'-inputs-only' if not is_complete else ''}.tar.gz"
    temporary = Path(str(destination) + ".tmp")
    if destination.exists():
        expected = {f"{attempt_path.name}/{path.relative_to(attempt_path)}": path
                    for path in set(paths)}
        with tarfile.open(destination, "r:gz") as archive:
            members = {member.name: member for member in archive.getmembers()
                       if member.isfile() or member.issym() or member.islnk()}
            if set(members) != set(expected):
                raise ValueError(f"existing preserved-attempt archive member set differs: {destination}")
            for name, source in expected.items():
                member = members[name]
                if source.is_symlink():
                    if not (member.issym() or member.islnk()) or member.linkname != os.readlink(source):
                        raise ValueError(f"preserved attempt symlink differs: {destination}:{name}")
                    continue
                stream = archive.extractfile(member)
                if stream is None:
                    raise ValueError(f"cannot read preserved attempt member: {destination}:{name}")
                digest = hashlib.sha256()
                for chunk in iter(lambda: stream.read(1 << 20), b""):
                    digest.update(chunk)
                if digest.hexdigest() != sha256(source):
                    raise ValueError(f"preserved attempt file differs: {destination}:{name}")
    else:
        with tarfile.open(temporary, "w:gz") as archive:
            for path in sorted(set(paths)):
                archive.add(path, arcname=f"{attempt_path.name}/{path.relative_to(attempt_path)}")
        temporary.replace(destination)
    return {
        "evidence_archive": str(destination.relative_to(Path(evidence_root))),
        "evidence_archive_sha256": sha256(destination),
        "evidence_archive_bytes": destination.stat().st_size,
        "evidence_archive_members": len(paths),
        "excluded_partial_outputs": excluded,
    }


def main():
    protocol = json.loads(PROTOCOL.read_text())
    if protocol["runtime_image_id"] != IMAGE_ID or protocol["runtime_image"] != IMAGE:
        raise ValueError("protocol runtime pin does not match this runner")
    if not BASELINE.is_file() or sha256(BASELINE) != protocol["comparison"]["reused_case"]["archive_sha256"]:
        raise ValueError("pre-existing n64/dt=0.001 baseline is missing or changed")

    run_root = Path(os.environ.get("CANS_OF14_RUN_ROOT", "work/of14-high-gradient-v1")).resolve()
    evidence_root = Path(os.environ.get("CANS_OF14_EVIDENCE_ROOT", "evidence/of14-high-gradient-v1-matrix")).resolve()
    case_timeout = int(os.environ.get("CANS_OF14_CASE_TIMEOUT_SECONDS", "14400"))
    if case_timeout <= 0:
        raise ValueError("CANS_OF14_CASE_TIMEOUT_SECONDS must be positive")
    resume = os.environ.get("CANS_OF14_RESUME", "false").lower() == "true"
    finalize_only = os.environ.get("CANS_OF14_FINALIZE_ONLY", "false").lower() == "true"
    if not resume and (run_root.exists() or evidence_root.exists()):
        raise FileExistsError("refusing to overwrite an existing run or evidence directory")

    dirty = run_checked(["git", "status", "--porcelain", "--untracked-files=no"], timeout=10).stdout.strip()
    if dirty and not finalize_only:
        raise RuntimeError("commit the frozen run sources before executing the solver")
    source_commit = run_checked(["git", "rev-parse", "HEAD"], timeout=10).stdout.strip()
    docker_cli = shutil.which("docker")
    if not docker_cli:
        raise FileNotFoundError("docker CLI was not found on PATH")
    context = run_checked([docker_cli, "context", "show"], timeout=8).stdout.strip()
    docker = [docker_cli, "--context", context]
    image_info = run_checked([
        *docker, "image", "inspect", IMAGE,
        "--format", "{{.Id}} {{.Os}}/{{.Architecture}}",
    ], timeout=8).stdout.strip()
    image_id, platform = image_info.split(maxsplit=1)
    if image_id != IMAGE_ID or platform != "linux/arm64":
        raise RuntimeError(f"unexpected runtime image: {image_id} {platform}")
    if resume:
        if not run_root.is_dir() or not evidence_root.is_dir():
            raise FileNotFoundError("resume requires both the prior run and evidence directories")
        prior_environment = json.loads((run_root / "run-environment.json").read_text())
        if prior_environment.get("protocol_sha256") != sha256(PROTOCOL):
            raise ValueError("resume protocol differs from the original run")
        if (evidence_root / "protocol.json").read_bytes() != PROTOCOL.read_bytes():
            raise ValueError("resume evidence contains a different protocol")
        if finalize_only:
            manifest = json.loads((evidence_root / "manifest.json").read_text())
            for attempt in manifest.get("attempt_history", []):
                attempt.update(archive_preserved_attempt(attempt, evidence_root, run_root))
            (evidence_root / "manifest.json").write_text(json.dumps(manifest, indent=2, allow_nan=False) + "\n")
            (run_root / "summary.json").write_text(json.dumps(manifest, indent=2, allow_nan=False) + "\n")
            print(json.dumps({"matrix_status": manifest["matrix_status"],
                              "completed": len(manifest["completed_cases"]),
                              "evidence": str(evidence_root)}, indent=2), flush=True)
            return
    else:
        run_root.mkdir(parents=True)
        evidence_root.mkdir(parents=True)
    environment = {
        "source_commit": source_commit,
        "protocol": str(PROTOCOL.relative_to(ROOT)),
        "protocol_sha256": sha256(PROTOCOL),
        "mathematical_protocol": "Foundation 13 high-gradient v2 MMS copied without changing equations, forcing, end time, mesh matrix, time steps, or gates",
        "binary_package": "OpenFOAM Foundation 14 package 20260724 arm64",
        "binary_package_sha256": "d20102ae6b39377ab3f5e654302ea0d58de166156fe681670f147ac555299a69",
        "container_image": IMAGE,
        "container_image_id": image_id,
        "container_platform": platform,
        "docker_cli": str(Path(docker_cli).resolve()),
        "docker_cli_sha256": sha256(Path(docker_cli).resolve()),
        "docker_cli_version": run_checked([*docker, "--version"], timeout=8).stdout.strip(),
        "docker_context": context,
        "per_case_timeout_seconds": case_timeout,
        "reused_baseline_archive_sha256": sha256(BASELINE),
        "scope": "Foundation 14 five-case successor matrix; not a solver-version defect verdict or continuous-extrema certificate",
    }
    if resume:
        environment["resumed_from_source_commit"] = prior_environment["source_commit"]
        environment["resume_note"] = "Preserved earlier complete cases; reruns only incomplete cases from clean generated inputs."
        (run_root / "run-environment-resume.json").write_text(json.dumps(environment, indent=2) + "\n")
        (evidence_root / "run-environment-resume.json").write_text(json.dumps(environment, indent=2) + "\n")
    else:
        (run_root / "run-environment.json").write_text(json.dumps(environment, indent=2) + "\n")
        (evidence_root / "protocol.json").write_bytes(PROTOCOL.read_bytes())
        (evidence_root / "run-environment.json").write_text(json.dumps(environment, indent=2) + "\n")

    names = expected_cases(protocol)
    reused = protocol["comparison"]["reused_case"]["case"]
    cases = []
    archived = [{
        "case": reused,
        "archive": str(BASELINE.relative_to(ROOT)),
        "archive_sha256": sha256(BASELINE),
        "reused_from_single_case_compatibility_probe": True,
    }]
    attempts = []
    preserved_attempts = run_root / "attempts"
    if preserved_attempts.is_dir():
        for attempt_dir in sorted(preserved_attempts.iterdir()):
            suffix = "-attempt-01-incomplete"
            complete_suffix = "-attempt-01-complete-preserved"
            if not attempt_dir.is_dir():
                continue
            if attempt_dir.name.endswith(complete_suffix):
                original_name = attempt_dir.name[:-len(complete_suffix)]
                status = "COMPLETE_REPLAY_PRESERVED_AFTER_FALSE_INCOMPLETE_CLASSIFICATION"
            elif attempt_dir.name.endswith(suffix):
                original_name = attempt_dir.name[:-len(suffix)]
                status = None
            else:
                continue
            if status is None and complete_case(attempt_dir, protocol["end_time"]):
                reclassified = attempt_dir.with_name(f"{original_name}-attempt-01-complete-preserved")
                if reclassified.exists():
                    raise FileExistsError(f"refusing to replace reclassified attempt: {reclassified}")
                shutil.move(str(attempt_dir), str(reclassified))
                attempt_dir = reclassified
                status = "COMPLETE_REPLAY_PRESERVED_AFTER_FALSE_INCOMPLETE_CLASSIFICATION"
            elif status is None:
                status = "INCOMPLETE_PRIOR_ATTEMPT_PRESERVED"
            old_log = attempt_dir / "log.foamRun"
            old_log_text = old_log.read_text(errors="replace") if old_log.is_file() else ""
            old_exit = attempt_dir / "exit.json"
            attempts.append({
                "case": original_name, "status": status,
                "path": str(attempt_dir.relative_to(run_root)),
                "prior_exit": json.loads(old_exit.read_text()) if old_exit.is_file() else {},
                "observed_steps": len(re.findall(r"^Time = ", old_log_text, re.MULTILINE)),
                "converged_steps": old_log_text.count("PIMPLE: Converged in"),
                "log_ends_with_End": old_log_text.rstrip().endswith("End"),
                "log_sha256": sha256(old_log) if old_log.is_file() else None,
                "diagnostics_sha256": sha256(attempt_dir / "diagnostics.json")
                if (attempt_dir / "diagnostics.json").is_file() else None,
                "input_hashes_sha256": sha256(attempt_dir / "input-hashes.json")
                if (attempt_dir / "input-hashes.json").is_file() else None,
            })
    for name in names:
        if name == reused:
            case_dir = run_root / name
            if not case_dir.exists():
                with tarfile.open(BASELINE, "r:gz") as archive:
                    archive.extractall(case_dir.parent, filter="data")
            if not complete_case(case_dir, protocol["end_time"]):
                raise ValueError("reused baseline case does not satisfy the frozen completion check")
            diagnostics = json.loads((case_dir / "diagnostics.json").read_text())
            cases.append(diagnostics)
            continue

        case = run_root / name
        if case.exists() and complete_case(case, protocol["end_time"]):
            diagnostics = json.loads((case / "diagnostics.json").read_text())
            archive_info = existing_archive_record(name, evidence_root)
            cases.append(diagnostics)
            archived.append({"case": name, **archive_info,
                             "standard_acceptance": diagnostics["standard_acceptance"]["status"],
                             "local_quality": diagnostics.get("local_quality", {}).get("status", "UNCERTAIN"),
                             "reused_from_prior_attempt": True})
            continue
        if case.exists():
            attempt_dir = run_root / "attempts" / f"{name}-attempt-01-incomplete"
            attempt_dir.parent.mkdir(parents=True, exist_ok=True)
            if attempt_dir.exists():
                raise FileExistsError(f"refusing to replace preserved partial attempt: {attempt_dir}")
            log_path = case / "log.foamRun"
            partial_log = log_path.read_text(errors="replace") if log_path.is_file() else ""
            prior_exit = json.loads((case / "exit.json").read_text()) if (case / "exit.json").is_file() else {}
            attempts.append({
                "case": name, "status": "INCOMPLETE_PRESERVED_BEFORE_RETRY",
                "path": str(attempt_dir.relative_to(run_root)), "prior_exit": prior_exit,
                "observed_steps": len(re.findall(r"^Time = ", partial_log, re.MULTILINE)),
                "converged_steps": partial_log.count("PIMPLE: Converged in"),
                "log_ends_with_End": partial_log.rstrip().endswith("End"),
                "log_sha256": sha256(log_path) if log_path.is_file() else None,
            })
            shutil.move(str(case), str(attempt_dir))

        n_text, dt_text = name.removeprefix("n").split("-dt", 1)
        n, dt = int(n_text), float(dt_text)
        generate(case, n=n, dt=dt, end=protocol["end_time"], nu=protocol["viscosity"],
                 profile="high-gradient", frequency=protocol["frequency_N"])
        inputs = {str(path.relative_to(case)): sha256(path)
                  for path in sorted(case.rglob("*")) if path.is_file()}
        (case / "input-hashes.json").write_text(json.dumps(inputs, indent=2) + "\n")
        container_name = f"cans-of14-{name}"
        command = [
            *docker, "run", "--rm", "--name", container_name, "--network", "none",
            "--entrypoint", "/bin/bash", "-v", f"{case}:/case", image_id, "-c",
            "useradd -o -u \"$1\" -m runner && su runner -s /bin/bash -c "
            "\"source /opt/openfoam14/etc/bashrc && cd /case && "
            "blockMesh > log.blockMesh 2>&1 && foamRun > log.foamRun 2>&1 && "
            "foamPostProcess -func writeCellCentres -latestTime > log.centres 2>&1\"",
            "--", str(os.getuid()),
        ]
        (case / "command.json").write_text(json.dumps(command, indent=2) + "\n")
        timed_out = False
        with (case / "log.container").open("w") as log:
            try:
                result = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT,
                                        timeout=case_timeout)
                exit_record = {"exit_code": result.returncode, "timed_out": False}
            except subprocess.TimeoutExpired:
                timed_out = True
                try:
                    stop = subprocess.run([*docker, "stop", "-t", "5", container_name],
                                          capture_output=True, text=True, timeout=15)
                    stop_record = {"exit_code": stop.returncode, "stdout": stop.stdout,
                                   "stderr": stop.stderr}
                except subprocess.TimeoutExpired:
                    stop_record = {"status": "unconfirmed; docker stop timed out"}
                exit_record = {"exit_code": None, "timed_out": True,
                               "timeout_seconds": case_timeout, "container_stop": stop_record}
                result = None
        (case / "exit.json").write_text(json.dumps(exit_record, indent=2) + "\n")
        if timed_out:
            raise RuntimeError(f"solver exceeded {case_timeout}s for {name}; partial inputs and logs preserved in {case}")
        if result.returncode:
            raise RuntimeError(f"solver run failed for {name}; inputs and logs preserved in {case}")
        diagnostics = analyze(case, json.loads((ROOT / "protocols/high-gradient-of13-v2.json").read_text()))
        (case / "diagnostics.json").write_text(json.dumps(diagnostics, indent=2, allow_nan=False) + "\n")
        cases.append(diagnostics)
        archive_info = archive_case(case, evidence_root, name)
        archived.append({"case": name, **archive_info,
                         "standard_acceptance": diagnostics["standard_acceptance"]["status"],
                         "local_quality": diagnostics.get("local_quality", {}).get("status", "UNCERTAIN")})
        print(json.dumps({"case": name, "status": "archived", "archive_sha256": archive_info["archive_sha256"]}), flush=True)

    baseline_diag = json.loads((run_root / reused / "diagnostics.json").read_text())
    baseline_diag["parameters"]
    for attempt in attempts:
        attempt.update(archive_preserved_attempt(attempt, evidence_root, run_root))
        if attempt["status"] != "COMPLETE_REPLAY_PRESERVED_AFTER_FALSE_INCOMPLETE_CLASSIFICATION":
            continue
        preserved = run_root / attempt["path"]
        replay = run_root / attempt["case"]
        attempt["replay_comparison"] = compare_completed_replay(preserved, replay)

    summary = {
        "protocol": str(PROTOCOL.relative_to(ROOT)),
        "protocol_sha256": sha256(PROTOCOL),
        "run_environment": environment,
        "expected_cases": names,
        "completed_cases": archived,
        "matrix_status": "COMPLETE" if len(archived) == len(names) else "INCOMPLETE",
        "case_diagnostics": cases,
        "attempt_history": attempts,
        "interpretation": protocol["comparison"]["interpretation"],
        "limitations": protocol["interpretation_limits"],
    }
    (evidence_root / "manifest.json").write_text(json.dumps(summary, indent=2, allow_nan=False) + "\n")
    (run_root / "summary.json").write_text(json.dumps(summary, indent=2, allow_nan=False) + "\n")
    print(json.dumps({"matrix_status": summary["matrix_status"], "completed": len(archived),
                      "evidence": str(evidence_root)}, indent=2), flush=True)


if __name__ == "__main__":
    main()
