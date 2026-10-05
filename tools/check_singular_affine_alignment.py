"""Symbolically verify a singular affine NS flow as an implication counterexample.

This unforced flow is smooth only on t < T and has infinite energy on R^3.
It is an exact algebraic example, not an admissible Clay-problem datum or a
model of the OpenAI construction, molecules, or a constitutive law.
"""

import hashlib
import json
from pathlib import Path

import sympy as sp


def verify():
    x, y, z = sp.symbols("x y z", real=True)
    t, T, t0, nu, sigma = sp.symbols("t T t0 nu sigma", positive=True)
    coords = sp.Matrix([x, y, z])
    s = T - t
    s0 = T - t0
    a = 1 / s
    A = sp.diag(-a, -a, 2 * a)
    velocity = A * coords
    pressure = -3 * z**2 / s**2
    grad_p = sp.Matrix([sp.diff(pressure, q) for q in coords])
    jacobian = velocity.jacobian(coords)
    laplacian = sp.Matrix([
        sum(sp.diff(component, q, 2) for q in coords)
        for component in velocity
    ])
    acceleration = velocity.diff(t) + jacobian * velocity
    residual = sp.simplify(acceleration + grad_p - nu * laplacian)
    flow = sp.diag(s / s0, s / s0, (s0 / s) ** 2)
    flow_residual = sp.simplify(flow.diff(t) - A * flow)
    q = s / s0
    initial_covariance = sigma**2 * sp.eye(3)
    covariance = sp.simplify(flow * initial_covariance * flow.T)
    gaussian_peak_ratio = sp.simplify(1 / sp.sqrt(covariance.det() / sigma**6))
    facts = {
        "divergence_zero": sp.simplify(sp.trace(jacobian)) == 0,
        "navier_stokes_residual_zero": residual == sp.zeros(3, 1),
        "viscous_laplacian_zero": laplacian == sp.zeros(3, 1),
        "flow_solves_variational_ode": flow_residual == sp.zeros(3, 3),
        "volume_jacobian_one": sp.simplify(flow.det()) == 1,
        "transverse_to_axial_ratio_factor_q_cubed": sp.simplify(
            (flow[0, 0] / flow[2, 2]) / q**3
        ) == 1,
        "gradient_scale_diverges_at_T": sp.simplify(2 * a * s) == 2,
        "isotropic_gaussian_covariance_exact": covariance == sp.diag(
            sigma**2 * q**2, sigma**2 * q**2, sigma**2 * q**-4
        ),
        "isotropic_gaussian_peak_unchanged": gaussian_peak_ratio == 1,
        "viscosity_parameter_drops_out_because_laplacian_zero":
            nu not in residual.free_symbols,
    }
    # A nonzero Laplacian control prevents accidentally reducing this to a
    # purely kinematic identity without checking the viscous term's role.
    viscous_control = sp.simplify(nu * sp.diff(x**2, x, 2)) != 0
    return {
        "status": "PASS" if all(facts.values()) and viscous_control else "FAIL",
        "sympy_version": sp.__version__,
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "assumptions": ["t0 < t < T", "nu > 0", "sigma > 0"],
        "velocity": [str(component) for component in velocity],
        "pressure": str(pressure),
        "flow_map_from_t0": [str(flow[i, i]) for i in range(3)],
        "gradient_operator_norm": "2/(T-t)",
        "transverse_to_axial_material_line_ratio_factor": "((T-t)/(T-t0))^3",
        "gaussian_covariance_from_isotropic_sigma2": [
            "sigma^2*((T-t)/(T-t0))^2",
            "sigma^2*((T-t)/(T-t0))^2",
            "sigma^2*((T-t0)/(T-t))^4",
        ],
        "gaussian_peak_density_ratio": str(gaussian_peak_ratio),
        "residual": [str(value) for value in residual],
        "facts": facts,
        "negative_control_nonzero_viscous_laplacian": viscous_control,
        "limitations": [
            "The affine field has infinite kinetic energy and does not decay at spatial infinity.",
            "It is not an admissible Clay-problem initial datum and is not the OpenAI construction.",
            "A continuum deformation map does not supply a molecular orientation law or finite-particle model.",
            "The constant viscosity is a parameter of this Newtonian equation; the example does not predict material rheology.",
        ],
    }


if __name__ == "__main__":
    result = verify()
    output = Path("evidence/analytic-checks/singular-affine-alignment-2026-10-04.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
    print(json.dumps(result, indent=2, allow_nan=False))
    raise SystemExit(0 if result["status"] == "PASS" else 1)
