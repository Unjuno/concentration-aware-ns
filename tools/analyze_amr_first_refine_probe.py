"""Analyze saved early checkpoints without assigning an AMR defect verdict."""
import hashlib
import json
import re
from pathlib import Path

import numpy as np

from tools.analyze_amr import values
from tools.analyze_openfoam import vectors
from tools.high_gradient_reference import fields


ROOT = Path("work/of13-amr-first-refinement-v1")
EVIDENCE = Path("evidence/of13-amr-first-refinement-v1")
TIMES = ("0.001", "0.002", "0.003")


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def case_metrics(case):
    case = Path(case)
    result = {}
    for time in TIMES:
        folder = case / time
        c_text = (folder / "C").read_text()
        count = int(re.search(r"List<vector>\s+(\d+)", c_text)[1])
        centers = vectors(folder / "C", count)
        velocity = vectors(folder / "U", count)
        volumes = values(folder / "Vc", count)
        if np.any(volumes <= 0) or not np.isclose(volumes.sum(), (2*np.pi)**3, rtol=1e-10):
            raise ValueError(f"invalid cell-volume sum at {case.name}/{time}")
        exact = fields(centers, N=4, nu=0.01, time=float(time))
        velocity_error = float(np.sqrt(
            np.sum(volumes*np.sum((velocity-exact["u"])**2, axis=1))
            / np.sum(volumes*np.sum(exact["u"]**2, axis=1))
        ))
        grad = values(folder / "grad(U)", count, 9).reshape(-1, 3, 3)
        exact_grad_norm = np.linalg.norm(exact["grad_u"], axis=(1, 2))
        computed_grad_norm = np.linalg.norm(grad, axis=(1, 2))
        max_gradient_sample_error = float(
            abs(computed_grad_norm.max()-exact_grad_norm.max())
            / max(exact_grad_norm.max(), 1e-300)
        )
        result[time] = {
            "cell_count": count,
            "domain_volume": float(volumes.sum()),
            "velocity_relative_volume_l2_error": velocity_error,
            "max_gradient_norm_relative_cell_sample_error": max_gradient_sample_error,
            "reference_max_gradient_norm_at_cell_centers": float(exact_grad_norm.max()),
            "computed_max_gradient_norm_at_cells": float(computed_grad_norm.max()),
        }
    return result


def difference_in_differences(amr_errors, uniform_errors):
    """Compare error growth from t=.002 to .003; descriptive, not causal proof."""
    return ((amr_errors["0.003"]-amr_errors["0.002"])
            -(uniform_errors["0.003"]-uniform_errors["0.002"]))


def analyze():
    manifest_path = EVIDENCE / "manifest.json"
    manifest = json.loads(manifest_path.read_text())
    if manifest.get("completion") != "PASS":
        raise ValueError("run manifest does not pass the checkpoint completion gate")
    if manifest["run_environment"]["protocol_sha256"] != sha256(
            "protocols/high-gradient-of13-amr-first-refinement-v1.json"):
        raise ValueError("protocol hash differs from the executed run")
    amr = case_metrics(ROOT / "amr-cap5000")
    uniform = case_metrics(ROOT / "uniform-n16")
    amr_errors = {time: row["velocity_relative_volume_l2_error"] for time, row in amr.items()}
    uniform_errors = {time: row["velocity_relative_volume_l2_error"] for time, row in uniform.items()}
    result = {
        "protocol_sha256": manifest["run_environment"]["protocol_sha256"],
        "run_manifest_sha256": sha256(manifest_path),
        "cases": {"amr-cap5000": amr, "uniform-n16": uniform},
        "predeclared_contrast": {
            "quantity": "(AMR e003-AMR e002)-(uniform e003-uniform e002)",
            "value": difference_in_differences(amr_errors, uniform_errors),
            "interpretation": "Positive means error increased more across the first-refinement interval in the AMR run than in the same-grid control. The AMR t=.003 field includes one solved post-remap timestep.",
        },
        "scope": "Exact-MMS comparison at three early checkpoints. Cell-gradient maxima are cell-center samples. This does not isolate remapping from flux correction, projection, sensor changes or post-remap evolution and is not a solver-defect or acceptance verdict.",
    }
    output = EVIDENCE / "analysis.json"
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    return result


if __name__ == "__main__":
    analyze()
