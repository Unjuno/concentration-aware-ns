"""Run the frozen SU2 high-gradient matrix without altering the Gaussian study."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tarfile

from tools.analyze_su2 import analyze
from tools.su2_case import generate


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def case_pairs(protocol):
    cases = protocol["cases"]
    pairs = [(int(n), float(dt)) for n, dt in cases["spatial"] + cases["temporal"]]
    return list(dict.fromkeys(pairs))


def expected_case_labels(protocol):
    return [f"n{n}-dt{dt:g}" for n, dt in case_pairs(protocol)]


def select_case_pairs(protocol, selected_case_labels=None):
    pairs = case_pairs(protocol)
    labels = expected_case_labels(protocol)
    if selected_case_labels is None:
        return pairs
    if not selected_case_labels:
        raise ValueError("at least one frozen case label must be selected")
    if len(set(selected_case_labels)) != len(selected_case_labels):
        raise ValueError("selected case labels must be unique")
    unknown = set(selected_case_labels) - set(labels)
    if unknown:
        raise ValueError(f"unknown selected case labels: {sorted(unknown)}")
    selected = set(selected_case_labels)
    return [pair for pair in pairs if f"n{pair[0]}-dt{pair[1]:g}" in selected]


def study_status(expected_labels, rows):
    """Report matrix coverage independently from per-case acceptance."""
    labels = [row.get("case") for row in rows]
    return ("COMPLETE" if len(labels) == len(expected_labels)
            and len(set(labels)) == len(expected_labels)
            and set(labels) == set(expected_labels) else "INCOMPLETE")


def aggregate_case_artifacts(case_artifacts_root, protocol_path, output_root):
    """Merge one-case workers that all loaded the same built solver image."""
    case_artifacts_root = Path(case_artifacts_root)
    protocol_path, output_root = Path(protocol_path), Path(output_root)
    protocol = json.loads(protocol_path.read_text())
    protocol_hash = sha256(protocol_path)
    expected = expected_case_labels(protocol)
    expected_by_label = {
        f"n{n}-dt{dt:g}": (n, dt) for n, dt in case_pairs(protocol)
    }
    patch_hash = sha256("runtime/su2/high_gradient.patch")
    workers, seen = [], set()
    image_id = image_name = None

    for worker_summary_path in sorted(case_artifacts_root.rglob("summary.json")):
        worker_root = worker_summary_path.parent
        worker = json.loads(worker_summary_path.read_text())
        if worker.get("protocol_sha256") != protocol_hash:
            raise ValueError(f"worker protocol hash mismatch: {worker_root}")
        if sha256(worker_root / "protocol.json") != protocol_hash:
            raise ValueError(f"worker protocol file mismatch: {worker_root}")
        if sha256(worker_root / "high_gradient.patch") != patch_hash:
            raise ValueError(f"worker SU2 adapter mismatch: {worker_root}")
        if worker.get("expected_cases") != len(expected):
            raise ValueError(f"worker expected-case count mismatch: {worker_root}")
        if worker.get("attempted_cases") != 1 or len(worker.get("cases", [])) != 1:
            raise ValueError(f"worker must contain exactly one case: {worker_root}")
        worker_image = worker.get("image_id")
        worker_name = worker.get("image")
        if (not worker_image or (image_id is not None and worker_image != image_id)
                or (image_name is not None and worker_name != image_name)):
            raise ValueError(f"workers did not use one shared image: {worker_root}")
        image_id, image_name = worker_image, worker_name
        row = worker["cases"][0]
        label = row.get("case")
        if label not in expected_by_label or label in seen:
            raise ValueError(f"unexpected or duplicate worker case: {label}")
        n, dt = expected_by_label[label]
        if row.get("n") != n or abs(row.get("dt", -1) - dt) > 1e-15:
            raise ValueError(f"worker case parameters mismatch: {label}")
        archive = worker_root / f"{label}.tar.gz"
        digest = sha256(archive)
        if digest != row.get("archive_sha256"):
            raise ValueError(f"worker case archive hash mismatch: {label}")
        seen.add(label)
        workers.append((label, row, archive, digest))

    if output_root.exists():
        raise ValueError(f"refusing to overwrite existing aggregate directory: {output_root}")
    output_root.mkdir(parents=True)
    shutil.copy2(protocol_path, output_root / "protocol.json")
    shutil.copy2("runtime/su2/high_gradient.patch", output_root / "high_gradient.patch")
    rows = []
    for label in expected:
        worker_case = next((item for item in workers if item[0] == label), None)
        if worker_case is None:
            continue
        _, row, archive, digest = worker_case
        shutil.copy2(archive, output_root / archive.name)
        rows.append({**row, "archive_sha256": digest})
    complete = study_status(expected, rows)
    all_standard = complete == "COMPLETE" and all(
        row.get("standard_acceptance") == "PASS" for row in rows
    )
    summary = {
        "study_id": protocol["study_id"],
        "status": complete,
        "standard_acceptance": "PASS" if all_standard else (
            "FAIL" if complete == "COMPLETE" else "INCOMPLETE"
        ),
        "expected_cases": len(expected),
        "attempted_cases": len(rows),
        "protocol_sha256": protocol_hash,
        "image": image_name,
        "image_id": image_id,
        "cases": rows,
        "missing_cases": [label for label in expected if label not in seen],
    }
    (output_root / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    return summary


def run(protocol_path, root, image, selected_case_labels=None):
    protocol_path, root = Path(protocol_path), Path(root)
    protocol = json.loads(protocol_path.read_text())
    if protocol.get("status") != "frozen before execution":
        raise ValueError("protocol must be frozen before execution")
    if protocol["adapter"]["frequency_N"] != 4:
        raise ValueError("the checked-in SU2 adapter is frozen at N=4")
    all_pairs = case_pairs(protocol)
    if len(all_pairs) != protocol["cases"]["expected_cases"]:
        raise ValueError("unique case count does not match the frozen protocol")
    all_labels = expected_case_labels(protocol)
    pairs = select_case_pairs(protocol, selected_case_labels)
    if root.exists():
        raise ValueError(f"refusing to overwrite existing run directory: {root}")
    identity = subprocess.check_output(["docker", "image", "inspect", image, "--format", "{{.Id}}"], text=True).strip()
    root.mkdir(parents=True)
    case_root = root / "cases"
    case_root.mkdir()
    shutil.copy2(protocol_path, root / "protocol.json")
    shutil.copy2("runtime/su2/high_gradient.patch", root / "high_gradient.patch")
    rows = []
    for n, dt in pairs:
        steps = round(protocol["time"]["end"] / dt)
        label = f"n{n}-dt{dt:g}"
        case = case_root / label
        generate(case, n=n, dt=dt, end=protocol["time"]["end"],
                 inner=protocol["time"]["inner_iteration_cap"],
                 profile="high-gradient", frequency=protocol["adapter"]["frequency_N"])
        params = json.loads((case / "parameters.json").read_text())
        params.update({"study_id": protocol["study_id"],
                       "protocol_sha256": sha256(protocol_path),
                       "image": image, "image_id": identity,
                       "nu": protocol["adapter"]["viscosity"],
                       "rho": protocol["adapter"]["density"],
                       "quality_thresholds": protocol["acceptance"]["quality_thresholds"]})
        (case / "parameters.json").write_text(json.dumps(params, indent=2) + "\n")
        cfg = case / "case.cfg"
        cfg.write_text(cfg.read_text().replace("OUTPUT_WRT_FREQ= 1", f"OUTPUT_WRT_FREQ= {steps}")
                       .replace("(RESTART_ASCII, PARAVIEW_ASCII)", "(RESTART_ASCII)"))
        cmd = ["docker", "run", "--rm", "--name", f"cans-su2-hg-{label}",
               "-e", "OMP_NUM_THREADS=2", "-v", f"{case.resolve()}:/case",
               image, "SU2_CFD", "case.cfg"]
        (case / "command.json").write_text(json.dumps(cmd, indent=2) + "\n")
        print(f"START {label} image={identity}", flush=True)
        with (case / "solver.log").open("w") as log:
            result = subprocess.run(cmd, stdout=log, stderr=subprocess.STDOUT)
        (case / "exit_code").write_text(f"{result.returncode}\n")
        row = {"case": label, "n": n, "dt": dt, "planned_steps": steps,
               "exit_code": result.returncode}
        if result.returncode == 0:
            metrics = analyze(case)
            standard_pass = metrics["steps"] == steps and metrics["converged_steps"] == steps
            row.update({"standard_acceptance": "PASS" if standard_pass else "FAIL",
                        "quality_sampled": metrics["quality_sampled"],
                        "metrics": metrics})
            (case / "diagnostics.json").write_text(json.dumps(metrics, indent=2) + "\n")
        else:
            row["standard_acceptance"] = "FAIL"
        archive = root / f"{label}.tar.gz"
        with tarfile.open(archive, "w:gz") as tar:
            tar.add(case, arcname=label)
        row["archive_sha256"] = sha256(archive)
        rows.append(row)
        overall = study_status(all_labels, rows)
        all_standard = overall == "COMPLETE" and all(
            item["standard_acceptance"] == "PASS" for item in rows
        )
        summary = {"study_id": protocol["study_id"], "status": overall,
                   "standard_acceptance": "PASS" if all_standard else (
                       "FAIL" if overall == "COMPLETE" else "INCOMPLETE"
                   ),
                   "expected_cases": len(all_pairs), "attempted_cases": len(rows),
                   "protocol_sha256": sha256(protocol_path), "image": image,
                   "image_id": identity, "cases": rows}
        (root / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
        print(f"END {label} standard={row['standard_acceptance']} quality={row.get('quality_sampled', 'N/A')}", flush=True)
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--protocol", default="protocols/su2-shared-high-gradient-v1.json")
    parser.add_argument("--root", required=True)
    parser.add_argument("--image", default="cans-su2-high-gradient")
    parser.add_argument("--case", action="append", dest="case_labels",
                        help="run only this frozen case label; repeat to select more")
    parser.add_argument("--allow-incomplete", action="store_true",
                        help="return success after a partial case-worker run")
    parser.add_argument("--aggregate-case-artifacts",
                        help="merge one-case worker artifact directories")
    args = parser.parse_args()
    if args.aggregate_case_artifacts:
        result = aggregate_case_artifacts(
            args.aggregate_case_artifacts, args.protocol, args.root
        )
    else:
        result = run(args.protocol, args.root, args.image, args.case_labels)
    print(json.dumps(result, indent=2))
    if result["status"] != "COMPLETE" and not args.allow_incomplete:
        raise SystemExit(2)
