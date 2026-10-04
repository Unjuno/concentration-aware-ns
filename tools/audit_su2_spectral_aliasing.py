"""Recompute a three-way spectral interpretation audit from frozen archives."""
import hashlib
import json
import tarfile
from pathlib import Path

import numpy as np

from tools.reference_spectrum import spectrum
from tools.su2_spectral_audit import compare_shell_spectra


def main():
    base = Path("evidence/su2-study-v1")
    summary = json.loads((base / "summary.json").read_text())
    continuum = spectrum(time=.05, sigma=.5, cutoff=32)
    continuum_shells = np.asarray(continuum["shell_energy"])
    rows = []
    for case in summary["cases"]:
        archive_path = base / f'{case["case"]}.tar.gz'
        digest = hashlib.sha256(archive_path.read_bytes()).hexdigest()
        if digest != case["archive_sha256"]:
            raise ValueError(f"archive hash mismatch: {archive_path}")
        with tarfile.open(archive_path) as archive:
            diagnostics = json.load(archive.extractfile("diagnostics.json"))
        actual = diagnostics["computed"]
        sampled_reference = diagnostics["reference_sampled_fd2"]
        reference_energy = continuum["continuum_energy"]
        contrasts = compare_shell_spectra(
            actual["shell_energy"], sampled_reference["shell_energy"],
            continuum_shells, reference_energy)
        actual_parseval = abs(actual["spectrum_energy"] -
                              actual["mean_kinetic_energy"])
        reference_parseval = abs(sampled_reference["spectrum_energy"] -
                                 sampled_reference["mean_kinetic_energy"])
        rows.append({
            "case": case["case"],
            "archive_sha256": digest,
            **contrasts,
            "actual_parseval_absolute_residual": actual_parseval,
            "analytic_sample_parseval_absolute_residual": reference_parseval,
            "analytic_sample_mean_energy": sampled_reference["mean_kinetic_energy"],
            "continuum_mean_energy": reference_energy,
        })
    result = {
        "scope": (
            "Three-way shell-spectrum comparison: saved solver vertex samples, "
            "analytic reference evaluated on the same vertices, and continuum "
            "Fourier shells. The middle contrast estimates reference sampling, "
            "aliasing and shell-assignment effects; the first is the discrete "
            "sample-field spectral discrepancy. This is not a continuous "
            "numerical-field spectrum certificate or an independent FFT implementation."
        ),
        "continuum_reference": continuum,
        "cases": rows,
    }
    out = Path("evidence/tests/su2-spectral-aliasing-audit.json")
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
