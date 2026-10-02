"""Pointwise derivative contrasts for periodic SU2 vertex samples."""
from __future__ import annotations

import numpy as np


def centered_gradient(field, lengths=(2*np.pi,)*3):
    value = np.asarray(field, dtype=float)
    if value.ndim != 4 or value.shape[-1] != 3 or min(value.shape[:3]) < 4:
        raise ValueError("field must have shape (nx, ny, nz, 3), each >= 4")
    lengths = np.asarray(lengths, dtype=float)
    if lengths.shape != (3,) or not np.isfinite(lengths).all() or np.any(lengths <= 0):
        raise ValueError("lengths must be three finite positive values")
    return np.stack([
        (np.roll(value, -1, axis=axis)-np.roll(value, 1, axis=axis))
        / (2*lengths[axis]/value.shape[axis])
        for axis in range(3)
    ], axis=-1)


def curl_from_gradient(gradient):
    g = np.asarray(gradient, dtype=float)
    if g.ndim != 5 or g.shape[-2:] != (3, 3) or not np.isfinite(g).all():
        raise ValueError("gradient must be finite with shape (nx, ny, nz, 3, 3)")
    return np.stack((g[..., 2, 1]-g[..., 1, 2],
                     g[..., 0, 2]-g[..., 2, 0],
                     g[..., 1, 0]-g[..., 0, 1]), axis=-1)


def _error_summary(approx, target, concentration, top_fraction):
    delta = np.asarray(approx, dtype=float)-np.asarray(target, dtype=float)
    if delta.shape[:-1] != np.shape(concentration) and delta.shape[:-2] != np.shape(concentration):
        raise ValueError("error and concentration spatial shapes do not match")
    err2 = np.sum(delta*delta, axis=tuple(range(np.ndim(concentration), delta.ndim)))
    q = np.asarray(concentration, dtype=float)
    if not np.isfinite(delta).all() or not np.isfinite(q).all() or q.ndim != 3:
        raise ValueError("finite pointwise fields on a 3-D grid are required")
    if not 0 < top_fraction < 1:
        raise ValueError("top_fraction must be between zero and one")
    count = max(1, int(np.ceil(top_fraction*q.size)))
    flat = q.ravel()
    high_ids = np.argpartition(flat, flat.size-count)[-count:]
    mask = np.zeros(flat.size, dtype=bool)
    mask[high_ids] = True
    mask = mask.reshape(q.shape)
    total_error = float(err2.sum())
    high_error = float(err2[mask].sum())
    high_volume = float(mask.mean())
    high_rms = float(np.sqrt(err2[mask].mean()))
    low_rms = float(np.sqrt(err2[~mask].mean())) if np.any(~mask) else 0.0
    return {
        "global_rms": float(np.sqrt(err2.mean())),
        "max_pointwise_norm": float(np.sqrt(err2.max())),
        "top_concentration_fraction": high_volume,
        "error_energy_fraction_in_top_concentration": high_error/total_error if total_error else 0.0,
        "top_concentration_error_enrichment": (
            (high_error/total_error)/high_volume if total_error else 0.0),
        "top_concentration_rms": high_rms,
        "remaining_region_rms": low_rms,
        "top_to_remaining_rms_ratio": high_rms/low_rms if low_rms else None,
    }


def audit_derivative_fields(actual_gradient, sampled_reference_gradient,
                            exact_gradient, top_fraction=.1):
    """Separate stencil truncation from changes due to solver vertex values."""
    exact_vorticity = curl_from_gradient(exact_gradient)
    sampled_vorticity = curl_from_gradient(sampled_reference_gradient)
    actual_vorticity = curl_from_gradient(actual_gradient)
    grad_concentration = np.linalg.norm(exact_gradient, axis=(-2, -1))
    vort_concentration = np.linalg.norm(exact_vorticity, axis=-1)
    return {
        "gradient_solver_fd_vs_exact": _error_summary(
            actual_gradient, exact_gradient, grad_concentration, top_fraction),
        "gradient_reference_fd_vs_exact": _error_summary(
            sampled_reference_gradient, exact_gradient, grad_concentration, top_fraction),
        "gradient_solver_fd_vs_reference_fd": _error_summary(
            actual_gradient, sampled_reference_gradient, grad_concentration, top_fraction),
        "vorticity_solver_fd_vs_exact": _error_summary(
            actual_vorticity, exact_vorticity, vort_concentration, top_fraction),
        "vorticity_reference_fd_vs_exact": _error_summary(
            sampled_vorticity, exact_vorticity, vort_concentration, top_fraction),
        "vorticity_solver_fd_vs_reference_fd": _error_summary(
            actual_vorticity, sampled_vorticity, vort_concentration, top_fraction),
    }
