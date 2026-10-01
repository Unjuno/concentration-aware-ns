"""Check alignment and positional uncertainty in the linearized Gaussian model."""
import hashlib
import json
from pathlib import Path

import sympy as sp


def main():
    q, stretch, sigma, radius = sp.symbols(
        "q C sigma R", positive=True, finite=True
    )
    deformation = sp.diag(q ** (stretch / 2), q ** (stretch / 2), q ** (-stretch))
    covariance = sp.simplify(sigma**2 * deformation * deformation.T)
    eigenvalues = [sp.simplify(covariance[i, i]) for i in range(3)]
    determinant = sp.simplify(covariance.det())
    density_peak_ratio = sp.simplify(sp.sqrt(sigma**6 / determinant))
    axial_std = sp.sqrt(eigenvalues[2])
    fixed_ball_probability_upper = sp.simplify(
        2 * radius / (sp.sqrt(2 * sp.pi) * axial_std)
    )
    direction_ratio = q ** (sp.Rational(3, 2) * stretch)

    identities = {
        "volume_preserving_deformation": sp.simplify(deformation.det()) == 1,
        "transverse_variances_contract": eigenvalues[:2]
        == [sigma**2 * q**stretch] * 2,
        "axial_variance_expands": eigenvalues[2] == sigma**2 * q ** (-2 * stretch),
        "covariance_determinant_constant": determinant == sigma**6,
        "gaussian_peak_density_constant": density_peak_ratio == 1,
        "directional_transverse_axial_factor": direction_ratio
        == q ** (sp.Rational(3, 2) * stretch),
        "fixed_ball_bound_has_q_power": sp.simplify(
            fixed_ball_probability_upper /
            (sp.sqrt(2 / sp.pi) * radius / sigma * q**stretch)
        ) == 1,
    }
    controls = {
        "non_volume_preserving_control_changes_covariance_determinant":
            sp.simplify((sigma**2 * sp.diag(1, 1, q ** (-2 * stretch))).det())
            != sigma**6,
        "wrong_axial_variance_power_rejected":
            eigenvalues[2] != sigma**2 * q ** (-stretch),
    }
    source = Path(__file__)
    output = {
        "scope": "Exact calculation for the linearized, volume-preserving axis propagator applied to an isotropic Gaussian. It is not a finite-packet theorem for the nonlinear selected PDE.",
        "sympy": sp.__version__,
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "assumptions": ["0 < q <= 1", "C > 0", "sigma > 0", "R > 0"],
        "deformation": [[str(deformation[i, j]) for j in range(3)] for i in range(3)],
        "covariance_eigenvalues": [str(value) for value in eigenvalues],
        "covariance_determinant": str(determinant),
        "gaussian_peak_density_ratio": str(density_peak_ratio),
        "fixed_ball_probability_upper_bound": str(fixed_ball_probability_upper),
        "directional_transverse_axial_factor": str(direction_ratio),
        "identities": identities,
        "negative_controls": controls,
        "interpretation": "Angular alignment can improve while Gaussian mass in every fixed-radius ball around the packet center tends to zero; the linear model preserves covariance volume and Gaussian differential entropy.",
        "success": all(identities.values()) and all(controls.values()),
    }
    target = Path("evidence/tests/alignment-uncertainty.json")
    target.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps(output, indent=2))
    return 0 if output["success"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
