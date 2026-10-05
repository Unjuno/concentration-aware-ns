"""Volume-integrated MMS error for archived AMR Gauss-gradient fields.

Integrates the exact gradient and vorticity error of each cellwise-constant
finite-volume reconstruction inside every retained cell. This is stronger
than evaluating the analytic derivatives only at cell centers, but it is not
a reconstruction of a continuous solver velocity field.
"""

import hashlib
import json
import math
from pathlib import Path
import tempfile

import numpy as np

from tools.analyze_amr_gauss_gradient import (
    _read_csv,
    _vector,
    gauss_gradient_from_internal_faces,
    interior_periodic_mask,
    least_squares_gradient_from_internal_faces,
    periodic_uniform_gauss_gradient,
    vorticity_from_gradient,
)
from tools.high_gradient_reference import fields
from tools.reconstruct_amr_published_archive import reconstruct


ROOT = Path(__file__).resolve().parents[1]
CASES = (
    (16, "evidence/of13-amr-same-run-map-v4-run3",
     "protocols/high-gradient-of13-amr-same-run-map-v4.json"),
    (32, "evidence/of13-amr-same-run-map-v5-n32",
     "protocols/high-gradient-of13-amr-same-run-map-v5-n32.json"),
    (64, "evidence/of13-amr-same-run-map-v7-n64",
     "protocols/high-gradient-of13-amr-same-run-map-v7-n64.json"),
)
LENGTH = 2 * math.pi
COMMON_MARGIN = math.pi / 4
QUADRATURE_ORDERS = (6, 8)
CHUNK_CELLS = 512


def _sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def _cell_widths_and_validate(centers, volumes, n):
    centers = np.asarray(centers, dtype=float)
    volumes = np.asarray(volumes, dtype=float)
    if centers.shape != (len(volumes), 3) or not np.isfinite(centers).all():
        raise ValueError("cell centers must be finite with shape (cells, 3)")
    if not np.isfinite(volumes).all() or np.any(volumes <= 0):
        raise ValueError("cell volumes must be finite and positive")
    widths = np.cbrt(volumes)
    base = LENGTH / n
    level_widths = np.array([base, base / 2])
    nearest = np.argmin(np.abs(widths[:, None] - level_widths[None, :]), axis=1)
    if np.max(np.abs(widths - level_widths[nearest])) > 2e-9:
        raise ValueError("archive contains cells outside the expected cubic AMR levels")
    wrapped = np.mod(centers, LENGTH)
    grid_index = np.rint((wrapped - widths[:, None] / 2) / widths[:, None])
    aligned = grid_index * widths[:, None] + widths[:, None] / 2
    residual = np.mod(wrapped - aligned + LENGTH / 2, LENGTH) - LENGTH / 2
    if np.max(np.abs(residual)) > 2e-8:
        raise ValueError("cell centers are not aligned to axis-aligned cubic AMR cells")
    return widths


def _quadrature_offsets(order):
    nodes, weights = np.polynomial.legendre.leggauss(order)
    mesh = np.meshgrid(nodes, nodes, nodes, indexing="ij")
    offsets = np.stack(mesh, axis=-1).reshape(-1, 3)
    wmesh = np.meshgrid(weights, weights, weights, indexing="ij")
    normalized_weights = np.prod(np.stack(wmesh, axis=-1), axis=-1).reshape(-1) / 8
    return offsets, normalized_weights


def _integrated_relative_errors(centers, widths, volumes, mask, discrete_grad,
                                n_frequency, time, order=QUADRATURE_ORDERS[-1]):
    offsets, qweights = _quadrature_offsets(order)
    selected = np.flatnonzero(mask)
    grad_num = grad_den = vort_num = vort_den = 0.0
    for start in range(0, len(selected), CHUNK_CELLS):
        ids = selected[start:start + CHUNK_CELLS]
        cell_centers = centers[ids]
        cell_widths = widths[ids]
        cell_volumes = volumes[ids]
        points = cell_centers[:, None, :] + (
            cell_widths[:, None, None] / 2
        ) * offsets[None, :, :]
        exact = fields(points, N=n_frequency, nu=0.01, time=time)
        exact_grad = exact["grad_u"]
        exact_vort = exact["vorticity"]
        grad_delta = discrete_grad[ids, None, :, :] - exact_grad
        vort_delta = vorticity_from_gradient(discrete_grad[ids])[:, None, :] - exact_vort
        grad_num += np.sum(cell_volumes * np.sum(
            qweights[None, :] * np.sum(grad_delta**2, axis=(-2, -1)), axis=1
        ))
        grad_den += np.sum(cell_volumes * np.sum(
            qweights[None, :] * np.sum(exact_grad**2, axis=(-2, -1)), axis=1
        ))
        vort_num += np.sum(cell_volumes * np.sum(
            qweights[None, :] * np.sum(vort_delta**2, axis=-1), axis=1
        ))
        vort_den += np.sum(cell_volumes * np.sum(
            qweights[None, :] * np.sum(exact_vort**2, axis=-1), axis=1
        ))
    return {
        "quadrature_order_per_axis": order,
        "integrated_cellwise_constant_gradient_relative_l2":
            math.sqrt(grad_num / grad_den),
        "integrated_cellwise_constant_curl_relative_l2":
            math.sqrt(vort_num / vort_den),
        "integrated_physical_volume": float(np.sum(volumes[mask])),
        "retained_cells": int(np.count_nonzero(mask)),
    }


def _analyze_stage(archive, case_dir, stage, time_label, n, frequency):
    cell = _read_csv(
        archive, f"{case_dir}/postProcessing/amrStages/{time_label}/{stage}_cells.csv"
    )
    centers = _vector(cell, ("cx", "cy", "cz"))
    volumes = cell["V"]
    widths = _cell_widths_and_validate(centers, volumes, n)
    if stage == "preMap":
        gradient = periodic_uniform_gauss_gradient(
            centers, _vector(cell, ("Ux", "Uy", "Uz"))
        )
        operator = "uniform periodic centered difference (midpoint Gauss equivalent)"
    else:
        face = _read_csv(
            archive, f"{case_dir}/postProcessing/amrStages/{time_label}/{stage}_faces.csv"
        )
        face_velocity = _vector(face, ("Ufx", "Ufy", "Ufz"))
        face_area = _vector(face, ("Sx", "Sy", "Sz"))
        gradient = gauss_gradient_from_internal_faces(
            volumes, face["owner"], face["neighbour"],
            face_velocity, face_area,
        )
        operator = "captured face-Uf finite-volume Gauss sum on mapped mesh"
    mask = interior_periodic_mask(
        centers, volumes, boundary_margin=COMMON_MARGIN
    )
    coarse, fine = (
        _integrated_relative_errors(
            centers, widths, volumes, mask, gradient, frequency,
            float(time_label), order=order,
        )
        for order in QUADRATURE_ORDERS
    )
    result = fine
    result["quadrature_convergence"] = {
        "comparison_order_per_axis": QUADRATURE_ORDERS[0],
        "fine_order_per_axis": QUADRATURE_ORDERS[1],
        "gradient_relative_l2_absolute_difference": abs(
            fine["integrated_cellwise_constant_gradient_relative_l2"]
            - coarse["integrated_cellwise_constant_gradient_relative_l2"]
        ),
        "vorticity_relative_l2_absolute_difference": abs(
            fine["integrated_cellwise_constant_curl_relative_l2"]
            - coarse["integrated_cellwise_constant_curl_relative_l2"]
        ),
    }
    result.update({
        "stage": stage,
        "operator": operator,
        "cells": int(len(volumes)),
        "interior_volume_fraction": float(volumes[mask].sum() / volumes.sum()),
        "cell_width_levels": [float(LENGTH / n), float(LENGTH / (2 * n))],
    })
    if stage == "mapped":
        ls_gradient, ls_diagnostics = least_squares_gradient_from_internal_faces(
            centers, _vector(cell, ("Ux", "Uy", "Uz")),
            face["owner"], face["neighbour"], periodic_length=LENGTH,
        )
        ls_coarse, ls_fine = (
            _integrated_relative_errors(
                centers, widths, volumes, mask, ls_gradient, frequency,
                float(time_label), order=order,
            )
            for order in QUADRATURE_ORDERS
        )
        result["alternative_reconstruction"] = {
            "name": "unweighted one-ring cell-center least-squares gradient",
            "construction": "Fit each cell's velocity differences to periodic minimum-image center displacements over captured internal-face neighbors; report the resulting cellwise-constant gradient and curl.",
            "operator_diagnostics": ls_diagnostics,
            "volume_integrated_error": ls_fine,
            "quadrature_convergence": {
                "comparison_order_per_axis": QUADRATURE_ORDERS[0],
                "fine_order_per_axis": QUADRATURE_ORDERS[1],
                "gradient_relative_l2_absolute_difference": abs(
                    ls_fine["integrated_cellwise_constant_gradient_relative_l2"]
                    - ls_coarse["integrated_cellwise_constant_gradient_relative_l2"]
                ),
                "vorticity_relative_l2_absolute_difference": abs(
                    ls_fine["integrated_cellwise_constant_curl_relative_l2"]
                    - ls_coarse["integrated_cellwise_constant_curl_relative_l2"]
                ),
            },
        }
    return result


def _case(n, evidence_rel, protocol_rel):
    evidence = ROOT / evidence_rel
    protocol_path = ROOT / protocol_rel
    manifest = json.loads((evidence / "manifest.json").read_text())
    protocol = json.loads(protocol_path.read_text())
    archive = evidence / manifest["archive"]
    label = archive.relative_to(ROOT).as_posix()
    if not archive.is_file():
        parts = evidence / "amr-stage-snapshot-n64-review.tar.gz.zst.parts.json"
        with tempfile.TemporaryDirectory(prefix="cans-amr-integrated-") as temp:
            archive = Path(temp) / manifest["archive"]
            reconstruct(parts, archive)
            row = _case_archive(n, evidence, protocol_path, protocol, manifest,
                                archive, label)
    else:
        row = _case_archive(n, evidence, protocol_path, protocol, manifest,
                            archive, label)
    return row


def _case_archive(n, evidence, protocol_path, protocol, manifest, archive, label):
    if _sha256(archive) != manifest["archive_sha256"]:
        raise ValueError(f"archive SHA-256 mismatch for n={n}")
    case = protocol["case"]
    if case["initial_grid_cells_per_axis"] != n:
        raise ValueError(f"protocol resolution mismatch for n={n}")
    if manifest.get("foundation_source_commit") != \
            "18870c24d21c6b982e2cdec27b2f59738cca5f90":
        raise ValueError(f"Foundation source pin mismatch for n={n}")
    case_dir = manifest.get("case_directory", "amr-cap5000")
    time_label = f"{case.get('pre_map_time', 0.002):g}"
    return {
        "n": n,
        "archive": label,
        "archive_sha256": manifest["archive_sha256"],
        "protocol": protocol_path.relative_to(ROOT).as_posix(),
        "protocol_sha256": _sha256(protocol_path),
        "frequency": case["frequency"],
        "time": time_label,
        "stages": [
            _analyze_stage(archive, case_dir, stage, time_label, n,
                           case["frequency"])
            for stage in ("preMap", "mapped")
        ],
    }


def compare():
    expected_fraction = ((LENGTH - 2 * COMMON_MARGIN) / LENGTH) ** 3
    return {
        "status": "PASS_VOLUME_INTEGRATED_AMR_RECONSTRUCTION_REPLAY",
        "analyzer_sha256": _sha256(Path(__file__)),
        "derivative_operators": {
            "path": "tools/analyze_amr_gauss_gradient.py",
            "sha256": _sha256(ROOT / "tools/analyze_amr_gauss_gradient.py"),
        },
        "reference": "Analytic manufactured-solution gradient and vorticity integrated inside each retained cell with tensor Gauss-Legendre quadrature.",
        "discrete_field": "Cellwise-constant finite-volume Gauss gradient and one-ring least-squares alternative, with their curls; neither is a reconstructed continuous OpenFOAM velocity field.",
        "mask": {
            "definition": "cell centers farther than pi/4 from all periodic boundaries; aligned physical support across resolutions",
            "physical_margin": COMMON_MARGIN,
            "expected_volume_fraction": expected_fraction,
        },
        "quadrature_orders_per_axis": list(QUADRATURE_ORDERS),
        "cases": [_case(*case) for case in CASES],
        "limitations": [
            "The quadrature integrates exact derivatives over each selected cell, but does not certify the spatial interpolation used by the solver or its continuous velocity field.",
            "The cell-center least-squares gradient is a post-processing alternative, not the solver's declared gradient operator or a fitted velocity polynomial over cell interiors.",
            "AMR events are exploratory single runs and have no preregistered quality threshold; no AMR PASS/FAIL or upstream defect conclusion is assigned.",
            "Numerical quadrature is a deterministic diagnostic, not an interval-arithmetic error bound.",
        ],
    }


if __name__ == "__main__":
    result = compare()
    output = ROOT / "evidence/of13-amr-volume-integrated-comparison-2026-10-02.json"
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
