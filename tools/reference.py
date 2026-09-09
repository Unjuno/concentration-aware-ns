"""Analytic smooth periodic manufactured solution; no PDE solver involved."""
import numpy as np


def fields(points, time=0.0, sigma=0.5, nu=0.01):
    """Return u, grad_u[i,j]=d_j u_i, vorticity and force, with p=0.

    Domain [0,2*pi)^3, center (pi,pi,pi), A(t)=exp(-t), density=1.
    Parameters and units are nondimensional. Inputs may be (..., 3).
    """
    points = np.asarray(points, dtype=float)
    if points.ndim == 0 or points.shape[-1] != 3:
        raise ValueError("points must have final dimension 3")
    if not np.isfinite(points).all() or not np.isfinite([time, sigma, nu]).all():
        raise ValueError("inputs must be finite")
    if sigma <= 0 or nu <= 0:
        raise ValueError("sigma and nu must be positive")
    d = points - np.pi
    q = -np.sin(d) / sigma**2
    r = -np.cos(d) / sigma**2
    s = np.sin(d) / sigma**2
    psi = np.exp(-time + np.sum(np.cos(d)-1, axis=-1) / sigma**2)
    a = np.array([1., 2., 3.])
    u = np.cross(psi[..., None] * q, a)
    hessian = psi[..., None, None] * (
        q[..., :, None] * q[..., None, :] + np.eye(3)*r[..., None, :])
    grad = np.stack([np.cross(hessian[..., :, j], a) for j in range(3)], axis=-1)
    lap_grad = psi[..., None] * (
        q * np.sum(q*q+r, axis=-1)[..., None] + 2*q*r+s)
    lap_u = np.cross(lap_grad, a)
    force = -u + np.einsum("...ij,...j->...i", grad, u) - nu*lap_u
    omega = np.stack([grad[..., 2, 1]-grad[..., 1, 2],
                      grad[..., 0, 2]-grad[..., 2, 0],
                      grad[..., 1, 0]-grad[..., 0, 1]], axis=-1)
    return {"u": u, "grad_u": grad, "vorticity": omega, "force": force}
