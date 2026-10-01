"""Reconstruct interior Gauss gradients and vorticity from AMR face snapshots."""

import csv
import io
import json
import os
import tarfile
from pathlib import Path

import numpy as np

from tools.high_gradient_reference import fields


PROTOCOL = Path(os.environ.get(
    "CANS_AMR_STAGE_PROTOCOL", "protocols/high-gradient-of13-amr-same-run-map-v4.json"
))
EVIDENCE = Path(os.environ.get(
    "CANS_AMR_STAGE_EVIDENCE", "evidence/of13-amr-same-run-map-v4-run3"
))
ARCHIVE_OVERRIDE = os.environ.get("CANS_AMR_STAGE_RAW_ARCHIVE")
CASE_DIRECTORY_OVERRIDE = os.environ.get("CANS_AMR_STAGE_ARCHIVE_CASE_DIR")


def _read_csv(archive, member):
    with tarfile.open(archive, "r:gz") as tf:
        stream = tf.extractfile(member)
        if stream is None:
            raise ValueError(f"missing archived snapshot {member}")
        rows = list(csv.DictReader(io.StringIO(stream.read().decode())))
    if not rows:
        raise ValueError(f"empty snapshot {member}")
    return {key: np.asarray([float(row[key]) for row in rows]) for key in rows[0]}


def gauss_gradient_from_internal_faces(volumes, owner, neighbour, face_u, face_area):
    """Compute Gauss-linear cell gradients from oriented internal-face Uf/S."""
    volumes = np.asarray(volumes, dtype=float)
    owner = np.asarray(owner, dtype=int)
    neighbour = np.asarray(neighbour, dtype=int)
    face_u = np.asarray(face_u, dtype=float)
    face_area = np.asarray(face_area, dtype=float)
    if volumes.ndim != 1 or np.any(volumes <= 0) or not np.isfinite(volumes).all():
        raise ValueError("volumes must be finite positive values")
    if owner.shape != neighbour.shape or owner.ndim != 1:
        raise ValueError("owner and neighbour must be matching vectors")
    if face_u.shape != (len(owner), 3) or face_area.shape != (len(owner), 3):
        raise ValueError("face velocity and area vectors must have shape (faces, 3)")
    if (np.any(owner < 0) or np.any(neighbour < 0)
            or np.any(owner >= len(volumes)) or np.any(neighbour >= len(volumes))
            or np.any(owner == neighbour)):
        raise ValueError("face addressing is invalid")
    if not np.isfinite(face_u).all() or not np.isfinite(face_area).all():
        raise ValueError("face values must be finite")

    integrated = np.zeros((len(volumes), 3, 3), dtype=float)
    flux_tensor = face_u[:, :, None] * face_area[:, None, :]
    np.add.at(integrated, owner, flux_tensor)
    np.add.at(integrated, neighbour, -flux_tensor)
    return integrated / volumes[:, None, None]


def interior_periodic_mask(centers, volumes, domain_length=2*np.pi,
                           boundary_margin=None, tolerance=1e-10):
    """Exclude cells touching periodic boundary patches omitted from snapshots."""
    centers = np.asarray(centers, dtype=float)
    widths = np.cbrt(np.asarray(volumes, dtype=float))
    if centers.shape != (len(widths), 3) or np.any(widths <= 0):
        raise ValueError("centers and positive volumes have incompatible shapes")
    distance = np.minimum(centers, domain_length-centers)
    margin = widths/2 if boundary_margin is None else np.full(len(widths), boundary_margin)
    return np.all(distance > margin[:, None] + tolerance, axis=1)


def vorticity_from_gradient(gradient):
    gradient = np.asarray(gradient, dtype=float)
    if gradient.ndim != 3 or gradient.shape[1:] != (3, 3):
        raise ValueError("gradient must have shape (cells, 3, 3)")
    return np.column_stack((
        gradient[:, 2, 1]-gradient[:, 1, 2],
        gradient[:, 0, 2]-gradient[:, 2, 0],
        gradient[:, 1, 0]-gradient[:, 0, 1],
    ))


def relative_volume_l2(values, reference, volumes, mask):
    values = np.asarray(values, dtype=float)
    reference = np.asarray(reference, dtype=float)
    volumes = np.asarray(volumes, dtype=float)
    mask = np.asarray(mask, dtype=bool)
    delta = values[mask]-reference[mask]
    ref = reference[mask]
    weight = volumes[mask]
    return float(np.sqrt(np.sum(weight.reshape((-1,)+(1,)*(delta.ndim-1))*delta**2)
                         / np.sum(weight.reshape((-1,)+(1,)*(ref.ndim-1))*ref**2)))


def same_parent_face_audit(pre_centers, pre_velocity, mapped_centers, face):
    """Check mapped-face interpolation on faces internal to one parent cube."""
    n_float = round(len(pre_centers)**(1/3))
    if n_float**3 != len(pre_centers):
        raise ValueError("preMap topology is not a uniform n^3 parent grid")
    n = int(n_float)
    length = 2*np.pi
    width = length/n
    pre_index = np.rint(np.mod(pre_centers, length)/width - 0.5).astype(int) % n
    parent_id = (pre_index[:, 0]*n + pre_index[:, 1])*n + pre_index[:, 2]
    parent_slot = {int(pid): i for i, pid in enumerate(parent_id)}

    mapped_parent = np.floor(np.mod(mapped_centers, length)/width).astype(int) % n
    mapped_parent_id = (mapped_parent[:, 0]*n + mapped_parent[:, 1])*n + mapped_parent[:, 2]
    owner = face["owner"].astype(int)
    neighbour = face["neighbour"].astype(int)
    same = mapped_parent_id[owner] == mapped_parent_id[neighbour]
    if not np.any(same):
        raise ValueError("mapped mesh has no internal same-parent faces")
    face_velocity = _vector(face, ("Ufx", "Ufy", "Ufz"))
    parent_values = np.asarray([
        pre_velocity[parent_slot[int(pid)]] for pid in mapped_parent_id[owner[same]]
    ])
    residual = face_velocity[same]-parent_values
    return {
        "internal_faces": int(len(owner)),
        "same_parent_internal_faces": int(same.sum()),
        "same_parent_internal_face_fraction": float(same.mean()),
        "same_parent_Uf_max_abs_difference_from_injected_parent_value":
            float(np.max(np.abs(residual))),
        "interpretation": "Same-parent child interfaces carry the injected constant parent value; these interfaces introduce no subcell slope in mapped U.",
    }


def _vector(table, names):
    return np.column_stack([table[key] for key in names])


def periodic_uniform_gauss_gradient(centers, velocity, length=2*np.pi):
    """Rebuild the uniform periodic Gauss gradient from arithmetic face U.

    On this orthogonal uniform mesh, linear face interpolation is the midpoint
    average, and the resulting Gauss sum is the centered periodic difference.
    """
    centers = np.asarray(centers, dtype=float)
    velocity = np.asarray(velocity, dtype=float)
    n_float = round(len(centers)**(1/3))
    if (n_float < 2 or n_float**3 != len(centers)
            or velocity.shape != (len(centers), 3)):
        raise ValueError("uniform preMap field must contain n^3 vector cells")
    n = int(n_float)
    h = length/n
    indices = np.rint(np.mod(centers, length)/h - 0.5).astype(int) % n
    expected = (indices+0.5)*h
    if np.max(np.abs(centers-expected)) > 1e-10*max(1.0, length):
        raise ValueError("preMap centers are not a uniform periodic Cartesian grid")
    grid = np.empty((n, n, n, 3), dtype=float)
    if len(np.unique(indices, axis=0)) != len(centers):
        raise ValueError("preMap centers do not uniquely fill the uniform grid")
    grid[indices[:, 0], indices[:, 1], indices[:, 2]] = velocity
    derivative = np.stack([
        (np.roll(grid, -1, axis=axis)-np.roll(grid, 1, axis=axis))/(2*h)
        for axis in range(3)
    ], axis=-1)
    return derivative[indices[:, 0], indices[:, 1], indices[:, 2]]


def _stage(archive, case_dir, stage, time_label, frequency, boundary_margin):
    cell = _read_csv(archive,
                     f"{case_dir}/postProcessing/amrStages/{time_label}/{stage}_cells.csv")
    centers = _vector(cell, ("cx", "cy", "cz"))
    volumes = cell["V"]
    face_member = f"{case_dir}/postProcessing/amrStages/{time_label}/{stage}_faces.csv"
    try:
        face = _read_csv(archive, face_member)
    except (KeyError, ValueError):
        if stage != "preMap":
            raise
        grad = periodic_uniform_gauss_gradient(
            centers, _vector(cell, ("Ux", "Uy", "Uz"))
        )
        gradient_method = "periodic centered difference, equivalent to the arithmetic-midpoint Gauss face sum on the uniform orthogonal preMap grid"
    else:
        grad = gauss_gradient_from_internal_faces(
            volumes, face["owner"], face["neighbour"],
            _vector(face, ("Ufx", "Ufy", "Ufz")),
            _vector(face, ("Sx", "Sy", "Sz")),
        )
        gradient_method = "Gauss sum of captured Uf outer oriented face area S divided by cell volume"
    time = float(time_label)
    exact = fields(centers, N=frequency, nu=0.01, time=time)
    mask = interior_periodic_mask(
        centers, volumes, boundary_margin=boundary_margin
    )
    if not np.any(mask):
        raise ValueError(f"no interior cells available at {stage}")
    omega = vorticity_from_gradient(grad)
    rows = {
        "stage": stage, "time": time_label, "cells": len(volumes),
        "gradient_method": gradient_method,
        "interior_cells": int(mask.sum()),
        "interior_volume_fraction": float(volumes[mask].sum()/volumes.sum()),
        "interior_gauss_gradient_relative_l2_vs_exact_point_gradient":
            relative_volume_l2(grad, exact["grad_u"], volumes, mask),
        "interior_gauss_vorticity_relative_l2_vs_exact_point_vorticity":
            relative_volume_l2(omega, exact["vorticity"], volumes, mask),
        "gauss_gradient_max_abs_component_error_interior": float(
            np.max(np.abs(grad[mask]-exact["grad_u"][mask]))
        ),
        "gauss_vorticity_max_abs_component_error_interior": float(
            np.max(np.abs(omega[mask]-exact["vorticity"][mask]))
        ),
    }
    return rows


def analyze():
    spec = json.loads(PROTOCOL.read_text())
    case = spec["case"]
    manifest = json.loads((EVIDENCE/"manifest.json").read_text())
    archive = (Path(ARCHIVE_OVERRIDE) if ARCHIVE_OVERRIDE else
               EVIDENCE/case.get("archive_name", "amr-stage-snapshot.tar.gz"))
    case_dir = (CASE_DIRECTORY_OVERRIDE or manifest.get(
        "case_directory", case.get("case_directory", "amr-cap5000")
    ))
    pre_time = f"{case.get('pre_map_time', 0.002):g}"
    post_time = f"{case.get('solver_stage_time', 0.003):g}"
    base_width = 2*np.pi/case["initial_grid_cells_per_axis"]
    # Two base widths place the retained boundary on the same coarse-grid
    # face after refinement, avoiding stage-dependent support at the mask edge.
    boundary_margin = 2*base_width
    rows = [
        _stage(archive, case_dir, "preMap", pre_time, case["frequency"], boundary_margin),
        _stage(archive, case_dir, "mapped", pre_time, case["frequency"], boundary_margin),
    ]
    pre_cells = _read_csv(
        archive, f"{case_dir}/postProcessing/amrStages/{pre_time}/preMap_cells.csv"
    )
    mapped_cells = _read_csv(
        archive, f"{case_dir}/postProcessing/amrStages/{pre_time}/mapped_cells.csv"
    )
    mapped_face = _read_csv(
        archive, f"{case_dir}/postProcessing/amrStages/{pre_time}/mapped_faces.csv"
    )
    same_parent_faces = same_parent_face_audit(
        _vector(pre_cells, ("cx", "cy", "cz")),
        _vector(pre_cells, ("Ux", "Uy", "Uz")),
        _vector(mapped_cells, ("cx", "cy", "cz")), mapped_face,
    )
    result = {
        "status": "INTERIOR_GAUSS_GRADIENT_AND_CURL_RECONSTRUCTED",
        "protocol": PROTOCOL.as_posix(),
        "archive_sha256": manifest["archive_sha256"],
        "method": "Finite-volume Gauss gradient. Mapped stage uses captured face-interpolated Uf and oriented area vectors; uniform preMap stage can be replayed without face CSVs using centered periodic differences, equivalent to arithmetic-midpoint Gauss interpolation on a uniform orthogonal mesh.",
        "reference": "Analytic MMS point gradient and vorticity evaluated at cell centers.",
        "boundary_treatment": f"A shared physical interior mask excludes centers within two base-grid widths ({boundary_margin:.17g}) of any periodic boundary, aligning the retained coarse-cell and refined-cell faces for both preMap and mapped stages; paired cyclic boundary faces are absent from the snapshot. Metrics are volume weighted over this same physical subdomain.",
        "stages": rows,
        "same_parent_face_audit": same_parent_faces,
        "interpretation_limits": [
            "This is an interior Gauss reconstruction from captured face Uf, not necessarily the solver's configured or stored grad(U) field.",
            "The exact reference is sampled at cell centers, not volume averaged; this is not a cell-integrated gradient norm.",
            "Periodic-boundary cells are excluded because paired cyclic boundary faces are not present in the face snapshot.",
            "A discrete gradient/vorticity discrepancy is not evidence of blow-up, particle alignment, phase transition, or constitutive-viscosity change."
        ]
    }
    (EVIDENCE/"gauss-gradient-audit.json").write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(result, indent=2))
    return result


if __name__ == "__main__":
    analyze()
