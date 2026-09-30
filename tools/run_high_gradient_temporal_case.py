"""Run one frozen n=64 temporal case without repeating the completed spatial sweep."""
import argparse
import hashlib
import json
import os
import subprocess
import tarfile
from datetime import datetime, timezone
from pathlib import Path

from tools.analyze_openfoam import analyze
from tools.openfoam_case import generate
from tools.run_high_gradient_openfoam import resolve_docker_cli, resolve_docker_context


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dt", type=float, required=True, choices=(0.0005, 0.00025))
    parser.add_argument("--run-root", type=Path, required=True)
    args = parser.parse_args()

    protocol = Path("protocols/high-gradient-of13-v2.json")
    spec = json.loads(protocol.read_text())
    root = args.run_root.expanduser().resolve()
    if root.exists():
        raise FileExistsError(f"refusing to overwrite temporal run root: {root}")
    dirty = subprocess.run(
        ["git", "status", "--porcelain", "--untracked-files=all"],
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    if dirty:
        raise RuntimeError("commit all sources and evidence before this reproducible run")
    source_commit = subprocess.run(
        ["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=True,
    ).stdout.strip()

    docker_cli, docker_cli_resolved = resolve_docker_cli()
    docker_context = resolve_docker_context(docker_cli)
    docker = [docker_cli, "--context", docker_context]
    image_info = subprocess.run(
        [*docker, "image", "inspect", "concentration-aware-ns:of13",
         "--format", "{{.Id}} {{.Os}}/{{.Architecture}}"],
        capture_output=True, text=True, timeout=8, check=True,
    ).stdout.strip()
    image_id, image_platform = image_info.split(maxsplit=1)
    root.mkdir(parents=True)
    environment = {
        "source_commit": source_commit,
        "container_image_id": image_id,
        "container_platform": image_platform,
        "docker_cli": docker_cli,
        "docker_cli_resolved": docker_cli_resolved,
        "docker_cli_sha256": sha256(docker_cli_resolved),
        "docker_cli_version": subprocess.run(
            [*docker, "--version"], capture_output=True, text=True,
            timeout=8, check=True,
        ).stdout.strip(),
        "docker_context": docker_context,
        "protocol": str(protocol),
        "protocol_sha256": sha256(protocol),
        "parent_matrix_manifest_sha256": sha256(Path("evidence/of13-high-gradient-v2/manifest.json")),
        "scope": "single frozen n=64 temporal addendum; not a complete matrix",
    }
    (root / "run-environment.json").write_text(json.dumps(environment, indent=2) + "\n")
    case = root / f"n64-dt{args.dt:g}"
    generate(case, n=64, dt=args.dt, end=spec["end_time"], nu=spec["viscosity"],
             profile="high-gradient", frequency=spec["frequency_N"])
    (case / "input-hashes.json").write_text(json.dumps({
        str(path.relative_to(case)): sha256(path)
        for path in sorted(case.rglob("*")) if path.is_file()
    }, indent=2) + "\n")
    command = [
        *docker, "run", "--rm", "--name", f"cans-hg-{case.name}-addendum",
        "--network", "none", "--entrypoint", "/bin/bash",
        "-v", f"{case}:/case", image_id, "-c",
        "useradd -o -u \"$1\" -m runner && su runner -s /bin/bash -c "
        "\"source /opt/openfoam13/etc/bashrc && cd /case && "
        "blockMesh > log.blockMesh 2>&1 && foamRun > log.foamRun 2>&1 && "
        "foamPostProcess -func writeCellCentres -latestTime > log.centres 2>&1\"",
        "--", str(os.getuid()),
    ]
    (case / "command.json").write_text(json.dumps(command, indent=2) + "\n")
    with (case / "log.container").open("w") as log:
        run = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT)
    (case / "exit.json").write_text(json.dumps({"exit_code": run.returncode}) + "\n")
    if run.returncode:
        raise RuntimeError(f"case {case.name} failed; preserved at {case}")

    diagnostics = analyze(case, spec)
    (case / "diagnostics.json").write_text(json.dumps(diagnostics, indent=2, allow_nan=False) + "\n")
    expected_steps = round(spec["end_time"] / args.dt)
    log = (case / "log.foamRun").read_text(errors="replace")
    steps = log.count("Time = ")
    converged = log.count("PIMPLE: Converged in")
    endpoint = case / f"{spec['end_time']:g}"
    fields = all((endpoint / name).is_file() for name in ("U", "p", "C", "phi"))
    complete = (steps == expected_steps and converged == expected_steps
                and log.rstrip().endswith("End") and fields)
    if not complete:
        raise RuntimeError(f"run exited zero but completion contract failed; preserved at {case}")

    archive = root / f"{case.name}.tar.gz"
    with tarfile.open(archive, "w:gz") as tar:
        tar.add(case, arcname=case.name)
    with tarfile.open(archive, "r:gz") as tar:
        members = {member.name: member for member in tar.getmembers() if member.isfile()}
        expected_paths = [path for path in case.rglob("*") if path.is_file()]
        if len(members) != len(expected_paths):
            raise RuntimeError("archive member count does not match the completed case")
        for path in expected_paths:
            member_name = f"{case.name}/{path.relative_to(case)}"
            stream = tar.extractfile(members.get(member_name))
            if stream is None or hashlib.sha256(stream.read()).hexdigest() != sha256(path):
                raise RuntimeError(f"archive content verification failed: {member_name}")
    manifest = {
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "matrix_status": "SINGLE_CASE_COMPLETE_NOT_FULL_MATRIX",
        "case": case.name,
        "complete": complete,
        "time_steps": steps,
        "converged_steps": converged,
        "end_marker": True,
        "endpoint_fields": ["U", "p", "C", "phi"],
        "standard_acceptance": diagnostics["standard_acceptance"]["status"],
        "local_quality": diagnostics.get("local_quality", {}).get("status", "UNCERTAIN"),
        "archive": archive.name,
        "archive_sha256": sha256(archive),
        "source_log_sha256": sha256(case / "log.foamRun"),
        "run_environment": "run-environment.json",
        "scope": "One time-resolution row appended as a distinct source-pinned addendum; no full-matrix or defect claim.",
    }
    (root / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
