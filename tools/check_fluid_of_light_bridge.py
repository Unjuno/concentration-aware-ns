"""Symbolically check the 1-D Madelung bridge for a defocusing optical NLSE.

This is an equation-identity check, not an optical experiment or a model of
the OpenAI Navier--Stokes construction.
"""

import hashlib
import json
from pathlib import Path

import sympy as sp


def verify():
    x, z = sp.symbols("x z", real=True)
    k, g = sp.symbols("k g", positive=True)
    rho = sp.Function("rho")(x, z)
    phi = sp.Function("phi")(x, z)
    amplitude = sp.sqrt(rho)
    dispersion = 1 / (2 * k)

    # Divide i*psi_z + D*psi_xx - g*|psi|^2*psi by
    # psi=sqrt(rho)*exp(i*phi), and separate its real/imaginary parts.
    real_part = -sp.diff(phi, z) + dispersion * (
        sp.diff(amplitude, x, 2) / amplitude - sp.diff(phi, x) ** 2
    ) - g * rho
    imaginary_part = (
        sp.diff(amplitude, z) / amplitude
        + dispersion * (
            2 * sp.diff(amplitude, x) / amplitude * sp.diff(phi, x)
            + sp.diff(phi, x, 2)
        )
    )
    continuity_residual = sp.simplify(
        sp.diff(rho, z)
        + sp.diff(rho * sp.diff(phi, x) / k, x)
    )
    bernoulli = (
        sp.diff(phi, z)
        + sp.diff(phi, x) ** 2 / (2 * k)
        + g * rho
        - sp.diff(amplitude, x, 2) / (2 * k * amplitude)
    )
    velocity = sp.diff(phi, x) / k
    quantum_pressure = sp.diff(amplitude, x, 2) / amplitude
    euler_residual = sp.simplify(
        sp.diff(velocity, z)
        + velocity * sp.diff(velocity, x)
        + sp.diff(g * rho / k - quantum_pressure / (2 * k**2), x)
    )
    identities = {
        "nlse_real_part_equals_negative_bernoulli": sp.simplify(real_part + bernoulli) == 0,
        "nlse_imaginary_part_gives_continuity": sp.simplify(
            2 * rho * imaginary_part - continuity_residual
        ) == 0,
        "bernoulli_gradient_equals_euler_residual": sp.simplify(
            euler_residual - sp.diff(bernoulli, x) / k
        ) == 0,
        "effective_velocity_is_phase_gradient": sp.simplify(
            velocity - sp.diff(phi, x) / k
        ) == 0,
    }
    return {
        "status": "PASS" if all(identities.values()) else "FAIL",
        "checker": "tools/check_fluid_of_light_bridge.py",
        "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "sympy_version": sp.__version__,
        "equation": "i*psi_z + (1/(2*k))*psi_xx - g*|psi|^2*psi = 0",
        "madelung_variables": "psi=sqrt(rho)*exp(i*phi); v=phi_x/k",
        "continuity_equation": "rho_z + (rho*v)_x = 0",
        "phase_equation": "phi_z + phi_x^2/(2*k) + g*rho - (1/(2*k))*sqrt(rho)_xx/sqrt(rho) = 0",
        "velocity_equation": "v_z + v*v_x = -(g/k)*rho_x + (1/(2*k^2))*d_x(sqrt(rho)_xx/sqrt(rho))",
        "viscous_laplacian_term_present": False,
        "identities": identities,
        "assumptions": ["rho>0 on the patch considered", "smooth envelope", "paraxial NLSE regime"],
        "scope": "Exact 1-D amplitude-phase identity for one conservative optical NLSE convention. No photon molecular positions, incompressible 3-D Navier-Stokes equivalence, viscous closure, OpenAI-profile mapping, or physical transition is established.",
    }


if __name__ == "__main__":
    result = verify()
    output = Path("evidence/analytic-checks/fluid-of-light-hydrodynamic-bridge-2026-10-04.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
    print(json.dumps(result, indent=2, allow_nan=False))
    raise SystemExit(0 if result["status"] == "PASS" else 1)
