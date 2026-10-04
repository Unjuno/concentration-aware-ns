"""Decompose archived OpenFOAM peak diagnostics against certified N=4 maxima."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import tarfile
import tempfile
from pathlib import Path

from tools.verify_openfoam_high_gradient_matrix import (
    INDEX, PROTOCOL, ROOT, _archive_path, sha256_file, verify_matrix,
)


def row_from_diagnostics(case: str, diagnostics: dict) -> dict:
    params = diagnostics["parameters"]
    if params.get("frequency") != 4:
        raise ValueError("the certified continuum peak formulas apply only to N=4")
    time = float(params["end"])
    continuum_gradient = math.sqrt(65) / 8 * math.exp(-time)
    continuum_vorticity = 9 / 8 * math.exp(-time)
    measured = {
        "reference_exact_gradient_sample": diagnostics["reference_gradient_peak_cell_samples"],
        "reference_exact_vorticity_sample": diagnostics["reference_vorticity_peak_cell_samples"],
        "reference_fd2_gradient": diagnostics["reference_sampled_fd2"]["max_gradient_fd2"],
        "reference_fd2_vorticity": diagnostics["reference_sampled_fd2"]["max_vorticity_fd2"],
        "solver_fd2_gradient": diagnostics["computed"]["max_gradient_fd2"],
        "solver_fd2_vorticity": diagnostics["computed"]["max_vorticity_fd2"],
    }
    return {
        "case": case,
        "n": int(params["n"]),
        "dt": float(params["dt"]),
        "end": time,
        "certified_continuum_gradient_peak": continuum_gradient,
        "certified_continuum_vorticity_peak": continuum_vorticity,
        **measured,
        **{
            f"{name}_fraction": float(value / (
                continuum_gradient if "gradient" in name else continuum_vorticity
            ))
            for name, value in measured.items()
        },
    }


def build_evidence() -> dict:
    replay = verify_matrix()
    if replay["status"] != "PASS":
        raise ValueError("archived six-case matrix replay did not pass")
    index = json.loads(INDEX.read_text())
    rows = []
    with tempfile.TemporaryDirectory(prefix="cans-continuum-peaks-") as tmp:
        for entry in index["completed_cases"]:
            archive_path = _archive_path(entry, tmp)
            archive_sha = sha256_file(archive_path)
            if archive_sha != entry["archive_sha256"]:
                raise ValueError(f"archive SHA-256 mismatch for {entry['case']}")
            with tarfile.open(archive_path, "r:gz") as archive:
                member = f"{entry['case']}/diagnostics.json"
                diagnostics = json.load(archive.extractfile(member))
            row = row_from_diagnostics(entry["case"], diagnostics)
            row["archive_sha256"] = archive_sha
            row["standard_acceptance"] = entry["standard_acceptance"]
            row["local_quality"] = entry["local_quality"]
            rows.append(row)
    return {
        "schema": "openfoam-archived-peak-continuum-decomposition/v1",
        "scope": (
            "Archived cell-center diagnostics only. The three layers are exact analytic "
            "derivatives sampled at cell centers, FD2 applied to sampled exact velocity, "
            "and FD2 applied to solver cell-centered velocity. None bounds the continuous "
            "solver field between cells."
        ),
        "interpretation": (
            "The ratios decompose reference sampling, finite-difference stencil, and the "
            "solver-output diagnostic. They do not change the frozen same-grid gates or "
            "establish a solver defect or physical concentration."
        ),
        "matrix_replay": replay,
        "rows": rows,
        "provenance": {
            "matrix_index_sha256": hashlib.sha256(INDEX.read_bytes()).hexdigest(),
            "protocol_sha256": hashlib.sha256(PROTOCOL.read_bytes()).hexdigest(),
            "analyzer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        },
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = build_evidence()
    serialized = json.dumps(result, indent=2, allow_nan=False) + "\n"
    if args.output:
        output = args.output if args.output.is_absolute() else ROOT / args.output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(serialized)
    print(serialized, end="")


if __name__ == "__main__":
    main()
