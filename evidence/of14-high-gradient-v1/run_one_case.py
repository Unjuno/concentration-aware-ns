"""One-off isolated Foundation 14 compatibility/comparison runner.

This exploratory harness is kept under ignored work/ until reviewed and is not
an official reusable runner. Use --case N:DT to run a single case.
"""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from tools.analyze_openfoam import analyze
from tools.openfoam_case import generate

REPO = Path.cwd()
PROTOCOL = REPO / "protocols/high-gradient-of13-v2.json"
IMAGE = "concentration-aware-ns:of14-20260724"


def sha256(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", default="64:0.001", help="cell count:time step")
    parser.add_argument("--root", required=True)
    args = parser.parse_args()
    n_text, dt_text = args.case.split(":", 1)
    n, dt = int(n_text), float(dt_text)
    root = Path(args.root).resolve()
    root.mkdir(parents=True, exist_ok=False)
    spec = json.loads(PROTOCOL.read_text())
    cli = str(Path(shutil.which("docker")).resolve())
    context = subprocess.run([cli, "context", "show"], capture_output=True,
                             text=True, check=True, timeout=8).stdout.strip()
    docker = [cli, "--context", context]
    image_info = subprocess.run(
        [*docker, "image", "inspect", IMAGE, "--format", "{{.Id}} {{.Os}}/{{.Architecture}}"],
        capture_output=True, text=True, check=True, timeout=8,
    ).stdout.strip()
    image_id, platform = image_info.split(maxsplit=1)
    run_env = {
        "source_commit": subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True,
                                          text=True, check=True).stdout.strip(),
        "protocol_path": str(PROTOCOL.relative_to(REPO)),
        "protocol_sha256": sha256(PROTOCOL),
        "derived_math_protocol": "OpenFOAM Foundation 13 v2 localized high-gradient MMS; equations, forcing, time, and thresholds reused unchanged",
        "binary_package": "OpenFOAM Foundation 14 package 20260724 arm64",
        "binary_package_sha256": "d20102ae6b39377ab3f5e654302ea0d58de166156fe681670f147ac555299a69",
        "container_image": IMAGE,
        "container_image_id": image_id,
        "container_platform": platform,
        "docker_cli": cli,
        "docker_cli_sha256": sha256(cli),
        "docker_cli_version": subprocess.run([*docker, "--version"], capture_output=True,
                                            text=True, check=True, timeout=8).stdout.strip(),
        "docker_context": context,
        "scope": "Foundation 14 one-case compatibility/comparison probe; not a complete version matrix or defect verdict",
        "case": {"cells_per_axis": n, "delta_t": dt, "end_time": spec["end_time"]},
    }
    (root / "run-environment.json").write_text(json.dumps(run_env, indent=2) + "\n")
    case = root / f"n{n}-dt{dt:g}"
    generate(case, n=n, dt=dt, end=spec["end_time"], nu=spec["viscosity"],
             profile="high-gradient", frequency=spec["frequency_N"])
    input_hashes = {
        str(path.relative_to(case)): sha256(path)
        for path in sorted(case.rglob("*")) if path.is_file()
    }
    (case / "input-hashes.json").write_text(json.dumps(input_hashes, indent=2) + "\n")
    name = f"cans-of14-probe-n{n}-dt{dt:g}"
    command = [
        *docker, "run", "--rm", "--name", name, "--network", "none",
        "--entrypoint", "/bin/bash", "-v", f"{case}:/case", image_id, "-c",
        "useradd -o -u \"$1\" -m runner && su runner -s /bin/bash -c "
        "\"source /opt/openfoam14/etc/bashrc && cd /case && "
        "blockMesh > log.blockMesh 2>&1 && foamRun > log.foamRun 2>&1 && "
        "foamPostProcess -func writeCellCentres -latestTime > log.centres 2>&1\"",
        "--", str(os.getuid()),
    ]
    (case / "command.json").write_text(json.dumps(command, indent=2) + "\n")
    with (case / "log.container").open("w") as log:
        result = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT)
    (case / "exit.json").write_text(json.dumps({"exit_code": result.returncode}) + "\n")
    if result.returncode:
        (root / "summary.json").write_text(json.dumps({
            "status": "INCOMPLETE", "case": str(case), "exit_code": result.returncode,
            "scope": run_env["scope"],
        }, indent=2) + "\n")
        raise SystemExit(result.returncode)
    diagnostics = analyze(case, spec)
    (case / "diagnostics.json").write_text(
        json.dumps(diagnostics, indent=2, allow_nan=False) + "\n"
    )
    summary = {
        "status": "COMPLETED_SINGLE_CASE_PROBE",
        "case": diagnostics,
        "scope": run_env["scope"],
        "limitations": [
            "One resolution and one time step do not establish convergence or a version-wide behavior.",
            "Any disagreement is a diagnostic requiring input, package, implementation, and independent reference audit.",
            "No physical, molecular, singularity, or software-defect inference follows from this probe.",
        ],
    }
    (root / "summary.json").write_text(json.dumps(summary, indent=2, allow_nan=False) + "\n")
    print(json.dumps({"case": diagnostics, "root": str(root)}, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
