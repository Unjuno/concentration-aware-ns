"""Run the frozen Foundation 14 five-case successor matrix serially."""
import hashlib
import json
import os
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


def main():
    protocol = json.loads(PROTOCOL.read_text())
    if protocol["runtime_image_id"] != IMAGE_ID or protocol["runtime_image"] != IMAGE:
        raise ValueError("protocol runtime pin does not match this runner")
    if not BASELINE.is_file() or sha256(BASELINE) != protocol["comparison"]["reused_case"]["archive_sha256"]:
        raise ValueError("pre-existing n64/dt=0.001 baseline is missing or changed")

    run_root = Path(os.environ.get("CANS_OF14_RUN_ROOT", "work/of14-high-gradient-v1")).resolve()
    evidence_root = Path(os.environ.get("CANS_OF14_EVIDENCE_ROOT", "evidence/of14-high-gradient-v1-matrix")).resolve()
    case_timeout = int(os.environ.get("CANS_OF14_CASE_TIMEOUT_SECONDS", "2400"))
    if case_timeout <= 0:
        raise ValueError("CANS_OF14_CASE_TIMEOUT_SECONDS must be positive")
    if run_root.exists() or evidence_root.exists():
        raise FileExistsError("refusing to overwrite an existing run or evidence directory")

    dirty = run_checked(["git", "status", "--porcelain", "--untracked-files=all"], timeout=10).stdout.strip()
    if dirty:
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
    for name in names:
        if name == reused:
            case_dir = run_root / name
            case_dir.mkdir()
            with tarfile.open(BASELINE, "r:gz") as archive:
                archive.extractall(case_dir.parent, filter="data")
            extracted = case_dir.parent / "n64-dt0.001"
            if extracted != case_dir:
                extracted.replace(case_dir)
            diagnostics = json.loads((case_dir / "diagnostics.json").read_text())
            cases.append(diagnostics)
            continue

        n_text, dt_text = name.removeprefix("n").split("-dt", 1)
        n, dt = int(n_text), float(dt_text)
        case = run_root / name
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
    summary = {
        "protocol": str(PROTOCOL.relative_to(ROOT)),
        "protocol_sha256": sha256(PROTOCOL),
        "run_environment": environment,
        "expected_cases": names,
        "completed_cases": archived,
        "matrix_status": "COMPLETE" if len(archived) == len(names) else "INCOMPLETE",
        "case_diagnostics": cases,
        "interpretation": protocol["comparison"]["interpretation"],
        "limitations": protocol["interpretation_limits"],
    }
    (evidence_root / "manifest.json").write_text(json.dumps(summary, indent=2, allow_nan=False) + "\n")
    (run_root / "summary.json").write_text(json.dumps(summary, indent=2, allow_nan=False) + "\n")
    print(json.dumps({"matrix_status": summary["matrix_status"], "completed": len(archived),
                      "evidence": str(evidence_root)}, indent=2), flush=True)


if __name__ == "__main__":
    main()
