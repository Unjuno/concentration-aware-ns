"""Separate AMR P0 field error into exact-mean mismatch and projection floor."""
import hashlib
import json
import re
import tarfile
from pathlib import Path

import numpy as np

from tools.audit_uniform_cell_center_quadrature import exact_cell_average_velocity
from tools.amr_projection_decomposition import (
    decompose_p0_error,
    exact_cell_mean_square_velocity,
    exact_cell_mean_square_gradient,
    exact_mms_mean_square_gradient,
    exact_mms_mean_square_velocity,
)


LENGTH = 2*np.pi
DOMAIN_VOLUME = LENGTH**3
FREQUENCY = 4


def _sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _field_bytes(archive, run, time, field):
    member = f"{run}/{time}/{field}"
    stream = archive.extractfile(member)
    if stream is None:
        raise ValueError(f"missing archived field {member}")
    return stream.read()


def _parse_vectors(raw):
    text = raw.decode("ascii")
    text = re.sub(r"/\*.*?\*/|//[^\n]*", "", text, flags=re.S)
    match = re.search(
        r"internalField\s+nonuniform\s+List<vector>\s+(\d+)\s*\((.*?)\)\s*;",
        text, re.S)
    if not match:
        raise ValueError("expected ASCII nonuniform vector field")
    count = int(match[1])
    values = np.fromstring(match[2].replace("(", " ").replace(")", " "), sep=" ")
    if values.size != count*3 or not np.isfinite(values).all():
        raise ValueError("invalid vector field values")
    return values.reshape(count, 3)


def _parse_volumes(raw, count):
    text = raw.decode("ascii")
    match = re.search(
        r"internalField\s+nonuniform\s+List<scalar>\s+(\d+)\s*\((.*?)\)\s*;",
        text, re.S)
    if not match or int(match[1]) != count:
        raise ValueError("volume field count mismatch")
    values = np.fromstring(match[2], sep=" ")
    if values.size != count or not np.isfinite(values).all() or np.any(values <= 0):
        raise ValueError("invalid cell volumes")
    return values


def _parse_levels(raw, count):
    text = raw.decode("ascii")
    match = re.search(
        r"internalField\s+nonuniform\s+List<scalar>\s+(\d+)\s*\((.*?)\)\s*;",
        text, re.S)
    if not match or int(match[1]) != count:
        raise ValueError("cell-level field count mismatch")
    levels = np.fromstring(match[2], sep=" ")
    if levels.size != count or not np.isfinite(levels).all():
        raise ValueError("invalid cell levels")
    rounded = np.rint(levels).astype(int)
    if not np.array_equal(levels, rounded) or np.any(rounded < 0):
        raise ValueError("cell levels must be nonnegative integers")
    return rounded
def main():
    evidence_dir = Path("evidence/of13-amr-first-refinement-v1")
    quadrature = json.loads(Path(
        "evidence/of13-amr-first-refinement-v1/cell-center-quadrature-audit.json"
    ).read_text())
    manifest = json.loads((evidence_dir/"manifest.json").read_text())
    expected_archives = {item["case"]: item["archive_sha256"]
                         for item in manifest["cases"]}
    cases = (
        ("amr-cap5000-t002", "amr-cap5000", "0.002", .002),
        ("uniform-n16-t002", "uniform-n16", "0.002", .002),
        ("amr-cap5000-t003", "amr-cap5000", "0.003", .003),
        ("uniform-n16-t003", "uniform-n16", "0.003", .003),
    )
    rows = []
    for name, run, time_name, time in cases:
        archive_path = evidence_dir/f"{run}.tar.gz"
        archive_digest = _sha256(archive_path)
        if archive_digest != expected_archives.get(run):
            raise ValueError(f"archive hash differs from manifest: {run}")
        with tarfile.open(archive_path) as archive:
            c_raw = _field_bytes(archive, run, time_name, "C")
            u_raw = _field_bytes(archive, run, time_name, "U")
            v_raw = _field_bytes(archive, run, time_name, "Vc")
            try:
                level_stream = archive.extractfile(f"{run}/{time_name}/cellLevel")
            except KeyError:
                level_stream = None
            if level_stream is None:
                level_raw = None
            else:
                level_raw = level_stream.read()
        centers = _parse_vectors(c_raw)
        velocity = _parse_vectors(u_raw)
        if len(centers) != len(velocity):
            raise ValueError(f"cell count mismatch in {name}")
        volume = _parse_volumes(v_raw, len(centers))
        widths = np.cbrt(volume)
        levels = np.rint(np.log2((LENGTH/16)/widths)).astype(int)
        expected_widths = (LENGTH/16)/(2.0**levels)
        if np.any(levels < 0) or np.any(levels > 2) or not np.allclose(
                widths, expected_widths, rtol=2e-10, atol=2e-12):
            raise ValueError(f"unsupported cell geometry in {name}")
        center_index = centers/widths[:, None]-.5
        if not np.allclose(center_index, np.rint(center_index), rtol=0, atol=2e-9):
            raise ValueError(f"cell centers do not match archived AMR hierarchy in {name}")
        if level_raw is None:
            levels = np.zeros(len(centers), dtype=int)
            level_source = "unrefined baseline inferred from the frozen checkpoints"
        else:
            levels = _parse_levels(level_raw, len(centers))
            level_source = "archived OpenFOAM cellLevel field"
        if not np.isclose(volume.sum(), DOMAIN_VOLUME, rtol=2e-12, atol=2e-12):
            raise ValueError(f"domain volume mismatch for {name}")
        average = exact_cell_average_velocity(centers, widths, time)
        exact_sq = exact_mms_mean_square_velocity(time, FREQUENCY)
        projected_sq = float(np.sum(volume*np.sum(average**2, axis=1))/DOMAIN_VOLUME)
        dof_sq = float(np.sum(volume*np.sum((velocity-average)**2, axis=1))/DOMAIN_VOLUME)
        exact_cell_sq = exact_cell_mean_square_velocity(
            centers, widths, time, FREQUENCY)
        exact_gradient_sq = exact_cell_mean_square_gradient(
            centers, widths, time, FREQUENCY)
        exact_gradient_global_sq = exact_mms_mean_square_gradient(time, FREQUENCY)
        if abs(float(np.sum(volume*exact_gradient_sq)/DOMAIN_VOLUME)
               - exact_gradient_global_sq) > 3e-12*exact_gradient_global_sq:
            raise ValueError(f"cell gradient-energy integrals fail Parseval check in {name}")
        variance_cells = exact_cell_sq-np.sum(average**2, axis=1)
        roundoff_tolerance = 2e-12*np.maximum(exact_cell_sq, exact_sq)
        if np.any(variance_cells < -roundoff_tolerance):
            raise ValueError(f"negative within-cell projection variance in {name}")
        variance_cells = np.maximum(variance_cells, 0)
        if abs(float(np.sum(volume*exact_cell_sq)/DOMAIN_VOLUME)-exact_sq) > 2e-12*exact_sq:
            raise ValueError(f"cell energy integrals fail Parseval check in {name}")
        split = decompose_p0_error(exact_sq, projected_sq, dof_sq)
        gauss8 = quadrature["cases"][name][
            "piecewise_constant_volume_l2_by_gauss_order"]["8"]
        agreement = abs(split["p0_total_relative_l2"]-gauss8)
        if agreement > 2e-7:
            raise ValueError(f"orthogonal split disagrees with independent Gauss P0 norm: {name}")
        level_rows = []
        for level in np.unique(levels):
            mask = levels == level
            level_rows.append({
                "level": int(level),
                "cell_count": int(mask.sum()),
                "volume_fraction": float(volume[mask].sum()/DOMAIN_VOLUME),
                "exact_kinetic_energy_fraction": float(
                    np.sum(volume[mask]*exact_cell_sq[mask])/(DOMAIN_VOLUME*exact_sq)),
                "exact_gradient_energy_fraction": float(
                    np.sum(volume[mask]*exact_gradient_sq[mask])
                    /(DOMAIN_VOLUME*exact_gradient_global_sq)),
                "projection_floor_fraction": float(
                    np.sum(volume[mask]*variance_cells[mask])
                    /max(DOMAIN_VOLUME*(exact_sq-projected_sq), 1e-300)),
                "dof_mismatch_fraction": float(
                    np.sum(volume[mask]*np.sum((velocity[mask]-average[mask])**2, axis=1))
                    /max(DOMAIN_VOLUME*dof_sq, 1e-300)),
            })
        rows.append({
            "case": name,
            "cell_count": int(len(centers)),
            "cell_level_source": level_source,
            "cell_levels": level_rows,
            "archive_sha256": archive_digest,
            "input_sha256": {
                "C": hashlib.sha256(c_raw).hexdigest(),
                "U": hashlib.sha256(u_raw).hexdigest(),
                "Vc": hashlib.sha256(v_raw).hexdigest(),
                "cellLevel": (hashlib.sha256(level_raw).hexdigest()
                              if level_raw is not None else None),
            },
            "exact_mean_square_velocity": exact_sq,
            "exact_mean_square_gradient": exact_gradient_global_sq,
            "cell_average_projection_mean_square": projected_sq,
            "mean_dof_mismatch_mean_square": dof_sq,
            **split,
            "independent_gauss8_p0_relative_l2": gauss8,
            "orthogonal_split_vs_gauss8_absolute_difference": agreement,
            "mean_dof_fraction_of_total_squared_error": dof_sq/(dof_sq+exact_sq-projected_sq),
            "projection_floor_fraction_of_total_squared_error": (
                (exact_sq-projected_sq)/(dof_sq+exact_sq-projected_sq)),
        })
    result = {
        "method": (
            "L2 orthogonal projection identity for the explicitly chosen P0 "
            "piecewise-constant reconstruction: ||U-u||^2 = ||U-P_hu||^2 + "
            "||P_hu-u||^2. Exact cell means use the closed-form Fourier factors; "
            "the continuum mean-square norm uses Parseval coefficients."
        ),
        "levelwise_method": (
            "Exact cell averages of |u|^2 and |grad u|_F^2 are evaluated from "
            "finite Fourier-coefficient convolutions and grouped by archived "
            "cellLevel. These are integrals of the known reference, not samples "
            "of solver gradients."
        ),
        "scope": (
            "Retrospective interpretation audit, not solver-native field semantics. "
            "It separates discrete cell-mean mismatch from unresolved within-cell "
            "reference variation; it does not identify transfer/flux-correction "
            "causality or establish an AMR defect."
        ),
        "source_sha256": {
            path: _sha256(path) for path in (
                "tools/audit_amr_projection_decomposition.py",
                "tools/amr_projection_decomposition.py",
                "tools/audit_uniform_cell_center_quadrature.py",
                "tools/high_gradient_reference.py",
            )
        },
        "independent_gauss_audit_sha256": _sha256(
            "evidence/of13-amr-first-refinement-v1/cell-center-quadrature-audit.json"),
        "cases": rows,
    }
    out = Path("evidence/tests/amr-p0-projection-decomposition.json")
    out.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
