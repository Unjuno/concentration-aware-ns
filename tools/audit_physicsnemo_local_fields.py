"""Cross-check sampled pointwise derivative errors against archived PINN runs.

The normalized absolute errors use the exact sampled peak as a fixed scale;
they are not pointwise relative errors or continuous-domain bounds.
"""
import hashlib
import io
import json
import tarfile
from pathlib import Path

import numpy as np


ROOT = Path("evidence/physicsnemo-study-v1")


def sha(data):
    return hashlib.sha256(data).hexdigest()


def audit(root=ROOT):
    root = Path(root)
    rows = []
    for archive in sorted(root.glob("n*-nt*.tar.gz")):
        case = archive.name.removesuffix(".tar.gz")
        grad_path = root / f"{case}-gradient.json"
        summary = json.loads((root / "summary.json").read_text())
        indexed = next(r for r in summary["cases"] if r["case"] == case)
        archive_hash = sha(archive.read_bytes())
        if archive_hash != indexed["archive_sha256"]:
            raise ValueError(f"archive hash mismatch: {case}")
        grad = json.loads(grad_path.read_text())
        with tarfile.open(archive, "r:gz") as tar:
            checkpoint = tar.extractfile("weights.pt").read()
            evaluation = tar.extractfile("evaluation.npz").read()
            diagnostics = json.load(tar.extractfile("diagnostics.json"))
        with np.load(io.BytesIO(evaluation)) as data:
            sample_count = len(data["coordinates"])
        if grad["checkpoint_sha256"] != sha(checkpoint):
            raise ValueError(f"checkpoint mismatch: {case}")
        if grad["evaluation_sha256"] != sha(evaluation):
            raise ValueError(f"evaluation mismatch: {case}")
        gpeak = diagnostics["reference_gradient_peak_samples"]
        wpeak = diagnostics["reference_vorticity_peak_samples"]
        ge = grad["maximum_gradient_field_error_samples"]
        we = grad["maximum_vorticity_field_error_samples"]
        rows.append({
            "case": case,
            "archive_sha256": archive_hash,
            "gradient_evidence_sha256": sha(grad_path.read_bytes()),
            "checkpoint_matches": True,
            "evaluation_matches": True,
            "sampled_gradient_peak_magnitude_error": grad["gradient_peak_relative_error_samples"],
            "sampled_vorticity_peak_magnitude_error": grad["vorticity_peak_relative_error_samples"],
            "max_sampled_gradient_field_error_over_exact_sampled_peak": ge / gpeak,
            "max_sampled_vorticity_field_error_over_exact_sampled_peak": we / wpeak,
            "sample_count": sample_count,
        })
    return {
        "cases": rows,
        "scope": "Cross-checks sampled analytic-autograd derivative metrics against archived checkpoint/evaluation artifacts. Ratios normalize maximum sampled absolute field difference by the exact sampled peak; no continuous extrema or pointwise relative-error bound is claimed.",
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2))
