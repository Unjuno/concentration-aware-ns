"""Hand-coded NumPy evaluator for the localized high-gradient MMS."""
import numpy as np


def envelope_derivatives(q):
    """Return d^k/dq^k ((1+cos(q))/2)^4 for k=0..3 via Fourier sums."""
    q = np.asarray(q, dtype=float)
    coefficients = ((1, 56.0), (2, 28.0), (3, 8.0), (4, 1.0))
    out = [np.full_like(q, 35.0 / 128.0) if k == 0 else np.zeros_like(q)
           for k in range(4)]
    for mode, a in coefficients:
        out[0] += a * np.cos(mode*q) / 128.0
        out[1] -= a * mode * np.sin(mode*q) / 128.0
        out[2] -= a * mode**2 * np.cos(mode*q) / 128.0
        out[3] += a * mode**3 * np.sin(mode*q) / 128.0
    return out


def fields(points, N=8, nu=0.01):
    """Return u, grad_u[i,j], vorticity and steady force at (...,3) points."""
    points = np.asarray(points, dtype=float)
    if points.ndim == 0 or points.shape[-1] != 3:
        raise ValueError("points must have final dimension 3")
    if not np.isfinite(points).all() or not np.isfinite([N, nu]).all():
        raise ValueError("inputs must be finite")
    if int(N) != N or N < 1 or nu <= 0:
        raise ValueError("N must be a positive integer and nu must be positive")

    x, y, z = np.moveaxis(points, -1, 0)
    gy = envelope_derivatives(y)
    hz = envelope_derivatives(z)
    chi = gy[0] * hz[0]
    chi_y = gy[1] * hz[0]
    chi_z = gy[0] * hz[1]
    chi_yy = gy[2] * hz[0]
    chi_zz = gy[0] * hz[2]
    chi_yz = gy[1] * hz[1]
    chi_yyy = gy[3] * hz[0]
    chi_yzz = gy[1] * hz[2]
    sx, cx = np.sin(N*x), np.cos(N*x)

    u = np.stack((chi_y*sx/N**2, -chi*cx/N, np.zeros_like(x)), axis=-1)
    grad = np.zeros(points.shape[:-1] + (3, 3), dtype=float)
    grad[..., 0, 0] = chi_y*cx/N
    grad[..., 0, 1] = chi_yy*sx/N**2
    grad[..., 0, 2] = chi_yz*sx/N**2
    grad[..., 1, 0] = chi*sx
    grad[..., 1, 1] = -chi_y*cx/N
    grad[..., 1, 2] = -chi_z*cx/N

    lap = np.stack((sx*(-chi_y + (chi_yyy+chi_yzz)/N**2),
                    cx*(N*chi - (chi_yy+chi_zz)/N),
                    np.zeros_like(x)), axis=-1)
    omega = np.stack((chi_z*cx/N,
                      chi_yz*sx/N**2,
                      (chi-chi_yy/N**2)*sx), axis=-1)
    force = np.einsum("...ij,...j->...i", grad, u) - nu*lap
    return {"u": u, "grad_u": grad, "vorticity": omega, "force": force}
