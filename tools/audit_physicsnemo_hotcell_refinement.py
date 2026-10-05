"""Refine the worst single cell from the frozen n16 PhysicsNeMo cover."""

import argparse
import hashlib
import io
import json
import math
import platform
import tarfile
import time
from pathlib import Path

import torch
from flint import __version__ as flint_version
from flint import ctx

from tools.arb_local_branch_cover import adaptive_axis_bisect_cover
from tools.audit_physicsnemo_arb_interval_probe import _frob_upper
from tools.physicsnemo_arb_interval_probe import centered_gradient_error_enclosure


DEFAULT_ARCHIVE = Path("evidence/physicsnemo-study-v1/n64-nt17.tar.gz")
DEFAULT_PARENT_EVIDENCE = Path("evidence/tests/physicsnemo-centered-domain-cover-n16.json")


def _sha(data):
    return hashlib.sha256(data).hexdigest()


def audit(archive=DEFAULT_ARCHIVE, parent_evidence=DEFAULT_PARENT_EVIDENCE,
          budgets=(129, 513, 2049, 8193), target=0.26, dps=30):
    archive = Path(archive)
    parent_evidence = Path(parent_evidence)
    raw = archive.read_bytes()
    with tarfile.open(fileobj=io.BytesIO(raw), mode="r:gz") as tar:
        params = json.load(tar.extractfile("parameters.json"))
        weights_bytes = tar.extractfile("weights.pt").read()
    state = torch.load(io.BytesIO(weights_bytes), map_location="cpu", weights_only=True)
    hidden = [
        (state[f"layers.{layer}.linear.weight"].numpy().tolist(),
         state[f"layers.{layer}.linear.bias"].numpy().tolist())
        for layer in range(3)
    ]
    output = (
        state["final_layer.linear.weight"][:3].numpy().tolist(),
        state["final_layer.linear.bias"][:3].numpy().tolist(),
    )
    cover_evidence = json.loads(parent_evidence.read_text())
    source_case = cover_evidence["divisions"][0]
    parent = source_case["worst_cell_decomposition"]["box"]
    old_prec = ctx.prec
    ctx.dps = dps
    rows = []
    final_cover = None
    started_all = time.perf_counter()
    try:
        for budget in budgets:
            started = time.perf_counter()

            def cell_upper(box):
                enclosure = centered_gradient_error_enclosure(
                    hidden, output, box, time=params["end"],
                    endpoint=params["end"], sigma=params["sigma"], dps=dps,
                )
                return _frob_upper(enclosure)

            result = adaptive_axis_bisect_cover(
                parent, cell_upper, target=target, max_evaluations=budget,
            )
            result["elapsed_seconds"] = time.perf_counter() - started
            result["parent_cell"] = parent
            result["evaluation_scope"] = "one frozen worst cell only; no claim about remaining domain cells"
            rows.append({key: value for key, value in result.items() if key != "leaves"})
            final_cover = result
    finally:
        ctx.prec = old_prec

    parent_volume = math.prod(hi - lo for lo, hi in parent)
    leaf_volumes = [math.prod(hi - lo for lo, hi in leaf["box"])
                    for leaf in final_cover["leaves"]]
    covered_volume = math.fsum(leaf_volumes)
    return {
        "scope": "Adaptive Arb mean-value refinement of the single worst cell in the 16^3 cover of frozen n64-nt17; this is not a complete periodic-domain certificate.",
        "archive": archive.name,
        "archive_sha256": _sha(raw),
        "checkpoint_sha256": _sha(weights_bytes),
        "parent_cover_evidence": parent_evidence.name,
        "parent_box": parent,
        "parent_frobenius_upper": source_case["max_centered_cell_frobenius_upper"],
        "target_frobenius_upper": target,
        "target_scope": "exploratory comparator only; not a preregistered acceptance threshold",
        "interval_decimal_precision": dps,
        "budget_sweep": rows,
        "final_leaf_cover": {
            "evaluation_count": final_cover["evaluation_count"],
            "leaf_count": final_cover["leaf_count"],
            "maximum_leaf_upper": final_cover["maximum_leaf_upper"],
            "target_met": final_cover["target_met"],
            "parent_volume": parent_volume,
            "sum_leaf_volumes": covered_volume,
            "volume_difference": abs(parent_volume - covered_volume),
            "leaves": final_cover["leaves"],
        },
        "wall_seconds_all_budgets": time.perf_counter() - started_all,
        "environment": {
            "python": platform.python_version(),
            "python_flint": flint_version,
            "torch": torch.__version__,
        },
        "limitations": [
            "This partitions and encloses only one of the 4,096 parent cells; all other domain cells retain their previous bounds.",
            "The exploratory 0.26 comparator is not a PhysicsNeMo quality threshold.",
            "Arb/FLINT arithmetic is not independently proof-kernel verified here.",
        ],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--archive", type=Path, default=DEFAULT_ARCHIVE)
    parser.add_argument("--parent-evidence", type=Path, default=DEFAULT_PARENT_EVIDENCE)
    parser.add_argument("--budgets", type=int, nargs="+", default=[129, 513, 2049, 8193])
    parser.add_argument("--target", type=float, default=0.26)
    parser.add_argument("--dps", type=int, default=30)
    parser.add_argument("--output", type=Path,
                        default=Path("evidence/tests/physicsnemo-hotcell-refinement-2026-10-01.json"))
    args = parser.parse_args()
    result = audit(args.archive, args.parent_evidence, tuple(args.budgets),
                   args.target, args.dps)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({
        "output": str(args.output),
        "budget_sweep": result["budget_sweep"],
        "final_cover": {key: value for key, value in result["final_leaf_cover"].items()
                        if key != "leaves"},
    }, indent=2))


if __name__ == "__main__":
    main()
