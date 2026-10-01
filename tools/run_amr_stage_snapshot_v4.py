"""Build and run the frozen OpenFOAM AMR-stage diagnostic protocol."""
import hashlib
import json
import os
import re
import shlex
import shutil
import subprocess
import tarfile
from pathlib import Path

from tools.openfoam_amr_case import generate_amr
from tools.run_high_gradient_openfoam import resolve_docker_cli, resolve_docker_context


ROOT = Path.cwd()
PROTOCOL = Path("protocols/high-gradient-of13-amr-same-run-map-v4.json")
SOURCE = Path(os.environ.get("CANS_OF13_SOURCE_TREE", "work/openfoam13-source-20260624"))
RUN_ROOT = Path(os.environ.get("CANS_AMR_STAGE_RUN_ROOT", "work/of13-amr-same-run-map-v4"))
EVIDENCE = Path(os.environ.get("CANS_AMR_STAGE_EVIDENCE", "evidence/of13-amr-same-run-map-v4"))
IMAGE = "sha256:dd2b2eb63b12896a9b6e7a46563ed96b26d1c78c3e3749536d40d456895f722b"
SOURCE_COMMIT = "18870c24d21c6b982e2cdec27b2f59738cca5f90"
STAGES = ("preMap", "mapped", "afterCorrectPhi", "prePressure", "postPressure", "postSolve")


def sha(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def docker(*args, check=True, **kwargs):
    return subprocess.run([*DOCKER, *args], check=check, **kwargs)


def main():
    if RUN_ROOT.exists() or EVIDENCE.exists():
        raise FileExistsError("refusing to overwrite prior AMR-stage work or evidence")
    dirty = subprocess.run(
        ["git", "status", "--porcelain", "--untracked-files=all"],
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    # Record the harness state rather than requiring an otherwise unrelated
    # commit merely to run this additive diagnostic.
    source_commit = subprocess.run(
        ["git", "-C", str(SOURCE), "rev-parse", "HEAD"],
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    if source_commit != SOURCE_COMMIT:
        raise ValueError(f"unexpected Foundation source commit: {source_commit}")

    spec = json.loads(PROTOCOL.read_text())
    protocol_sha = sha(PROTOCOL)
    docker_cli, docker_resolved = resolve_docker_cli()
    context = resolve_docker_context(docker_cli)
    DOCKER[:] = [docker_cli, "--context", context]
    image_info = docker(
        "image", "inspect", IMAGE, "--format", "{{.Id}} {{.Os}}/{{.Architecture}}",
        capture_output=True, text=True, timeout=10,
    ).stdout.strip()
    if image_info != f"{IMAGE} linux/arm64":
        raise RuntimeError(f"unexpected OpenFOAM runtime image: {image_info}")

    RUN_ROOT.mkdir(parents=True, exist_ok=False)
    module = RUN_ROOT / "instrumented-module"
    build = RUN_ROOT / "build"
    case = RUN_ROOT / "amr-cap5000"
    build.mkdir()
    EVIDENCE.mkdir(parents=True, exist_ok=False)
    transformer = Path("runtime/openfoam13/instrumentation/prepare_amr_stage_module.py")
    subprocess.run(["python3", str(transformer), str(SOURCE), str(module), "--include-pre-map"], check=True)

    docker_build = [
        "run", "--rm", "--network", "none", "--name", "cans-amr-stage-build",
        "--entrypoint", "/bin/bash",
        "-v", f"{module.resolve()}:/src:ro",
        "-v", f"{build.resolve()}:/out",
        IMAGE, "-lc",
        "source /opt/openfoam13/etc/bashrc && "
        "cp -a /src /tmp/incompressibleFluid && "
        "export FOAM_LIBBIN=/out && "
        "cd /tmp/incompressibleFluid && wmake libso",
    ]
    (build / "build-command.json").write_text(json.dumps([*DOCKER, *docker_build], indent=2) + "\n")
    with (build / "build.log").open("w") as log:
        built = subprocess.run([*DOCKER, *docker_build], stdout=log, stderr=subprocess.STDOUT)
    (build / "build-exit.json").write_text(json.dumps({"exit_code": built.returncode}) + "\n")
    if built.returncode:
        raise RuntimeError(f"instrumented module build failed; preserve {build / 'build.log'}")
    library = build / "libincompressibleFluid.so"
    if not library.is_file():
        raise FileNotFoundError("wmake exited zero without the expected module")

    case_spec = spec["case"]
    generate_amr(
        case, max_cells=case_spec["max_cells"], max_level=case_spec["max_refinement"],
        refine_interval=case_spec["refine_interval"], end=case_spec["end_time"],
        profile="high-gradient", frequency=case_spec["frequency"],
        n=case_spec["initial_grid_cells_per_axis"], dt=case_spec["delta_t"],
    )
    input_hashes = {
        str(path.relative_to(case)): sha(path)
        for path in sorted(case.rglob("*")) if path.is_file()
    }
    (case / "input-hashes.json").write_text(json.dumps(input_hashes, indent=2) + "\n")

    uid = os.getuid()
    name = "cans-amr-same-run-map-v4"
    inner_script = """source /opt/openfoam13/etc/bashrc
export LD_LIBRARY_PATH=/instrumented:$LD_LIBRARY_PATH
cd /case
blockMesh > log.blockMesh 2>&1 || exit $?
LD_DEBUG=libs foamRun > log.foamRun 2>&1
exit_code=$?
exit $exit_code
"""
    inner = (
        f"useradd -o -u {uid} -m runner && "
        f"su runner -s /bin/bash -c {shlex.quote(inner_script)}"
    )
    run_command = [
        *DOCKER, "run", "--rm", "--name", name, "--network", "none",
        "--entrypoint", "/bin/bash",
        "-v", f"{case.resolve()}:/case",
        "-v", f"{library.resolve()}:/instrumented/libincompressibleFluid.so:ro",
        IMAGE, "-lc", inner, "--", str(uid),
    ]
    (case / "run-command.json").write_text(json.dumps(run_command, indent=2) + "\n")
    with (case / "log.container").open("w") as log:
        run = subprocess.run(run_command, stdout=log, stderr=subprocess.STDOUT)
    (case / "exit.json").write_text(json.dumps({"exit_code": run.returncode}) + "\n")
    log_text = (case / "log.foamRun").read_text(errors="replace") if (case / "log.foamRun").exists() else ""
    snapshot_events = [line for line in log_text.splitlines() if "AMR_STAGE_SNAPSHOT" in line]
    library_loaded = "/instrumented/libincompressibleFluid.so" in log_text
    if run.returncode or "End" not in log_text:
        raise RuntimeError(f"instrumented OpenFOAM run did not complete; preserve {case}")
    if not library_loaded:
        raise RuntimeError("LD_DEBUG did not confirm loading the instrumented solver module")
    if len(snapshot_events) != len(STAGES):
        raise RuntimeError(f"expected {len(STAGES)} stage events, observed {len(snapshot_events)}")
    parsed_events = {}
    for event in snapshot_events:
        match = re.search(r"stage=(\w+) time=([0-9.]+) cells=(\d+)", event)
        if not match:
            raise RuntimeError(f"unparseable snapshot event: {event}")
        parsed_events[match[1]] = (match[2], int(match[3]))
    if set(parsed_events) != set(STAGES):
        raise RuntimeError("snapshot stage names differ from the frozen protocol")
    if parsed_events["preMap"] != ("0.002", 4096) or parsed_events["mapped"] != ("0.002", 16640):
        raise RuntimeError("same-time preMap/mapped count gate failed")
    stage_times = {"preMap": "0.002", "mapped": "0.002", "afterCorrectPhi": "0.003",
                   "prePressure": "0.003", "postPressure": "0.003",
                   "postSolve": "0.003"}
    stage_files = [case / "postProcessing" / "amrStages" / stage_times[stage] /
                   f"{stage}_{kind}.csv" for stage in STAGES for kind in ("cells", "faces")]
    missing = [str(path) for path in stage_files if not path.is_file()]
    if missing:
        raise RuntimeError(f"missing stage snapshots: {missing}")

    archive = EVIDENCE / "amr-stage-snapshot.tar.gz"
    with tarfile.open(archive, "w:gz", compresslevel=6) as tf:
        tf.add(case, arcname="amr-cap5000")
    shutil.copy2(build / "build.log", EVIDENCE / "module-build.log")
    shutil.copy2(library, EVIDENCE / "libincompressibleFluid.so")
    shutil.copy2(module / "instrumentation-provenance.json", EVIDENCE / "instrumentation-provenance.json")

    manifest = {
        "status": "RUN_COMPLETE_SAME_RUN_MAP_CAPTURED",
        "source_commit": subprocess.run(
            ["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=True
        ).stdout.strip(),
        "harness_worktree_porcelain": dirty,
        "foundation_source_commit": source_commit,
        "protocol": str(PROTOCOL),
        "protocol_sha256": protocol_sha,
        "container_image_id": IMAGE,
        "docker_cli": docker_cli,
        "docker_cli_resolved": docker_resolved,
        "docker_cli_sha256": sha(Path(docker_resolved)),
        "docker_context": context,
        "docker_cli_version": docker(
            "--version", capture_output=True, text=True, timeout=10
        ).stdout.strip(),
        "instrumented_module_sha256": sha(library),
        "instrumented_source_files": json.loads(
            (module / "instrumentation-provenance.json").read_text()
        )["instrumented_file_sha256"],
        "case_input_sha256": input_hashes,
        "exit_code": run.returncode,
        "end_marker": "End" in log_text,
        "instrumented_library_load_confirmed": library_loaded,
        "snapshot_events": snapshot_events,
        "snapshot_sha256": {str(path.relative_to(case)): sha(path) for path in stage_files},
        "archive": archive.name,
        "archive_sha256": sha(archive),
        "solver_log_sha256": sha(case / "log.foamRun"),
        "limitations": spec["limitations"],
    }
    (EVIDENCE / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps(manifest, indent=2))


DOCKER = []

if __name__ == "__main__":
    main()
