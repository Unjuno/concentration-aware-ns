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


def run(protocol_path, root, image):
    protocol_path, root = Path(protocol_path), Path(root)
    protocol = json.loads(protocol_path.read_text())
    if protocol.get("status") != "frozen before execution":
        raise ValueError("protocol must be frozen before execution")
    if protocol["adapter"]["frequency_N"] != 4:
        raise ValueError("the checked-in SU2 adapter is frozen at N=4")
    pairs = case_pairs(protocol)
    if len(pairs) != protocol["cases"]["expected_cases"]:
        raise ValueError("unique case count does not match the frozen protocol")
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
        overall = "COMPLETE" if len(rows) == len(pairs) else "INCOMPLETE"
        if any(item["standard_acceptance"] != "PASS" for item in rows):
            overall = "INCOMPLETE"
        summary = {"study_id": protocol["study_id"], "status": overall,
                   "expected_cases": len(pairs), "attempted_cases": len(rows),
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
    args = parser.parse_args()
    result = run(args.protocol, args.root, args.image)
    print(json.dumps(result, indent=2))
    if result["status"] != "COMPLETE":
        raise SystemExit(2)
