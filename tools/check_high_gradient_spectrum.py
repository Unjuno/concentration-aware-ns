"""Cross-check analytic shell sums against a resolved uniform-grid FFT."""
import json
from pathlib import Path

import numpy as np

from tools.high_gradient_reference import fields
from tools.high_gradient_spectrum import shell_spectrum
from tools.metrics import diagnostics


def check():
    time = 0.137
    rows = []
    for n_frequency in (4, 8, 16):
        grid_n = 4*n_frequency
        axis = (np.arange(grid_n)+0.5)*2*np.pi/grid_n
        x, y, z = np.meshgrid(axis, axis, axis, indexing="ij")
        points = np.stack((x, y, z), axis=-1)
        velocity = fields(points, N=n_frequency, time=time)["u"]
        sampled = diagnostics(velocity)
        analytic = shell_spectrum(n_frequency, time)
        a = np.asarray(analytic["shell_energy"])
        b = np.asarray(sampled["shell_energy"])
        width = max(a.size, b.size)
        a = np.pad(a, (0, width-a.size))
        b = np.pad(b, (0, width-b.size))
        error = float(np.max(np.abs(a-b)))
        total_error = abs(analytic["total_energy"]-sampled["spectrum_energy"])
        rows.append({
            "N": n_frequency,
            "uniform_grid": [grid_n]*3,
            "analytic_nonzero_shells": int(np.count_nonzero(a)),
            "sampled_nonzero_shells": int(np.count_nonzero(b)),
            "maximum_absolute_shell_error": error,
            "total_energy_absolute_error": total_error,
        })
    result = {
        "time": time,
        "tolerance": 2e-14,
        "cases": rows,
        "passed": all(max(r["maximum_absolute_shell_error"],
                           r["total_energy_absolute_error"]) < 2e-14 for r in rows),
        "scope": "Independent finite-mode analytic shell sum versus sampled FFT on resolved uniform grids; not a solver run or intersample solution-error certificate.",
    }
    path = Path("evidence/tests/high-gradient-spectrum.json")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(result, indent=2))
    if not result["passed"]:
        raise SystemExit(1)
    return result


if __name__ == "__main__":
    check()
