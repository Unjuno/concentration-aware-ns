"""Independent symbolic replay of an exact periodic forced-NS solution.

Based on equations (5.1), (5.4), and Theorem 4.1 of arXiv:2609.38210v1.
The field is re-derived here; no ancillary code is copied. This checks algebra,
not any numerical concentration computation or a solver implementation.
"""
import json

import sympy as sp

x, y, z, t, nu = sp.symbols("x y z t nu", real=True, positive=True)
coords = (x, y, z)
decay = sp.exp(-2 * nu * t)
decay2 = decay**2

u0 = sp.Matrix(
    [
        sp.sin(x) * sp.sin(z) + sp.cos(x) * sp.cos(y),
        sp.sin(y) * sp.sin(x) + sp.cos(y) * sp.cos(z),
        sp.sin(z) * sp.sin(y) + sp.cos(z) * sp.cos(x),
    ]
)
grad_u0 = u0.jacobian(coords)
div_u0 = sp.trigsimp(sp.trace(grad_u0))
lap_u0 = sp.Matrix([sum(sp.diff(ui, q, 2) for q in coords) for ui in u0])
assert div_u0 == 0
assert all(sp.trigsimp(lap_u0[i] + 2 * u0[i]) == 0 for i in range(3))

g0 = sp.trigsimp(grad_u0 * u0)
p0 = -sp.Rational(1, 6) * (
    sp.sin(x) * sp.sin(2 * y) * sp.cos(z)
    + sp.sin(2 * x) * sp.sin(z) * sp.cos(y)
    + sp.sin(y) * sp.sin(2 * z) * sp.cos(x)
)
grad_p0 = sp.Matrix([sp.diff(p0, q) for q in coords])
U0 = sp.Matrix([sp.trigsimp(g0[i] + grad_p0[i]) for i in range(3)])
div_U0 = sp.trigsimp(sum(sp.diff(U0[i], coords[i]) for i in range(3)))
assert div_U0 == 0

u = decay * u0
pressure = decay2 * p0
force = decay2 * U0
g = sp.trigsimp(u.jacobian(coords) * u)
residual = sp.Matrix(
    [
        sp.diff(u[i], t)
        - nu * sum(sp.diff(u[i], q, 2) for q in coords)
        + sp.diff(pressure, coords[i])
        + g[i]
        - force[i]
        for i in range(3)
    ]
)
residual = sp.Matrix([sp.trigsimp(sp.expand_trig(r)) for r in residual])
assert all(r == 0 for r in residual)

# Periodic integration by parts gives both orthogonality identities exactly.
work_convective_divergence = sp.trigsimp(
    sum(sp.diff(u0[i] * sum(u0[j] ** 2 for j in range(3)) / 2, coords[i]) for i in range(3))
    - sum(u0[i] * g0[i] for i in range(3))
)
work_pressure_divergence = sp.trigsimp(
    sum(sp.diff(p0 * u0[i], coords[i]) for i in range(3))
    - sum(u0[i] * grad_p0[i] for i in range(3))
)
assert work_convective_divergence == 0
assert work_pressure_divergence == 0

print(
    json.dumps(
        {
            "sympy_version": sp.__version__,
            "source": "arXiv:2609.38210v1 equations (5.1), (5.4), Theorem 4.1",
            "exact_checks": {
                "divergence_u0": str(div_u0),
                "laplacian_plus_2u0": [str(sp.trigsimp(lap_u0[i] + 2 * u0[i])) for i in range(3)],
                "divergence_U0": str(div_U0),
                "forced_ns_residual": [str(r) for r in residual],
                "convective_work_divergence_identity": str(work_convective_divergence),
                "pressure_work_divergence_identity": str(work_pressure_divergence),
            },
            "scope": "Independent algebraic replay of the smooth periodic exact solution only; no concentration simulation, discretization, or particle-trajectory claim is verified.",
        },
        indent=2,
    )
)

