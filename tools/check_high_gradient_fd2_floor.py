"""Reference-only periodic-FD2 resolution audit for the frozen MMS matrix."""
import json
from pathlib import Path

import numpy as np

from tools.high_gradient_reference import fields
from tools.metrics import diagnostics


def audit(protocol_path="protocols/high-gradient-of13-v2.json"):
    protocol_path = Path(protocol_path)
    spec = json.loads(protocol_path.read_text())
    n_values = spec["spatial_matrix"]["cell_counts"]
    frequency = spec["frequency_N"]
    time = spec["end_time"]
    L = 2 * np.pi
    rows = []
    for n in n_values:
        axis = (np.arange(n) + 0.5) * L / n
        z, y, x = np.meshgrid(axis, axis, axis, indexing="ij")
        points = np.stack((x, y, z), axis=-1).reshape(-1, 3)
        reference = fields(points, N=frequency, nu=spec["viscosity"], time=time)
        grid = reference["u"].reshape(n, n, n, 3).transpose(2, 1, 0, 3)
        fd2 = diagnostics(grid)
        exact_gradient_peak = float(np.linalg.norm(reference["grad_u"], axis=(-2, -1)).max())
        exact_vorticity_peak = float(np.linalg.norm(reference["vorticity"], axis=-1).max())
        g_floor = abs(fd2["max_gradient_fd2"] - exact_gradient_peak) / exact_gradient_peak
        w_floor = abs(fd2["max_vorticity_fd2"] - exact_vorticity_peak) / exact_vorticity_peak
        selected = float(np.sin(frequency * L / n) / (frequency * L / n))
        rows.append({
            "n": n,
            "exact_solution_fd2_gradient_peak_relative_error": g_floor,
            "exact_solution_fd2_vorticity_peak_relative_error": w_floor,
            "selected_component_fd2_to_exact_derivative_ratio": selected,
            "gradient_threshold": spec["local_quality_relative_error_thresholds"]["max_gradient"],
            "vorticity_threshold": spec["local_quality_relative_error_thresholds"]["max_vorticity"],
            "gradient_stencil_floor_within_threshold": g_floor <= spec["local_quality_relative_error_thresholds"]["max_gradient"],
            "vorticity_stencil_floor_within_threshold": w_floor <= spec["local_quality_relative_error_thresholds"]["max_vorticity"],
        })
    passing = [r["n"] for r in rows if r["gradient_stencil_floor_within_threshold"]
               and r["vorticity_stencil_floor_within_threshold"]]
    if len(passing) < 2:
        raise AssertionError("protocol must include at least two grids whose reference-only FD2 floors meet local thresholds")
    return {
        "protocol": str(protocol_path),
        "scope": "Exact MMS samples passed through the benchmark's periodic centered-FD2 diagnostics; reference-only truncation floor, not solver output or defect evidence.",
        "n": frequency,
        "rows": rows,
        "at_least_two_finer_grids_meet_both_derivative_thresholds": passing,
    }


if __name__ == "__main__":
    result = audit()
    Path("evidence/tests/high-gradient-fd2-resolution-floor.json").write_text(
        json.dumps(result, indent=2) + "\n"
    )
    print(json.dumps(result, indent=2))
