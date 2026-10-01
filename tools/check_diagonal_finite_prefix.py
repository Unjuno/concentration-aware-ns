"""Counterexample to exchanging a fixed-prefix limit with a growing cutoff sum.

This is a generic logic audit, not a model of the OpenAI construction.
"""
import json
import math
from pathlib import Path


def _eta(x):
    return math.exp(-1.0 / x) if x > 0 else 0.0


def cutoff(x):
    """C-infinity cutoff: 1 on x<=1, transitions, and 0 on x>=2."""
    if x <= 1:
        return 1.0
    if x >= 2:
        return 0.0
    return _eta(2 - x) / (_eta(2 - x) + _eta(x - 1))


def stage(j, q):
    return q * cutoff(j * q)


def diagonal_sum(q):
    return math.fsum(stage(j, q) for j in range(1, math.ceil(2 / q)))


def audit(ns=(8, 16, 32, 64, 128, 256, 512)):
    rows = []
    for n in ns:
        q = 1 / n
        total = diagonal_sum(q)
        rows.append({"n": n, "q": q, "active_stage_count_bound": math.ceil(2 / q),
                     "diagonal_sum": total, "exact_lower_bound": 1.0,
                     "exact_upper_bound": 2.0})
    fixed_prefix = []
    for j in (1, 2, 8, 32):
        fixed_prefix.append({"stage": j,
                             "values": [stage(j, 1 / n) for n in (64, 128, 256, 512)]})
    result = {
        "scope": "Generic smooth counterexample to inferring a full growing-cutoff-sum limit from decay of each fixed finite prefix. It is not a model or counterexample to the pinned OpenAI field.",
        "schedule": "a(j)=j, diverging",
        "stage_term": "q * chi(j*q)",
        "cutoff": "C-infinity chi=1 on (-infinity,1], transitions on (1,2), and 0 on [2,infinity)",
        "fixed_prefix_limit": "for each fixed j, q*chi(j*q)=q -> 0 as q -> 0",
        "growing_sum": "S(q)=sum_{j>=1} q*chi(j*q); support makes it finite for each q>0",
        "diagonal_subsequence": "q=1/n: the first n terms equal 1/n, hence S(1/n)>=1; at most 2n terms are nonzero, hence S(1/n)<=2",
        "rows": rows,
        "fixed_prefix_samples": fixed_prefix,
        "checks": {
            "each_diagonal_sum_respects_exact_bounds": all(
                1 <= row["diagonal_sum"] <= 2 for row in rows),
            "fixed_stage_samples_decay": all(
                vals["values"][-1] < vals["values"][0]
                for vals in fixed_prefix),
            "growing_sum_does_not_tend_to_zero_on_subsequence": all(
                row["diagonal_sum"] >= 1 for row in rows),
        },
        "interpretation": "Pointwise decay of every fixed stage plus a diverging cutoff schedule does not by itself justify exchanging the limit with the growing sum. A construction-specific uniform summability or tail estimate is needed.",
    }
    result["success"] = all(result["checks"].values())
    Path("evidence/tests/diagonal-finite-prefix.json").write_text(
        json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    return result


if __name__ == "__main__":
    raise SystemExit(0 if audit()["success"] else 1)
