"""Compare saved package operators with complete matrices and exact chains.

Native scalar residuals are diagnostics; they are not the quality gate.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np

from tools.check_interface_stress_compatibility import couette_chain

PROTOCOL = Path("protocols/of13-interface-operator-v1.json")


def maximum(values):
    array = np.asarray(values, dtype=float)
    if not np.all(np.isfinite(array)):
        raise ValueError("nonfinite diagnostic reduction")
    return float(np.max(np.abs(array), initial=0))


def finite_array(values, shape, name):
    array = np.asarray(values, dtype=float)
    if array.shape != shape or not np.all(np.isfinite(array)):
        raise ValueError(f"invalid finite array {name}: expected {shape}, got {array.shape}")
    return array


def address_array(values, shape, name):
    array = finite_array(values, shape, name)
    if np.any(array != np.rint(array)):
        raise ValueError(f"noninteger addressing {name}")
    return array.astype(int)


def validate_snapshot(snapshot, metadata, mode, stage):
    """Validate the complete utility schema before any numerical reduction."""
    nx = metadata["inputs"]["nx"]
    count, internal_count, face_count = 4 * nx, 8 * nx - 4, 16 * nx + 4
    field_name = f"shear_{mode}" if mode != "constant" else "constantControl_probe"
    if (type(snapshot["schemaVersion"]) is not int or snapshot["schemaVersion"] != 1
            or snapshot["operator"] != "negative_fvm_laplacian"
            or snapshot["mode"] != mode or snapshot["stage"] != stage
            or snapshot["fieldName"] != field_name):
        raise ValueError("wrong snapshot schema/operator/field identity")
    for name, expected in (("fieldDimensions", [0, 1, -1, 0, 0, 0, 0]),
                           ("equationDimensions", [0, 4, -2, 0, 0, 0, 0])):
        if not np.array_equal(finite_array(snapshot[name], (7,), name), expected):
            raise ValueError(f"wrong snapshot {name}")
    cells = snapshot["cells"]
    centres = finite_array(cells["centres"], (count, 3), "cell centres")
    expected_centres = finite_array(metadata["mesh"]["cell_centres"], (count, 3), "input centres")
    if not np.allclose(centres, expected_centres, rtol=0, atol=1e-12):
        raise ValueError("actual cell centres/order differ from the initial-array convention")
    volumes = finite_array(cells["volumes"], (count,), "cell volumes")
    if not np.allclose(volumes, .5 / nx, rtol=0, atol=1e-12):
        raise ValueError("cell volumes differ from the specified Cartesian mesh")
    for name in ("values", "rawDiag", "completeDiag", "source", "nativeResidual",
                 "divPhysicalFluxTimesVolume"):
        finite_array(cells[name], (count,), name)
    internal, faces = snapshot["internalMatrix"], snapshot["faces"]
    for name in ("owner", "neighbour"):
        address_array(internal[name], (internal_count,), f"internal {name}")
        address_array(faces[name], (face_count,), f"face {name}")
    for name in ("upper", "lower"):
        finite_array(internal[name], (internal_count,), name)
    for name in ("symmetric", "hasLower"):
        if type(internal[name]) is not bool:
            raise ValueError(f"invalid matrix flag {name}")
    for name in ("centres", "areas"):
        finite_array(faces[name], (face_count, 3), f"face {name}")
    for name in ("gamma", "deltaCoeffs", "snGrad", "physicalFlux", "matrixFlux"):
        finite_array(faces[name], (face_count,), name)
    patches = snapshot["patches"]
    expected_names = {"xm", "xp", "ym", "yp", "zm", "zp"}
    if len(patches) != 6 or {patch["name"] for patch in patches} != expected_names:
        raise ValueError("wrong or duplicate patch names")
    for patch in patches:
        coupled = patch["name"][0] != "x"
        size = 2 * nx if coupled else 4
        if (type(patch["start"]) is not int or type(patch["size"]) is not int
                or patch["start"] < internal_count or patch["size"] != size
                or patch["start"] + size > face_count
                or type(patch["coupled"]) is not bool or patch["coupled"] != coupled
                or patch["type"] != ("cyclic" if coupled else "wall")
                or patch["fieldType"] != ("cyclic" if coupled else "fixedValue")):
            raise ValueError("patch topology or field type differs from the specified mesh")
        address_array(patch["faceCells"], (size,), "patch faceCells")
        for name in ("internalCoeffs", "boundaryCoeffs"):
            finite_array(patch[name], (size,), name)
        finite_array(patch["neighbourValues"], (size if coupled else 0,), "neighbourValues")
    performance = snapshot["solverPerformance"]
    if stage == "after" and mode != "constant":
        residuals = finite_array([performance["initialResidual"], performance["finalResidual"]],
                                 (2,), "solver residuals")
        if (np.any(residuals < 0) or type(performance["iterations"]) is not int
                or performance["iterations"] < 0):
            raise ValueError("invalid solver performance")
    elif performance is not None:
        raise ValueError("unexpected solver performance for an unsolved snapshot")
    correction = snapshot["explicitCorrection"]
    if mode == "constant":
        if correction is not None:
            raise ValueError("unexpected constant-control explicit correction")
    else:
        if correction["coefficientMode"] != "arithmetic":
            raise ValueError("explicit correction must retain the arithmetic coefficient")
        for name in ("gradU", "dev2TransposeGradU"):
            finite_array(correction[name], (count, 9), name)
        for name in ("separateFlux", "parentProductFlux"):
            finite_array(correction[name], (face_count, 3), name)
        for name in ("divSeparateTimesVolume", "divParentProductTimesVolume"):
            finite_array(correction[name], (count, 3), name)


def cyclic_neighbours(centres, owners, areas, patch_name):
    """Match this unrotated Cartesian periodic fixture from geometry only."""
    axis = {"ym": 1, "yp": 1, "zm": 2, "zp": 2}.get(patch_name)
    if axis is None:
        raise ValueError(f"unsupported coupled patch {patch_name}")
    target = centres[:, axis].max() if patch_name.endswith("m") else centres[:, axis].min()
    transverse = [other for other in range(3) if other != axis]
    result = []
    for owner, area in zip(owners, areas):
        if np.count_nonzero(np.abs(area) > 1e-12) != 1 or abs(area[axis]) < 1e-12:
            raise ValueError("cyclic face is not axis aligned")
        candidates = np.flatnonzero(
            np.isclose(centres[:, axis], target, rtol=0, atol=1e-12)
            & np.all(np.isclose(centres[:, transverse], centres[owner, transverse],
                                rtol=0, atol=1e-12), axis=1))
        if len(candidates) != 1:
            raise ValueError("periodic neighbour is not uniquely matched by coordinates")
        result.append(int(candidates[0]))
    return np.asarray(result, dtype=int)


def reconstruct(snapshot):
    """Include boundary diagonal/RHS and each cyclic coupling exactly once."""
    cells, internal, faces = snapshot["cells"], snapshot["internalMatrix"], snapshot["faces"]
    values = np.asarray(cells["values"], dtype=float); count = len(values)
    centres = finite_array(cells["centres"], (count, 3), "centres")
    raw = finite_array(cells["rawDiag"], (count,), "rawDiag")
    matrix = np.diag(raw); rhs = finite_array(cells["source"], (count,), "source").copy()
    owner = address_array(internal["owner"], (len(internal["owner"]),), "internal owner")
    neighbour = address_array(internal["neighbour"], owner.shape, "internal neighbour")
    if owner.shape != neighbour.shape or np.any(owner < 0) or np.any(neighbour < 0) or np.any(owner >= count) or np.any(neighbour >= count):
        raise ValueError("invalid internal addressing")
    upper = finite_array(internal["upper"], owner.shape, "upper")
    lower = finite_array(internal["lower"], owner.shape, "lower")
    np.add.at(matrix, (owner, neighbour), upper)
    np.add.at(matrix, (neighbour, owner), lower)
    all_owner = address_array(faces["owner"], (len(faces["owner"]),), "face owner")
    areas = finite_array(faces["areas"], (len(all_owner), 3), "areas")
    if np.any(all_owner < 0) or np.any(all_owner >= count):
        raise ValueError("invalid face owner")
    if not np.array_equal(all_owner[:len(owner)], owner):
        raise ValueError("internal and global owner addressing differ")
    all_neighbour = address_array(faces["neighbour"], all_owner.shape, "face neighbour")
    if (all_neighbour.shape != all_owner.shape
            or not np.array_equal(all_neighbour[:len(neighbour)], neighbour)
            or np.any(all_neighbour[len(neighbour):] != -1)):
        raise ValueError("internal and global neighbour addressing differ")
    added_diagonal = np.zeros(count); cyclic_load = np.zeros(count)
    seen = set(range(len(owner)))
    for patch in snapshot["patches"]:
        if (type(patch["start"]) is not int or type(patch["size"]) is not int
                or patch["start"] < len(owner) or patch["size"] < 0
                or patch["start"] + patch["size"] > len(all_owner)):
            raise ValueError("invalid patch range")
        ids = np.arange(patch["start"], patch["start"] + patch["size"], dtype=int)
        patch_owner = address_array(patch["faceCells"], ids.shape, "patch owner")
        if not np.array_equal(all_owner[ids], patch_owner) or any(int(face) in seen for face in ids):
            raise ValueError("invalid or duplicate patch addressing")
        seen.update(map(int, ids))
        ic = finite_array(patch["internalCoeffs"], ids.shape, "internalCoeffs")
        bc = finite_array(patch["boundaryCoeffs"], ids.shape, "boundaryCoeffs")
        np.add.at(matrix, (patch_owner, patch_owner), ic)
        np.add.at(added_diagonal, patch_owner, ic)
        if patch["coupled"]:
            neighbours = cyclic_neighbours(centres, patch_owner, areas[ids], patch["name"])
            neighbour_values = finite_array(patch["neighbourValues"], ids.shape, "neighbourValues")
            if not np.allclose(neighbour_values, values[neighbours], rtol=0, atol=1e-10):
                raise ValueError("saved cyclic neighbour values disagree with geometric match")
            np.add.at(matrix, (patch_owner, neighbours), -bc)
            np.add.at(cyclic_load, patch_owner, bc * values[neighbours])
        else:
            # Fixed-value boundaryCoeffs already include the boundary value.
            np.add.at(rhs, patch_owner, bc)
    if seen != set(range(len(all_owner))):
        raise ValueError("not all faces accounted for")
    complete = finite_array(cells["completeDiag"], (count,), "completeDiag")
    if not np.allclose(raw + added_diagonal, complete, rtol=1e-12, atol=1e-10):
        raise ValueError("saved complete diagonal differs from boundary-complete reconstruction")
    physical = finite_array(faces["physicalFlux"], all_owner.shape, "physicalFlux")
    flux_balance = np.zeros(count)
    np.add.at(flux_balance, all_owner, physical)
    np.add.at(flux_balance, neighbour, -physical[:len(neighbour)])
    return matrix, rhs, flux_balance, cyclic_load


def face_consistency(snapshot, nx, mode, mu_left, mu_right, traction=1):
    faces = snapshot["faces"]; count = len(faces["owner"])
    centres = finite_array(faces["centres"], (count, 3), "face centres")
    areas = finite_array(faces["areas"], (count, 3), "face areas")
    axes = np.argmax(np.abs(areas), axis=1)
    if np.any(np.sum(np.abs(areas) > 1e-12, axis=1) != 1):
        raise ValueError("non-Cartesian face in specified orthogonal probe")
    h = 2 / nx
    expected_area = np.where(axes == 0, .25, h / 2)
    expected_delta = np.where(axes == 0, 1 / h, 2.)
    walls = (axes == 0) & np.isclose(np.abs(centres[:, 0]), 1., rtol=0, atol=1e-12)
    expected_delta[walls] = 2 / h
    gamma = finite_array(faces["gamma"], (count,), "gamma")
    expected_gamma = np.where(centres[:, 0] < 0, float(mu_left), float(mu_right))
    interface = (axes == 0) & np.isclose(centres[:, 0], 0., rtol=0, atol=1e-12)
    expected_gamma[interface] = ((mu_left + mu_right) / 2 if mode == "arithmetic"
                                 else 2 * mu_left * mu_right / (mu_left + mu_right))
    if mode == "constant":
        expected_gamma[:] = 1
    delta = finite_array(faces["deltaCoeffs"], (count,), "deltaCoeffs")
    sn = finite_array(faces["snGrad"], (count,), "snGrad")
    flux = finite_array(faces["physicalFlux"], (count,), "physicalFlux")
    owner = np.asarray(faces["owner"], dtype=int)
    neighbour = np.asarray(faces["neighbour"], dtype=int)
    cells = np.asarray(snapshot["cells"]["centres"], dtype=float)
    values = np.asarray(snapshot["cells"]["values"], dtype=float)
    internal = neighbour >= 0
    displacement = cells[neighbour[internal]] - cells[owner[internal]]
    if (np.any(np.sum(displacement * areas[internal], axis=1) <= 0)
            or not np.allclose(centres[internal], (cells[owner[internal]] + cells[neighbour[internal]]) / 2,
                               rtol=0, atol=1e-12)):
        raise ValueError("internal face centre or owner-to-neighbour orientation differs")
    expected_sn = np.zeros(count)
    expected_sn[internal] = (values[neighbour[internal]] - values[owner[internal]]) * delta[internal]
    for patch in snapshot["patches"]:
        ids = np.arange(patch["start"], patch["start"] + patch["size"])
        axis = {"x": 0, "y": 1, "z": 2}[patch["name"][0]]
        sign = -1 if patch["name"].endswith("m") else 1
        expected_centre = cells[owner[ids]].copy()
        expected_centre[:, axis] = sign if axis == 0 else (0 if sign < 0 else 1)
        if (np.any(areas[ids, axis] * sign <= 0)
                or np.any(axes[ids] != axis)
                or not np.allclose(centres[ids], expected_centre, rtol=0, atol=1e-12)):
            raise ValueError("boundary face centre or outward orientation differs")
        if patch["coupled"]:
            paired = cyclic_neighbours(cells, owner[ids], areas[ids], patch["name"])
            opposite_values = values[paired]
        else:
            opposite_values = 1 if mode == "constant" else sign * traction / (mu_left if sign < 0 else mu_right)
        expected_sn[ids] = (opposite_values - values[owner[ids]]) * delta[ids]
    return {"area_error_Linf": maximum(np.linalg.norm(areas, axis=1) - expected_area),
            "distance_coefficient_error_Linf": maximum(delta - expected_delta),
            "face_coefficient_error_Linf": maximum(gamma - expected_gamma),
            "physical_flux_product_error_Linf": maximum(flux - gamma * np.linalg.norm(areas, axis=1) * sn),
            "normal_gradient_to_saved_values_error_Linf": maximum(sn - expected_sn)}


def snapshot_metrics(snapshot):
    matrix, rhs, balance, cyclic_load = reconstruct(snapshot)
    values = finite_array(snapshot["cells"]["values"], rhs.shape, "values")
    native = finite_array(snapshot["cells"]["nativeResidual"], rhs.shape, "nativeResidual")
    div_v = finite_array(snapshot["cells"]["divPhysicalFluxTimesVolume"], rhs.shape, "divFluxTimesV")
    residual = rhs - matrix @ values
    matrix_flux = finite_array(snapshot["faces"]["matrixFlux"], (len(snapshot["faces"]["owner"]),), "matrixFlux")
    physical = np.asarray(snapshot["faces"]["physicalFlux"])
    return {
        "complete_integrated_residual_Linf": maximum(residual),
        "oriented_physical_balance_Linf": maximum(balance),
        "complete_residual_minus_face_balance_Linf": maximum(residual - balance),
        "div_times_V_minus_face_balance_Linf": maximum(div_v - balance),
        "matrix_flux_plus_physical_flux_Linf": maximum(matrix_flux + physical),
        "native_integrated_residual_Linf": maximum(native),
        "native_minus_complete_residual_Linf": maximum(native - residual),
        "native_minus_complete_minus_cyclic_load_Linf": maximum(native - residual - cyclic_load),
        "full_matrix_symmetry_error_Linf": maximum(matrix - matrix.T),
    }


def analyze_case(case, protocol):
    metadata = json.loads((case / "case_metadata.json").read_text())
    nx = metadata["inputs"]["nx"]; h = 2 / nx
    limits = protocol["acceptance"]["operator_quality"]
    output = {"nx": nx, "modes": {}}
    for mode in ("arithmetic", "harmonic"):
        before = json.loads((case / f"probe/{mode}/before.json").read_text())
        after = json.loads((case / f"probe/{mode}/after.json").read_text())
        validate_snapshot(before, metadata, mode, "before")
        validate_snapshot(after, metadata, mode, "after")
        centres = np.asarray(after["cells"]["centres"])
        expected_centres = np.asarray(metadata["mesh"]["cell_centres"])
        if not np.allclose(centres, expected_centres, rtol=0, atol=1e-12):
            raise ValueError("actual mesh cell ordering/centres differ from initial-array convention")
        if before["mode"] != mode or after["mode"] != mode or before["stage"] != "before" or after["stage"] != "after":
            raise ValueError("wrong named snapshot identity")
        ref = couette_chain(nx, metadata["inputs"]["mu_left"], metadata["inputs"]["mu_right"],
                            metadata["inputs"]["traction"], harmonic=mode == "harmonic")
        index = np.rint((centres[:, 0] + 1) / h - .5).astype(int)
        reference = np.asarray([float(value) for value in ref["values"]])[index]
        exact = np.asarray([float(value) for value in ref["reference"]])[index]
        actual = np.asarray(after["cells"]["values"])
        metrics = snapshot_metrics(after); initial_metrics = snapshot_metrics(before)
        face_metrics = face_consistency(after, nx, mode, metadata["inputs"]["mu_left"], metadata["inputs"]["mu_right"], metadata["inputs"]["traction"])
        initial_face_metrics = face_consistency(before, nx, mode, metadata["inputs"]["mu_left"], metadata["inputs"]["mu_right"], metadata["inputs"]["traction"])
        error = maximum(actual - reference)
        x_faces = np.abs(np.asarray(after["faces"]["areas"])[:, 0]) > 1e-12
        x_area = np.asarray(after["faces"]["areas"])[x_faces, 0]
        ratio = np.asarray(after["faces"]["physicalFlux"])[x_faces] / x_area
        flux_error = maximum(ratio / float(ref["flux"]) - 1)
        explicit_x, explicit_div = 0., 0.
        for state in (before, after):
            record = state["explicitCorrection"]
            mask = np.abs(np.asarray(state["faces"]["areas"])[:, 0]) > 1e-12
            explicit_x = max(explicit_x, maximum(np.asarray(record["separateFlux"])[mask]),
                             maximum(np.asarray(record["parentProductFlux"])[mask]))
            explicit_div = max(explicit_div, maximum(record["divSeparateTimesVolume"]),
                               maximum(record["divParentProductTimesVolume"]))
        checks = {
            "solved_field_matches_exact_chain": error <= limits["absolute_cell_value_error"],
            "initial_field_matches_exact_nodal_values": maximum(np.asarray(before["cells"]["values"]) - exact) <= 1e-12,
            "complete_integrated_residual_small": metrics["complete_integrated_residual_Linf"] <= limits["absolute_complete_integrated_residual"],
            "all_x_face_fluxes_match_chain": flux_error <= limits["relative_physical_shear_flux_error_to_chain"],
            "complete_matrix_matches_physical_flux_balance": metrics["complete_residual_minus_face_balance_Linf"] <= limits["absolute_flux_balance_difference"],
            "saved_divergence_matches_oriented_balance": metrics["div_times_V_minus_face_balance_Linf"] <= limits["absolute_flux_balance_difference"],
            "matrix_flux_sign_matches_negative_laplacian": metrics["matrix_flux_plus_physical_flux_Linf"] <= limits["absolute_matrix_flux_plus_physical_flux"],
            "x_explicit_correction_zero": explicit_x <= limits["absolute_x_face_explicit_correction"],
            "explicit_correction_divergence_cancels": explicit_div <= limits["absolute_explicit_correction_integrated_divergence"],
            "saved_face_geometry_and_coefficients_match_model": max(face_metrics.values()) <= 1e-9,
            "initial_matrix_matches_physical_flux_balance": initial_metrics["complete_residual_minus_face_balance_Linf"] <= limits["absolute_flux_balance_difference"],
            "initial_saved_divergence_matches_oriented_balance": initial_metrics["div_times_V_minus_face_balance_Linf"] <= limits["absolute_flux_balance_difference"],
            "initial_matrix_flux_sign_matches_negative_laplacian": initial_metrics["matrix_flux_plus_physical_flux_Linf"] <= limits["absolute_matrix_flux_plus_physical_flux"],
            "initial_saved_face_geometry_and_coefficients_match_model": max(initial_face_metrics.values()) <= 1e-9,
        }
        output["modes"][mode] = {"quality": "PASS" if all(checks.values()) else "FAIL_SPECIFIED_OPERATOR_GATE",
            "checks": checks, "after": metrics, "before": initial_metrics,
            "cell_error_to_chain_Linf": error, "relative_flux_error_to_chain_Linf": flux_error,
            "face_metrics": face_metrics,
            "initial_face_metrics": initial_face_metrics,
            "relative_flux_error_to_continuum_expected": float(ref["relative_flux_error"]),
            "expected_chain_flux": float(ref["flux"]), "relative_velocity_L2_to_continuum": float(np.linalg.norm(actual - exact) / np.linalg.norm(exact)),
            "solverPerformance": after["solverPerformance"],
            "explicit_x_face_flux_Linf": explicit_x, "explicit_integrated_divergence_Linf": explicit_div}
    constant = json.loads((case / "probe/constant/before.json").read_text())
    validate_snapshot(constant, metadata, "constant", "before")
    metrics = snapshot_metrics(constant)
    native = np.asarray(constant["cells"]["nativeResidual"])
    if (constant["mode"] != "constant" or constant["stage"] != "before"
            or not np.allclose(constant["cells"]["centres"], metadata["mesh"]["cell_centres"], rtol=0, atol=1e-12)
            or maximum(np.asarray(constant["cells"]["values"]) - 1) > 1e-12):
        raise ValueError("constant control identity or initial values differ")
    face_metrics = face_consistency(constant, nx, "constant", 1., 1.)
    limit = protocol["acceptance"]["constant_control"]["absolute_complete_residual_and_physical_flux"]
    independent = max(metrics["complete_integrated_residual_Linf"], metrics["oriented_physical_balance_Linf"],
                      metrics["complete_residual_minus_face_balance_Linf"],
                      metrics["div_times_V_minus_face_balance_Linf"],
                      metrics["matrix_flux_plus_physical_flux_Linf"],
                      maximum(constant["faces"]["physicalFlux"]), max(face_metrics.values())) <= limit
    observed = independent and maximum(native - 2 * h) <= protocol["acceptance"]["constant_control"]["absolute_prediction_difference"]
    output["constant_control"] = {"independent_zero_balance": independent,
        "source_predicted_extra_cyclic_term": "OBSERVED" if observed else "NOT_OBSERVED",
        "native_residual_expected_per_cell_if_predicted": 2*h, "metrics": metrics}
    output["constant_control"]["face_metrics"] = face_metrics
    output["operator_quality"] = "PASS" if independent and all(row["quality"] == "PASS" for row in output["modes"].values()) else "FAIL_SPECIFIED_OPERATOR_GATE"
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--protocol", type=Path, default=PROTOCOL)
    args = parser.parse_args(); spec = json.loads(args.protocol.read_text())
    rows = [analyze_case(args.case_root / f"nx{nx}", spec) for nx in spec["inputs"]["nx"]]
    result = {"scope": "Three-grid stationary scalar package operator probe only; native residual diagnostic is separate from complete physical balance and solver normalization.",
        "analyzer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "protocol_sha256": hashlib.sha256(args.protocol.read_bytes()).hexdigest(),
        "input_sha256": {str(path.relative_to(args.case_root)): hashlib.sha256(path.read_bytes()).hexdigest()
                         for path in sorted(args.case_root.rglob("*.json"))},
        "cases": rows, "operator_quality": "PASS" if all(row["operator_quality"] == "PASS" for row in rows) else "FAIL_SPECIFIED_OPERATOR_GATE",
        "upstream_disposition": "Native residual candidate requires package/source identity, API contract review and duplicate search; no issue automatically created.",
        "physical_scope": "No molecular alignment, constitutive-viscosity change, phase transition or continuum singularity verdict."}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
    print(json.dumps(result, indent=2, allow_nan=False))
    return 0 if result["operator_quality"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
