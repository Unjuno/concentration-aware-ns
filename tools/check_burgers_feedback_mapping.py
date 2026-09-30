#!/usr/bin/env python3
"""Numerically cross-check the algebraic Burgers-feedback parametrization.

This is an arithmetic regression check of a stated reduced model, not a PDE
solver, proof of blow-up, or validation of OpenAI's construction.
"""

from __future__ import annotations

import json
import math
from pathlib import Path


def close(a: float, b: float, *, tol: float = 2e-13) -> bool:
    return math.isclose(a, b, rel_tol=tol, abs_tol=tol)


def main() -> None:
    checks: list[dict[str, float]] = []
    for nu, kappa, mu in [
        (1.0, 1.0, 1.25),
        (1.0, 1.0, 2.0),
        (1.0, 1.0, 7.0),
        (0.3, 2.5, 1.5),
        (2.0, 0.4, 4.0),
    ]:
        # Invert mu = kappa*Gamma/(kappa*Gamma - 4*pi*nu).
        gamma = 4.0 * math.pi * nu * mu / (kappa * (mu - 1.0))
        threshold = kappa * gamma > 4.0 * math.pi * nu
        mu_recovered = kappa * gamma / (kappa * gamma - 4.0 * math.pi * nu)
        q_slope = kappa * gamma / math.pi - 4.0 * nu
        q_coefficient = 4.0 * nu / (mu_recovered - 1.0)
        strain_coefficient = kappa * gamma / (math.pi * q_coefficient)
        vorticity_coefficient = gamma / (math.pi * q_coefficient)

        assert threshold and close(mu_recovered, mu)
        assert close(q_slope, q_coefficient)
        assert close(strain_coefficient, mu)
        assert close(vorticity_coefficient, mu / kappa)

        # Check the explicit shrinking width against its affine ODE at samples.
        for tau in (0.9, 0.25, 1e-3):
            q = q_coefficient * tau
            qdot = -q_coefficient
            rhs = 4.0 * nu - strain_coefficient / tau * q
            assert close(qdot, rhs)
        checks.append(
            {
                "nu": nu,
                "kappa": kappa,
                "mu_input": mu,
                "Gamma": gamma,
                "mu_recovered": mu_recovered,
                "q_over_T_minus_t": q_coefficient,
                "a_times_T_minus_t": strain_coefficient,
                "W_times_T_minus_t": vorticity_coefficient,
                "threshold_kappa_Gamma_gt_4_pi_nu": float(threshold),
            }
        )

    threshold_checks: list[dict[str, float]] = []
    nu, kappa = 1.25, 0.8
    for circulation_ratio in (0.0, 0.5, 1.0, 1.1):
        # circulation_ratio = kappa*Gamma/(4*pi*nu)
        gamma = circulation_ratio * 4.0 * math.pi * nu / kappa
        qdot_raw = 4.0 * nu - kappa * gamma / math.pi
        expected_sign = 1 if circulation_ratio < 1 else -1 if circulation_ratio > 1 else 0
        assert (
            (qdot_raw > 0 and expected_sign == 1)
            or (qdot_raw < 0 and expected_sign == -1)
            or (close(qdot_raw, 0.0) and expected_sign == 0)
        )
        qdot = 0.0 if close(qdot_raw, 0.0) else qdot_raw
        threshold_checks.append(
            {
                "nu": nu,
                "kappa": kappa,
                "kappa_Gamma_over_4_pi_nu": circulation_ratio,
                "qdot": qdot,
            }
        )

    # OpenAI core comparison is an exponent comparison only: if its stated
    # profile coefficient is nonzero, a/W is proportional to tau**h.
    for h in (1e-3, 0.01, 0.1):
        ratio_at_tau = (1e-6) ** h
        assert ratio_at_tau < 1.0

    output = {
        "status": "PASS_ARITHMETIC_ONLY",
        "model": "q_dot=4*nu-a*q; W=Gamma/(pi*q); a=kappa*W",
        "derived": {
            "threshold": "kappa*Gamma > 4*pi*nu",
            "mu": "kappa*Gamma/(kappa*Gamma-4*pi*nu) > 1",
            "q": "4*nu*(T-t)/(mu-1)",
            "a": "mu/(T-t)",
            "W_peak": "mu/(kappa*(T-t))",
            "openai_core_pointwise_a_over_W": "constant* tau**h when f(0,eta_*) != 0",
            "global_peak_comparison": "not evaluated; axis path is not proved to attain spatial peak",
        },
        "cases": checks,
        "threshold_cases": threshold_checks,
        "limitations": [
            "floating-point algebra check, not a formal proof",
            "does not solve or validate the Navier-Stokes PDE",
            "does not establish finite-energy blow-up or molecular consequences",
            "OpenAI pointwise exponent comparison does not identify the global vorticity maximum",
        ],
    }
    out = Path("evidence/tests/burgers-feedback-mapping.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(f"{output['status']}: wrote {out}")


if __name__ == "__main__":
    main()
