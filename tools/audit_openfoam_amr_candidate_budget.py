"""Reconstruct cap4096 AMR candidates from the frozen Foundation 13 archive.

This is a retrospective, source-pinned reconstruction. It does not rerun
OpenFOAM or claim a solver defect.
"""
import hashlib
import json
import re
import tarfile
from pathlib import Path

import numpy as np


ARCHIVE = Path("evidence/of13-high-gradient-amr-v2-2026-09-30/cap4096.tar.gz")
MANIFEST = Path("evidence/of13-high-gradient-amr-v2-manifest-2026-09-30.json")
SOURCE_COMMIT = "18870c24d21c6b982e2cdec27b2f59738cca5f90"
SOURCE_FILE_SHA256 = "4b0635ea65709ef917f05fd9375558a0fe9d1064eaf561521fbd2abf5f20af96"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def parse_field(data, kind):
    text = data.decode("ascii")
    match = re.search(
        rf"internalField\s+nonuniform\s+List<{kind}>\s+(\d+)\s*\((.*?)\)\s*;",
        text, re.S)
    if not match:
        raise ValueError(f"expected ASCII nonuniform List<{kind}>")
    count = int(match[1])
    body = match[2]
    values = np.fromstring(body.replace("(", " ").replace(")", " "), sep=" ")
    width = 3 if kind == "vector" else 1
    if values.size != count * width or not np.isfinite(values).all():
        raise ValueError(f"invalid {kind} field length or values")
    return values.reshape(count, width) if width == 3 else values


def main():
    manifest = json.loads(MANIFEST.read_text())
    case = next(row for row in manifest["cases"] if row["case"] == "cap4096")
    archive_bytes = ARCHIVE.read_bytes()
    archive_hash = sha(archive_bytes)
    if archive_hash != case["raw_archive_sha256"]:
        raise ValueError("cap4096 archive hash differs from manifest")

    with tarfile.open(ARCHIVE, "r:gz") as tf:
        def read(name):
            member = tf.extractfile(f"cap4096/{name}")
            if member is None:
                raise ValueError(f"missing archived file {name}")
            return member.read()

        centers = parse_field(read("0.05/C"), "vector")
        volumes = parse_field(read("0.05/Vc"), "scalar")
        sensor = parse_field(read("0.05/refineSensor"), "scalar")
        mesh_dict = read("constant/dynamicMeshDict").decode("ascii")
        block_dict = read("system/blockMeshDict").decode("ascii")
        log = read("log.foamRun").decode("utf-8", errors="replace")

    def scalar(key):
        found = re.search(rf"\b{re.escape(key)}\s+([0-9.eE+-]+)\s*;", mesh_dict)
        if not found:
            raise ValueError(f"missing {key} from dynamicMeshDict")
        return float(found[1])

    n = round(len(sensor) ** (1 / 3))
    if n**3 != len(sensor) or centers.shape != (len(sensor), 3):
        raise ValueError("expected a cubic structured initial mesh")
    if not np.all(volumes > 0) or not np.allclose(volumes, volumes[0], rtol=1e-12, atol=1e-14):
        raise ValueError("cell volumes are not uniform positive values")
    length = 2 * np.pi
    h = length / n
    ijk_float = centers / h - 0.5
    ijk = np.rint(ijk_float).astype(int) % n
    coordinate_error = float(np.max(np.abs(ijk_float - np.rint(ijk_float))))
    grid = np.full((n, n, n), np.nan)
    if len(np.unique(ijk, axis=0)) != n**3 or coordinate_error > 1e-10:
        raise ValueError("centers do not map one-to-one to a periodic Cartesian grid")
    grid[ijk[:, 0], ijk[:, 1], ijk[:, 2]] = sensor
    if not np.isfinite(grid).all():
        raise ValueError("sensor grid has missing entries")
    reconstructed_sensor = ((1 + np.cos(centers[:, 1])) / 2) ** 4 * ((1 + np.cos(centers[:, 2])) / 2) ** 4
    sensor_residual = float(np.max(np.abs(sensor - reconstructed_sensor)))

    lower, upper = scalar("lowerRefineLevel"), scalar("upperRefineLevel")
    max_cells, max_level = int(scalar("maxCells")), int(scalar("maxRefinement"))
    buffer_layers = int(scalar("nBufferLayers"))
    raw = (grid > lower) & (grid < upper)
    buffered = raw.copy()
    for _ in range(buffer_layers):
        expanded = buffered.copy()
        for axis in range(3):
            expanded |= np.roll(buffered, 1, axis=axis) | np.roll(buffered, -1, axis=axis)
        buffered = expanded

    if "type cyclic" not in block_dict or block_dict.count("type cyclic") != 6:
        raise ValueError("periodic face-neighbor assumption not confirmed by archived blockMeshDict")
    if max_cells != len(sensor):
        raise ValueError("cap4096 does not equal the archived initial mesh count")
    if "Refined from" in log:
        raise ValueError("cap4096 log unexpectedly contains a mesh refinement event")

    # Independent cross-check: cap5000 sees the same sensor and buffer setup,
    # and its archived first event logs the reconstructed count.
    cap5000_path = Path("evidence/of13-high-gradient-amr-v2-2026-09-30/cap5000.tar.gz")
    cap5000_manifest = next(row for row in manifest["cases"] if row["case"] == "cap5000")
    with tarfile.open(cap5000_path, "r:gz") as tf:
        if sha(cap5000_path.read_bytes()) != cap5000_manifest["raw_archive_sha256"]:
            raise ValueError("cap5000 archive hash differs from manifest")
        log5000 = tf.extractfile("cap5000/log.foamRun").read().decode("utf-8", errors="replace")
    crosscheck = re.search(r"Selected\s+(\d+)\s+cells for refinement out of\s+4096", log5000)
    if not crosscheck or int(crosscheck[1]) != int(buffered.sum()):
        raise ValueError("cap5000 logged selection does not match reconstructed candidate count")

    result = {
        "scope": "Retrospective candidate reconstruction for cap4096 from archived sensor/mesh and pinned Foundation 13 buffering semantics; not a solver rerun or defect finding.",
        "archive": ARCHIVE.as_posix(),
        "archive_sha256": archive_hash,
        "foundation_source_commit": SOURCE_COMMIT,
        "source_file": "src/fvMeshTopoChangers/refiner/refiner_fvMeshTopoChanger.C",
        "source_file_sha256": SOURCE_FILE_SHA256,
        "checkpoint": "0.05",
        "mesh": {"cells": len(sensor), "structured_periodic_shape": [n, n, n], "max_center_grid_error": coordinate_error, "uniform_cell_volume": float(volumes[0])},
        "sensor": {"formula": "g(y)*g(z), g(q)=(1+cos(q))^4/16", "max_abs_residual": sensor_residual, "lower_refine_level_strict": lower, "upper_refine_level_strict": upper},
        "candidate_reconstruction": {
            "raw_sensor_eligible_cells": int(raw.sum()),
            "buffer_layers": buffer_layers,
            "periodic_face_neighbor_buffered_cells": int(buffered.sum()),
            "buffer_added_cells": int(buffered.sum() - raw.sum()),
            "max_refinement": max_level,
            "pre_maxCells_guard_candidate_count": int(buffered.sum()),
            "initial_global_cells": len(sensor),
            "maxCells": max_cells,
            "selection_guard_skips_when_current_cells_equal_maxCells": True,
            "blocked_by_guard_at_each_eligible_check": int(buffered.sum()),
            "eligible_check_count": "not inferred from unrefinement diagnostics",
        },
        "cross_check": {"case": "cap5000", "archived_logged_selected_cells": int(crosscheck[1]), "matches_reconstructed_buffered_count": True, "mesh_growth": "4096 to 16640 (7*1792 added cells)"},
        "limits": ["Sensor field is stationary and final checkpoint confirms the prescribed analytic sensor; the per-check candidate count is inferred to remain the same because the mesh did not change.", "The number of eligible adaptation checks is not reconstructed here.", "This establishes candidates bypassed by the configured maxCells selection guard, not that the cap policy is erroneous."],
    }
    output = Path("evidence/tests/openfoam-amr-candidate-budget-audit.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
