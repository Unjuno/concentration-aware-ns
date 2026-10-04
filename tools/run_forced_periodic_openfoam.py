"""Run the frozen Foundation 13 smooth exact-control space/time study."""

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
from tools.openfoam_case import generate


def build_cases(protocol):
    required = {"protocol", "profile", "nu", "end", "spatial_cases", "temporal_cases",
                "expected_time_step_counts", "recorded_metrics", "claims_boundary"}
    missing = required - protocol.keys()
    if missing:
        raise ValueError(f"protocol missing {', '.join(sorted(missing))}")
    if protocol["protocol"] != "of13-forced-periodic-control-v1" or protocol["profile"] != "forced-periodic":
        raise ValueError("unsupported protocol or profile")
    nu, end = float(protocol["nu"]), float(protocol["end"])
    if not math.isfinite(nu) or not math.isfinite(end) or nu <= 0 or end <= 0:
        raise ValueError("nu and end must be finite and positive")
    rows = []
    for group in ("spatial", "temporal"):
        raw_rows = protocol[f"{group}_cases"]
        if not isinstance(raw_rows, list) or len(raw_rows) != 3:
            raise ValueError(f"{group}_cases must contain exactly three frozen rows")
        for row in raw_rows:
            n, dt = row.get("n"), float(row.get("dt", 0))
            if not isinstance(n, int) or n < 4 or not math.isfinite(dt) or dt <= 0:
                raise ValueError(f"invalid {group} case: {row}")
            steps = end / dt
            if abs(steps - round(steps)) > 1e-10:
                raise ValueError(f"end/dt must be an integer for {row}")
            name = f"{group}-n{n:03d}-dt{dt:.7g}".replace(".", "p")
            rows.append({"group": group, "name": name, "n": n, "dt": dt,
                         "end": end, "nu": nu, "steps": int(round(steps))})
    if len({row["name"] for row in rows}) != len(rows):
        raise ValueError("case names must be unique")
    expected = protocol["expected_time_step_counts"]
    for row in rows:
        if expected.get(str(row["dt"])) != row["steps"]:
            raise ValueError(f"time-step receipt mismatch for {row['name']}")
    return rows


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def logged_times(path):
    text = Path(path).read_text(errors="replace")
    return [float(value) for value in re.findall(r"^Time = ([0-9.eE+-]+)", text, flags=re.M)]


def run(protocol_path, output_root, image, source_commit):
    protocol_path = Path(protocol_path)
    output_root = Path(output_root).resolve()
    if output_root.exists():
        raise ValueError(f"refusing to overwrite existing output: {output_root}")
    cases = build_cases(json.loads(protocol_path.read_text()))
    image_inspect = subprocess.run(
        ["docker", "image", "inspect", image, "--format", "{{.Id}} {{.Os}}/{{.Architecture}}"],
        check=True, capture_output=True, text=True,
    ).stdout.strip()
    if not image_inspect.endswith("linux/arm64"):
        raise ValueError(f"expected Linux/arm64 OpenFOAM image, got {image_inspect!r}")

    output_root.mkdir(parents=True)
    case_root, archive_root = output_root / "cases", output_root / "archives"
    case_root.mkdir()
    archive_root.mkdir()
    (output_root / "protocol.json").write_bytes(protocol_path.read_bytes())
    receipt = {
        "protocol": json.loads(protocol_path.read_text()),
        "protocol_sha256": digest(protocol_path),
        "source_commit": source_commit,
        "image": image,
        "image_inspect": image_inspect,
        "status": "RUNNING",
        "cases": [],
        "limitations": [
            "solver/source calibration for a smooth fixed-spectrum solution only",
            "space/time convergence is measured, not presumed",
            "no concentration, molecular, singularity, constitutive-transition, or engineering inference",
        ],
    }
    (output_root / "manifest.json").write_text(json.dumps(receipt, indent=2) + "\n")
    for row in cases:
        case = case_root / row["name"]
        row_receipt = {**row, "status": "PREPARING"}
        receipt["cases"].append(row_receipt)
        (output_root / "manifest.json").write_text(json.dumps(receipt, indent=2) + "\n")
        generate(case, n=row["n"], dt=row["dt"], end=row["end"], nu=row["nu"],
                 profile="forced-periodic")
        command = [
            "docker", "run", "--rm", "--name", f"cans-{row['name']}",
            "--entrypoint", "/bin/bash", "-v", f"{case}:/case", image, "-c",
            'useradd -o -u "$1" -m runner && su runner -s /bin/bash -c '
            '"source /opt/openfoam13/etc/bashrc && cd /case && blockMesh > log.blockMesh 2>&1 '
            '&& foamRun > log.foamRun 2>&1 && foamPostProcess -func writeCellCentres '
            '-latestTime > log.centres 2>&1"', "--", str(os.getuid()),
        ]
        (case / "command.json").write_text(json.dumps(command, indent=2) + "\n")
        with (case / "log.container").open("w") as log:
            result = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT, check=False)
        times = logged_times(case / "log.foamRun") if (case / "log.foamRun").exists() else []
        row_receipt["exit_code"] = result.returncode
        row_receipt["observed_time_steps"] = len(times)
        row_receipt["last_logged_time"] = times[-1] if times else None
        row_receipt["status"] = "SOLVER_FAILED" if result.returncode else "SOLVER_COMPLETED"
        (case / "exit.json").write_text(json.dumps({
            "exit_code": result.returncode, "expected_time_steps": row["steps"],
            "observed_time_steps": len(times), "last_logged_time": times[-1] if times else None,
        }, indent=2) + "\n")
        archive_path = archive_root / f"{row['name']}.tar.gz"
        with tarfile.open(archive_path, "w:gz") as archive:
            archive.add(case, arcname=case.name)
        row_receipt["archive"] = str(archive_path.relative_to(output_root))
        row_receipt["archive_sha256"] = digest(archive_path)
        if result.returncode == 0:
            if len(times) != row["steps"] or not times or abs(times[-1] - row["end"]) > 1e-10:
                row_receipt["status"] = "TIME_GRID_MISMATCH"
                receipt["status"] = "FAIL"
            else:
                try:
                    row_receipt["diagnostics"] = analyze(case)
                    row_receipt["status"] = "COMPLETE"
                except Exception as error:
                    row_receipt["status"] = "ANALYSIS_FAILED"
                    row_receipt["analysis_error"] = f"{type(error).__name__}: {error}"
        if row_receipt["status"] != "COMPLETE":
            receipt["status"] = "FAIL"
            (output_root / "manifest.json").write_text(json.dumps(receipt, indent=2) + "\n")
            raise RuntimeError(f"{row['name']} ended with {row_receipt['status']}; evidence preserved")
        (output_root / "manifest.json").write_text(json.dumps(receipt, indent=2, allow_nan=False) + "\n")
    receipt["status"] = "COMPLETE_WITH_DIAGNOSTICS"
    (output_root / "manifest.json").write_text(json.dumps(receipt, indent=2, allow_nan=False) + "\n")
    print(json.dumps({"status": receipt["status"], "output": str(output_root),
                      "cases": [{"name": row["name"], "diagnostics": row["diagnostics"]}
                                for row in receipt["cases"]]}, indent=2, allow_nan=False))
    return receipt


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--protocol", default="protocols/of13-forced-periodic-control-v1.json")
    parser.add_argument("--output", default="work/of13-forced-periodic-control-v1")
    parser.add_argument("--image", default="concentration-aware-ns:of13")
    parser.add_argument("--source-commit", default="unknown")
    args = parser.parse_args()
    run(args.protocol, args.output, args.image, args.source_commit)
