"""Recompute high-gradient AMR velocity errors by refinement level."""
import hashlib
import json
from pathlib import Path

import numpy as np

from tools.analyze_amr import values
from tools.analyze_openfoam import vectors
from tools.high_gradient_reference import fields


ROOT = Path("work/of13-high-gradient-v2")
CASES = ("amr-cap4096", "amr-cap5000", "amr-cap100000")


def analyze_case(name):
    case = ROOT / name
    diagnostics = json.loads((case / "diagnostics.json").read_text())
    time_dir = case / str(diagnostics["parameters"]["end"])
    count = diagnostics["cells"]
    centers = vectors(time_dir / "C", count)
    velocity = vectors(time_dir / "U", count)
    volumes = values(time_dir / "Vc", count)
    if (time_dir / "cellLevel").exists():
        levels = values(time_dir / "cellLevel", count)
        level_source = "written cellLevel field"
    elif (count == diagnostics["parameters"]["n"] ** 3
          and not any(line.startswith("Refined from ")
                      for line in (case / "log.foamRun").read_text().splitlines())):
        levels = np.zeros(count)
        level_source = "initial mesh count and no refinement event"
    else:
        raise ValueError(f"cannot reconstruct level labels: {case}")
    params = diagnostics["parameters"]
    reference = fields(centers, N=params["frequency"], nu=params["nu"],
                       time=params["end"])["u"]
    squared_error = np.sum((velocity - reference) ** 2, axis=1)
    squared_reference = np.sum(reference ** 2, axis=1)
    denominator = float(np.sum(volumes * squared_reference))
    total = float(np.sqrt(np.sum(volumes * squared_error) / denominator))
    if not np.isclose(total, diagnostics["velocity_relative_volume_l2"], rtol=1e-12, atol=1e-14):
        raise ValueError(f"independent AMR L2 recomputation differs for {name}: {total}")
    by_level = {}
    for level in np.unique(levels):
        mask = levels == level
        ref_norm = float(np.sum(volumes[mask] * squared_reference[mask]))
        error_norm = float(np.sum(volumes[mask] * squared_error[mask]))
        by_level[str(int(level))] = {
            "cells": int(mask.sum()),
            "volume_fraction": float(np.sum(volumes[mask]) / np.sum(volumes)),
            "reference_squared_norm_contribution_fraction": ref_norm / denominator,
            "weighted_absolute_error_norm_contribution_fraction": error_norm / float(np.sum(volumes * squared_error)),
            "relative_l2_within_level": float(np.sqrt(error_norm / ref_norm)) if ref_norm else None,
            "max_pointwise_velocity_error": float(np.sqrt(squared_error[mask]).max()),
        }
    return {
        "case": name,
        "status": "COMPLETE" if diagnostics and (case / "log.foamRun").read_text().rstrip().endswith("End") else "INCOMPLETE",
        "requested_max_cells": params["amr"]["maxCells"],
        "actual_cells": count,
        "over_budget_cells": max(0, count - params["amr"]["maxCells"]),
        "maximum_refinement_level": max(map(int, diagnostics["level_counts"])),
        "level_source": level_source,
        "cell_volume_sum": float(np.sum(volumes)),
        "global_velocity_relative_volume_l2": total,
        "level_errors": by_level,
        "sha256": {
            str(path.relative_to(case)): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in (time_dir / "C", time_dir / "U", time_dir / "Vc", case / "diagnostics.json")
        },
    }


def main():
    control = json.loads((ROOT / "n64-dt0.001" / "diagnostics.json").read_text())
    report = {
        "schema_version": 1,
        "scope": "Independent volume-weighted velocity-error recomputation and decomposition by AMR level",
        "uniform_n16_velocity_relative_l2": json.loads((ROOT / "n16-dt0.001" / "diagnostics.json").read_text())["velocity_relative_l2"],
        "uniform_n64_velocity_relative_l2": control["velocity_relative_l2"],
        "amr_cases": [analyze_case(name) for name in CASES],
        "limitations": [
            "The recomputation uses the analytic reference evaluator already cross-checked against SymPy, not a second solver.",
            "A large local error is not a software-defect finding without a validated AMR interpolation/source/runtime audit.",
            "No nonuniform spectral reconstruction or continuous-extremum certification is available.",
        ],
    }
    destination = Path("evidence/tests/of13-high-gradient-amr-error-strata.json")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
