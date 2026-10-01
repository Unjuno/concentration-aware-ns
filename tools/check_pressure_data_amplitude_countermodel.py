#!/usr/bin/env python3
"""Symbolically check the generic-pressure countermodel in the provenance audit.

This checks exact integral and derivative identities. It is deliberately not a
model of the selected SchedulePressure or EntranceProfile construction.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import sympy as sp


def check() -> dict[str, object]:
    B, eta, y = sp.symbols("B eta y", positive=True, real=True)
    prefix_density = B**2 * sp.exp(y / 5)
    prefix_mass = sp.integrate(prefix_density, (y, -sp.oo, 0))
    tail_mass = sp.integrate(sp.Integer(2), (y, 1, 2))
    kernel_prefix = (1 + eta**2) ** -2
    kernel_tail = sp.Integer(1)

    pressure_from_parts = -sp.Rational(1, 2) * (
        prefix_mass * kernel_prefix + tail_mass * kernel_tail
    )
    expected_pressure = -1 - sp.Rational(5, 2) * B**2 / (1 + eta**2) ** 2
    assert sp.simplify(prefix_mass - 5 * B**2) == 0
    assert tail_mass == 2
    assert sp.simplify(pressure_from_parts - expected_pressure) == 0

    pressure_derivative = sp.factor(sp.diff(expected_pressure, eta))
    signed_derivative = sp.factor(eta * pressure_derivative)
    assert sp.simplify(pressure_derivative - 10 * B**2 * eta / (1 + eta**2) ** 3) == 0
    assert sp.simplify(signed_derivative - 10 * B**2 * eta**2 / (1 + eta**2) ** 3) == 0
    assert sp.simplify(expected_pressure + 1) == -sp.Rational(5, 2) * B**2 / (1 + eta**2) ** 2

    # B=1 is one explicit sub-threshold witness; the identities above hold for
    # every positive B. Positivity of the displayed factors gives the signs.
    witness_pressure = sp.simplify(expected_pressure.subs(B, 1))
    witness_signed_derivative = sp.simplify(signed_derivative.subs(B, 1))
    return {
        "status": "PASS",
        "tool": "SymPy exact symbolic identities",
        "sympy_version": sp.__version__,
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "prefix_mass": str(prefix_mass),
        "tail_mass": str(tail_mass),
        "pressure": str(expected_pressure),
        "pressure_derivative": str(pressure_derivative),
        "eta_times_pressure_derivative": str(signed_derivative),
        "subthreshold_witness_B": "1",
        "witness_pressure": str(witness_pressure),
        "witness_eta_times_pressure_derivative": str(witness_signed_derivative),
        "scope": (
            "Exact algebra for generic PressureDatum.Admissible data only; "
            "does not instantiate the selected SchedulePressure, "
            "CoefficientProfile, EntranceProfile, or actualProfile."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output", type=Path,
        default=Path("evidence/tests/pressure-data-amplitude-countermodel-2026-10-02.json"),
    )
    args = parser.parse_args()
    text = json.dumps(check(), indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
