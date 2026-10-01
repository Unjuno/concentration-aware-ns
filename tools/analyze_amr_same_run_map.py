"""Analyze the same-run preMap-to-mapped OpenFOAM AMR snapshot pair."""
import csv
import hashlib
import io
import json
import os
import tarfile
from pathlib import Path

import numpy as np

from tools.analyze_amr_stage_snapshots import (
    _parent_indices_for_children,
    parent_value_injection_audit,
)


EVIDENCE = Path(os.environ.get("CANS_AMR_STAGE_EVIDENCE", "evidence/of13-amr-same-run-map-v4-run3"))
ARCHIVE = EVIDENCE / "amr-stage-snapshot.tar.gz"
MANIFEST = EVIDENCE / "manifest.json"


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read_csv(archive, member):
    with tarfile.open(archive, "r:gz") as tf:
        stream = tf.extractfile(member)
        if stream is None:
            raise ValueError(f"missing {member}")
        rows = list(csv.DictReader(io.StringIO(stream.read().decode("utf-8"))))
    if not rows:
        raise ValueError(f"empty {member}")
    return {key: np.asarray([float(row[key]) for row in rows]) for key in rows[0]}


def analyze():
    manifest = json.loads(MANIFEST.read_text())
    if manifest["status"] != "RUN_COMPLETE_SAME_RUN_MAP_CAPTURED":
        raise ValueError("same-run mapping gate is not complete")
    if sha(ARCHIVE) != manifest["archive_sha256"]:
        raise ValueError("archive hash differs from manifest")
    if manifest["exit_code"] != 0 or not manifest["end_marker"]:
        raise ValueError("solver did not complete normally")
    if not manifest["instrumented_library_load_confirmed"]:
        raise ValueError("instrumented library load is not confirmed")

    pre = read_csv(ARCHIVE, "amr-cap5000/postProcessing/amrStages/0.002/preMap_cells.csv")
    mapped = read_csv(ARCHIVE, "amr-cap5000/postProcessing/amrStages/0.002/mapped_cells.csv")
    pre_centers = np.column_stack([pre[k] for k in ("cx", "cy", "cz")])
    mapped_centers = np.column_stack([mapped[k] for k in ("cx", "cy", "cz")])
    pre_u = np.column_stack([pre[k] for k in ("Ux", "Uy", "Uz")])
    mapped_u = np.column_stack([mapped[k] for k in ("Ux", "Uy", "Uz")])
    audit = parent_value_injection_audit(
        pre_centers, pre_u, pre["V"], mapped_centers, mapped_u, mapped["V"]
    )
    pre_integral = np.sum(pre["V"][:, None]*pre_u, axis=0)
    mapped_integral = np.sum(mapped["V"][:, None]*mapped_u, axis=0)
    integrated_speed_scale = max(
        float(np.sum(pre["V"]*np.linalg.norm(pre_u, axis=1))), 1e-300
    )
    exact = mapped_centers
    from tools.high_gradient_reference import fields
    exact_u = fields(exact, N=4, nu=0.01, time=0.002)["u"]
    exact_pre_u = fields(pre_centers, N=4, nu=0.01, time=0.002)["u"]
    parent_for_child = _parent_indices_for_children(pre_centers, mapped_centers)
    inherited_error = pre_u[parent_for_child]-exact_pre_u[parent_for_child]
    exact_center_shift = exact_pre_u[parent_for_child]-exact_u
    mapped_error = mapped_u-exact_u
    denominator = float(np.sum(mapped["V"][:, None]*exact_u**2))
    inherited_sq = float(np.sum(mapped["V"][:, None]*inherited_error**2)/denominator)
    center_shift_sq = float(np.sum(mapped["V"][:, None]*exact_center_shift**2)/denominator)
    cross_term = float(2*np.sum(
        mapped["V"][:, None]*inherited_error*exact_center_shift
    )/denominator)
    total_sq = float(np.sum(mapped["V"][:, None]*mapped_error**2)/denominator)
    exact_error = float(np.sqrt(
        np.sum(mapped["V"][:, None]*(mapped_u-exact_u)**2)
        / max(np.sum(mapped["V"][:, None]*exact_u**2), 1e-300)
    ))
    result = {
        "status": "SAME_RUN_PARENT_INJECTION_MATCH" if audit["mapped_vs_parent_injection_relative_l2"] < 1e-12 else "SAME_RUN_PARENT_INJECTION_MISMATCH",
        "protocol": manifest["protocol"],
        "archive_sha256": manifest["archive_sha256"],
        "preMap_time": "0.002",
        "mapped_time": "0.002",
        "preMap_cells": int(len(pre_u)),
        "mapped_cells": int(len(mapped_u)),
        "parent_value_injection": audit,
        "volume_integral_velocity_preMap": pre_integral.tolist(),
        "volume_integral_velocity_mapped": mapped_integral.tolist(),
        "absolute_volume_integral_velocity_change": float(np.linalg.norm(mapped_integral-pre_integral)),
        "net_integral_change_scaled_by_integrated_speed": float(
            np.linalg.norm(mapped_integral-pre_integral)/integrated_speed_scale
        ),
        "mapped_velocity_point_sample_error_vs_exact_mms": exact_error,
        "point_sample_error_decomposition": {
            "inherited_parent_solution_error_squared_relative": inherited_sq,
            "exact_parent_to_child_center_change_squared_relative": center_shift_sq,
            "twice_normalized_cross_term": cross_term,
            "total_mapped_error_squared_relative": total_sq,
            "identity_residual": float(total_sq-inherited_sq-center_shift_sq-cross_term),
            "basis": "Same-run preMap U is compared with exact MMS at preMap centers; exact reference change is evaluated from each containing parent center to each mapped child center. This is a point-sample identity, not a finite-volume cell-average error decomposition."
        },
        "interpretation_limits": [
            "This same-run comparison directly tests whether mapped cell-centered velocity equals containing-parent piecewise-constant injection for this single event.",
            "It is a point-value mapping audit, not a finite-volume cell-average accuracy certificate.",
            "A single n=16 diagnostic does not establish convergence, a general solver defect, or physical behavior."
        ]
    }
    out = EVIDENCE / "analysis.json"
    out.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(result, indent=2))
    if result["status"] != "SAME_RUN_PARENT_INJECTION_MATCH":
        raise SystemExit(2)


if __name__ == "__main__":
    analyze()
