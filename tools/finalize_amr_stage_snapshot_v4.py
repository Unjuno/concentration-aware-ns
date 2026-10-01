"""Recover/validate the v4 manifest from preserved run and archive artifacts."""
import hashlib
import json
import os
import re
import tarfile
from pathlib import Path


RUN_ROOT = Path(os.environ.get("CANS_AMR_STAGE_RUN_ROOT", "work/of13-amr-same-run-map-v4-run3"))
EVIDENCE = Path(os.environ.get("CANS_AMR_STAGE_EVIDENCE", "evidence/of13-amr-same-run-map-v4-run3"))
PROTOCOL = Path(os.environ.get(
    "CANS_AMR_STAGE_PROTOCOL", "protocols/high-gradient-of13-amr-same-run-map-v4.json"
))
SOURCE_COMMIT = "18870c24d21c6b982e2cdec27b2f59738cca5f90"
IMAGE = "sha256:dd2b2eb63b12896a9b6e7a46563ed96b26d1c78c3e3749536d40d456895f722b"
STAGES = ("preMap", "mapped", "afterCorrectPhi", "prePressure", "postPressure", "postSolve")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    spec = json.loads(PROTOCOL.read_text())
    case_spec = spec["case"]
    case = RUN_ROOT / case_spec.get("case_directory", "amr-cap5000")
    log_path = case / "log.foamRun"
    archive = EVIDENCE / case_spec.get("archive_name", "amr-stage-snapshot.tar.gz")
    log = log_path.read_text(errors="replace")
    events = [line.strip() for line in log.splitlines() if "AMR_STAGE_SNAPSHOT" in line]
    if len(events) != len(STAGES) or "End" not in log:
        raise ValueError("run does not have six snapshot events and normal End")
    if not (case / "exit.json").is_file() or json.loads((case / "exit.json").read_text())["exit_code"] != 0:
        raise ValueError("run exit status is missing or nonzero")
    if not archive.is_file() or not (EVIDENCE / "libincompressibleFluid.so").is_file():
        raise ValueError("archive or instrumented library is missing")
    if "/instrumented/libincompressibleFluid.so" not in log:
        raise ValueError("instrumented library load path not found in solver log")
    events_by_name = {}
    for event in events:
        match = re.search(r"stage=(\w+) time=([0-9.]+) cells=(\d+)", event)
        if not match:
            raise ValueError(f"unparseable event: {event}")
        events_by_name[match[1]] = (match[2], int(match[3]))
    if set(events_by_name) != set(STAGES):
        raise ValueError("snapshot stage names differ from protocol")
    pre_map_time = f"{case_spec.get('pre_map_time', 0.002):g}"
    if events_by_name["preMap"] != (pre_map_time, case_spec["initial_cells"]):
        raise ValueError("same-time preMap cell-count gate failed")
    if events_by_name["mapped"] != (
        pre_map_time, case_spec.get("expected_mapped_cells", 16640)
    ):
        raise ValueError("same-time preMap/mapped cell-count gate failed")

    snapshot_hashes = {}
    stage_times = {
        "preMap": pre_map_time, "mapped": pre_map_time,
        **{stage: f"{case_spec.get('solver_stage_time', 0.003):g}"
           for stage in STAGES if stage not in ("preMap", "mapped")},
    }
    for stage in STAGES:
        for kind in ("cells", "faces"):
            rel = Path("postProcessing/amrStages") / stage_times[stage] / f"{stage}_{kind}.csv"
            if not (case / rel).is_file():
                raise ValueError(f"missing snapshot file: {rel}")
            snapshot_hashes[rel.as_posix()] = sha(case / rel)

    run_cmd_path = case / "run-command.json"
    run_command = json.loads(run_cmd_path.read_text())
    docker_cli = run_command[0]
    docker_resolved = os.path.realpath(docker_cli)
    result = {
        "status": "RUN_COMPLETE_SAME_RUN_MAP_CAPTURED",
        "run_manifest_recovered_posthoc": True,
        "harness_commit": "1fcce026c8751dc73e837dc1a95064933f4d4b5b",
        "harness_worktree_status_at_execution": "not serialized by the original runner after its post-run KeyError; current status cannot substitute for historical state",
        "foundation_source_commit": SOURCE_COMMIT,
        "protocol": PROTOCOL.as_posix(),
        "protocol_sha256_at_execution": None,
        "protocol_sha256_current_at_manifest_recovery": sha(PROTOCOL),
        "protocol_hash_limitation": "The original runner computed the protocol hash but raised before serializing its manifest; the tracked protocol was augmented afterward with analysis criteria and a complete limitations field. Do not treat the current file hash as the exact at-run hash.",
        "container_image_id": IMAGE,
        "docker_cli": docker_cli,
        "docker_cli_resolved": docker_resolved,
        "docker_cli_sha256": sha(Path(docker_resolved)),
        "docker_context": "orbstack",
        "container_platform": "linux/arm64",
        "instrumented_module_sha256": sha(EVIDENCE / "libincompressibleFluid.so"),
        "instrumented_source_files": json.loads((EVIDENCE / "instrumentation-provenance.json").read_text())["instrumented_file_sha256"],
        "case_input_sha256": json.loads((case / "input-hashes.json").read_text()),
        "exit_code": 0,
        "end_marker": True,
        "instrumented_library_load_confirmed": True,
        "snapshot_events": events,
        "case_directory": case.name,
        "stage_times": stage_times,
        "snapshot_sha256": snapshot_hashes,
        "archive": archive.name,
        "archive_sha256": sha(archive),
        "solver_log_sha256": sha(log_path),
        "module_build_log_sha256": sha(EVIDENCE / "module-build.log"),
        "limitations": json.loads(PROTOCOL.read_text())["limitations"],
        "recovery_note": "The solver and tar archive completed successfully, but the runner raised KeyError after archiving because the initial protocol omitted the limitations key. This manifest was reconstructed from the preserved logs, exit.json, hashes, and archive; no solver rerun was used."
    }
    (EVIDENCE / "manifest.json").write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
