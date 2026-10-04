"""Symbolically check that a constant-velocity boost preserves Newtonian NS terms."""
import json
from pathlib import Path

import sympy as sp


def main() -> dict:
    X, Y, Z, T = sp.symbols("X Y Z T", real=True)
    old_coords = (X, Y, Z)
    x, y, z, t = sp.symbols("x y z t", real=True)
    new_coords = (x, y, z)
    V = sp.symbols("V1 V2 V3", real=True)
    nu = sp.symbols("nu", real=True)
    velocity = tuple(sp.Function(f"u{i}")(*old_coords, T) for i in range(3))
    pressure = sp.Function("p")(*old_coords, T)
    force = tuple(sp.Function(f"f{i}")(*old_coords, T) for i in range(3))
    mapping = {X: x + V[0] * t, Y: y + V[1] * t,
               Z: z + V[2] * t, T: t}

    velocity_sub = tuple(component.subs(mapping, simultaneous=True)
                         for component in velocity)
    boosted_velocity = tuple(velocity_sub[i] - V[i] for i in range(3))
    boosted_pressure = pressure.subs(mapping, simultaneous=True)
    boosted_force = tuple(component.subs(mapping, simultaneous=True)
                          for component in force)

    grad_u = sp.Matrix([[sp.diff(velocity[i], old_coords[j]) for j in range(3)]
                        for i in range(3)])
    grad_u_sub = grad_u.applyfunc(lambda entry: entry.subs(mapping, simultaneous=True))
    boosted_grad = sp.Matrix([[sp.diff(boosted_velocity[i], new_coords[j])
                               for j in range(3)] for i in range(3)])
    lap_u = sp.Matrix([sum(sp.diff(velocity[i], c, 2) for c in old_coords)
                       for i in range(3)])
    lap_u_sub = lap_u.applyfunc(lambda entry: entry.subs(mapping, simultaneous=True))
    boosted_lap = sp.Matrix([sum(sp.diff(boosted_velocity[i], c, 2)
                                 for c in new_coords) for i in range(3)])
    rate = (grad_u + grad_u.T) / 2
    boosted_rate = (boosted_grad + boosted_grad.T) / 2
    pressure_gradient = sp.Matrix([sp.diff(pressure, c) for c in old_coords])
    pressure_gradient_sub = pressure_gradient.applyfunc(
        lambda entry: entry.subs(mapping, simultaneous=True)
    )
    boosted_pressure_gradient = sp.Matrix([sp.diff(boosted_pressure, c)
                                            for c in new_coords])

    original_acceleration = sp.Matrix([
        sp.diff(velocity[i], T) + sum(velocity[j] * grad_u[i, j]
                                      for j in range(3))
        for i in range(3)
    ]).applyfunc(lambda entry: entry.subs(mapping, simultaneous=True))
    boosted_acceleration = sp.Matrix([
        sp.diff(boosted_velocity[i], t) + sum(
            boosted_velocity[j] * sp.diff(boosted_velocity[i], new_coords[j])
            for j in range(3)
        )
        for i in range(3)
    ])
    original_rhs = (-pressure_gradient + nu * lap_u + sp.Matrix(force)).applyfunc(
        lambda entry: entry.subs(mapping, simultaneous=True)
    )
    boosted_rhs = (-boosted_pressure_gradient + nu * boosted_lap
                   + sp.Matrix(boosted_force))

    def zero_matrix(matrix: sp.MatrixBase) -> bool:
        return all(sp.simplify(entry) == 0 for entry in matrix)

    checks = {
        "material_acceleration_invariant": zero_matrix(boosted_acceleration - original_acceleration),
        "velocity_gradient_invariant": zero_matrix(boosted_grad - grad_u_sub),
        "divergence_invariant": sp.simplify(sp.trace(boosted_grad) - sp.trace(grad_u_sub)) == 0,
        "laplacian_invariant": zero_matrix(boosted_lap - lap_u_sub),
        "symmetric_strain_rate_invariant": zero_matrix(boosted_rate - rate.applyfunc(
            lambda entry: entry.subs(mapping, simultaneous=True)
        )),
        "pressure_gradient_invariant": zero_matrix(boosted_pressure_gradient - pressure_gradient_sub),
        "constant_viscosity_ns_rhs_invariant": zero_matrix(boosted_rhs - original_rhs),
    }
    result = {
        "scope": "Exact chain-rule identities for smooth forced incompressible Navier-Stokes fields under a constant Galilean boost; not a constitutive model or molecular simulation.",
        "sympy": sp.__version__,
        "assumptions": ["V is constant", "u, p, and f are smooth", "the force is transformed with the observer frame", "nu is constant"],
        "boost": "u'(x',t)=u(x'+Vt,t)-V; p'(x',t)=p(x'+Vt,t); f'(x',t)=f(x'+Vt,t)",
        "checks": checks,
        "success": all(checks.values()),
    }
    if not result["success"]:
        raise SystemExit(json.dumps(result, indent=2))
    destination = Path("evidence/tests/galilean-viscosity-invariance.json")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    return result


if __name__ == "__main__":
    main()
