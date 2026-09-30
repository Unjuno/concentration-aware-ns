"""Run a preregistered paired-seed PhysicsNeMo sampling-robustness control."""
import argparse
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path, PurePosixPath
import platform
import subprocess
import sys
import tarfile
import time


ROOT = Path(__file__).resolve().parents[1]


def validate_plan(plan):
    seeds = plan.get("seeds")
    cases = plan.get("cases")
    reference_seed = plan.get("reference_seed")
    if not isinstance(seeds, list) or not seeds:
        raise ValueError("seeds must be a nonempty list")
    if any(not isinstance(seed, int) or isinstance(seed, bool) for seed in seeds):
        raise ValueError("seeds must be integers")
    if len(set(seeds)) != len(seeds):
        raise ValueError("seeds must be unique")
    if reference_seed not in seeds:
        raise ValueError("reference seed must be included in seeds")
    if len(seeds) < 2:
        raise ValueError("at least one new seed is required")
    if not isinstance(cases, list) or not cases:
        raise ValueError("cases must be a nonempty list")
    normalized = []
    for case in cases:
        if not isinstance(case, list) or len(case) != 2:
            raise ValueError("each case must be [n, time_nodes]")
        n, time_nodes = case
        if any(not isinstance(x, int) or isinstance(x, bool) for x in case):
            raise ValueError("case dimensions must be integers")
        if n < 4:
            raise ValueError("n must be at least 4")
        if time_nodes < 2:
            raise ValueError("time_nodes must be at least 2")
        normalized.append((n, time_nodes))
    if len(set(normalized)) != len(normalized):
        raise ValueError("cases must be unique")


def expand_runs(plan):
    validate_plan(plan)
    return [
        {"seed": seed, "n": n, "time_nodes": time_nodes}
        for seed in plan["seeds"]
        if seed != plan["reference_seed"]
        for n, time_nodes in plan["cases"]
    ]


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def sha256_file(path):
    return sha256_bytes(Path(path).read_bytes())


def _local_tree(root):
    root = Path(root)
    entries = {}
    for path in root.rglob("*"):
        rel = path.relative_to(root).as_posix()
        if path.is_symlink():
            entries[rel] = ("symlink", os.readlink(path))
        elif path.is_file():
            entries[rel] = ("file", sha256_file(path))
    return entries


def _is_allowed_python_cache(path):
    return "__pycache__" in PurePosixPath(path).parts or path.endswith(".pyc")


def verify_source_tree(archive, source_root, expected_archive_sha256):
    archive = Path(archive)
    source_root = Path(source_root)
    archive_sha256 = sha256_file(archive)
    if archive_sha256 != expected_archive_sha256:
        raise ValueError("source archive hash mismatch")
    local = _local_tree(source_root)
    archived = {}
    with tarfile.open(archive, "r:gz") as tar:
        members = tar.getmembers()
        prefix = next((m.name.split("/", 1)[0] + "/" for m in members if m.name), None)
        if prefix is None:
            raise ValueError("source archive is empty")
        for member in members:
            if not member.name.startswith(prefix) or member.isdir():
                continue
            rel = member.name[len(prefix):]
            if not rel:
                continue
            if member.isfile():
                stream = tar.extractfile(member)
                archived[rel] = ("file", sha256_bytes(stream.read()))
            elif member.issym():
                archived[rel] = ("symlink", member.linkname)
            else:
                raise ValueError(f"unsupported source archive entry: {rel}")
    missing = sorted(set(archived) - set(local))
    changed = sorted(k for k in archived.keys() & local.keys() if archived[k] != local[k])
    extras = sorted(set(local) - set(archived))
    forbidden_extras = [p for p in extras if not _is_allowed_python_cache(p)]
    if missing or changed or forbidden_extras:
        raise ValueError(
            "source mismatch: "
            f"missing={len(missing)}, changed={len(changed)}, "
            f"forbidden_extras={len(forbidden_extras)}"
        )
    return {
        "archive_sha256": archive_sha256,
        "archive_files": len(archived),
        "matching_files": len(archived) - sum(1 for k in archived if archived[k][0] == "symlink"),
        "matching_symlinks": sum(1 for v in archived.values() if v[0] == "symlink"),
        "missing_files": len(missing),
        "changed_files": len(changed),
        "allowed_extra_files": len(extras),
        "allowed_extra_examples": extras[:12],
    }


def _write_json(path, value):
    Path(path).write_text(json.dumps(value, indent=2) + "\n")


def _archive_case(case_root, archive_path):
    archive_path = Path(archive_path)
    archive_path.parent.mkdir(parents=True, exist_ok=True)
    with tarfile.open(archive_path, "w:gz") as tar:
        for path in sorted(Path(case_root).iterdir()):
            tar.add(path, arcname=path.name)
    return sha256_file(archive_path)


def run(protocol_path, source_archive, source_root, work_root, archive_root):
    protocol_path = Path(protocol_path)
    if not protocol_path.is_absolute():
        protocol_path = ROOT / protocol_path
    protocol = json.loads(protocol_path.read_text())
    validate_plan(protocol)
    if protocol.get("status") != "frozen-before-execution":
        raise ValueError("protocol must be frozen-before-execution")
    if platform.python_version() != protocol["environment"]["python"]:
        raise ValueError("Python version does not match frozen environment")
    if importlib.metadata.version("torch") != protocol["environment"]["torch"]:
        raise ValueError("Torch version does not match frozen environment")
    baseline_path = ROOT / protocol["baseline_protocol"]["path"]
    if sha256_file(baseline_path) != protocol["baseline_protocol"]["sha256"]:
        raise ValueError("baseline protocol hash mismatch")
    baseline = json.loads(baseline_path.read_text())
    if baseline["base"]["seed"] != protocol["reference_seed"]:
        raise ValueError("baseline seed does not match reference seed")
    if baseline["base"]["source_commit"] != protocol["source"]["commit"]:
        raise ValueError("baseline source commit does not match protocol")
    for path_name, path in (("source archive", source_archive), ("source root", source_root)):
        resolved = Path(path)
        if not resolved.is_absolute():
            resolved = ROOT / resolved
        if path_name == "source archive":
            source_archive = resolved
        else:
            source_root = resolved
    tree_check = verify_source_tree(
        source_archive, source_root, protocol["source"]["archive_sha256"]
    )
    if tree_check["matching_files"] != protocol["source"]["expected_regular_files"]:
        raise ValueError("source archive regular-file count does not match protocol")
    status = subprocess.run(
        ["git", "status", "--porcelain"], cwd=ROOT, text=True, capture_output=True, check=True
    ).stdout
    if status.strip():
        raise ValueError("repository worktree must be clean before starting the frozen study")
    harness_commit = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, capture_output=True, check=True
    ).stdout.strip()

    work_root = Path(work_root)
    archive_root = Path(archive_root)
    if not work_root.is_absolute():
        work_root = ROOT / work_root
    if not archive_root.is_absolute():
        archive_root = ROOT / archive_root
    work_root = work_root.resolve()
    archive_root = archive_root.resolve()
    work_root.mkdir(parents=True, exist_ok=False)
    archive_root.mkdir(parents=True, exist_ok=False)
    protocol_sha256 = sha256_file(protocol_path)
    (archive_root / "protocol.json").write_bytes(protocol_path.read_bytes())
    rows = []
    manifest = {
        "study_id": protocol["study_id"],
        "status": "IN_PROGRESS",
        "protocol_sha256": protocol_sha256,
        "baseline_protocol_sha256": protocol["baseline_protocol"]["sha256"],
        "source_commit": protocol["source"]["commit"],
        "harness_commit": harness_commit,
        "source_tree_check": tree_check,
        "environment": {
            "python": sys.version,
            "torch": importlib.metadata.version("torch"),
            "platform": platform.platform(),
            "device": "cpu",
        },
        "expected_runs": len(expand_runs(protocol)),
        "completed_runs": 0,
        "runs": rows,
    }
    manifest_path = archive_root / "summary.json"

    def save():
        manifest["completed_runs"] = len(rows)
        _write_json(manifest_path, manifest)

    save()
    env = os.environ.copy()
    old_pythonpath = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = str(Path(source_root).resolve()) + (os.pathsep + old_pythonpath if old_pythonpath else "")
    base_config = baseline["base"]
    for spec in expand_runs(protocol):
        seed, n, time_nodes = spec["seed"], spec["n"], spec["time_nodes"]
        label = f"seed{seed}-n{n}-nt{time_nodes}"
        run_root = work_root / "runs" / label
        run_root.parent.mkdir(parents=True, exist_ok=True)
        config = {**base_config, "seed": seed, "n": n, "time_nodes": time_nodes}
        config["scope"] = protocol["question"] + " Fixed optimization budget; descriptive seed control only."
        config_path = work_root / f"{label}.json"
        _write_json(config_path, config)
        run_rel = run_root.relative_to(ROOT)
        config_rel = config_path.relative_to(ROOT)
        command = [
            sys.executable,
            "-m",
            "tools.train_physicsnemo_pilot",
            "--protocol",
            str(config_rel),
            "--output",
            str(run_rel),
        ]
        log_path = work_root / f"{label}.log"
        print(f"START {label}", flush=True)
        start = time.monotonic()
        with log_path.open("w") as log:
            result = subprocess.run(command, cwd=ROOT, env=env, stdout=log, stderr=subprocess.STDOUT)
        elapsed = time.monotonic() - start
        if run_root.exists():
            (run_root / "console.log").write_bytes(log_path.read_bytes())
            _write_json(run_root / "command.json", {
                "command": ["python", *command[1:]],
                "cwd": ".",
                "runner_protocol_sha256": protocol_sha256,
            })
            (run_root / "exit_code").write_text(f"{result.returncode}\n")
        if result.returncode != 0:
            row = {**spec, "case": label, "exit_code": result.returncode, "elapsed_seconds": elapsed}
            rows.append(row)
            manifest["status"] = "INCOMPLETE"
            manifest["failed_run"] = label
            save()
            print(f"FAIL {label}: exit {result.returncode}; work outputs retained", flush=True)
            return 1
        diagnostics = json.loads((run_root / "diagnostics.json").read_text())
        gradient_command = [
            sys.executable,
            "-m",
            "tools.analyze_physicsnemo_gradient",
            str(run_rel),
        ]
        gradient_log = work_root / f"{label}-gradient.json"
        with gradient_log.open("w") as out:
            gradient_result = subprocess.run(
                gradient_command, cwd=ROOT, env=env, stdout=out, stderr=subprocess.STDOUT
            )
        if gradient_result.returncode != 0:
            manifest["status"] = "INCOMPLETE"
            manifest["failed_run"] = label + "-gradient-audit"
            _write_json(run_root / "gradient-audit-failure.json", {"returncode": gradient_result.returncode})
            save()
            return 1
        gradient = json.loads(gradient_log.read_text())
        _write_json(run_root / "gradient.json", gradient)
        log_rows = [json.loads(line) for line in (run_root / "training.jsonl").read_text().splitlines() if line]
        archive_rel = archive_root / f"{label}.tar.gz"
        archive_hash = _archive_case(run_root, archive_rel)
        rows.append({
            **spec,
            "case": label,
            "exit_code": 0,
            "elapsed_seconds": elapsed,
            "final_training_loss": log_rows[-1]["loss"],
            "velocity_relative_l2": diagnostics["velocity_relative_l2"],
            "gradient_peak_relative_error_samples": gradient["gradient_peak_relative_error_samples"],
            "vorticity_peak_relative_error_samples": gradient["vorticity_peak_relative_error_samples"],
            "archive": archive_rel.name,
            "archive_sha256": archive_hash,
            "archive_bytes": archive_rel.stat().st_size,
        })
        save()
        print(f"END {label} velocity_rel_l2={diagnostics['velocity_relative_l2']:.8g}", flush=True)
    manifest["status"] = "COMPLETE"
    save()
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--protocol", default="protocols/physicsnemo-seed-control-v1.json")
    parser.add_argument("--source-archive", required=True)
    parser.add_argument("--source-root", required=True)
    parser.add_argument("--work-root", required=True)
    parser.add_argument("--archive-root", required=True)
    args = parser.parse_args()
    return run(args.protocol, args.source_archive, args.source_root, args.work_root, args.archive_root)


if __name__ == "__main__":
    raise SystemExit(main())
