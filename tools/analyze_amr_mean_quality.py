"""Evaluate frozen AMR mean gates from verified raw cell snapshots."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import tarfile

import numpy as np

from tools.amr_derivative_projection import split_derivative_error
from tools.amr_projection_decomposition import exact_cell_mean_square_velocity, exact_mms_mean_square_velocity
from tools.analyze_amr_gauss_gradient import _read_csv, _vector, vorticity_from_gradient, periodic_uniform_gauss_gradient
from tools.compare_amr_resolution_volume_integrated import LENGTH, _cell_widths_and_validate
from tools.high_gradient_acceptance import local_quality, standard_acceptance
from tools.high_gradient_cell_average import exact_cell_average_velocity
from tools.high_gradient_reference import fields
from tools.run_amr_mean_quality import PROTOCOL, SOURCE_FILES, sha
from tools.run_amr_mean_quality import ROOT


def verify_cube_coverage(centers, widths, n):
    """Require every dyadic finest-grid voxel to occur exactly once."""
    m = 2*n
    unit = LENGTH/m
    sizes = np.rint(widths/unit).astype(int)
    starts = np.rint((centers-widths[:, None]/2)/unit).astype(int)
    if np.any(starts < 0) or np.any(starts+sizes[:, None] > m) or np.any((sizes != 1) & (sizes != 2)):
        raise ValueError("cubes lie outside the frozen periodic domain")
    ids = []
    for size in (1, 2):
        base = starts[sizes == size]
        for dx in range(size):
            for dy in range(size):
                for dz in range(size):
                    p = base+np.array([dx, dy, dz])
                    ids.append((p[:, 0]*m+p[:, 1])*m+p[:, 2])
    counts = np.bincount(np.concatenate(ids), minlength=m**3)
    if len(counts) != m**3 or not np.all(counts == 1):
        raise ValueError("cube partition has overlaps or holes")
    return {"finest_voxels": m**3, "minimum_coverage": 1, "maximum_coverage": 1}


def stage_metrics(centers, volumes, velocity, gradient, reference_gradient, n, time, frequency):
    centers, volumes = np.asarray(centers), np.asarray(volumes)
    velocity, gradient, reference_gradient = map(np.asarray, (velocity, gradient, reference_gradient))
    widths = _cell_widths_and_validate(centers, volumes, n)
    coverage = verify_cube_coverage(centers, widths, n)
    if (velocity.shape != (len(volumes), 3) or gradient.shape != (len(volumes), 3, 3)
            or reference_gradient.shape != gradient.shape
            or not all(np.isfinite(a).all() for a in (velocity, gradient, reference_gradient))):
        raise ValueError("invalid/nonfinite captured field tensors")
    means = exact_cell_average_velocity(centers, widths, time, frequency)
    reference_energy = float(np.sum(volumes*exact_cell_mean_square_velocity(centers, widths, time, frequency)))
    parseval = LENGTH**3*exact_mms_mean_square_velocity(time, frequency)
    if not math.isfinite(reference_energy) or reference_energy <= 0 or abs(reference_energy/parseval-1) > 2e-11:
        raise ValueError("velocity reference energy fails periodic Parseval check")
    mean_error = float(np.sum(volumes*np.sum((velocity-means)**2, axis=1)))
    projected = float(np.sum(volumes*np.sum(means**2, axis=1)))
    if projected > reference_energy*(1+2e-12):
        raise ValueError("invalid velocity projection energy")
    velocity_floor = max(0.0, reference_energy-projected)
    split = split_derivative_error(centers, widths, volumes, gradient, time, frequency)
    ref_split = split_derivative_error(centers, widths, volumes, reference_gradient, time, frequency)
    point_reference = fields(centers, N=frequency, time=time)
    peak_diagnostics = {}
    for kind, actual, exact in (("gradient", np.linalg.norm(gradient, axis=(-2, -1)),
                                 np.linalg.norm(point_reference["grad_u"], axis=(-2, -1))),
                                ("curl", np.linalg.norm(vorticity_from_gradient(gradient), axis=-1),
                                 np.linalg.norm(point_reference["vorticity"], axis=-1))):
        peak_diagnostics[kind] = {"measured_sampled_peak": float(actual.max()),
                                  "reference_sampled_peak": float(exact.max()),
                                  "sampled_peak_relative_discrepancy": float(abs(actual.max()/exact.max()-1))}
    metrics = {"velocity_mean_mismatch_relative_l2": math.sqrt(mean_error/reference_energy),
               "gradient_mean_mismatch_relative_l2": split["gradient"]["mean_mismatch_relative_l2"],
               "curl_mean_mismatch_relative_l2": split["curl"]["mean_mismatch_relative_l2"]}
    return {"coverage": coverage, "metrics": metrics,
            "derivative_decomposition": split, "reference_operator_decomposition": ref_split,
            "velocity_projection_floor_relative_l2": math.sqrt(velocity_floor/reference_energy),
            "velocity_p0_total_relative_l2": math.sqrt((mean_error+velocity_floor)/reference_energy),
            "sampled_peak_diagnostics": peak_diagnostics,
            "spectrum": "UNAVAILABLE_PENDING_VALIDATED_NONUNIFORM_RECONSTRUCTION",
            "continuous_extrema": "NOT_CERTIFIED_FOR_THE_NUMERICAL_FIELD"}


def verify_archive(path, manifest):
    expected = manifest["archive"]["members_sha256"]
    if sha(path) != manifest["archive"]["sha256"]:
        raise ValueError("raw archive hash mismatch")
    found = set(); total = 0
    with tarfile.open(path, "r:gz") as archive:
        for member in archive:
            total += member.size
            if (not member.isfile() or member.issparse() or member.name not in expected
                    or member.name in found or member.size < 0 or total > 8*1024**3):
                raise ValueError("unexpected/duplicate/nonregular archive member")
            stream = archive.extractfile(member); digest = hashlib.sha256()
            for block in iter(lambda: stream.read(1 << 20), b""):
                digest.update(block)
            if digest.hexdigest() != expected[member.name]:
                raise ValueError("archive member checksum mismatch")
            found.add(member.name)
    if found != set(expected):
        raise ValueError("missing archived members")


def analyze(evidence, protocol=PROTOCOL):
    evidence = Path(evidence)
    spec = json.loads(Path(protocol).read_text()); manifest = json.loads((evidence/"manifest.json").read_text())
    if (manifest["status"] != "RUN_COMPLETE_MEASURED_MEAN_QUALITY_INPUTS"
            or manifest["protocol_sha256"] != sha(protocol) or manifest["tracked_status"].strip()):
        raise ValueError("run/protocol integrity incomplete")
    if (set(manifest["source_files_sha256"]) != set(SOURCE_FILES)
            or any(sha(ROOT/path) != value for path, value in manifest["source_files_sha256"].items())):
        raise ValueError("current protocol/harness differs from frozen run sources")
    case = next(c for c in spec["cases"] if c["id"] == manifest["case_id"])
    model = spec["model"]
    archive = evidence/manifest["archive"]["path"]
    verify_archive(archive, manifest)
    main = next(r for r in manifest["runs"] if r["label"] == "main")
    if case["capture_disabled_control"]:
        control = next(r for r in manifest["runs"] if r["label"] == "disabled-control")
        if (main["inputs_sha256"] != control["inputs_sha256"]
                or main["final_field_sha256"] != control["final_field_sha256"]
                or control["events"] or manifest["disabled_control"] != "BYTE_IDENTICAL_FINAL_U_AND_P"):
            raise ValueError("disabled-capture control did not match")
    for run in manifest["runs"]:
        state = run["container_state"]
        if state["Running"] is not False or type(state["ExitCode"]) is not int or state["ExitCode"] != 0 or state["Status"] != "exited":
            raise ValueError("unverified container exit")
    def read_text(name):
        with tarfile.open(archive, "r:gz") as tf:
            return tf.extractfile(name).read().decode()
    standard = standard_acceptance(read_text("main/log.foamRun"), model["end"], case["dt"],
        spec["standard"]["residual_tolerance"], spec["standard"]["max_outer_correctors"], read_text("main/system/fvSolution"))
    rows = []
    for stage, time in spec["measurements"]["state_times"].items():
        member = f"main/postProcessing/amrStages/{time:g}/{stage}_cells.csv"
        raw = _read_csv(archive, member)
        count = len(raw["V"])
        if not np.isfinite(np.array(list(raw.values()))).all() or not np.array_equal(raw["cell"], np.arange(count)):
            raise ValueError("nonfinite snapshot or invalid cell IDs")
        if stage == "preMap" and count != case["n"]**3 or stage == "mapped" and count != case["expected_first_mapped_cells"]:
            raise ValueError("first-map topology differs from frozen prediction")
        g = np.stack([raw[f"g{i}{j}"] for i in range(3) for j in range(3)], axis=-1).reshape(count, 3, 3)
        r = np.stack([raw[f"r{i}{j}"] for i in range(3) for j in range(3)], axis=-1).reshape(count, 3, 3)
        result = stage_metrics(_vector(raw, ("cx", "cy", "cz")), raw["V"],
            _vector(raw, ("Ux", "Uy", "Uz")), g, r, case["n"], time, model["frequency"])
        if stage == "preMap":
            centers = _vector(raw, ("cx", "cy", "cz"))
            ref_points = fields(centers, N=model["frequency"], time=time)["u"]
            comparisons = {}
            for name, values, observed in (("measured", _vector(raw, ("Ux", "Uy", "Uz")), g),
                                           ("reference", ref_points, r)):
                independent = periodic_uniform_gauss_gradient(centers, values)
                relative = float(np.linalg.norm(observed-independent)/np.linalg.norm(independent))
                if not math.isfinite(relative) or relative > 5e-11:
                    raise ValueError("native tensor convention/uniform Gauss control does not match independent reconstruction")
                comparisons[name] = relative
            result["independent_uniform_operator_relative_differences"] = comparisons
        result.update(stage=stage, time=time, cells=count,
                      cell_budget_reached_or_exceeded=count >= case["max_cells"],
                      maximum_refinement_level=int(np.rint(np.log2((LENGTH/case["n"])/np.cbrt(raw["V"]))).max()))
        result["local_mean_quality"] = local_quality(result["metrics"], spec["quality"])
        ref_metrics = {kind+"_mean_mismatch_relative_l2": result["reference_operator_decomposition"][kind]["mean_mismatch_relative_l2"]
                       for kind in ("gradient", "curl")}
        result["reference_operator_quality"] = local_quality(ref_metrics,
            {k: spec["quality"][k] for k in ref_metrics})
        rows.append(result)
    return {"status": "COMPLETE_SPECIFIED_MEAN_GATE_ANALYSIS", "source_commit": manifest["source_commit"],
            "case_id": case["id"], "case": case, "model": model,
            "archive_sha256": manifest["archive"]["sha256"], "protocol_sha256": manifest["protocol_sha256"],
            "standard_acceptance": standard, "stages": rows,
            "instrumentation_control": manifest["disabled_control"],
            "quality_scope": spec["quality_scope"], "limits": spec["limits"],
            "overall_original_AMR_peak_spectrum_gate": "UNCERTAIN_SEPARATE_OPEN_OBLIGATIONS"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence-root", type=Path, required=True)
    args = parser.parse_args()
    result = analyze(args.evidence_root)
    (args.evidence_root/"analysis.json").write_text(json.dumps(result, indent=2, allow_nan=False)+"\n")
    print(json.dumps({"status": result["status"], "standard": result["standard_acceptance"]["status"],
        "final_mean_quality": result["stages"][-1]["local_mean_quality"]["status"]}))


if __name__ == "__main__":
    main()
