"""Measure exact-sample FD2 peak-error floors on SU2's periodic vertex phase."""
import argparse
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys

import numpy as np

from tools.high_gradient_reference import fields
from tools.metrics import diagnostics


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def audit(protocol_path="protocols/su2-shared-high-gradient-v1.json"):
    protocol_path = Path(protocol_path)
    protocol = json.loads(protocol_path.read_text())
    N = protocol["adapter"]["frequency_N"]
    nu = protocol["adapter"]["viscosity"]
    time = protocol["time"]["end"]
    thresholds = protocol["acceptance"]["quality_thresholds"]
    rows = []
    for n, _dt in protocol["cases"]["spatial"]:
        axis = 2 * np.pi * np.arange(n) / n
        xyz = np.array(np.meshgrid(axis, axis, axis, indexing="ij")).reshape(3, -1).T
        reference = fields(xyz, N=N, nu=nu, time=time)
        computed = diagnostics(reference["u"].reshape(n, n, n, 3))
        gradient_peak = float(np.linalg.norm(reference["grad_u"], axis=(-2, -1)).max())
        vorticity_peak = float(np.linalg.norm(reference["vorticity"], axis=-1).max())
        grad_error = abs(computed["max_gradient_fd2"] - gradient_peak) / gradient_peak
        vort_error = abs(computed["max_vorticity_fd2"] - vorticity_peak) / vorticity_peak
        status = "PASS" if (grad_error <= thresholds["max_gradient_relative_error_samples"]
                            and vort_error <= thresholds["max_vorticity_relative_error_samples"]) else "FAIL"
        rows.append({"n": int(n), "unique_periodic_vertices": int(n**3),
                     "mean_kinetic_energy": computed["mean_kinetic_energy"],
                     "gradient_peak_exact_sampled": gradient_peak,
                     "gradient_peak_fd2": computed["max_gradient_fd2"],
                     "gradient_peak_relative_error_floor": float(grad_error),
                     "vorticity_peak_exact_sampled": vorticity_peak,
                     "vorticity_peak_fd2": computed["max_vorticity_fd2"],
                     "vorticity_peak_relative_error_floor": float(vort_error),
                     "fd2_divergence_peak_on_exact_velocity": computed["max_divergence_fd2"],
                     "operator_floor": status})
    return {"protocol": str(protocol_path), "mms_profile": protocol["adapter"]["mms_profile"],
            "benchmark_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
            "frequency_N": N, "viscosity": nu, "evaluation_time": time,
            "sample_phase": "unique periodic vertices x_i=2*pi*i/n; duplicates omitted by construction",
            "scope": "analytic reference sampled without a solver; isolates the FD2 diagnostic floor, not SU2 error",
            "thresholds": {"max_gradient_relative_error_samples": thresholds["max_gradient_relative_error_samples"],
                           "max_vorticity_relative_error_samples": thresholds["max_vorticity_relative_error_samples"]},
            "environment": {"python": sys.version, "platform": platform.platform(), "numpy": np.__version__},
            "sha256": {str(p): sha256(p) for p in (protocol_path, Path("tools/high_gradient_reference.py"),
                         Path("tools/metrics.py"), Path("tools/audit_su2_high_gradient_resolution.py"))},
            "rows": rows}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--protocol", default="protocols/su2-shared-high-gradient-v1.json")
    parser.add_argument("--output", default="evidence/tests/su2-shared-high-gradient-resolution-floor.json")
    args = parser.parse_args()
    result = audit(args.protocol)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
