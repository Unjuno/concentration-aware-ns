"""Run one frozen n=64 temporal case without repeating the completed spatial sweep."""
import argparse
import hashlib
import json
import os
import subprocess
from pathlib import Path

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

    from tools.validate_high_gradient_temporal_case import validate_and_archive
    print(json.dumps(validate_and_archive(root), indent=2))


if __name__ == "__main__":
    main()
