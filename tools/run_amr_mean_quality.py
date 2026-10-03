"""Execute one frozen AMR mean-quality case in an isolated pinned package."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import tarfile

from tools.openfoam_amr_case import generate_amr
from tools.prepare_amr_mean_quality_module import prepare
from tools.run_high_gradient_openfoam import resolve_docker_cli, resolve_docker_context

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT/"protocols/of13-amr-mean-quality-v1.json"
PAYLOAD_AUDIT = ROOT/"evidence/upstream-refresh/of13-amr-stock-payload-hashes-v1.json"
SOURCE_FILES = (
        "tools/run_amr_mean_quality.py", "tools/analyze_amr_mean_quality.py",
        "tools/run_high_gradient_openfoam.py", "requirements-verification-locked.txt",
        "requirements-verification.txt", "requirements.txt",
        "tools/prepare_amr_mean_quality_module.py", "tools/openfoam_amr_case.py",
        "tools/openfoam_case.py", "tools/high_gradient_reference.py",
        "tools/amr_derivative_projection.py", "tools/amr_projection_decomposition.py",
        "tools/high_gradient_cell_average.py", "tools/high_gradient_acceptance.py",
        "runtime/openfoam13/instrumentation/prepare_amr_stage_module.py",
        "runtime/of13-interface-operator/Dockerfile", "runtime/of13-interface-operator/fetch_pinned_package.sh",
        "tools/analyze_amr_gauss_gradient.py", "tools/compare_amr_resolution_volume_integrated.py",
        "evidence/upstream-refresh/of13-amr-stock-payload-hashes-v1.json")


def sha(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def generate_case(path, case_spec, spec):
    model = spec["model"]
    generate_amr(path, max_cells=case_spec["max_cells"], max_level=model["max_refinement"],
                 end=model["end"], profile="high-gradient", frequency=model["frequency"],
                 n=case_spec["n"], dt=case_spec["dt"], refine_interval=case_spec["refine_interval"])
    params = json.loads((path/"parameters.json").read_text())
    if params["nu"] != model["nu"]:
        raise ValueError("case viscosity differs from frozen protocol")
    params["purpose"] = "prospective AMR mean-quality v1; separate from original peak/spectrum gate"
    (path/"parameters.json").write_text(json.dumps(params, indent=2)+"\n")
    return {p.relative_to(path).as_posix(): sha(p) for p in sorted(path.rglob("*")) if p.is_file()}


def run(case_id, image, source, work_root, evidence):
    spec = json.loads(PROTOCOL.read_text())
    case_spec = next(c for c in spec["cases"] if c["id"] == case_id)
    resources = spec["resources"]
    if work_root.exists() or evidence.exists():
        raise FileExistsError("refusing to overwrite prior work/evidence")
    tracked_status = subprocess.check_output(["git", "status", "--porcelain", "--untracked-files=no"],
                                             cwd=ROOT, text=True)
    if tracked_status.strip():
        raise ValueError("commit tracked protocol/harness changes before execution")
    if shutil.disk_usage(ROOT).free < resources["minimum_free_disk_bytes"]:
        raise RuntimeError("STOP_RESOURCE: less than frozen free-disk requirement")
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    cli, resolved = resolve_docker_cli()
    docker = [cli, "--context", resolve_docker_context(cli)]
    image_info = json.loads(subprocess.check_output([*docker, "image", "inspect", image], text=True, timeout=15))[0]
    if image_info["Os"] != "linux" or image_info["Architecture"] != "arm64":
        raise ValueError("wrong runtime architecture")
    work_root.mkdir(parents=True); evidence.mkdir(parents=True)
    module, build = work_root/"module", work_root/"build"
    build.mkdir()
    record = {"schema": "of13-amr-mean-quality-run/v1", "status": "INCOMPLETE",
              "case_id": case_id, "source_commit": head, "protocol_sha256": sha(PROTOCOL),
              "tracked_status": tracked_status, "image": image_info,
              "docker_cli_sha256": sha(resolved), "commands": [], "runs": [],
              "host_free_disk_bytes_at_start": shutil.disk_usage(ROOT).free,
              "package_hash_required_by_recipe": spec["target"]["package_sha256"],
              "scope": "AMR mean-quality experiment; no original peak/spectrum or physical verdict"}
    record["source_files_sha256"] = {p: sha(ROOT/p) for p in SOURCE_FILES}

    manifest = evidence/"manifest.json"
    def save():
        manifest.write_text(json.dumps(record, indent=2)+"\n")
    def command(label, argv, timeout):
        log = evidence/(label+".log")
        entry = {"label": label, "argv": argv, "exit_code": None}
        record["commands"].append(entry); save()
        try:
            with log.open("w") as stream:
                proc = subprocess.run(argv, stdout=stream, stderr=subprocess.STDOUT, timeout=timeout)
            entry["exit_code"] = proc.returncode
        except subprocess.TimeoutExpired:
            entry["timed_out"] = True
            save()
            raise RuntimeError(f"STOP_RESOURCE_TIMEOUT: {label}") from None
        entry["log_sha256"] = sha(log); save()
        if proc.returncode:
            raise RuntimeError(f"command failed: {label}; preserve evidence")
    save()
    try:
        payload = json.loads(PAYLOAD_AUDIT.read_text())
        if (sha(PAYLOAD_AUDIT) != spec["target"]["stock_payload_audit_sha256"]
                or payload["package_sha256"] != spec["target"]["package_sha256"]):
            raise ValueError("stock payload audit names a different package")
        command("package-stock-libraries", [*docker, "run", "--rm", "--network", "none", "--platform", "linux/arm64",
            "--entrypoint", "/usr/bin/sha256sum", image_info["Id"], *payload["stock_library_sha256"]], 120)
        observed = {}
        for line in (evidence/"package-stock-libraries.log").read_text().splitlines():
            match = re.fullmatch(r"([0-9a-f]{64})\s+(/opt/openfoam13/.+)", line)
            if not match or match[2] in observed:
                raise ValueError("malformed/duplicate stock-library checksum row")
            observed[match[2]] = match[1]
        if observed != payload["stock_library_sha256"]:
            raise ValueError("runtime stock libraries differ from official package payloads")
        record["stock_library_payloads_verified"] = len(observed)
        record["instrumentation"] = prepare(source, module, spec)
        command("module-build", [*docker, "run", "--rm", "--network", "none", "--platform", "linux/arm64",
            "--cpus", "3", "--memory", "12g", "--pids-limit", "512", "--entrypoint", "/bin/bash",
            "-v", f"{module}:/src:ro", "-v", f"{build}:/out", image_info["Id"], "-lc",
            "source /opt/openfoam13/etc/bashrc && cp -a /src /tmp/incompressibleFluid && "
            "export FOAM_LIBBIN=/out && cd /tmp/incompressibleFluid && wmake libso"], 600)
        library = build/"libincompressibleFluid.so"
        record["module_library_sha256"] = sha(library)
        shutil.copy2(module/"instrumentation-provenance.json", evidence/"instrumentation-provenance.json")
        for disabled in (False, True) if case_spec["capture_disabled_control"] else (False,):
            label = "disabled-control" if disabled else "main"
            case = work_root/label
            inputs = generate_case(case, case_spec, spec)
            name = "cans-amr-mean-"+case_id.replace(".", "p")+"-"+label
            script = """source /opt/openfoam13/etc/bashrc
export LD_LIBRARY_PATH=/instrumented:$LD_LIBRARY_PATH
cd /case
blockMesh > log.blockMesh 2>&1 || exit $?
LD_DEBUG=libs LD_DEBUG_OUTPUT=/case/log.loader foamRun > log.foamRun 2>&1
exit $?
"""
            inner = f"useradd -o -u {os.getuid()} -m runner && su runner -s /bin/bash -c {shlex.quote(script)}"
            argv = [*docker, "run", "--name", name, "--network", "none", "--platform", "linux/arm64",
                    "--cpus", "3", "--memory", "12g", "--pids-limit", "512", "--entrypoint", "/bin/bash",
                    "-v", f"{case}:/case", "-v", f"{library}:/instrumented/libincompressibleFluid.so:ro"]
            if disabled:
                argv.extend(["-e", "CANS_AMR_CAPTURE_DISABLED=1"])
            argv.extend([image_info["Id"], "-lc", inner])
            try:
                command("container-"+label, argv, resources["case_timeout_seconds"])
            except RuntimeError:
                # Only the uniquely named container created by this task is touched.
                subprocess.run([*docker, "stop", "--time", "10", name], capture_output=True, timeout=30)
                raise
            state = json.loads(subprocess.check_output([*docker, "inspect", name], text=True, timeout=15))[0]["State"]
            if state["Running"] or state["Status"] != "exited" or state["ExitCode"] != 0:
                raise ValueError("container state is not a verified successful exit")
            log = (case/"log.foamRun").read_text()
            loader_paths = sorted(case.glob("log.loader.*"))
            loader_text = "".join(p.read_text() for p in loader_paths)
            if not log.rstrip().endswith("End") or "/instrumented/libincompressibleFluid.so" not in loader_text:
                raise ValueError("missing solver completion/instrumented-library marker")
            events = re.findall(r"AMR_MEAN_QUALITY_SNAPSHOT stage=(\w+) time=([0-9.eE+-]+) cells=(\d+)", log)
            if disabled and events:
                raise ValueError("disabled control produced snapshots")
            if not disabled:
                expected = {"preMap": (.002, case_spec["n"]**3), "mapped": (.002, case_spec["expected_first_mapped_cells"]),
                            "postSolve": (.05, None)}
                if len(events) != 3 or {e[0] for e in events} != set(expected):
                    raise ValueError("wrong snapshot event count/names")
                for stage, time, cells in events:
                    t, count = expected[stage]
                    if float(time) != t or (count is not None and int(cells) != count):
                        raise ValueError("wrong snapshot time/cell count")
            run_record = {"label": label, "inputs_sha256": inputs, "container_state": state,
                          "events": events, "log_sha256": sha(case/"log.foamRun"),
                          "final_field_sha256": {f: sha(case/"0.05"/f) for f in ("U", "p")}}
            record["runs"].append(run_record); save()
            subprocess.run([*docker, "rm", name], check=True, capture_output=True, timeout=15)
        if case_spec["capture_disabled_control"]:
            main, control = record["runs"]
            if main["inputs_sha256"] != control["inputs_sha256"] or main["final_field_sha256"] != control["final_field_sha256"]:
                raise ValueError("snapshot instrumentation changed final U/p or inputs")
            record["disabled_control"] = "BYTE_IDENTICAL_FINAL_U_AND_P"
        else:
            record["disabled_control"] = "INDEPENDENT_N16_CONTROL_REQUIRED_FOR_MATRIX"
        archive_path = evidence/"raw.tar.gz"
        archive_members = {}
        with tarfile.open(archive_path, "w:gz") as archive:
            for run_record in record["runs"]:
                label = run_record["label"]; case = work_root/label
                paths = [case/p for p in run_record["inputs_sha256"]]
                paths += [case/"log.foamRun", case/"log.blockMesh", case/"0.05/U", case/"0.05/p"]
                paths += sorted(case.glob("log.loader.*"))
                if label == "main":
                    paths += sorted((case/"postProcessing/amrStages").rglob("*.csv"))
                for path in sorted(paths):
                    name = label+"/"+path.relative_to(case).as_posix()
                    archive_members[name] = sha(path)
                    archive.add(path, arcname=name, recursive=False)
            for path in sorted(module.rglob("*")):
                if path.is_file():
                    name = "module/"+path.relative_to(module).as_posix()
                    archive_members[name] = sha(path); archive.add(path, arcname=name, recursive=False)
        record["archive"] = {"path": "raw.tar.gz", "sha256": sha(archive_path),
                             "bytes": archive_path.stat().st_size, "members_sha256": archive_members}
        record["status"] = "RUN_COMPLETE_MEASURED_MEAN_QUALITY_INPUTS"; save()
    except Exception as error:
        record["status"] = "STOP_INCOMPLETE"; record["reason"] = str(error); save()
        # Preserve logs even if failure occurs before complete packaging.
        for path in work_root.rglob("log.*"):
            if path.is_file():
                destination = evidence/"partial"/path.relative_to(work_root)
                destination.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(path, destination)
        raise
    return record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case-id", required=True); parser.add_argument("--image", required=True)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--work-root", type=Path, required=True); parser.add_argument("--evidence-root", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.case_id, args.image, args.source.resolve(), args.work_root.resolve(), args.evidence_root.resolve())
    print(json.dumps({"status": result["status"], "case_id": result["case_id"]}))


if __name__ == "__main__":
    main()
