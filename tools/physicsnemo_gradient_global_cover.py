"""Adaptive Arb enclosure of the frozen PhysicsNeMo gradient-error maximum.

This is a finite interval cover, not a formally verified proof kernel or a
preregistered acceptance gate. The cover remains useful when its global upper
bound is too loose: every reported upper bound still comes from Arb enclosures
over boxes that partition a full periodic fundamental domain.
"""
from __future__ import annotations

import heapq
import io
import itertools
import json
import math
import sys
import tarfile
import time
from pathlib import Path

from flint import arb, ctx

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.physicsnemo_arb_interval_probe import (
    gradient_error_enclosure,
    quadratic_taylor_gradient_error_enclosure,
)


DEFAULT_ARCHIVE = Path("evidence/physicsnemo-study-v1/n64-nt17.tar.gz")
DEFAULT_POINT = Path("evidence/tests/physicsnemo-local-interval-probe-2026-10-01.json")


def _outward_float(value, *, upper):
    """Convert an Arb enclosure endpoint to a conservative binary float."""
    endpoint = value.upper() if upper else value.lower()
    rounded = float(endpoint)
    return math.nextafter(rounded, math.inf if upper else -math.inf)


def frobenius_upper(gradient_box):
    """Rigorous float upper bound for the Frobenius norm of interval entries."""
    squares = sum((entry.abs_upper() ** 2 for row in gradient_box for entry in row), arb(0))
    return _outward_float(squares.sqrt(), upper=True)


def frobenius_lower(gradient_box):
    """Rigorous float lower bound for every matrix enclosed by entries."""
    squares = sum((entry.abs_lower() ** 2 for row in gradient_box for entry in row), arb(0))
    return max(0.0, _outward_float(squares.sqrt(), upper=False))


def split_box(box):
    """Bisect the widest coordinate; children share their exact float boundary."""
    widths = [hi - lo for lo, hi in box]
    axis = max(range(3), key=widths.__getitem__)
    lo, hi = box[axis]
    mid = lo + (hi - lo) / 2
    left, right = list(box), list(box)
    left[axis], right[axis] = (lo, mid), (mid, hi)
    return tuple(left), tuple(right)


def _load_model(archive):
    import torch

    raw = archive.read_bytes()
    with tarfile.open(fileobj=io.BytesIO(raw), mode="r:gz") as tar:
        params = json.load(tar.extractfile("parameters.json"))
        weights_bytes = tar.extractfile("weights.pt").read()
    state = torch.load(io.BytesIO(weights_bytes), map_location="cpu", weights_only=True)
    hidden = [
        (state[f"layers.{i}.linear.weight"].numpy().tolist(),
         state[f"layers.{i}.linear.bias"].numpy().tolist())
        for i in range(3)
    ]
    output = (
        state["final_layer.linear.weight"][:3].numpy().tolist(),
        state["final_layer.linear.bias"][:3].numpy().tolist(),
    )
    return raw, weights_bytes, params, hidden, output


def certify_cover(archive=DEFAULT_ARCHIVE, candidate=DEFAULT_POINT, *,
                  initial_divisions=4, max_boxes=8192, relative_gap=0.10,
                  precision=40, taylor_width_threshold=0.1):
    if initial_divisions < 1 or max_boxes < initial_divisions**3:
        raise ValueError("max_boxes must accommodate the initial uniform cover")
    if relative_gap <= 0 or precision < 20 or taylor_width_threshold <= 0:
        raise ValueError("relative_gap must be positive and precision at least 20 dps")

    archive, candidate = Path(archive), Path(candidate)
    raw, weight_bytes, params, hidden, output = _load_model(archive)
    candidate_data = json.loads(candidate.read_text())
    point = tuple(float(v) for v in candidate_data["candidate_point_from_saved_evaluation_grid"])
    time_value, sigma, endpoint = params["end"], params["sigma"], params["end"]

    old_prec = ctx.prec
    ctx.dps = precision
    started = time.monotonic()
    try:
        point_gradient = gradient_error_enclosure(
            hidden, output, [(v, v) for v in point], time=time_value,
            sigma=sigma, endpoint=endpoint, dps=precision,
        )
        lower = frobenius_lower(point_gradient)
        if lower <= 0:
            raise ArithmeticError("candidate did not yield a positive norm lower bound")

        # pi < 22/7 < 16/5; the exact binary float 3.2 is slightly larger
        # than 16/5. Periodicity therefore makes this cube cover the torus.
        edge = float(16 / 5)
        boundaries = [-edge + (2 * edge) * i / initial_divisions
                      for i in range(initial_divisions + 1)]
        initial = []
        method_counts = {"direct_interval": 0, "quadratic_taylor": 0}

        def enclose(box):
            width = max(hi - lo for lo, hi in box)
            method = (quadratic_taylor_gradient_error_enclosure
                      if width <= taylor_width_threshold else gradient_error_enclosure)
            name = "quadratic_taylor" if method is quadratic_taylor_gradient_error_enclosure else "direct_interval"
            method_counts[name] += 1
            return method(
                hidden, output, box, time=time_value, sigma=sigma,
                endpoint=endpoint, dps=precision,
            )

        for cell in itertools.product(range(initial_divisions), repeat=3):
            box = tuple((boundaries[i], boundaries[i + 1]) for i in cell)
            enclosure = enclose(box)
            upper = frobenius_upper(enclosure)
            initial.append((box, upper))

        # The heap is only a refinement heuristic. All stopping/reporting
        # comparisons below scan every leaf's outward-rounded upper bound.
        heap = [(-upper, index) for index, (_, upper) in enumerate(initial)]
        heapq.heapify(heap)
        leaves = {index: item for index, item in enumerate(initial)}
        next_id = len(leaves)
        evaluations = len(leaves) + 1
        gap_target = math.nextafter(lower * (1 + relative_gap), math.inf)
        while len(leaves) < max_boxes:
            global_upper = max(upper for _, upper in leaves.values())
            if global_upper <= gap_target:
                break
            while heap:
                _, parent_id = heapq.heappop(heap)
                if parent_id in leaves:
                    break
            else:
                raise AssertionError("refinement queue lost all live leaves")
            parent_box, _ = leaves.pop(parent_id)
            for child_box in split_box(parent_box):
                enclosure = enclose(child_box)
                upper = frobenius_upper(enclosure)
                leaves[next_id] = (child_box, upper)
                heapq.heappush(heap, (-upper, next_id))
                next_id += 1
                evaluations += 1

        global_upper = max(upper for _, upper in leaves.values())
        success_gap = global_upper <= gap_target
        return {
            "scope": "Adaptive Arb enclosure of the continuous Frobenius norm of the PhysicsNeMo spatial gradient error over one full periodic domain. Not a preregistered quality gate and not a formally verified proof kernel.",
            "archive": str(archive),
            "archive_sha256": __import__("hashlib").sha256(raw).hexdigest(),
            "checkpoint_sha256": __import__("hashlib").sha256(weight_bytes).hexdigest(),
            "candidate_source": str(candidate),
            "candidate_point": point,
            "candidate_point_lower_bound": lower,
            "global_upper_bound": global_upper,
            "relative_gap_target": relative_gap,
            "achieved_upper_to_lower_ratio": global_upper / lower,
            "cover_domain": [[-edge, edge]] * 3,
            "periodic_cover_justification": "The exact interval [-16/5,16/5] contains [-pi,pi] because pi<22/7<16/5; each field input is 2pi-periodic.",
            "initial_uniform_divisions_per_axis": initial_divisions,
            "leaf_box_count": len(leaves),
            "interval_evaluations": evaluations,
            "precision_decimal_digits": precision,
            "small_box_taylor_width_threshold": taylor_width_threshold,
            "enclosure_method_counts": method_counts,
            "elapsed_seconds": time.monotonic() - started,
            "result": "GAP_TARGET_MET" if success_gap else "CERTIFIED_ENCLOSURE_GAP_REMAINS",
            "all_leaves_cover_domain": True,
            "limitations": [
                "The candidate lower bound is at one fixed point; it is not claimed to be the global maximum.",
                "Arb interval arithmetic is not an independently verified proof kernel.",
                "No PhysicsNeMo acceptance threshold was preregistered, so this does not change the quality verdict.",
            ],
        }
    finally:
        ctx.prec = old_prec


def main():
    result = certify_cover()
    path = Path("evidence/tests/physicsnemo-gradient-global-cover-2026-10-01.json")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
