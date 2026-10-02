"""Run the preregistered localized high-gradient OpenFOAM AMR matrix.

Existing case directories are never overwritten; inspect and preserve partial
runs before making any new attempt.
"""
import hashlib
import argparse
import json
import os
import subprocess
from pathlib import Path

from tools.analyze_amr import analyze
from tools.openfoam_amr_case import generate_amr

ROOT = Path("work/of13-high-gradient-v2").resolve()
PROTOCOL = Path("protocols/high-gradient-of13-amr-v1.json")
INPUTS = (
    "0/U", "0/p", "constant/fvModels", "constant/dynamicMeshDict",
    "constant/momentumTransport", "constant/physicalProperties",
    "parameters.json", "system/blockMeshDict", "system/controlDict",
    "system/fvSchemes", "system/fvSolution",
)


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def run_case(spec, cap, image):
    name = f"amr-cap{cap}"
    case = ROOT / name
    if case.exists():
        exit_path = case / "exit.json"
        log_path = case / "log.foamRun"
        if not (exit_path.is_file() and log_path.is_file()
                and json.loads(exit_path.read_text()).get("exit_code") == 0
                and log_path.read_text().rstrip().endswith("End")):
            raise FileExistsError(f"preserving existing incomplete AMR case: {case}")
        diagnostics = analyze(case)
        saved = case / "diagnostics.json"
        content = json.dumps(diagnostics, indent=2, allow_nan=False) + "\n"
        if saved.is_file() and saved.read_text() != content:
            raise ValueError(f"replayed diagnostics differ; preserve both for review: {case}")
        if not saved.exists():
            saved.write_text(content)
        print(json.dumps({
            "case": name,
            "cells": diagnostics["cells"],
            "level_counts": diagnostics["level_counts"],
            "max_level_reached": diagnostics["max_level_reached"],
            "velocity_relative_volume_l2": diagnostics["velocity_relative_volume_l2"],
            "quality": diagnostics["quality"],
            "reused": True,
        }), flush=True)
        return
    generate_amr(
        case, max_cells=cap, max_level=spec["amr_cases"]["max_refinement_level"],
        end=spec["end_time"], profile="high-gradient",
        frequency=spec["frequency_N"], n=spec["amr_cases"]["base_cell_count"],
        dt=spec["amr_cases"]["delta_t"], nu=spec["viscosity"],
    )
    command = [
        "docker", "run", "--rm", "--network", "none", "--name", f"cans-hg-{name}",
        "--entrypoint", "/bin/bash", "-v", f"{case}:/case", image,
        "-c", "useradd -o -u \"$1\" -m runner && su runner -s /bin/bash -c "
        "\"source /opt/openfoam13/etc/bashrc && cd /case && "
        "blockMesh > log.blockMesh 2>&1 && foamRun > log.foamRun 2>&1 && "
        "foamPostProcess -func writeCellCentres -latestTime > log.centres 2>&1 && "
        "foamPostProcess -func writeCellVolumes -latestTime > log.volumes 2>&1 && "
        "foamPostProcess -func 'grad(U)' -latestTime > log.gradient 2>&1\"",
        "--", str(os.getuid()),
    ]
    (case / "command.json").write_text(json.dumps(command, indent=2) + "\n")
    (case / "input-hashes.json").write_text(json.dumps(
        {path: sha256(case / path) for path in INPUTS}, indent=2
    ) + "\n")
    print(f"START {name}", flush=True)
    with (case / "log.container").open("w") as stream:
        result = subprocess.run(command, stdout=stream, stderr=subprocess.STDOUT)
    (case / "exit.json").write_text(json.dumps({"exit_code": result.returncode}) + "\n")
    if result.returncode:
        raise RuntimeError(f"{name} returned {result.returncode}; preserve and inspect its logs")
    diagnostics = analyze(case)
    (case / "diagnostics.json").write_text(json.dumps(diagnostics, indent=2, allow_nan=False) + "\n")
    print(json.dumps({
        "case": name,
        "cells": diagnostics["cells"],
        "level_counts": diagnostics["level_counts"],
        "max_level_reached": diagnostics["max_level_reached"],
        "velocity_relative_volume_l2": diagnostics["velocity_relative_volume_l2"],
        "quality": diagnostics["quality"],
    }), flush=True)


def main():
    spec = json.loads(PROTOCOL.read_text())
    environment = json.loads((ROOT / "run-environment.json").read_text())
    for cap in spec["amr_cases"]["max_cells"]:
        run_case(spec, cap, environment["container_image_id"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()
    if not args.resume and any((ROOT / f"amr-cap{cap}").exists()
                               for cap in (4096, 5000, 100000)):
        raise FileExistsError("AMR output exists; use --resume only for verified complete cases")
    main()
