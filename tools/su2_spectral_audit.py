"""Separate sampled-solution shell spectra from reference sampling effects."""
from __future__ import annotations

import numpy as np


def compare_shell_spectra(actual, sampled_reference, continuum_reference, energy_scale):
    """Return zero-padded shell-L1 contrasts on one common energy scale."""
    arrays = [np.asarray(x, dtype=float) for x in
              (actual, sampled_reference, continuum_reference)]
    if any(x.ndim != 1 or not np.isfinite(x).all() or np.any(x < 0) for x in arrays):
        raise ValueError("shell spectra must be finite nonnegative vectors")
    if not np.isfinite(energy_scale) or energy_scale <= 0:
        raise ValueError("energy_scale must be finite and positive")
    size = max(map(len, arrays))
    padded = [np.pad(x, (0, size-len(x))) for x in arrays]
    a, r, c = padded
    return {
        "solver_samples_vs_analytic_samples_l1": float(np.abs(a-r).sum()/energy_scale),
        "analytic_samples_vs_continuum_l1": float(np.abs(r-c).sum()/energy_scale),
        "solver_samples_vs_continuum_l1": float(np.abs(a-c).sum()/energy_scale),
        "triangle_residual": float(abs(np.abs(a-c).sum()
                                       - np.abs(a-r).sum()
                                       - np.abs(r-c).sum())/energy_scale),
    }
