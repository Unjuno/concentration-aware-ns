"""Quantify only the analytic MMS force mismatch from SU2's old-time callback."""
import hashlib
import json
import math
from pathlib import Path

import numpy as np

from tools.high_gradient_reference import fields


def audit():
    base = Path("evidence/su2-study-v1")
    summary = json.loads((base / "summary.json").read_text())
    cases = [row for row in summary["cases"] if row["case"].startswith("n64-dt")]
    rng = np.random.default_rng(20261001)
    points = rng.uniform(0.0, 2.0 * np.pi, size=(4096, 3))
    rows = []
    for case in cases:
        path = base / f"{case['case']}.tar.gz"
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest != case["archive_sha256"]:
            raise ValueError(f"archive hash mismatch: {path}")
        with __import__("tarfile").open(path) as archive:
            params = json.load(archive.extractfile("parameters.json"))
        h = float(params["dt"])
        end = float(params["end"])
        if abs(round(end / h) * h - end) > 1e-14:
            raise ValueError("endpoint is not aligned with time step")

        old = fields(points, N=params["n"], nu=params["nu"], time=end - h)["force"]
        target = fields(points, N=params["n"], nu=params["nu"], time=end)["force"]
        delta = old - target
        norms = np.linalg.norm(delta, axis=-1)
        target_norms = np.linalg.norm(target, axis=-1)
        rows.append({
            "case": case["case"], "archive_sha256": digest,
            "dt": h, "endpoint": end, "sample_count": len(points),
            "seed": 20261001,
            "max_force_difference": float(norms.max()),
            "rms_force_difference": float(np.sqrt(np.mean(norms**2))),
            "max_relative_force_difference": float(np.max(norms / np.maximum(target_norms, 1e-300))),
            "analytic_identity": "f(t)=exp(-t)*L + exp(-2t)*Q; f(t-h)-f(t)=(exp(h)-1)*exp(-t)*L + (exp(2h)-1)*exp(-2t)*Q",
        })
    orders = [math.log2(rows[i]["rms_force_difference"] / rows[i+1]["rms_force_difference"])
              for i in range(len(rows)-1)]
    return {
        "scope": "Analytic manufactured-force pointwise old-time versus target-time mismatch only. This is not a PDE solution-error attribution or a solver defect finding.",
        "source_time_contract": "completed k updates represent k*dt; callback uses (k-1)*dt",
        "cases": rows,
        "successive_halving_force_difference_orders": orders,
        "interpretation": "The sampled forcing mismatch scales approximately linearly with dt, consistent with first-order time-level displacement. It cannot quantify its contribution to endpoint velocity error because the discrete flow operator, nonlinear response, spatial error, and failed inner solves also contribute.",
    }


if __name__ == "__main__":
    result = audit()
    out = Path("evidence/tests/su2-localized-source-lag.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
