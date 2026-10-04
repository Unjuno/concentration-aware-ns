"""Analyze captured Foundation-13 AMR stages without assigning defect status."""
import csv
import hashlib
import io
import json
from pathlib import Path
import re
import tarfile

import numpy as np

from tools.high_gradient_reference import fields


EVIDENCE = Path("evidence/of13-amr-stage-snapshot-v3")
PARENT_EVIDENCE = Path("evidence/of13-amr-first-refinement-v1")
STAGE_ARCHIVE = EVIDENCE / "amr-stage-snapshot.tar.gz"
PARENT_ARCHIVE = PARENT_EVIDENCE / "amr-cap5000.tar.gz"
STAGES = ("mapped", "afterCorrectPhi", "prePressure", "postPressure", "postSolve")
TIMES = {"mapped": "0.002", "afterCorrectPhi": "0.003", "prePressure": "0.003",
         "postPressure": "0.003", "postSolve": "0.003"}


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read_csv(stage, kind):
    member = (
        f"amr-cap5000/postProcessing/amrStages/{TIMES[stage]}/"
        f"{stage}_{kind}.csv"
    )
    raw = _archive_member(STAGE_ARCHIVE, member)
    rows = list(csv.DictReader(io.StringIO(raw.decode("utf-8"))))
    if not rows:
        raise ValueError(f"empty archived stage output: {member}")
    return {key: np.asarray([float(row[key]) for row in rows]) for key in rows[0]}


def _archive_member(archive_path, member):
    with tarfile.open(archive_path, "r:gz") as archive:
        stream = archive.extractfile(member)
        if stream is None:
            raise ValueError(f"missing archive member {member} in {archive_path}")
        return stream.read()


def _parse_field(raw, kind, width):
    text = raw.decode("ascii")
    text = re.sub(r"/\*.*?\*/|//[^\n]*", "", text, flags=re.S)
    match = re.search(
        rf"internalField\s+nonuniform\s+List<{kind}>\s+(\d+)\s*\((.*?)\)\s*;",
        text, re.S,
    )
    if not match:
        raise ValueError(f"expected ASCII nonuniform List<{kind}>")
    count = int(match.group(1))
    values = np.fromstring(
        match.group(2).replace("(", " ").replace(")", " "), sep=" "
    )
    if values.size != count*width or not np.isfinite(values).all():
        raise ValueError(f"invalid archived {kind} field values")
    return values.reshape(count, width) if width > 1 else values


def _volume_weighted_relative_l2(values, reference, volumes):
    numerator = np.sum(volumes[:, None]*(values-reference)**2)
    denominator = np.sum(volumes[:, None]*reference**2)
    return float(np.sqrt(numerator/max(denominator, 1e-300)))


def rel_l2(a, b):
    return float(np.linalg.norm(a-b) / max(np.linalg.norm(a), 1e-300))


def field_change(a, b):
    return {
        "relative_l2_change_from_previous": rel_l2(a, b),
        "absolute_l2_change": float(np.linalg.norm(a-b)),
        "previous_l2_norm": float(np.linalg.norm(a)),
        "current_l2_norm": float(np.linalg.norm(b)),
    }


def _uniform_parent_lookup(parent_centers, domain_length=2*np.pi):
    parent_centers = np.asarray(parent_centers, dtype=float)
    if (parent_centers.ndim != 2 or parent_centers.shape[1] != 3
            or not np.isfinite(parent_centers).all()):
        raise ValueError("parent centers must be a finite (N, 3) array")
    n_float = round(len(parent_centers) ** (1/3))
    if n_float < 1 or n_float**3 != len(parent_centers):
        raise ValueError("uniform parent grid must contain n^3 cells")
    n = int(n_float)
    width = domain_length/n
    axes = (np.arange(n) + 0.5)*width
    indices = np.rint(parent_centers/width - 0.5).astype(int) % n
    expected = np.column_stack((
        axes[indices[:, 0]], axes[indices[:, 1]], axes[indices[:, 2]]
    ))
    if np.max(np.abs(parent_centers-expected)) > 1e-9*max(1.0, domain_length):
        raise ValueError("expected a uniform parent grid")
    linear = (indices[:, 2]*n + indices[:, 1])*n + indices[:, 0]
    if not np.array_equal(np.sort(linear), np.arange(n**3)):
        raise ValueError("expected a complete uniform parent grid")
    return n, width, linear


def _parent_indices_for_children(parent_centers, child_centers, domain_length=2*np.pi):
    n, width, parent_linear = _uniform_parent_lookup(parent_centers, domain_length)
    child_centers = np.asarray(child_centers, dtype=float)
    if (child_centers.ndim != 2 or child_centers.shape[1] != 3
            or not np.isfinite(child_centers).all()):
        raise ValueError("child centers must be a finite (N, 3) array")
    cell = np.floor(np.mod(child_centers, domain_length)/width).astype(int) % n
    child_linear = (cell[:, 2]*n + cell[:, 1])*n + cell[:, 0]
    parent_for_linear = np.empty(n**3, dtype=int)
    parent_for_linear[parent_linear] = np.arange(n**3)
    return parent_for_linear[child_linear]


def parent_value_injection_audit(
    parent_centers, parent_values, parent_volumes,
    mapped_centers, mapped_values, mapped_volumes, domain_length=2*np.pi,
):
    """Compare mapped FV values with independent containing-parent injection."""
    parent_centers = np.asarray(parent_centers, dtype=float)
    parent_values = np.asarray(parent_values, dtype=float)
    parent_volumes = np.asarray(parent_volumes, dtype=float)
    mapped_values = np.asarray(mapped_values, dtype=float)
    mapped_volumes = np.asarray(mapped_volumes, dtype=float)
    if parent_values.shape != parent_centers.shape:
        raise ValueError("parent values must match parent center shape")
    if parent_volumes.shape != (len(parent_centers),) or np.any(parent_volumes <= 0):
        raise ValueError("parent volumes must be positive and match parent cells")
    if mapped_values.shape != np.asarray(mapped_centers).shape:
        raise ValueError("mapped values must match mapped center shape")
    if mapped_volumes.shape != (len(mapped_values),) or np.any(mapped_volumes <= 0):
        raise ValueError("mapped volumes must be positive and match mapped cells")

    parent_indices = _parent_indices_for_children(
        parent_centers, mapped_centers, domain_length
    )
    prediction = parent_values[parent_indices]
    groups = np.bincount(parent_indices, minlength=len(parent_centers))
    grouped_volume = np.bincount(
        parent_indices, weights=mapped_volumes, minlength=len(parent_centers)
    )
    closure = np.max(np.abs(grouped_volume-parent_volumes)/parent_volumes)
    difference = mapped_values-prediction
    relative_l2 = np.sqrt(
        np.sum(mapped_volumes[:, None]*difference**2)
        / max(np.sum(mapped_volumes[:, None]*mapped_values**2), 1e-300)
    )
    sizes, counts = np.unique(groups, return_counts=True)
    return {
        "parent_grid_cells_per_axis": int(round(len(parent_centers)**(1/3))),
        "mapped_cells": int(len(mapped_values)),
        "parent_group_size_counts": {
            str(int(size)): int(count) for size, count in zip(sizes, counts)
        },
        "parent_volume_closure_relative_max": float(closure),
        "mapped_vs_parent_injection_relative_l2": float(relative_l2),
        "mapped_vs_parent_injection_max_abs": float(np.max(np.abs(difference))),
    }


def analyze():
    manifest = json.loads((EVIDENCE / "manifest.json").read_text())
    if manifest.get("status") != "RUN_COMPLETE_STAGE_CAPTURED" or manifest.get("exit_code") != 0:
        raise ValueError("stage-capture run is not complete")
    if sha(STAGE_ARCHIVE) != manifest["archive_sha256"]:
        raise ValueError("stage snapshot archive hash differs from its manifest")
    parent_manifest = json.loads((PARENT_EVIDENCE / "manifest.json").read_text())
    parent_case = next(row for row in parent_manifest["cases"]
                       if row["case"] == "amr-cap5000")
    if sha(PARENT_ARCHIVE) != parent_case["archive_sha256"]:
        raise ValueError("parent-state archive hash differs from its manifest")
    cells = {stage: read_csv(stage, "cells") for stage in STAGES}
    faces = {stage: read_csv(stage, "faces") for stage in STAGES}
    provenance_path = EVIDENCE / "instrumentation-provenance.json"
    provenance = json.loads(provenance_path.read_text())
    provenance_correction = {
        "status": "METADATA_CORRECTION; raw provenance file preserved unchanged",
        "raw_provenance_sha256": sha(provenance_path),
        "raw_checkpoint_text": provenance["checkpoint"],
        "corrected_stage_times_from_protocol_and_solver_log": TIMES,
        "supporting_snapshot_events": manifest["snapshot_events"],
        "reason": "The checkpoint description string was not updated when v3 introduced a distinct mapped-stage time. Generated source hashes, v3 protocol, and solver events agree on mapped t=0.002 and later stages t=0.003.",
    }
    (EVIDENCE / "provenance-correction.json").write_text(
        json.dumps(provenance_correction, indent=2) + "\n"
    )

    # Every stage must refer to the same post-refinement mesh, regardless of
    # whether the solver has advanced the time label.
    cell_topology = ("cx", "cy", "cz", "V")
    face_topology = ("owner", "neighbour", "cx", "cy", "cz", "Sx", "Sy", "Sz")
    for stage in STAGES[1:]:
        for key in cell_topology:
            if not np.array_equal(cells[STAGES[0]][key], cells[stage][key]):
                raise ValueError(f"cell topology differs at {stage}/{key}")
        for key in face_topology:
            if not np.array_equal(faces[STAGES[0]][key], faces[stage][key]):
                raise ValueError(f"face topology differs at {stage}/{key}")

    errors = {}
    for stage in STAGES:
        data = cells[stage]
        xyz = np.column_stack([data[key] for key in ("cx", "cy", "cz")])
        u = np.column_stack([data[key] for key in ("Ux", "Uy", "Uz")])
        exact = fields(xyz, N=4, nu=0.01, time=float(TIMES[stage]))["u"]
        volume = data["V"]
        errors[stage] = float(np.sqrt(
            np.sum(volume * np.sum((u-exact)**2, axis=1))
            / np.sum(volume * np.sum(exact**2, axis=1))
        ))

    parent_centers = _parse_field(
        _archive_member(PARENT_ARCHIVE, "amr-cap5000/0.002/C"), "vector", 3
    )
    parent_velocity = _parse_field(
        _archive_member(PARENT_ARCHIVE, "amr-cap5000/0.002/U"), "vector", 3
    )
    parent_volumes = _parse_field(
        _archive_member(PARENT_ARCHIVE, "amr-cap5000/0.002/Vc"), "scalar", 1
    )
    mapped = cells["mapped"]
    mapped_centers = np.column_stack([mapped[key] for key in ("cx", "cy", "cz")])
    mapped_velocity = np.column_stack([mapped[key] for key in ("Ux", "Uy", "Uz")])
    mapped_volumes = mapped["V"]
    parent_audit = parent_value_injection_audit(
        parent_centers, parent_velocity, parent_volumes,
        mapped_centers, mapped_velocity, mapped_volumes,
    )
    parent_indices = _parent_indices_for_children(parent_centers, mapped_centers)
    injected_velocity = parent_velocity[parent_indices]
    exact_parent = fields(parent_centers, N=4, nu=0.01, time=0.002)["u"]
    exact_mapped = fields(mapped_centers, N=4, nu=0.01, time=0.002)["u"]
    inherited_parent_error = injected_velocity-exact_parent[parent_indices]
    exact_parent_to_child_change = exact_parent[parent_indices]-exact_mapped
    mapped_error = mapped_velocity-exact_mapped
    denominator = np.sum(mapped_volumes[:, None]*exact_mapped**2)
    inherited_sq = float(
        np.sum(mapped_volumes[:, None]*inherited_parent_error**2)/denominator
    )
    prolongation_sq = float(
        np.sum(mapped_volumes[:, None]*exact_parent_to_child_change**2)/denominator
    )
    cross_term = float(
        2*np.sum(mapped_volumes[:, None]
                 * inherited_parent_error*exact_parent_to_child_change)/denominator
    )
    total_sq = float(np.sum(mapped_volumes[:, None]*mapped_error**2)/denominator)
    cell_levels = _parse_field(
        _archive_member(STAGE_ARCHIVE, "amr-cap5000/0.003/cellLevel"),
        "scalar", 1,
    ).astype(int)
    if len(cell_levels) != len(mapped_velocity):
        raise ValueError("cellLevel field count differs from mapped snapshot")
    level_rows = {}
    for level in sorted(np.unique(cell_levels)):
        mask = cell_levels == level
        level_rows[str(int(level))] = {
            "cells": int(mask.sum()),
            "volume_fraction": float(mapped_volumes[mask].sum()/mapped_volumes.sum()),
            "mapped_vs_exact_cell_center_relative_l2":
                _volume_weighted_relative_l2(
                    mapped_velocity[mask], exact_mapped[mask], mapped_volumes[mask]
                ),
            "parent_injection_vs_exact_cell_center_relative_l2":
                _volume_weighted_relative_l2(
                    injected_velocity[mask], exact_mapped[mask], mapped_volumes[mask]
                ),
        }
    parent_audit.update({
        "source_parent_archive_sha256": sha(PARENT_ARCHIVE),
        "source_stage_archive_sha256": sha(STAGE_ARCHIVE),
        "mapped_vs_exact_child_cell_center_relative_l2": errors["mapped"],
        "independent_parent_injection_vs_exact_child_cell_center_relative_l2":
            _volume_weighted_relative_l2(
                injected_velocity, exact_mapped, mapped_volumes
            ),
        "point_sample_error_decomposition": {
            "inherited_parent_solution_error_squared_relative": inherited_sq,
            "exact_parent_to_child_center_change_squared_relative": prolongation_sq,
            "twice_normalized_cross_term": cross_term,
            "total_mapped_error_squared_relative": total_sq,
            "squared_error_identity_residual":
                float(total_sq-inherited_sq-prolongation_sq-cross_term),
            "interpretation": (
                "Algebraic decomposition at cell centers: parent numerical "
                "error plus exact-reference change from parent center to mapped "
                "child center. Not a canonical finite-volume interpolation "
                "error bound."
            ),
        },
        "by_cell_level": level_rows,
        "scope": (
            "Archived t=0.002 parent field is injected to geometrically "
            "containing uniform-grid parents. This post-hoc point-sample "
            "diagnostic is not an OpenFOAM defect verdict or a finite-volume "
            "cell-average accuracy claim."
        ),
    })

    # Reconstruct the finite-volume flux divergence from OpenFOAM's oriented
    # owner/neighbour incidence: owner gets +phi, internal neighbour gets
    # -phi, and boundary faces contribute to their owner cell.
    flux_divergence = {}
    for stage in STAGES[:4]:
        data, face = cells[stage], faces[stage]
        volume = data["V"]
        net_flux = np.zeros(len(volume))
        owner = face["owner"].astype(int)
        neighbour = face["neighbour"].astype(int)
        np.add.at(net_flux, owner, face["phi"])
        internal = neighbour >= 0
        np.add.at(net_flux, neighbour[internal], -face["phi"][internal])
        divergence = net_flux / volume
        flux_divergence[stage] = {
            "volume_weighted_rms_cell_div_phi": float(np.sqrt(
                np.sum(volume*divergence**2) / np.sum(volume)
            )),
            "max_abs_cell_div_phi": float(np.max(np.abs(divergence))),
            "sum_abs_net_cell_flux": float(np.sum(np.abs(net_flux))),
            "global_net_cell_flux": float(np.sum(net_flux)),
        }
    flux_divergence["mapped_to_afterCorrectPhi_rms_reduction_fraction"] = float(
        1.0 - flux_divergence["afterCorrectPhi"]["volume_weighted_rms_cell_div_phi"]
        / flux_divergence["mapped"]["volume_weighted_rms_cell_div_phi"]
    )

    transitions = {}
    error_changes_pp = {}
    pairs = list(zip(STAGES, STAGES[1:]))
    for before, after in pairs:
        a, b = cells[before], cells[after]
        fa, fb = faces[before], faces[after]
        transitions[f"{before}_to_{after}"] = {
            "cell_U": field_change(
                np.column_stack([a[k] for k in ("Ux", "Uy", "Uz")]),
                np.column_stack([b[k] for k in ("Ux", "Uy", "Uz")]),
            ),
            "cell_p": field_change(a["p"], b["p"]),
            "face_phi": field_change(fa["phi"], fb["phi"]),
            "face_Uf": field_change(
                np.column_stack([fa[k] for k in ("Ufx", "Ufy", "Ufz")]),
                np.column_stack([fb[k] for k in ("Ufx", "Ufy", "Ufz")]),
            ),
        }
        error_changes_pp[f"{before}_to_{after}"] = 100*(errors[after]-errors[before])

    control_hashes = {}
    instrumented_hashes = {}
    for field in ("U", "p", "phi", "Uf"):
        control_hashes[field] = hashlib.sha256(_archive_member(
            PARENT_ARCHIVE, f"amr-cap5000/0.003/{field}"
        )).hexdigest()
        instrumented_hashes[field] = hashlib.sha256(_archive_member(
            STAGE_ARCHIVE, f"amr-cap5000/0.003/{field}"
        )).hexdigest()
    exact_match = control_hashes == instrumented_hashes

    result = {
        "status": "ANALYZED_FINAL_STATE_EXACT_MATCH" if exact_match else "NONINTERFERENCE_NOT_ESTABLISHED",
        "run_manifest_sha256": sha(EVIDENCE / "manifest.json"),
        "stage_capture_manifest_sha256": sha(EVIDENCE / "manifest.json"),
        "provenance_correction_sha256": sha(EVIDENCE / "provenance-correction.json"),
        "stage_times": TIMES,
        "mesh": {
            "cells_each_stage": len(cells["mapped"]["V"]),
            "faces_each_stage": len(faces["mapped"]["phi"]),
            "topology_equal_across_all_stages": True,
            "total_cell_volume": float(cells["mapped"]["V"].sum()),
        },
        "volume_weighted_velocity_relative_l2_error_vs_exact_mms": errors,
        "independent_parent_value_mapping_audit": parent_audit,
        "change_in_exact_mms_velocity_error_percentage_points": error_changes_pp,
        "reconstructed_finite_volume_phi_divergence": {
            "method": "sum oriented face phi into owner cells and subtract from internal neighbours, then divide by cell volume",
            "stages": flux_divergence,
            "scope_note": "Derived from recorded face phi and topology; it is a diagnostic reconstruction, not an independent solver run.",
        },
        "stage_transition_relative_l2_changes": transitions,
        "final_field_sha256": {
            "instrumented": instrumented_hashes,
            "unmodified_control": control_hashes,
            "exact_byte_match": exact_match,
        },
        "scope": "One n=16, first-refinement mechanism diagnostic. The final U/p/phi/Uf byte match establishes noninterference for this run only. Stage differences locate changes in this run; they are not a general solver defect, convergence result, PDE singularity, or physical claim.",
    }
    (EVIDENCE / "analysis.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    if not exact_match:
        raise SystemExit(2)


if __name__ == "__main__":
    analyze()
