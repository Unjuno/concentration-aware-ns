"""Archive only verified-complete cases from the frozen high-gradient run."""
import hashlib
import json
import os
import re
import tarfile
from datetime import datetime, timezone
from pathlib import Path

from tools.high_gradient_acceptance import matrix_reproduction


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def expected_cases(spec):
    spatial = spec["spatial_matrix"]
    temporal = spec["temporal_matrix"]
    rows = [(n, spatial["delta_t"]) for n in spatial["cell_counts"]]
    rows.extend((temporal["cell_count"], dt) for dt in temporal["delta_t"]
                if (temporal["cell_count"], dt) not in rows)
    return [f"n{n}-dt{dt:g}" for n, dt in rows]


def completion_check(case, end_time):
    exit_path = case / "exit.json"
    log_path = case / "log.foamRun"
    diagnostics_path = case / "diagnostics.json"
    if not all(path.is_file() for path in (exit_path, log_path, diagnostics_path)):
        return None

    exit_record = json.loads(exit_path.read_text())
    diagnostics = json.loads(diagnostics_path.read_text())
    parameters = diagnostics.get("parameters", {})
    dt = parameters.get("dt")
    if not isinstance(dt, (float, int)) or dt <= 0:
        return None
    expected_steps = round(end_time / dt)
    log = log_path.read_text(errors="replace")
    steps = len(re.findall(r"^Time = ", log, re.MULTILINE))
    converged = log.count("PIMPLE: Converged in")
    endpoint = f"{end_time:g}"
    required_fields = [case / endpoint / name for name in ("U", "p", "C", "phi")]
    accepted = (
        exit_record.get("exit_code") == 0
        and parameters.get("end") == end_time
        and steps == expected_steps
        and converged == expected_steps
        and log.rstrip().endswith("End")
        and all(path.is_file() for path in required_fields)
        and diagnostics.get("standard_acceptance", {}).get("status") in {"PASS", "FAIL"}
    )
    if not accepted:
        return None
    return {
        "diagnostics": diagnostics,
        "time_steps": steps,
        "converged_steps": converged,
        "endpoint": endpoint,
        "log_sha256": sha256(log_path),
    }


def verify_archive(archive_path, case, case_name):
    files = sorted(path for path in case.rglob("*") if path.is_file() or path.is_symlink())
    expected = {f"{case_name}/{path.relative_to(case)}": path for path in files}
    with tarfile.open(archive_path, "r:gz") as archive:
        members = {member.name: member for member in archive.getmembers()
                   if member.isfile() or member.issym() or member.islnk()}
        if set(members) != set(expected):
            raise ValueError(f"archive member set differs from source case: {archive_path}")
        for name, path in expected.items():
            member = members[name]
            if path.is_symlink():
                if not (member.issym() or member.islnk()) or member.linkname != os.readlink(path):
                    raise ValueError(f"archive symlink differs from source case: {name}")
                continue
            if not member.isfile():
                raise ValueError(f"archive file type differs from source case: {name}")
            archived = archive.extractfile(member)
            if archived is None:
                raise ValueError(f"cannot read archived case file: {name}")
            digest = hashlib.sha256()
            for chunk in iter(lambda: archived.read(1 << 20), b""):
                digest.update(chunk)
            if digest.hexdigest() != sha256(path):
                raise ValueError(f"archive content differs from source case: {name}")


def archive_completed(work_root, evidence_root, protocol_path):
    work_root = Path(work_root)
    evidence_root = Path(evidence_root)
    protocol_path = Path(protocol_path)
    spec = json.loads(protocol_path.read_text())
    environment_path = work_root / "run-environment.json"
    environment = json.loads(environment_path.read_text()) if environment_path.is_file() else None
    if environment is None:
        raise FileNotFoundError(f"missing run environment manifest: {environment_path}")

    evidence_root.mkdir(parents=True, exist_ok=True)
    completed = []
    incomplete = []
    for name in expected_cases(spec):
        case = work_root / name
        result = completion_check(case, spec["end_time"]) if case.is_dir() else None
        if result is None:
            observation = {"case": name, "archived": False}
            log = case / "log.foamRun"
            if log.is_file():
                content = log.read_text(errors="replace")
                observation.update({
                    "observed_steps": len(re.findall(r"^Time = ", content, re.MULTILINE)),
                    "observed_converged_steps": content.count("PIMPLE: Converged in"),
                    "log_ends_with_End": content.rstrip().endswith("End"),
                    "log_sha256": sha256(log),
                })
            incomplete.append(observation)
            continue

        archive_path = evidence_root / f"{name}.tar.gz"
        if archive_path.exists():
            try:
                verify_archive(archive_path, case, name)
            except (OSError, EOFError, tarfile.TarError, ValueError):
                archive_path.unlink()
        if not archive_path.exists():
            temporary_archive = archive_path.with_suffix(archive_path.suffix + ".tmp")
            try:
                with tarfile.open(temporary_archive, "w:gz") as archive:
                    for path in sorted(case.rglob("*")):
                        if path.is_file():
                            archive.add(path, arcname=f"{name}/{path.relative_to(case)}")
                verify_archive(temporary_archive, case, name)
                temporary_archive.replace(archive_path)
            except Exception:
                temporary_archive.unlink(missing_ok=True)
                raise
        completed.append({
            "case": name,
            "archive": archive_path.name,
            "archive_sha256": sha256(archive_path),
            "source_log_sha256": result["log_sha256"],
            "standard_acceptance": result["diagnostics"]["standard_acceptance"]["status"],
            "local_quality": result["diagnostics"].get("local_quality", {}).get("status", "UNCERTAIN"),
            "time_steps": result["time_steps"],
            "converged_steps": result["converged_steps"],
        })

    fully_archived = len(completed) == len(expected_cases(spec))
    reproduction = (
        matrix_reproduction([json.loads((work_root / name / "diagnostics.json").read_text())
                             for name in expected_cases(spec)],
                            spec["problem_reproduction_rule"]["required_fine_grid_counts"])
        if fully_archived else {"status": "UNCERTAIN", "reason": "required run matrix is incomplete"}
    )
    manifest = {
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "protocol": str(protocol_path),
        "protocol_sha256": sha256(protocol_path),
        "run_environment": environment,
        "expected_cases": expected_cases(spec),
        "completed_cases": completed,
        "incomplete_cases": incomplete,
        "matrix_status": "COMPLETE" if fully_archived else "INCOMPLETE",
        "problem_reproduction": reproduction,
        "interpretation": "Only complete cases with zero runner exit, full expected time-step and PIMPLE-convergence counts, End log marker, and endpoint U/p/C/phi fields are archived. Partial cases remain UNCERTAIN.",
    }
    (evidence_root / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return manifest


def main():
    manifest = archive_completed(
        "work/of13-high-gradient-v2",
        "evidence/of13-high-gradient-v2",
        "protocols/high-gradient-of13-v2.json",
    )
    print(json.dumps({
        "matrix_status": manifest["matrix_status"],
        "completed": len(manifest["completed_cases"]),
        "incomplete": len(manifest["incomplete_cases"]),
        "reproduction": manifest["problem_reproduction"]["status"],
    }, indent=2))


if __name__ == "__main__":
    main()
