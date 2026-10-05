"""Audit derivative errors by location from the frozen SU2 raw archives."""
import hashlib
import io
import json
import tarfile
from pathlib import Path

import numpy as np

from tools.reference import fields
from tools.su2_local_derivative_audit import (
    audit_derivative_fields,
    centered_gradient,
)


def _grid_from_restart(csv_bytes, n):
    data = np.genfromtxt(io.BytesIO(csv_bytes), delimiter=",", names=True)
    xyz = np.stack([data[name] for name in ("x", "y", "z")], axis=-1)
    velocity = np.stack([data[f"Velocity_{name}"] for name in ("x", "y", "z")], axis=-1)
    index = np.rint(xyz*n/(2*np.pi)).astype(int)
    if np.max(np.abs(xyz-index*(2*np.pi/n))) > 1e-12 or np.any(index < 0) or np.any(index > n):
        raise ValueError("restart coordinates do not match the frozen periodic grid")
    keep = np.all(index < n, axis=1)
    ids = index[keep]
    if len(ids) != n**3 or len(np.unique(ids, axis=0)) != n**3:
        raise ValueError("restart does not have exactly n^3 unique periodic vertices")
    grid = np.empty((n, n, n, 3))
    grid[tuple(ids.T)] = velocity[keep]
    return xyz[keep], ids, grid, velocity, index


def main():
    base = Path("evidence/su2-study-v1")
    summary = json.loads((base / "summary.json").read_text())
    rows = []
    for case in summary["cases"]:
        path = base / f'{case["case"]}.tar.gz'
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest != case["archive_sha256"]:
            raise ValueError(f"archive hash mismatch: {path}")
        with tarfile.open(path) as archive:
            parameters = json.load(archive.extractfile("parameters.json"))
            diagnostics = json.load(archive.extractfile("diagnostics.json"))
            n = parameters["n"]
            steps = diagnostics["steps"]
            raw = archive.extractfile(f"restart_{steps-1:05d}.csv").read()
        xyz, ids, actual, duplicated_velocity, all_indices = _grid_from_restart(raw, n)
        periodic_mismatch = float(np.max(np.abs(
            duplicated_velocity - actual[tuple((all_indices % n).T)])))
        if periodic_mismatch != diagnostics["periodic_duplicate_max_mismatch"]:
            raise ValueError("periodic duplicate check differs from archived diagnostics")

        reference = fields(xyz, diagnostics["updated_solution_time"],
                           sigma=parameters["sigma"], nu=parameters["nu"])
        reference_velocity = np.empty_like(actual)
        reference_gradient = np.empty((n, n, n, 3, 3))
        reference_vorticity = np.empty((n, n, n, 3))
        reference_velocity[tuple(ids.T)] = reference["u"]
        reference_gradient[tuple(ids.T)] = reference["grad_u"]
        reference_vorticity[tuple(ids.T)] = reference["vorticity"]

        actual_gradient = centered_gradient(actual)
        sampled_reference_gradient = centered_gradient(reference_velocity)
        replayed_max_gradient = float(np.linalg.norm(actual_gradient, axis=(-2, -1)).max())
        replayed_max_vorticity = float(np.linalg.norm(
            np.stack((actual_gradient[..., 2, 1]-actual_gradient[..., 1, 2],
                      actual_gradient[..., 0, 2]-actual_gradient[..., 2, 0],
                      actual_gradient[..., 1, 0]-actual_gradient[..., 0, 1]), axis=-1),
            axis=-1).max())
        if abs(replayed_max_gradient-diagnostics["computed"]["max_gradient_fd2"]) > 1e-12:
            raise ValueError("gradient replay differs from archived diagnostic")
        if abs(replayed_max_vorticity-diagnostics["computed"]["max_vorticity_fd2"]) > 1e-12:
            raise ValueError("vorticity replay differs from archived diagnostic")
        contrasts = audit_derivative_fields(
            actual_gradient, sampled_reference_gradient, reference_gradient,
            top_fraction=.1)
        rows.append({
            "case": case["case"],
            "archive_sha256": digest,
            "unique_vertices": n**3,
            "periodic_duplicate_max_mismatch": periodic_mismatch,
            "reference_time": diagnostics["updated_solution_time"],
            "top_concentration_fraction": .1,
            "gradient_reference_peak": float(np.linalg.norm(reference_gradient, axis=(-2, -1)).max()),
            "vorticity_reference_peak": float(np.linalg.norm(reference_vorticity, axis=-1).max()),
            "contrasts": contrasts,
        })
    result = {
        "scope": (
            "Pointwise centered-FD2 derivative audit on archived SU2 vertex samples. "
            "For each derivative, solver FD2 versus exact analytic derivative combines "
            "stencil truncation and solver-field error; analytic-reference FD2 versus "
            "exact derivative measures stencil truncation; solver FD2 versus reference "
            "FD2 isolates differences between the two sampled fields under the same "
            "stencil. Top-decile enrichment is descriptive and does not certify "
            "continuous-domain extrema, physical concentration, or solver correctness."
        ),
        "cases": rows,
    }
    out = Path("evidence/tests/su2-local-derivative-audit.json")
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
