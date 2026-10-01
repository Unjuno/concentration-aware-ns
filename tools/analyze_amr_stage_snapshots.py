"""Analyze captured Foundation-13 AMR stages without assigning defect status."""
import csv
import hashlib
import json
from pathlib import Path

import numpy as np

from tools.high_gradient_reference import fields


RUN = Path("work/of13-amr-stage-snapshot-v3/amr-cap5000")
EVIDENCE = Path("evidence/of13-amr-stage-snapshot-v3")
CONTROL = Path("work/of13-amr-first-refinement-v1/amr-cap5000/0.003")
STAGES = ("mapped", "afterCorrectPhi", "prePressure", "postPressure", "postSolve")
TIMES = {"mapped": "0.002", "afterCorrectPhi": "0.003", "prePressure": "0.003",
         "postPressure": "0.003", "postSolve": "0.003"}


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read_csv(stage, kind):
    path = RUN / "postProcessing" / "amrStages" / TIMES[stage] / f"{stage}_{kind}.csv"
    with path.open(newline="") as stream:
        rows = list(csv.DictReader(stream))
    if not rows:
        raise ValueError(f"empty stage output: {path}")
    return {key: np.asarray([float(row[key]) for row in rows]) for key in rows[0]}


def rel_l2(a, b):
    return float(np.linalg.norm(a-b) / max(np.linalg.norm(a), 1e-300))


def field_change(a, b):
    return {
        "relative_l2_change_from_previous": rel_l2(a, b),
        "absolute_l2_change": float(np.linalg.norm(a-b)),
        "previous_l2_norm": float(np.linalg.norm(a)),
        "current_l2_norm": float(np.linalg.norm(b)),
    }


def analyze():
    manifest = json.loads((EVIDENCE / "manifest.json").read_text())
    if manifest.get("status") != "RUN_COMPLETE_STAGE_CAPTURED" or manifest.get("exit_code") != 0:
        raise ValueError("stage-capture run is not complete")
    cells = {stage: read_csv(stage, "cells") for stage in STAGES}
    faces = {stage: read_csv(stage, "faces") for stage in STAGES}
    provenance_path = RUN.parent / "instrumented-module" / "instrumentation-provenance.json"
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
        control_hashes[field] = sha(CONTROL / field)
        instrumented_hashes[field] = sha(RUN / "0.003" / field)
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
