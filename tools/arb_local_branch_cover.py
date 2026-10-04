"""Deterministic adaptive axis-bisection cover for bounded local probes."""

from __future__ import annotations

import heapq
import math
from collections.abc import Callable, Sequence

Box = tuple[tuple[float, float], tuple[float, float], tuple[float, float]]


def adaptive_axis_bisect_cover(
    box: Sequence[Sequence[float]],
    upper_bound: Callable[[Box], float],
    *,
    target: float,
    max_evaluations: int,
) -> dict:
    """Bisect the current worst-upper-bound cell while preserving a full cover.

    The callback must return a valid upper bound for the entire supplied box.
    This routine checks its shape and finiteness, but cannot establish that
    mathematical property itself.
    """
    if len(box) != 3:
        raise ValueError("box must have three coordinate intervals")
    normalized = tuple(tuple(float(v) for v in interval) for interval in box)
    if any(len(interval) != 2 or not all(math.isfinite(v) for v in interval)
           or interval[0] >= interval[1] for interval in normalized):
        raise ValueError("each box interval must be finite and increasing")
    if not math.isfinite(target):
        raise ValueError("target must be finite")
    if not isinstance(max_evaluations, int) or max_evaluations < 1:
        raise ValueError("max_evaluations must be a positive integer")

    next_id = 0
    evaluations = 0
    leaves: dict[int, tuple[Box, float]] = {}
    heap: list[tuple[float, int]] = []

    def evaluate(cell: Box) -> int:
        nonlocal next_id, evaluations
        bound = float(upper_bound(cell))
        if not math.isfinite(bound) or bound < 0:
            raise ValueError("upper_bound must return a finite nonnegative value")
        cell_id = next_id
        next_id += 1
        evaluations += 1
        leaves[cell_id] = (cell, bound)
        heapq.heappush(heap, (-bound, cell_id))
        return cell_id

    evaluate(normalized)  # type: ignore[arg-type]
    stop_reason = "target_met"
    while -heap[0][0] > target:
        if evaluations + 2 > max_evaluations:
            stop_reason = "evaluation_budget"
            break
        _, cell_id = heapq.heappop(heap)
        cell, _ = leaves.pop(cell_id)
        axis = max(range(3), key=lambda i: (cell[i][1] - cell[i][0], -i))
        lo, hi = cell[axis]
        mid = lo + (hi - lo) / 2.0
        if mid <= lo or mid >= hi:
            leaves[cell_id] = (cell, -heap[0][0] if heap else 0.0)
            stop_reason = "stagnated"
            break
        left = list(cell)
        right = list(cell)
        left[axis] = (lo, mid)
        right[axis] = (mid, hi)
        evaluate(tuple(left))  # type: ignore[arg-type]
        evaluate(tuple(right))  # type: ignore[arg-type]

    ordered = [
        {"box": [list(interval) for interval in cell], "upper": bound}
        for _, (cell, bound) in sorted(leaves.items())
    ]
    maximum = max(item["upper"] for item in ordered)
    target_met = maximum <= target
    if target_met:
        stop_reason = "target_met"
    return {
        "target": target,
        "target_met": target_met,
        "stop_reason": stop_reason,
        "evaluation_count": evaluations,
        "leaf_count": len(ordered),
        "maximum_leaf_upper": maximum,
        "leaves": ordered,
    }
