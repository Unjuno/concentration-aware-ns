"""Run one frozen operator probe, retaining its container and raw evidence.

Run completion describes process/output integrity only.  Scientific analysis
is a separate step and this runner never reports a numerical-quality PASS.
"""

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import stat
import subprocess
import sys
import tarfile
import uuid


REPOSITORY = Path(__file__).resolve().parents[1]
EXPECTED_OUTPUTS = (
    "probe/arithmetic/before.json", "probe/arithmetic/after.json",
    "probe/harmonic/before.json", "probe/harmonic/after.json",
    "probe/constant/before.json",
)
END_MARKER = "INTERFACE_OPERATOR_PROBE_COMPLETE"


class StopRun(RuntimeError):
    """An incomplete execution that must retain its evidence."""


def now():
    return datetime.now(timezone.utc).isoformat()


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path, value):
    path = Path(path)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True, allow_nan=False)
                         + "\n", encoding="utf-8")
    temporary.replace(path)


def is_regular(path):
    try:
        return stat.S_ISREG(Path(path).lstat().st_mode)
    except FileNotFoundError:
        return False


def reject_json_constant(value):
    raise ValueError(f"nonstandard JSON constant {value}")


def regular_files(root):
    """Return regular files without following directory or file symlinks."""
    files, excluded = [], []
    for directory, names, leaves in os.walk(root, followlinks=False):
        names.sort()
        leaves.sort()
        for name in list(names):
            path = Path(directory) / name
            if path.is_symlink():
                excluded.append(path.relative_to(root).as_posix())
                names.remove(name)
        for name in leaves:
            path = Path(directory) / name
            if stat.S_ISREG(path.lstat().st_mode):
                files.append(path)
            else:
                excluded.append(path.relative_to(root).as_posix())
    return sorted(files), sorted(excluded)


class Recorder:
    def __init__(self, root, manifest):
        self.root = root
        self.manifest = manifest
        (root / "command-logs").mkdir()
        self.progress()

    def progress(self):
        write_json(self.root / "run-manifest-progress.json", self.manifest)

    def command(self, argv, label, *, timeout=15, combined_log=None):
        row = {"argv": list(argv), "label": label, "started_at": now(),
               "timeout_seconds": timeout}
        self.manifest["commands"].append(row)
        self.manifest["phase"] = label
        self.progress()
        stem = f"{len(self.manifest['commands']):02d}-{label}"
        stdout_path = self.root / "command-logs" / f"{stem}.stdout"
        stderr_path = self.root / "command-logs" / f"{stem}.stderr"
        try:
            if combined_log is not None:
                row["combined_log"] = combined_log.relative_to(self.root).as_posix()
                with combined_log.open("wb") as stream:
                    result = subprocess.run(argv, cwd=REPOSITORY, stdout=stream,
                                            stderr=subprocess.STDOUT, timeout=timeout)
                output, error = b"", b""
            else:
                result = subprocess.run(argv, cwd=REPOSITORY, capture_output=True,
                                        timeout=timeout)
                output, error = result.stdout, result.stderr
                stdout_path.write_bytes(output)
                stderr_path.write_bytes(error)
                row["stdout_file"] = stdout_path.relative_to(self.root).as_posix()
                row["stderr_file"] = stderr_path.relative_to(self.root).as_posix()
            row["return_code"] = result.returncode
            return result.returncode, output.decode("utf-8", errors="replace")
        except subprocess.TimeoutExpired as error:
            stdout_path.write_bytes(error.stdout or b"")
            stderr_path.write_bytes(error.stderr or b"")
            row.update({"error": "timeout", "stdout_file": stdout_path.relative_to(self.root).as_posix(),
                        "stderr_file": stderr_path.relative_to(self.root).as_posix()})
            raise StopRun(f"{label} exceeded its {timeout}s API timeout") from error
        except (OSError, KeyboardInterrupt) as error:
            row["error"] = f"{type(error).__name__}: {error}"
            raise
        finally:
            row["finished_at"] = now()
            self.progress()

    def checked(self, argv, label):
        code, output = self.command(argv, label)
        if code:
            raise StopRun(f"{label} exited {code}; command logs are preserved")
        return output


def destination(path):
    candidate = Path(path).expanduser()
    if candidate.exists() or candidate.is_symlink():
        raise ValueError(f"refusing to overwrite existing destination: {candidate}")
    return candidate.resolve()


def validate_protocol(spec):
    inputs = spec["inputs"]
    expected = {"nx": [16, 32, 64], "ny": 2, "nz": 2, "density": 1,
                "mu_left": 1, "mu_right": 100, "traction": 1}
    if any(inputs.get(key) != value for key, value in expected.items()):
        raise StopRun("protocol inputs differ from the frozen 16/32/64, rho1, mu1/100, tau1 control")
    return inputs


def inspect_container(recorder, docker, manifest):
    cidfile = recorder.root / "container-id"
    requested = cidfile.read_text().strip() if cidfile.is_file() else manifest["container_name"]
    if cidfile.is_file():
        manifest["container_id"] = requested
    code, output = recorder.command([*docker, "inspect", "--type", "container", requested],
                                    "container-inspect")
    if code:
        manifest["container_inspection_error"] = f"docker inspect exited {code}"
        return
    records = json.loads(output)
    if len(records) != 1:
        raise StopRun("container inspection did not identify one container")
    info = records[0]
    manifest["container_id"] = info["Id"]
    manifest["container_state"] = info["State"]
    manifest["container_image_id"] = info["Image"]
    if cidfile.is_file() and requested != info["Id"]:
        raise StopRun("recorded container ID differs from inspected container ID")


def prepare_and_run(recorder, args):
    manifest = recorder.manifest
    protocol_path = Path(args.protocol).expanduser()
    if not protocol_path.is_absolute():
        protocol_path = REPOSITORY / protocol_path
    protocol_path = protocol_path.resolve(strict=True)
    protocol_relative = protocol_path.relative_to(REPOSITORY).as_posix()
    protocol_bytes = protocol_path.read_bytes()
    manifest["protocol"] = {"path": protocol_relative, "sha256": sha256(protocol_path)}
    (recorder.root / "protocol-frozen.json").write_bytes(protocol_bytes)
    spec = json.loads(protocol_bytes)
    manifest["protocol"]["content"] = spec
    inputs = validate_protocol(spec)
    manifest["git_head"] = recorder.checked(["git", "rev-parse", "HEAD"], "git-head").strip()
    tracked_status = recorder.checked(
        ["git", "status", "--porcelain=v1", "--untracked-files=no"], "git-tracked-status")
    manifest["tracked_status"] = tracked_status
    if tracked_status.strip():
        raise StopRun("tracked Git state is dirty; commit the frozen sources before execution")
    tracked_protocol = recorder.checked(
        ["git", "show", f"{manifest['git_head']}:{protocol_relative}"], "git-protocol-blob")
    if tracked_protocol.encode("utf-8") != protocol_bytes:
        raise StopRun("protocol bytes differ from the recorded Git HEAD blob")
    manifest["protocol"]["head_blob_verified"] = True

    utility = REPOSITORY / "runtime/of13-interface-operator"
    source_paths, excluded = regular_files(utility)
    if excluded:
        raise StopRun("utility source contains symlinks or nonregular files")
    required = {"interfaceOperatorProbe.C", "Make/files", "Make/options", "run_cases.sh"}
    if not required.issubset({path.relative_to(utility).as_posix() for path in source_paths}):
        raise StopRun("utility source or its runtime script is incomplete")
    source_paths.extend([Path(__file__).resolve(), REPOSITORY / "tools/build_interface_operator_cases.py",
                         REPOSITORY / "tools/analyze_interface_operator_probe.py",
                         REPOSITORY / spec["target"]["runtime_recipe"],
                         REPOSITORY / "requirements-interface-operator.txt",
                         REPOSITORY / ".github/workflows/interface-operator.yml", protocol_path])
    source_paths = sorted(set(source_paths))
    source_names = [path.relative_to(REPOSITORY).as_posix() for path in source_paths]
    recorder.checked(["git", "ls-files", "--error-unmatch", "--", *source_names],
                     "git-source-tracked")
    manifest["source_files_sha256"] = {name: sha256(path)
                                        for name, path in zip(source_names, source_paths)}

    requested_cli = os.environ.get("CANS_DOCKER_CLI")
    if requested_cli and not Path(requested_cli).is_absolute():
        raise StopRun("CANS_DOCKER_CLI must be an absolute path")
    docker_cli = requested_cli or shutil.which("docker")
    if not docker_cli:
        raise StopRun("docker CLI was not found on PATH")
    resolved_cli = Path(docker_cli).resolve(strict=True)
    if not resolved_cli.is_file() or not os.access(resolved_cli, os.X_OK):
        raise StopRun("docker CLI is not an executable regular file")
    manifest["docker_cli"] = {"path": str(docker_cli), "resolved_path": str(resolved_cli),
                              "sha256": sha256(resolved_cli)}
    context = os.environ.get("CANS_DOCKER_CONTEXT") or recorder.checked(
        [str(docker_cli), "context", "show"], "docker-context").strip()
    if not context.strip():
        raise StopRun("Docker context is empty")
    manifest["docker_context"] = context
    docker = [str(docker_cli), "--context", context]
    manifest["docker_version"] = json.loads(recorder.checked(
        [*docker, "version", "--format", "{{json .}}"], "docker-version"))
    image_records = json.loads(recorder.checked(
        [*docker, "image", "inspect", args.image], "image-inspect"))
    if len(image_records) != 1:
        raise StopRun("image inspection did not identify exactly one local image")
    image = image_records[0]
    manifest["image_requested"] = args.image
    manifest["image_inspect"] = image
    if image.get("Os") != "linux" or image.get("Architecture") != "arm64":
        raise StopRun("operator probe requires an existing linux/arm64 image")
    image_id = image["Id"]
    if not image_id.startswith("sha256:") or len(image_id) != 71:
        raise StopRun("image inspection did not return a content-addressed image ID")
    manifest["resolved_image_id"] = image_id

    shutil.copytree(utility, recorder.root / "app")
    # Import the case builder only after provenance and image preflight.
    from tools.build_interface_operator_cases import build_cases
    cases = build_cases(recorder.root / "cases", nx_values=inputs["nx"],
                        mu_left=inputs["mu_left"], mu_right=inputs["mu_right"],
                        traction=inputs["traction"])
    manifest["case_input_hashes"] = {
        f"nx{row['inputs']['nx']}": {"inputs_sha256": row["inputs_sha256"],
                                    "files_sha256": row["files_sha256"],
                                    "metadata_sha256": sha256(recorder.root / "cases" /
                                                             f"nx{row['inputs']['nx']}" /
                                                             "case_metadata.json")}
        for row in cases
    }
    manifest["container_name"] = ("cans-interface-operator-" + manifest["git_head"][:12]
                                    + "-" + uuid.uuid4().hex[:12])
    command = [
        *docker, "run", "--pull=never", "--name", manifest["container_name"],
        "--cidfile", str(recorder.root / "container-id"), "--network", "none",
        "--cpus", "2", "--memory", "2g", "--pids-limit", "512",
        "--platform", "linux/arm64", "--entrypoint", "/bin/bash",
        "-v", f"{recorder.root}:/probe", image_id, "/probe/app/run_cases.sh",
    ]
    write_json(recorder.root / "container-command.json", command)
    # Compilation and the live probe have no global deadline.  Only short
    # engine/API observations use the bounded timeout above.
    try:
        code, _ = recorder.command(command, "container-run", timeout=None,
                                   combined_log=recorder.root / "container.log")
        manifest["docker_run_exit_code"] = code
    finally:
        inspect_container(recorder, docker, manifest)

    state = manifest.get("container_state", {})
    if (code != 0 or state.get("Status") != "exited" or state.get("Running")
            or state.get("ExitCode") != 0):
        raise StopRun("container did not exit cleanly with verified zero process/engine exit codes")
    if manifest.get("container_image_id") != image_id:
        raise StopRun("container image ID differs from the inspected image")
    marker = recorder.root / "COMPLETED"
    if not is_regular(marker) or marker.read_text().strip() != "RUN_CASES_COMPLETE":
        raise StopRun("runtime completion marker is missing")
    binary = recorder.root / "interfaceOperatorProbe"
    if not is_regular(binary) or not os.access(binary, os.X_OK):
        raise StopRun("compiled utility binary is missing or not executable")
    manifest["utility_binary_sha256"] = sha256(binary)
    runtime_logs = ("runtime-environment.log", "package-inventory.log", "linked-libraries.log",
                    "binary-sha256.txt", "build.log", "package-source-sha256.log",
                    "linked-library-sha256.log")
    if any(not is_regular(recorder.root / name) for name in runtime_logs):
        raise StopRun("build or package/runtime provenance logs are missing")
    manifest["runtime_logs_sha256"] = {name: sha256(recorder.root / name) for name in runtime_logs}
    observations = {}
    for nx in inputs["nx"]:
        case = recorder.root / "cases" / f"nx{nx}"
        log = case / "log.interfaceOperatorProbe"
        marked = is_regular(log) and log.read_text(errors="replace").rstrip().endswith(END_MARKER)
        missing = [name for name in EXPECTED_OUTPUTS if not is_regular(case / name)
                   or (case / name).stat().st_size == 0]
        observations[f"nx{nx}"] = {"end_marker_verified": marked, "missing_outputs": missing}
        manifest["case_output_integrity"] = observations
        if missing or not marked:
            raise StopRun(f"nx{nx} lacks expected JSON outputs or its final completion marker")
        for name in EXPECTED_OUTPUTS:
            with (case / name).open() as stream:
                json.load(stream, parse_constant=reject_json_constant)
    manifest["status"] = "RUN_COMPLETE_OPERATOR_ONLY"
    manifest["disposition"] = "COMPLETE"


def run(args):
    work = destination(args.work_root)
    evidence = destination(args.evidence_root)
    if work == evidence or work in evidence.parents or evidence in work.parents:
        raise ValueError("work and evidence destinations must be disjoint")
    work.mkdir(parents=True, exist_ok=False)
    evidence.mkdir(parents=True, exist_ok=False)
    manifest = {
        "schema": "of13-interface-operator-run/v1", "status": "INCOMPLETE",
        "disposition": "STOP", "scientific_quality": "NOT_ASSESSED",
        "started_at": now(), "runner_argv": list(getattr(sys, "orig_argv", [sys.executable, *sys.argv])),
        "image_requested": args.image,
        "work_root": str(work), "evidence_root": str(evidence), "commands": [],
        "environment": {
            "python": sys.version, "executable": sys.executable,
            "platform": platform.platform(), "machine": platform.machine(),
            "cwd": str(Path.cwd()), "uid": os.getuid(), "gid": os.getgid(),
            "variables": {key: os.environ[key] for key in (
                "PATH", "LANG", "LC_ALL", "TZ", "CANS_DOCKER_CLI", "CANS_DOCKER_CONTEXT"
            ) if key in os.environ},
        },
    }
    recorder = Recorder(work, manifest)
    try:
        prepare_and_run(recorder, args)
    except (Exception, KeyboardInterrupt) as error:
        manifest["stop_reason"] = f"{type(error).__name__}: {error}"
    manifest["finished_at"] = now()
    recorder.progress()
    files, excluded = regular_files(work)
    manifest["excluded_nonregular_paths"] = excluded
    manifest["work_files_sha256"] = {path.relative_to(work).as_posix(): sha256(path)
                                      for path in files}
    archive_path = evidence / "raw.tar.gz"
    with tarfile.open(archive_path, "w:gz", dereference=True) as archive:
        for path in files:
            archive.add(path, arcname=path.relative_to(work).as_posix(), recursive=False)
    manifest["archive"] = {"path": "raw.tar.gz", "sha256": sha256(archive_path),
                           "regular_file_count": len(files)}
    manifest["container_retained"] = bool(manifest.get("container_id"))
    write_json(evidence / "run-manifest.json", manifest)
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--image", required=True)
    parser.add_argument("--work-root", default="work/of13-interface-operator-v1")
    parser.add_argument("--evidence-root", default="evidence/of13-interface-operator-v1")
    parser.add_argument("--protocol", default="protocols/of13-interface-operator-v1.json")
    args = parser.parse_args()
    try:
        result = run(args)
    except (OSError, ValueError) as error:
        print(json.dumps({"status": "STOP", "reason": str(error)}), file=sys.stderr)
        return 2
    print(json.dumps({key: result[key] for key in (
        "status", "disposition", "scientific_quality", "work_root", "evidence_root"
    )}, sort_keys=True))
    return 0 if result["status"] == "RUN_COMPLETE_OPERATOR_ONLY" else 2


if __name__ == "__main__":
    raise SystemExit(main())
