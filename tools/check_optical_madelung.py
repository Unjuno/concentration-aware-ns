"""Symbolically audit the Madelung form of the paraxial optical NLSE.

This is an algebra check for the model stated in the analytic crosswalk. It is
not an optical experiment, a derivation of the paraxial approximation from
Maxwell's equations, or a mapping to viscous Navier--Stokes.
"""
import json
from pathlib import Path

import sympy as sp


def audit():
    x, y, z = sp.symbols("x y z", real=True)
    mass, coupling = sp.symbols("m g", nonzero=True, real=True)
    rho = sp.Function("rho", positive=True)(x, y, z)
    theta = sp.Function("theta", real=True)(x, y, z)
    potential = sp.Function("V", real=True)(x, y, z)
    amplitude = sp.sqrt(rho)
    grad = lambda f: sp.Matrix([sp.diff(f, x), sp.diff(f, y)])
    lap = lambda f: sp.diff(f, x, 2) + sp.diff(f, y, 2)

    phase_eq = (
        sp.diff(theta, z)
        + grad(theta).dot(grad(theta)) / (2 * mass)
        + coupling * rho
        + potential
        - lap(amplitude) / (2 * mass * amplitude)
    )
    continuity = sp.diff(rho, z) + (
        sp.diff(rho * sp.diff(theta, x) / mass, x)
        + sp.diff(rho * sp.diff(theta, y) / mass, y)
    )

    velocity = grad(theta) / mass
    theta_z_from_real_nlse = (
        -grad(theta).dot(grad(theta)) / (2 * mass)
        - coupling * rho - potential + lap(amplitude) / (2 * mass * amplitude)
    )
    euler = grad(theta_z_from_real_nlse) / mass + sp.Matrix([
        sum(velocity[j] * sp.diff(velocity[i], (x, y)[j]) for j in range(2))
        for i in range(2)
    ])
    euler_rhs = (
        -coupling * grad(rho) / mass
        -grad(potential) / mass
        +grad(lap(amplitude) / amplitude) / (2 * mass**2)
    )
    euler_residual = [sp.simplify(v) for v in euler - euler_rhs]

    nlse_real_residual = (
        -sp.diff(theta, z)
        + (lap(amplitude) / amplitude - grad(theta).dot(grad(theta))) / (2 * mass)
        - coupling * rho - potential
    )
    grad_amplitude = grad(amplitude)
    nlse_imaginary_residual = (
        sp.diff(amplitude, z) / amplitude
        + (lap(theta) + 2 * grad_amplitude.dot(grad(theta)) / amplitude) / (2 * mass)
    )
    checks = {
        "real_nlse_residual_is_negative_phase_equation": sp.simplify(nlse_real_residual + phase_eq) == 0,
        "imaginary_nlse_residual_is_continuity_over_2rho": sp.simplify(nlse_imaginary_residual - continuity / (2 * rho)) == 0,
        "phase_gradient_is_euler_equation_with_quantum_pressure": all(
            value == 0 for value in euler_residual
        ),
        "space_dimension_is_two_transverse_coordinates": len(velocity) == 2,
        "model_has_no_viscosity_parameter_or_laplacian_velocity_term":
            not any(symbol.name in {"nu", "viscosity"} for symbol in phase_eq.free_symbols),
    }
    return {
        "schema_version": 1,
        "scope": "Symbolic Madelung identities for a 2D paraxial NLSE; not Maxwell derivation or Navier-Stokes validation",
        "equation": "i*d_z psi = -(1/(2*m))*Delta_perp psi + (g*|psi|^2+V)*psi",
        "variables": {"rho": "|psi|^2", "theta": "phase(psi)", "v": "grad_perp(theta)/m"},
        "identities": {
            "continuity": "d_z rho + div_perp(rho*v) = 0",
            "momentum": "d_z v + (v.grad_perp)v = -(g/m)grad_perp(rho) -(1/m)grad_perp(V) +(1/(2*m^2))*grad_perp(Delta_perp(sqrt(rho))/sqrt(rho))",
        },
        "checks": checks,
        "nlse_residual_decomposition": {
            "real_part": "- phase equation",
            "imaginary_part": "continuity residual / (2*rho)",
        },
        "euler_residual": [str(value) for value in euler_residual],
        "limitations": [
            "The paraxial NLSE is assumed; its derivation from Maxwell equations is outside this symbolic check.",
            "Madelung variables require nonzero amplitude and a smooth phase chart; phase singularities need separate treatment.",
            "The check does not model molecular dynamics, photon shot noise, or constitutive viscosity.",
        ],
        "success": all(checks.values()),
    }


def main():
    result = audit()
    output = Path("evidence/tests/optical-madelung.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    if not result["success"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
