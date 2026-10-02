"""Exact finite cutoff-schedule extraction from certified rational jet bounds.

The arithmetic here is exact. The caller must independently certify that the
input C[j,m] values bound the source compact jet maxima and that h >= h_lower.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path


def _fraction(value, name):
    try:
        result = Fraction(str(value))
    except (ValueError, ZeroDivisionError) as exc:
        raise ValueError(f"{name} must be an exact rational string") from exc
    return result


def _meets_all_bounds(a, j, h_lower, bounds):
    """Check C*(1/a)^(h_lower*j) <= 2^-j by integer cross multiplication."""
    p, r = h_lower.numerator, h_lower.denominator
    exponent_numerator = p * j
    for m, c in bounds.items():
        n, d = c.numerator, c.denominator
        lhs = pow(a, exponent_numerator) * pow(d, r)
        rhs = pow(n, r) * pow(2, j * r)
        if lhs < rhs:
            return False
    return True


def _minimal_stage_scale(j, h_lower, bounds):
    lo, hi = 0, 1
    while not _meets_all_bounds(hi, j, h_lower, bounds):
        hi *= 2
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if _meets_all_bounds(mid, j, h_lower, bounds):
            hi = mid
        else:
            lo = mid
    return hi


def extract_schedule(data):
    if data.get("schema_version") != 1:
        raise ValueError("schema_version must be 1")
    if not data.get("bound_provenance", "").strip():
        raise ValueError("bound_provenance must identify the independent certificate")
    h_lower = _fraction(data.get("h_lower"), "h_lower")
    q_min = _fraction(data.get("q_min"), "q_min")
    if h_lower <= 0:
        raise ValueError("h_lower must be positive")
    if not 0 < q_min <= 1:
        raise ValueError("q_min must lie in (0,1]")
    B = int(data.get("initial_scale_lower_bound", 1))
    if B < 0:
        raise ValueError("initial_scale_lower_bound must be nonnegative")

    raw = data.get("coefficient_upper_bounds", {})
    if not isinstance(raw, dict) or not raw:
        raise ValueError("coefficient_upper_bounds must contain stage-indexed bounds")
    stages = {}
    for key, stage_data in raw.items():
        try:
            j = int(key)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"invalid stage index: {key}") from exc
        if str(j) != str(key) or j < 1:
            raise ValueError("stage indices must be canonical positive integers")
        if not isinstance(stage_data, dict):
            raise ValueError(f"stage {j} must map jet orders to rational bounds")
        expected = set(range(j + 3))
        try:
            found = {int(m) for m in stage_data}
        except (TypeError, ValueError) as exc:
            raise ValueError(f"stage {j} has an invalid jet-order key") from exc
        if any(str(int(m)) != str(m) for m in stage_data):
            raise ValueError(f"stage {j} jet-order keys must be canonical integers")
        if found != expected:
            raise ValueError(f"stage {j} requires jet orders 0..{j+2}")
        bounds = {int(m): _fraction(v, f"C[{j},{m}]")
                  for m, v in stage_data.items()}
        if any(c <= 0 for c in bounds.values()):
            raise ValueError(f"stage {j} bounds must be positive")
        stages[j] = bounds

    a_prev = max(1, B)
    schedule = [{"stage": 0, "stage_threshold": None,
                 "schedule_scale": a_prev, "reason": "initial lower bound"}]
    terminal_zero_from = None
    for j in range(1, max(stages) + 1):
        if j not in stages:
            raise ValueError(f"missing certified coefficient bounds for stage {j}")
        threshold = _minimal_stage_scale(j, h_lower, stages[j])
        a_j = max(threshold, 2 * a_prev)
        if not _meets_all_bounds(a_j, j, h_lower, stages[j]):
            raise AssertionError("exact stage-bound postcondition failed")
        row = {"stage": j, "stage_threshold": threshold,
               "schedule_scale": a_j,
               "doubling_verified": a_j >= 2 * a_prev,
               "all_jet_bounds_verified": True,
               "jet_order_count": len(stages[j])}
        schedule.append(row)
        a_prev = a_j
        if q_min * a_j > 1:
            terminal_zero_from = j
            break
    if terminal_zero_from is None:
        raise ValueError("provided bounds do not reach q_min cutoff; add more stages")

    return {
        "schema_version": 1,
        "scope": "Finite prefix of the OpenAI diagonal cutoff schedule, computed from caller-supplied rational upper bounds. Exact arithmetic verifies the schedule inequalities but does not certify the input bounds or h_lower.",
        "upstream_source_commit": "f9e8bc5b38b6e212696e8a30e3e91517af887bbd",
        "source_lemmas_reproduced": ["exists_admissibleScales", "DiagonalScale.exists_diagonal_scales"],
        "assumptions": {
            "h_lower": str(h_lower),
            "true_h_requirement": "h >= h_lower; must be certified independently",
            "q_min": str(q_min),
            "q_range": "q_min <= q <= 1",
            "coefficient_bounds": "each supplied C[j,m] is a certified positive upper bound for the compact template jet norm, for all active scales c in [0,1] and inner points in K",
            "bound_provenance": data["bound_provenance"],
            "initial_scale_lower_bound": B,
        },
        "verified_contract": {
            "stage_inequality": "C[j,m] * (1/a_j)^(h_lower*j) <= 2^(-j); hence the source absorption inequality holds for every q <= 1/a_j when h >= h_lower",
            "jet_orders_per_stage": "0 through j+2",
            "schedule_doubling": "a_(j+1) >= 2*a_j",
            "terminal_cutoff": "q_min*a_N > 1, so every stage j >= N is zero for every q >= q_min",
            "finite_prefix_includes_stages": f"0 through {terminal_zero_from - 1}",
        },
        "terminal_zero_from_stage": terminal_zero_from,
        "finite_prefix_last_stage": terminal_zero_from - 1,
        "schedule": schedule,
        "limitations": [
            "No compact derivative upper bounds for the selected OpenAI coefficients are currently extracted in this repository.",
            "The noncomputable selected coefficient functions and their compact jet maxima are not supplied by this tool.",
            "This creates a finite schedule only on q >= q_min; it does not provide a single finite approximation through q=0 or prove a Navier-Stokes numerical reproduction.",
        ],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    raw = args.input.read_bytes()
    data = json.loads(raw)
    result = extract_schedule(data)
    result["input_sha256"] = hashlib.sha256(raw).hexdigest()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({key: result[key] for key in
                      ("terminal_zero_from_stage", "finite_prefix_last_stage", "schedule")},
                     indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
