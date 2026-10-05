"""Run a preregistered, short first-refinement AMR timing diagnostic."""
import hashlib
import json
import os
import shutil
import subprocess
from pathlib import Path

from tools.openfoam_amr_case import generate_amr
from tools.openfoam_case import generate
from tools.run_high_gradient_openfoam import resolve_docker_cli, resolve_docker_context


PROTOCOL = Path("protocols/high-gradient-of13-amr-first-refinement-v1.json")
IMAGE = "sha256:dd2b2eb63b12896a9b6e7a46563ed96b26d1c78c3e3749536d40d456895f722b"
WORK = Path("work/of13-amr-first-refinement-v1")
EVIDENCE = Path("evidence/of13-amr-first-refinement-v1")
CHECKPOINTS = ("0.001", "0.002", "0.003")


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _write_checkpoint_control(case):
    path = case / "system/controlDict"
    text = path.read_text().replace("writeInterval 0.003;", "writeInterval 0.001;")
    if text == path.read_text():
        raise ValueError("expected generated end-time write interval was not found")
    path.write_text(text)


def _run_case(case, docker, image, uid):
    name = case.name
    post = " && ".join(
        f"foamPostProcess -func {func} -time {time} > log.{label}-{time} 2>&1"
        for time in CHECKPOINTS
        for func, label in (("writeCellCentres", "centres"),
                            ("writeCellVolumes", "volumes"),
                            ("'grad(U)'", "gradient"))
    )
    command = [
        *docker, "run", "--rm", "--name", f"cans-amr-first-{name}",
        "--network", "none", "--entrypoint", "/bin/bash", "-v",
        f"{case.resolve()}:/case", image, "-c",
        "useradd -o -u \"$1\" -m runner && su runner -s /bin/bash -c "
        f"\"source /opt/openfoam13/etc/bashrc && cd /case && blockMesh > log.blockMesh 2>&1 "
        f"&& foamRun > log.foamRun 2>&1 && {post}\"",
        "--", str(uid),
    ]
    (case / "command.json").write_text(json.dumps(command, indent=2) + "\n")
    with (case / "log.container").open("w") as log:
        result = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT)
    (case / "exit.json").write_text(json.dumps({"exit_code": result.returncode}) + "\n")
    if result.returncode:
        raise RuntimeError(f"AMR first-refinement case failed; preserve {case} and its logs")


def _case_manifest(case, adaptation):
    return {
        "case": case.name,
        "adaptation": adaptation,
        "input_sha256": json.loads((case / "input-hashes.json").read_text()),
        "exit": json.loads((case / "exit.json").read_text()),
        "solver_log_sha256": sha256(case / "log.foamRun"),
        "time_steps": (case / "log.foamRun").read_text().count("\nTime = "),
        "converged_steps": (case / "log.foamRun").read_text().count("PIMPLE: Converged in"),
        "checkpoints": {
            t: {
                "fields_present": all((case / t / field).is_file() for field in ("U", "p", "C")),
                "centres_log_sha256": sha256(case / f"log.centres-{t}"),
                "volumes_log_sha256": sha256(case / f"log.volumes-{t}"),
                "gradient_log_sha256": sha256(case / f"log.gradient-{t}"),
            }
            for t in CHECKPOINTS
        },
    }


def main():
    dirty = subprocess.run(
        ["git", "status", "--porcelain", "--untracked-files=all"],
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    if dirty:
        raise RuntimeError("commit the frozen probe sources before execution")
    if WORK.exists() or EVIDENCE.exists():
        raise FileExistsError("refusing to overwrite a prior probe work or evidence directory")
    source_commit = subprocess.run(
        ["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=True
    ).stdout.strip()
    spec = json.loads(PROTOCOL.read_text())
    if spec["target"]["container_image_id"] != IMAGE:
        raise ValueError("runner image does not match the frozen probe protocol")
    docker_cli, docker_resolved = resolve_docker_cli()
    context = resolve_docker_context(docker_cli)
    docker = [docker_cli, "--context", context]
    image_info = subprocess.run(
        [*docker, "image", "inspect", IMAGE, "--format", "{{.Id}} {{.Os}}/{{.Architecture}}"],
        capture_output=True, text=True, timeout=8, check=True,
    ).stdout.strip()
    if image_info != f"{IMAGE} linux/arm64":
        raise RuntimeError(f"unexpected runtime image: {image_info}")

    WORK.mkdir(parents=True, exist_ok=False)
    EVIDENCE.mkdir(parents=True, exist_ok=False)
    runtime = {
        "source_commit": source_commit,
        "protocol_sha256": sha256(PROTOCOL),
        "container_image_id": IMAGE,
        "container_platform": "linux/arm64",
        "docker_cli": docker_cli,
        "docker_cli_resolved": docker_resolved,
        "docker_cli_sha256": sha256(docker_resolved),
        "docker_cli_version": subprocess.run(
            [*docker, "--version"], capture_output=True, text=True, timeout=8, check=True
        ).stdout.strip(),
        "docker_context": context,
    }
    (WORK / "run-environment.json").write_text(json.dumps(runtime, indent=2) + "\n")
    params = spec["manufactured_solution"]
    common = dict(n=params["initial_grid_cells_per_axis"], dt=params["delta_t"],
                  end=params["end_time"], nu=params["viscosity"],
                  profile="high-gradient", frequency=params["frequency"])
    amr_case = WORK / "amr-cap5000"
    amr_params = {key: value for key, value in common.items() if key != "nu"}
    amr_params["frequency"] = common["frequency"]
    # generate_amr does not expose viscosity; this short probe uses the
    # generator's default nu=0.01, which is fixed in the protocol.
    if common["nu"] != 0.01:
        raise RuntimeError("protocol viscosity differs from generate_amr default")
    generate_amr(amr_case, max_cells=5000, max_level=2, refine_interval=2, **amr_params)
    uniform_case = WORK / "uniform-n16"
    generate(uniform_case, **common)
    for case in (amr_case, uniform_case):
        _write_checkpoint_control(case)
        hashes = {str(p.relative_to(case)): sha256(p)
                  for p in sorted(case.rglob("*")) if p.is_file()}
        (case / "input-hashes.json").write_text(json.dumps(hashes, indent=2) + "\n")
    for case in (amr_case, uniform_case):
        _run_case(case, docker, IMAGE, os.getuid())

    rows = [_case_manifest(amr_case, True), _case_manifest(uniform_case, False)]
    complete = all(
        row["exit"].get("exit_code") == 0
        and row["time_steps"] == len(CHECKPOINTS)
        and row["converged_steps"] == len(CHECKPOINTS)
        and all(item["fields_present"] for item in row["checkpoints"].values())
        for row in rows
    )
    if not complete:
        raise RuntimeError("checkpoint completion gate failed; preserve work and logs")
    manifest = {
        "protocol": str(PROTOCOL),
        "run_environment": runtime,
        "cases": rows,
        "completion": "PASS",
        "scope": "Raw early-time checkpoints only; analysis and adaptive attribution are separate.",
    }
    (EVIDENCE / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    for case in (amr_case, uniform_case):
        archive = EVIDENCE / f"{case.name}.tar.gz"
        subprocess.run(["tar", "-czf", str(archive), "-C", str(WORK), case.name], check=True)
        manifest["cases"][[row["case"] for row in rows].index(case.name)]["archive_sha256"] = sha256(archive)
    (EVIDENCE / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps({"completion": "PASS", "evidence": str(EVIDENCE / 'manifest.json'),
                      "cases": [{"case": row["case"], "time_steps": row["time_steps"],
                                 "converged_steps": row["converged_steps"]} for row in rows]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
