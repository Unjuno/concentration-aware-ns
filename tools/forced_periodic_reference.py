"""Exact periodic Navier–Stokes reference with nonlinear forcing and pressure.

Independent NumPy transcription of the trigonometric solution in
arXiv:2609.38210v1, equations (5.1), (5.4), and Theorem 4.1.  Coordinates
are nondimensional and periodic with period 2*pi in each spatial direction.
This is a solver-verification control, not a concentration solution.
"""

import numpy as np


def fields(points, time=0.0, nu=0.01):
    """Return exact velocity, derivatives, pressure, and body force.

    ``grad_u[..., i, j]`` is ``d_j u_i``.  The equations use unit density,
    viscosity ``nu``, and

    ``u = exp(-2*nu*time) * u0``,
    ``p = exp(-4*nu*time) * p0``,
    ``f = exp(-4*nu*time) * ((u0 . grad)u0 + grad(p0))``.

    The exact identity ``laplacian(u0) = -2*u0`` cancels the time derivative
    against viscosity.  All returned arrays have the leading shape of
    ``points``.
    """
    points = np.asarray(points, dtype=float)
    if points.ndim == 0 or points.shape[-1] != 3:
        raise ValueError("points must have final dimension 3")
    if not np.isfinite(points).all() or not np.isfinite([time, nu]).all():
        raise ValueError("inputs must be finite")
    if nu <= 0:
        raise ValueError("nu must be positive")

    x, y, z = np.moveaxis(points, -1, 0)
    sx, sy, sz = np.sin(x), np.sin(y), np.sin(z)
    cx, cy, cz = np.cos(x), np.cos(y), np.cos(z)

    u0 = np.stack(
        (sx * sz + cx * cy, sy * sx + cy * cz, sz * sy + cz * cx), axis=-1
    )
    grad0 = np.empty(points.shape[:-1] + (3, 3), dtype=float)
    grad0[..., 0, 0] = cx * sz - sx * cy
    grad0[..., 0, 1] = -cx * sy
    grad0[..., 0, 2] = sx * cz
    grad0[..., 1, 0] = sy * cx
    grad0[..., 1, 1] = cy * sx - sy * cz
    grad0[..., 1, 2] = -cy * sz
    grad0[..., 2, 0] = -cz * sx
    grad0[..., 2, 1] = sz * cy
    grad0[..., 2, 2] = cz * sy - sz * cx

    sin2x, sin2y, sin2z = np.sin(2 * x), np.sin(2 * y), np.sin(2 * z)
    cos2x, cos2y, cos2z = np.cos(2 * x), np.cos(2 * y), np.cos(2 * z)
    p0 = -(
        sx * sin2y * cz + sin2x * sz * cy + sy * sin2z * cx
    ) / 6
    gradp0 = np.stack(
        (
            -(cx * sin2y * cz + 2 * cos2x * sz * cy - sy * sin2z * sx) / 6,
            -(2 * sx * cos2y * cz - sin2x * sz * sy + cy * sin2z * cx) / 6,
            -(-sx * sin2y * sz + sin2x * cz * cy + 2 * sy * cos2z * cx) / 6,
        ),
        axis=-1,
    )

    velocity_scale = np.exp(-2 * nu * time)
    nonlinear_scale = velocity_scale**2
    u = velocity_scale * u0
    grad_u = velocity_scale * grad0
    pressure = nonlinear_scale * p0
    grad_pressure = nonlinear_scale * gradp0
    convection = np.einsum("...ij,...j->...i", grad0, u0)
    force = nonlinear_scale * (convection + gradp0)
    vorticity = np.stack(
        (
            grad_u[..., 2, 1] - grad_u[..., 1, 2],
            grad_u[..., 0, 2] - grad_u[..., 2, 0],
            grad_u[..., 1, 0] - grad_u[..., 0, 1],
        ),
        axis=-1,
    )
    return {
        "u": u,
        "grad_u": grad_u,
        "vorticity": vorticity,
        "pressure": pressure,
        "grad_pressure": grad_pressure,
        "force": force,
    }
