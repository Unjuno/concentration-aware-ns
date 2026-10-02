"""Integrate saved cap100000 OpenFOAM grad(U) against the MMS at t=0.05.

This is a separate endpoint diagnostic, not an addition to the first-map
resolution sweep: the run history and adaptation budget differ.
"""

import hashlib
import json
import re
import tarfile
from pathlib import Path

import numpy as np

from tools.analyze_amr_gauss_gradient import interior_periodic_mask
from tools.compare_amr_resolution_volume_integrated import (
    COMMON_MARGIN, LENGTH, QUADRATURE_ORDERS, _integrated_relative_errors,
)

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "evidence/of13-high-gradient-amr-v2-2026-09-30/cap100000.tar.gz"
MANIFEST = ROOT / "evidence/of13-high-gradient-amr-v2-manifest-2026-09-30.json"


def _field(raw, kind, width):
    text = raw.decode("ascii")
    match = re.search(
        rf"internalField\s+nonuniform\s+List<{kind}>\s+(\d+)\s*\((.*?)\)\s*;",
        text, re.S,
    )
    if not match:
        raise ValueError(f"expected ASCII nonuniform List<{kind}>")
    count = int(match.group(1))
    values = np.fromstring(match.group(2).replace("(", " ").replace(")", " "), sep=" ")
    if values.size != count * width or not np.isfinite(values).all():
        raise ValueError(f"invalid {kind} field dimensions or values")
    return values.reshape(count, width) if width > 1 else values


def analyze():
    manifest = json.loads(MANIFEST.read_text())
    row = next(case for case in manifest["cases"] if case["case"] == "cap100000")
    raw_archive = ARCHIVE.read_bytes()
    archive_sha = hashlib.sha256(raw_archive).hexdigest()
    if archive_sha != row["raw_archive_sha256"]:
        raise ValueError("cap100000 archive hash mismatch")
    with tarfile.open(ARCHIVE, "r:gz") as tf:
        def read(name):
            stream = tf.extractfile(f"cap100000/0.05/{name}")
            if stream is None:
                raise ValueError(f"missing archived field {name}")
            return stream.read()
        centers = _field(read("C"), "vector", 3)
        volumes = _field(read("Vc"), "scalar", 1)
        levels_raw = _field(read("cellLevel"), "scalar", 1)
        if np.any(levels_raw != np.floor(levels_raw)) or np.any(levels_raw < 0):
            raise ValueError("cellLevel must contain nonnegative integers")
        levels = levels_raw.astype(int)
        gradient = _field(read("grad(U)"), "tensor", 9).reshape(-1, 3, 3)

    if not (len(centers) == len(volumes) == len(levels) == len(gradient) == row["diagnostics"]["cells"]):
        raise ValueError("saved field lengths differ from manifest cell count")
    level_counts = {str(level): int(np.count_nonzero(levels == level))
                    for level in sorted(np.unique(levels))}
    if level_counts != row["diagnostics"]["level_counts"]:
        raise ValueError("saved cellLevel counts differ from run manifest")
    if int(levels.max()) != row["diagnostics"]["parameters"]["amr"]["maxRefinement"]:
        raise ValueError("saved field did not reach configured maximum refinement")

    widths = np.cbrt(volumes)
    base = LENGTH / row["diagnostics"]["parameters"]["n"]
    allowed = base / (2.0 ** levels)
    if np.max(np.abs(widths - allowed)) > 2e-9:
        raise ValueError("cell volumes do not match their declared cubic refinement levels")
    mask = interior_periodic_mask(centers, volumes, boundary_margin=COMMON_MARGIN)
    coarse = _integrated_relative_errors(
        centers, widths, volumes, mask, gradient, 4, 0.05,
        order=QUADRATURE_ORDERS[0],
    )
    fine = _integrated_relative_errors(
        centers, widths, volumes, mask, gradient, 4, 0.05,
        order=QUADRATURE_ORDERS[1],
    )
    return {
        "status": "DIAGNOSTIC_ONLY_QUALITY_UNCERTAIN",
        "scope": "Saved OpenFOAM volTensorField grad(U), treated cellwise constant, integrated against the analytic frequency-4 MMS at t=0.05. Separate endpoint case, not part of the first-map resolution sweep.",
        "archive": ARCHIVE.relative_to(ROOT).as_posix(),
        "archive_sha256": archive_sha,
        "analyzer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "source_commit": manifest["run_environment"]["source_commit"],
        "foundation_solver_commit": row["diagnostics"].get("foundation_source_commit", "18870c24d21c6b982e2cdec27b2f59738cca5f90"),
        "final_time": 0.05,
        "mesh": {"cells": len(volumes), "level_counts": level_counts,
                 "maximum_refinement_level": int(levels.max()),
                 "retained_cells": fine["retained_cells"],
                 "retained_volume": fine["integrated_physical_volume"]},
        "operator": "Archived OpenFOAM grad(U) tensor field; constant within each cell for integration",
        "gradient_relative_l2": fine["integrated_cellwise_constant_gradient_relative_l2"],
        "curl_relative_l2": fine["integrated_cellwise_constant_curl_relative_l2"],
        "quadrature_order_comparison": {
            "orders_per_axis": list(QUADRATURE_ORDERS),
            "gradient_absolute_difference": abs(fine["integrated_cellwise_constant_gradient_relative_l2"]-coarse["integrated_cellwise_constant_gradient_relative_l2"]),
            "curl_absolute_difference": abs(fine["integrated_cellwise_constant_curl_relative_l2"]-coarse["integrated_cellwise_constant_curl_relative_l2"]),
        },
        "interpretation_limits": [
            "A cellwise-constant derivative-field reconstruction error, not continuous velocity-field error or proof of solver failure.",
            "This endpoint used a different adaptation history and budget from the first-map n16/n32/n64 resolution sweep; do not combine the values into a convergence trend.",
            "No preregistered AMR quality threshold exists; this does not establish a defect or physical singularity.",
        ],
    }


if __name__ == "__main__":
    result = analyze()
    output = ROOT / "evidence/tests/amr-cap100000-integrated-endpoint-2026-10-02.json"
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
