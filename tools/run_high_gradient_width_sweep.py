"""Run the frozen Foundation 13 envelope-width space/time matrix once."""
import argparse
import hashlib
import json
import math
import os
import re
import subprocess
import tarfile
from pathlib import Path

from tools.analyze_openfoam import analyze
from tools.audit_high_gradient_width_sweep import audit as audit_reference
from tools.run_high_gradient_openfoam import resolve_docker_cli, resolve_docker_context


def digest(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def build_cases(protocol):
    if protocol.get("version") != "width-v1":
        raise ValueError("unsupported high-gradient width protocol")
    powers = protocol.get("envelope_powers")
    spatial = protocol.get("spatial_matrix", {})
    temporal = protocol.get("temporal_matrix", {})
    counts, dts = spatial.get("cell_counts"), temporal.get("delta_t")
    if (not isinstance(powers, list) or not powers
            or any(type(m) is not int or m < 1 for m in powers)
            or len(set(powers)) != len(powers)):
        raise ValueError("envelope_powers must be distinct positive integers")
    if (not isinstance(counts, list) or not counts
            or any(type(n) is not int or n < 4 for n in counts)
            or len(set(counts)) != len(counts)):
        raise ValueError("spatial cell_counts must be distinct integers >= 4")
    n_temporal = temporal.get("cell_count")
    if type(n_temporal) is not int or n_temporal < 4 or not isinstance(dts, list) or len(dts) < 2:
        raise ValueError("invalid temporal matrix")
    nu, end = float(protocol["viscosity"]), float(protocol["end_time"])
    if not math.isfinite(nu) or nu <= 0 or not math.isfinite(end) or end <= 0:
        raise ValueError("viscosity and end_time must be finite and positive")

    pairs = []
    seen_pairs = set()
    for n in counts:
        pair = (n, float(spatial["delta_t"]))
        if pair not in seen_pairs:
            pairs.append((*pair, "spatial"))
            seen_pairs.add(pair)
    for dt in dts:
        pair = (n_temporal, float(dt))
        if pair not in seen_pairs:
            pairs.append((*pair, "temporal"))
            seen_pairs.add(pair)
    rows = []
    for power in powers:
        for n, dt, group in pairs:
            if not math.isfinite(dt) or dt <= 0:
                raise ValueError("all delta_t values must be finite and positive")
            steps = end / dt
            if abs(steps - round(steps)) > 1e-10:
                raise ValueError(f"end_time/delta_t must be integral for m={power}, n={n}, dt={dt}")
            name = f"m{power}-{group}-n{n:03d}-dt{dt:.7g}".replace(".", "p")
            rows.append({"name": name, "group": group, "envelope_power": power,
                         "n": n, "dt": dt, "end": end, "nu": nu,
                         "steps": int(round(steps))})
    if len(rows) != protocol.get("expected_unique_cases") or len({r["name"] for r in rows}) != len(rows):
        raise ValueError("case matrix differs from expected_unique_cases or contains duplicates")
    return rows


def resolution_gate(protocol, audit_result):
    gate = protocol["reference_resolution_gate"]
    required_n = set(gate["required_fine_grid_counts"])
    if not required_n:
        raise ValueError("reference resolution gate must name fine grids")
    thresholds = protocol["local_quality_relative_error_thresholds"]
    by_power = {row["envelope_power"]: row for row in audit_result["widths"]}
    results = {}
    for power in protocol["envelope_powers"]:
        if power not in by_power:
            raise ValueError(f"reference audit is missing envelope power {power}")
        by_n = {row["n"]: row for row in by_power[power]["rows"]}
        results[str(power)] = {}
        for n in sorted(required_n):
            row = by_n.get(n)
            if row is None:
                raise ValueError(f"reference audit for m={power} is missing n={n}")
            passed = (row["gradient_stencil_floor_relative_error"] <= thresholds["max_gradient"]
                      and row["vorticity_stencil_floor_relative_error"] <= thresholds["max_vorticity"])
            results[str(power)][str(n)] = {"passed": passed,
                "gradient_floor": row["gradient_stencil_floor_relative_error"],
                "vorticity_floor": row["vorticity_stencil_floor_relative_error"]}
            if not passed:
                raise ValueError(f"exact reference FD2 floor does not clear the gate for m={power}, n={n}")
    return results



def verify_reference_artifact(path, computed):
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(f"frozen exact-reference audit is missing: {path}")
    recorded = json.loads(path.read_text())
    if recorded != computed:
        raise ValueError(f"frozen exact-reference audit does not replay byte-for-data: {path}")
    return digest(path)


def classify_width(cases, power, required_n, resolution_results):
    selected = [next((case for case in cases
                      if case["parameters"]["envelope_power"] == power
                      and case["parameters"]["n"] == n
                      and case["parameters"]["dt"] == 0.001), None)
                for n in required_n]
    if any(case is None for case in selected):
        status = "UNCERTAIN"
    elif not all(resolution_results[str(power)][str(n)]["passed"] for n in required_n):
        status = "UNCERTAIN"
    elif all(case["standard_acceptance"]["status"] == "PASS"
             and case["local_quality"]["status"] == "FAIL" for case in selected):
        status = "REPRODUCED"
    elif all(case["standard_acceptance"]["status"] == "PASS"
             and case["local_quality"]["status"] == "PASS" for case in selected):
        status = "NOT_OBSERVED"
    else:
        status = "UNCERTAIN"
    return {"envelope_power": power, "status": status,
            "required_fine_grid_counts": list(required_n),
            "rule": "Persistent standard-PASS/local-FAIL or standard-PASS/local-PASS at every listed fine grid, after the exact-reference FD2 floors pass.",
            "scope": "This frozen manufactured-solution benchmark only; it cannot establish a general solver defect or physical singularity."}


def run(protocol_path, output_root, image="concentration-aware-ns:of13", source_commit=None):
    protocol_path = Path(protocol_path)
    protocol = json.loads(protocol_path.read_text())
    cases = build_cases(protocol)
    output_root = Path(output_root).resolve()
    if output_root.exists():
        raise ValueError(f"refusing to overwrite existing output: {output_root}")
    source_commit = source_commit or subprocess.run(
        ["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=True
    ).stdout.strip()
    head = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True,
                          text=True, check=True).stdout.strip()
    if source_commit != head:
        raise ValueError(f"source_commit {source_commit} does not match checked-out HEAD {head}")
    tracked_changes = subprocess.run(
        ["git", "status", "--porcelain", "--untracked-files=no"],
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    if tracked_changes:
        raise RuntimeError("commit tracked source changes before running the frozen matrix")

    audit_counts = tuple(sorted(set(protocol["spatial_matrix"]["cell_counts"]
        + [protocol["temporal_matrix"]["cell_count"]]
        + protocol["reference_resolution_gate"]["required_fine_grid_counts"])))
    reference = audit_reference(tuple(protocol["envelope_powers"]), audit_counts,
                                str(protocol_path))
    resolution_results = resolution_gate(protocol, reference)
    reference_artifact_sha256 = verify_reference_artifact(
        protocol["reference_resolution_gate"]["artifact"], reference)
    docker_cli, docker_resolved = resolve_docker_cli()
    docker_context = resolve_docker_context(docker_cli)
    docker = [docker_cli, "--context", docker_context]
    docker_version = subprocess.run([*docker, "--version"], capture_output=True,
                                    text=True, check=True, timeout=8).stdout.strip()
    image_info = subprocess.run([*docker, "image", "inspect", image,
        "--format", "{{.Id}} {{.Os}}/{{.Architecture}}"], capture_output=True,
        text=True, check=True, timeout=8).stdout.strip()
    image_id, platform = image_info.split(maxsplit=1)
    if platform != "linux/arm64":
        raise ValueError(f"expected the Foundation 13 linux/arm64 image, got {platform!r}")

    output_root.mkdir(parents=True)
    (output_root / "cases").mkdir()
    (output_root / "archives").mkdir()
    (output_root / "protocol.json").write_bytes(protocol_path.read_bytes())
    (output_root / "reference-resolution-audit.json").write_text(
        json.dumps(reference, indent=2, allow_nan=False) + "\n")
    receipt = {"protocol": protocol, "protocol_sha256": digest(protocol_path),
        "source_commit": source_commit, "image": image,
        "image_id": image_id, "image_platform": platform,
        "docker_cli": docker_cli, "docker_cli_resolved": docker_resolved,
        "docker_cli_sha256": digest(docker_resolved), "docker_cli_version": docker_version,
        "docker_context": docker_context, "status": "RUNNING", "cases": [],
        "reference_resolution_gate": resolution_results,
        "reference_resolution_artifact_sha256": reference_artifact_sha256,
        "limitations": protocol["interpretation_limits"]}
    manifest = output_root / "manifest.json"
    manifest.write_text(json.dumps(receipt, indent=2, allow_nan=False) + "\n")
    for row in cases:
        case = output_root / "cases" / row["name"]
        item = {**row, "status": "PREPARING"}
        receipt["cases"].append(item)
        manifest.write_text(json.dumps(receipt, indent=2, allow_nan=False) + "\n")
        from tools.openfoam_case import generate
        generate(case, n=row["n"], dt=row["dt"], end=row["end"], nu=row["nu"],
                 profile="high-gradient", frequency=protocol["frequency_N"],
                 envelope_power=row["envelope_power"])
        item["input_hashes"] = {str(path.relative_to(case)): digest(path)
            for path in sorted(case.rglob("*")) if path.is_file()}
        command = [*docker, "run", "--rm", "--name", f"cans-hgw-{row['name']}",
            "--network", "none", "--entrypoint", "/bin/bash", "-v", f"{case}:/case",
            image_id, "-c", 'useradd -o -u "$1" -m runner && su runner -s /bin/bash -c '
            '"source /opt/openfoam13/etc/bashrc && cd /case && blockMesh > log.blockMesh 2>&1 '
            '&& foamRun > log.foamRun 2>&1 && foamPostProcess -func writeCellCentres '
            '-latestTime > log.centres 2>&1"', "--", str(os.getuid())]
        (case / "command.json").write_text(json.dumps(command, indent=2) + "\n")
        with (case / "log.container").open("w") as log:
            result = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT, check=False)
        log_path = case / "log.foamRun"
        times = ([float(value) for value in re.findall(r"^Time\s*=\s*([0-9.eE+-]+)",
                 log_path.read_text(errors="replace"), flags=re.M)] if log_path.exists() else [])
        item.update(exit_code=result.returncode, observed_time_steps=len(times),
                    last_logged_time=times[-1] if times else None,
                    status="SOLVER_FAILED" if result.returncode else "SOLVER_COMPLETED")
        (case / "exit.json").write_text(json.dumps({"exit_code": result.returncode,
            "expected_time_steps": row["steps"], "observed_time_steps": len(times),
            "last_logged_time": times[-1] if times else None}, indent=2) + "\n")
        archive_path = output_root / "archives" / f"{row['name']}.tar.gz"
        with tarfile.open(archive_path, "w:gz") as archive:
            archive.add(case, arcname=case.name)
        item["archive"] = str(archive_path.relative_to(output_root))
        item["archive_sha256"] = digest(archive_path)
        if result.returncode == 0 and len(times) == row["steps"] and times and abs(times[-1]-row["end"]) <= 1e-10:
            try:
                item["diagnostics"] = analyze(case, protocol)
                item["status"] = "COMPLETE"
            except Exception as error:
                item["status"] = "ANALYSIS_FAILED"
                item["analysis_error"] = f"{type(error).__name__}: {error}"
        elif result.returncode == 0:
            item["status"] = "TIME_GRID_MISMATCH"
        if item["status"] != "COMPLETE":
            receipt["status"] = "INCOMPLETE"
            receipt["failure"] = item["name"]
            manifest.write_text(json.dumps(receipt, indent=2, allow_nan=False) + "\n")
            raise RuntimeError(f"{item['name']} ended with {item['status']}; preserve {output_root}")
        manifest.write_text(json.dumps(receipt, indent=2, allow_nan=False) + "\n")

    required_n = protocol["reference_resolution_gate"]["required_fine_grid_counts"]
    receipt["width_classifications"] = [classify_width(
        [case["diagnostics"] for case in receipt["cases"]], power, required_n,
        resolution_results) for power in protocol["envelope_powers"]]
    receipt["status"] = "COMPLETE_WITH_DIAGNOSTICS"
    manifest.write_text(json.dumps(receipt, indent=2, allow_nan=False) + "\n")
    print(json.dumps({"status": receipt["status"], "output": str(output_root),
        "width_classifications": receipt["width_classifications"]}, indent=2, allow_nan=False))
    return receipt


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--protocol", default="protocols/high-gradient-of13-width-v1.json")
    parser.add_argument("--output", default="work/of13-high-gradient-width-v1")
    parser.add_argument("--image", default="concentration-aware-ns:of13")
    parser.add_argument("--source-commit")
    args = parser.parse_args()
    run(args.protocol, args.output, args.image, args.source_commit)
