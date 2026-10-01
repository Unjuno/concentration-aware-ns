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
from tools.high_gradient_cell_average import exact_cell_average_velocity


EVIDENCE = Path(os.environ.get("CANS_AMR_STAGE_EVIDENCE", "evidence/of13-amr-same-run-map-v4-run3"))
PROTOCOL = Path(os.environ.get(
    "CANS_AMR_STAGE_PROTOCOL", "protocols/high-gradient-of13-amr-same-run-map-v4.json"
))
CELL_AVERAGE_AUDIT = Path("evidence/of13-high-gradient-v2/uniform-cell-center-quadrature-audit.json")
MANIFEST = EVIDENCE / "manifest.json"
_DEFAULT_CASE_SPEC = json.loads(PROTOCOL.read_text())["case"]
ARCHIVE = EVIDENCE / _DEFAULT_CASE_SPEC.get(
    "archive_name", "amr-stage-snapshot.tar.gz"
)


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
    spec = json.loads(PROTOCOL.read_text())
    case_spec = spec["case"]
    archive = EVIDENCE / case_spec.get("archive_name", "amr-stage-snapshot.tar.gz")
    case_directory = manifest.get("case_directory", case_spec.get("case_directory", "amr-cap5000"))
    pre_map_time = case_spec.get("pre_map_time", 0.002)
    pre_map_label = f"{pre_map_time:g}"
    if not archive.is_file():
        raise FileNotFoundError(archive)
    if manifest["status"] != "RUN_COMPLETE_SAME_RUN_MAP_CAPTURED":
        raise ValueError("same-run mapping gate is not complete")
    if sha(archive) != manifest["archive_sha256"]:
        raise ValueError("archive hash differs from manifest")
    if manifest["exit_code"] != 0 or not manifest["end_marker"]:
        raise ValueError("solver did not complete normally")
    if not manifest["instrumented_library_load_confirmed"]:
        raise ValueError("instrumented library load is not confirmed")
    if manifest.get("protocol") != PROTOCOL.as_posix():
        raise ValueError("manifest protocol path differs from selected protocol")

    pre = read_csv(archive, f"{case_directory}/postProcessing/amrStages/{pre_map_label}/preMap_cells.csv")
    mapped = read_csv(archive, f"{case_directory}/postProcessing/amrStages/{pre_map_label}/mapped_cells.csv")
    pre_centers = np.column_stack([pre[k] for k in ("cx", "cy", "cz")])
    mapped_centers = np.column_stack([mapped[k] for k in ("cx", "cy", "cz")])
    pre_u = np.column_stack([pre[k] for k in ("Ux", "Uy", "Uz")])
    mapped_u = np.column_stack([mapped[k] for k in ("Ux", "Uy", "Uz")])
    if len(pre_u) != case_spec["initial_cells"]:
        raise ValueError("captured preMap cell count differs from protocol")
    expected_mapped = case_spec.get("expected_mapped_cells")
    if expected_mapped is not None and len(mapped_u) != expected_mapped:
        raise ValueError("captured mapped cell count differs from protocol")
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
    exact_u = fields(exact, N=case_spec["frequency"], nu=0.01, time=pre_map_time)["u"]
    exact_pre_u = fields(pre_centers, N=case_spec["frequency"], nu=0.01, time=pre_map_time)["u"]
    pre_exact_average = exact_cell_average_velocity(
        pre_centers, np.cbrt(pre["V"]), pre_map_time, frequency=case_spec["frequency"]
    )
    mapped_exact_average = exact_cell_average_velocity(
        mapped_centers, np.cbrt(mapped["V"]), pre_map_time, frequency=case_spec["frequency"]
    )
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
    inherited_average_error = pre_u[parent_for_child]-pre_exact_average[parent_for_child]
    exact_average_refinement_delta = pre_exact_average[parent_for_child]-mapped_exact_average
    average_denominator = float(np.sum(mapped["V"][:, None]*mapped_exact_average**2))
    inherited_average_sq = float(np.sum(
        mapped["V"][:, None]*inherited_average_error**2
    )/average_denominator)
    average_refinement_sq = float(np.sum(
        mapped["V"][:, None]*exact_average_refinement_delta**2
    )/average_denominator)
    average_cross_term = float(2*np.sum(
        mapped["V"][:, None]*inherited_average_error*exact_average_refinement_delta
    )/average_denominator)
    average_total_sq = float(np.sum(
        mapped["V"][:, None]*(mapped_u-mapped_exact_average)**2
    )/average_denominator)
    exact_error = float(np.sqrt(
        np.sum(mapped["V"][:, None]*(mapped_u-exact_u)**2)
        / max(np.sum(mapped["V"][:, None]*exact_u**2), 1e-300)
    ))
    pre_cell_average_error = float(np.sqrt(
        np.sum(pre["V"][:, None]*(pre_u-pre_exact_average)**2)
        / max(np.sum(pre["V"][:, None]*pre_exact_average**2), 1e-300)
    ))
    mapped_cell_average_error = float(np.sqrt(
        np.sum(mapped["V"][:, None]*(mapped_u-mapped_exact_average)**2)
        / max(np.sum(mapped["V"][:, None]*mapped_exact_average**2), 1e-300)
    ))
    result = {
        "status": "SAME_RUN_PARENT_INJECTION_MATCH" if audit["mapped_vs_parent_injection_relative_l2"] < 1e-12 else "SAME_RUN_PARENT_INJECTION_MISMATCH",
        "protocol": manifest["protocol"],
        "archive_sha256": manifest["archive_sha256"],
        "preMap_time": pre_map_label,
        "mapped_time": pre_map_label,
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
        "exact_cell_average_reference": {
            "method": "Closed-form tensor factorization of the separable Fourier-polynomial MMS; each one-dimensional Fourier mode is integrated over its cell with a sinc factor. The formula is independently checked against tensor Gauss quadrature in tools.audit_uniform_cell_center_quadrature.",
            "preMap_velocity_relative_l2_vs_exact_cell_averages": pre_cell_average_error,
            "mapped_velocity_relative_l2_vs_exact_cell_averages": mapped_cell_average_error,
            "independent_formula_validation": {
                "crosscheck_artifact": CELL_AVERAGE_AUDIT.as_posix(),
                "crosscheck_artifact_sha256": sha(CELL_AVERAGE_AUDIT),
                "closed_form_vs_tensor_gauss_max_abs_difference": json.loads(CELL_AVERAGE_AUDIT.read_text())["cell_average_formula_crosscheck_max_abs_difference"]
            },
            "same_run_cell_average_error_decomposition": {
                "inherited_parent_solution_error_squared_relative": inherited_average_sq,
                "exact_child_average_refinement_change_squared_relative": average_refinement_sq,
                "twice_normalized_cross_term": average_cross_term,
                "total_mapped_cell_average_error_squared_relative": average_total_sq,
                "identity_residual": float(average_total_sq-inherited_average_sq-average_refinement_sq-average_cross_term),
                "basis": "Exact averages use the closed form on preMap parent cubes and mapped child cubes. This DOF-level identity separates inherited coarse average error from exact-reference variation revealed by refinement; it is not a continuous P0 reconstruction norm."
            },
            "cubic_cell_width_range": {
                "preMap_min": float(np.min(np.cbrt(pre["V"]))),
                "preMap_max": float(np.max(np.cbrt(pre["V"]))),
                "mapped_min": float(np.min(np.cbrt(mapped["V"]))),
                "mapped_max": float(np.max(np.cbrt(mapped["V"]))),
            },
            "interpretation": "This is a comparison of stored cell degrees of freedom to analytic volume averages. OpenFOAM volVectorField storage is cell-associated; this diagnostic does not assume the evolved stored U is itself defined as an exact cell average."
        },
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
            f"A single n={case_spec['initial_grid_cells_per_axis']} diagnostic does not establish convergence, a general solver defect, or physical behavior."
        ]
    }
    out = EVIDENCE / "analysis.json"
    out.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(result, indent=2))
    if result["status"] != "SAME_RUN_PARENT_INJECTION_MATCH":
        raise SystemExit(2)


if __name__ == "__main__":
    analyze()
