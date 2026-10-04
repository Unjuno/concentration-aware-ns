"""Recompute derivative error splits from hash-verified AMR snapshot archives."""
import argparse
import json
from pathlib import Path
import tempfile

import numpy as np

from tools.amr_derivative_projection import split_derivative_error
from tools.analyze_amr_gauss_gradient import (
    _read_csv, _vector, gauss_gradient_from_internal_faces,
    interior_periodic_mask, least_squares_gradient_from_internal_faces,
    periodic_uniform_gauss_gradient,
)
from tools.compare_amr_resolution_volume_integrated import (
    CASES, COMMON_MARGIN, LENGTH, ROOT, _cell_widths_and_validate, _sha256,
)
from tools.reconstruct_amr_published_archive import reconstruct


BASELINE = "evidence/of13-amr-volume-integrated-comparison-2026-10-02.json"
OUTPUT = "evidence/tests/openfoam-amr-derivative-projection-2026-10-03.json"


def analyze_archive(archive, n, evidence, protocol_path, baseline):
    manifest = json.loads((evidence/"manifest.json").read_text())
    protocol = json.loads(protocol_path.read_text())
    if _sha256(archive) != manifest["archive_sha256"] or \
            manifest["archive_sha256"] != baseline["archive_sha256"]:
        raise ValueError(f"archive identity mismatch: n={n}")
    if (_sha256(protocol_path) != baseline["protocol_sha256"]
            or protocol["case"]["initial_grid_cells_per_axis"] != n
            or manifest["foundation_source_commit"] !=
            "18870c24d21c6b982e2cdec27b2f59738cca5f90"):
        raise ValueError(f"protocol/source identity mismatch: n={n}")
    case_dir = manifest.get("case_directory", "amr-cap5000")
    time = protocol["case"].get("pre_map_time", .002)
    frequency = protocol["case"]["frequency"]
    rows = []
    for stage in ("preMap", "mapped"):
        print(f"Recomputing n={n} {stage}", flush=True)
        cell = _read_csv(archive, f"{case_dir}/postProcessing/amrStages/{time:g}/{stage}_cells.csv")
        centers = _vector(cell, ("cx", "cy", "cz"))
        volumes = cell["V"]
        widths = _cell_widths_and_validate(centers, volumes, n)
        velocity = _vector(cell, ("Ux", "Uy", "Uz"))
        old = next(s for s in baseline["stages"] if s["stage"] == stage)
        expected_cells = n**3 if stage == "preMap" else protocol["case"].get(
            "expected_mapped_cells", old["cells"])
        if len(volumes) != expected_cells or len(volumes) != old["cells"] or not np.isfinite(velocity).all():
            raise ValueError(f"unexpected or nonfinite captured cells: n={n} {stage}")
        operators = {}
        if stage == "preMap":
            operators["Gauss"] = periodic_uniform_gauss_gradient(centers, velocity)
        else:
            face = _read_csv(archive, f"{case_dir}/postProcessing/amrStages/{time:g}/{stage}_faces.csv")
            operators["Gauss"] = gauss_gradient_from_internal_faces(
                volumes, face["owner"], face["neighbour"],
                _vector(face, ("Ufx", "Ufy", "Ufz")),
                _vector(face, ("Sx", "Sy", "Sz")))
            operators["least_squares"], _ = least_squares_gradient_from_internal_faces(
                centers, velocity, face["owner"], face["neighbour"], periodic_length=LENGTH)
            del face
        mask = interior_periodic_mask(centers, volumes, boundary_margin=COMMON_MARGIN)
        selected_centers, selected_widths = centers[mask], widths[mask]
        # Ensure whole cubes, rather than centers alone, define the shared region.
        if (np.any(selected_centers-selected_widths[:, None]/2 < COMMON_MARGIN-2e-8)
                or np.any(selected_centers+selected_widths[:, None]/2 > LENGTH-COMMON_MARGIN+2e-8)
                or abs(volumes[mask].sum()/LENGTH**3-.421875) > 2e-12):
            raise ValueError("selected cubes do not tile the fixed physical support")
        if old["retained_cells"] != int(mask.sum()):
            raise ValueError("retained cell count differs from quadrature baseline")
        for name, gradient in operators.items():
            split = split_derivative_error(selected_centers, selected_widths,
                                           volumes[mask], gradient[mask], time, frequency)
            comparison = old if name == "Gauss" else old["alternative_reconstruction"]["volume_integrated_error"]
            agreement = {}
            for kind, metric in (("gradient", "gradient"), ("curl", "curl")):
                saved = comparison[f"integrated_cellwise_constant_{metric}_relative_l2"]
                delta = abs(split[kind]["p0_total_relative_l2"]-saved)
                if not np.isfinite(saved) or delta > 2e-10:
                    raise ValueError(f"closed-form/quadrature disagreement: n={n} {stage} {name} {kind}")
                agreement[kind] = {"saved_gauss8_relative_l2": saved,
                                   "absolute_difference": delta}
            rows.append({"stage": stage, "operator": name, "cells": len(volumes),
                         "retained_cells": int(mask.sum()),
                         "integrated_physical_volume": float(volumes[mask].sum()),
                         "decomposition": split, "independent_quadrature_comparison": agreement})
    return {"n": n, "archive_sha256": manifest["archive_sha256"],
            "manifest_sha256": _sha256(evidence/"manifest.json"),
            "protocol": protocol_path.relative_to(ROOT).as_posix(),
            "protocol_sha256": _sha256(protocol_path), "time": time,
            "frequency": frequency, "rows": rows}


def audit():
    baseline_path = ROOT/BASELINE
    baseline = json.loads(baseline_path.read_text())
    rows = []
    for n, evidence_rel, protocol_rel in CASES:
        evidence, protocol = ROOT/evidence_rel, ROOT/protocol_rel
        manifest = json.loads((evidence/"manifest.json").read_text())
        archive = evidence/manifest["archive"]
        old = next(c for c in baseline["cases"] if c["n"] == n)
        if archive.is_file():
            rows.append(analyze_archive(archive, n, evidence, protocol, old))
        else:
            # Reconstruct from the published, hash-checked parts; no solver run.
            with tempfile.TemporaryDirectory(prefix="cans-derivative-projection-") as temp:
                archive = Path(temp)/manifest["archive"]
                reconstruct(evidence/"amr-stage-snapshot-n64-review.tar.gz.zst.parts.json", archive)
                rows.append(analyze_archive(archive, n, evidence, protocol, old))
    return {
        "status": "PASS_ARCHIVED_DERIVATIVE_PROJECTION_REPLAY",
        "identity": "||G_h-Du||^2 = ||G_h-P_h(Du)||^2 + ||P_h(Du)-Du||^2",
        "representation": "Arbitrary constant gradient tensor per cube, and its constant curl; P_h is the exact volume-average projection on those cubes.",
        "reference_integration": "Finite Fourier products with analytic sinc interval factors, evaluated in floating point; not interval arithmetic.",
        "support": {"cube_region": "[pi/4,7*pi/4]^3", "domain_volume_fraction": .421875},
        "source_sha256": {p: _sha256(ROOT/p) for p in (
            "tools/audit_amr_derivative_projection.py", "tools/amr_derivative_projection.py",
            "tools/analyze_amr_gauss_gradient.py", "tools/compare_amr_resolution_volume_integrated.py")},
        "independent_quadrature_artifact": {"path": BASELINE, "sha256": _sha256(baseline_path)},
        "cases": rows,
        "limits": [
            "Retrospective diagnostic; no preregistered AMR quality threshold or quality verdict is introduced.",
            "The n=16 run's original protocol hash was not serialized; the current protocol hash is a replay identity and does not repair that historical limitation.",
            "The P0 representation floor is a best-approximation bound for that explicit representation, not a bound on every solver reconstruction.",
            "No solver, time trajectory, instrumentation library or n=128 derivative operator is rerun here.",
            "An operator mismatch includes the archived velocity error and post-processing error; it does not isolate a defect in the solver or mapping.",
            "Closed formulas and saved quadrature are independently evaluated numerical checks, not rigorous enclosures."
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT/OUTPUT)
    args = parser.parse_args()
    result = audit()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({"status": result["status"], "output": str(args.output)}))


if __name__ == "__main__":
    main()
