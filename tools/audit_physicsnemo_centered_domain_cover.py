"""Build a reproducible centered-Arb cover of the frozen periodic cube."""

import argparse
import hashlib
import io
import json
import math
import platform
import tarfile
import time
from pathlib import Path

import numpy as np
import torch
from flint import __version__ as flint_version
from flint import arb, ctx

from tools.audit_physicsnemo_arb_interval_probe import _frob_upper
from tools.physicsnemo_arb_interval_probe import centered_gradient_error_enclosure
from tools.physicsnemo_arb_interval_probe import _error_jet
from tools.physicsnemo_arb_interval_probe import quadratic_taylor_gradient_error_enclosure
from tools.reference import fields


DEFAULT_ARCHIVE = Path("evidence/physicsnemo-study-v1/n64-nt17.tar.gz")
DOMAIN_ENDPOINT = 3.141592653589794


def _sha(data):
    return hashlib.sha256(data).hexdigest()


def _load_case(archive):
    raw = Path(archive).read_bytes()
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
    return raw, weights_bytes, params, state, hidden, output


def _autograd_error_jacobian(points, state, params):
    points = np.asarray(points, dtype=np.float64)
    x = torch.tensor(points, dtype=torch.float64, requires_grad=True)
    t = torch.full((len(x), 1), params["end"], dtype=torch.float64)
    psi = torch.exp(((torch.cos(x - torch.pi) - 1) / params["sigma"]**2)
                    .sum(dim=1, keepdim=True))
    grad_psi = -psi * torch.sin(x - torch.pi) / params["sigma"]**2
    u0 = torch.linalg.cross(grad_psi, torch.tensor([1., 2., 3.]).expand_as(grad_psi))
    value = torch.cat((torch.sin(x), torch.cos(x), t / params["end"]), dim=1)
    for layer in range(3):
        value = torch.tanh(torch.nn.functional.linear(
            value, state[f"layers.{layer}.linear.weight"],
            state[f"layers.{layer}.linear.bias"],
        ))
    predicted = u0 + t * torch.nn.functional.linear(
        value, state["final_layer.linear.weight"][:3],
        state["final_layer.linear.bias"][:3],
    )
    jacobian = torch.stack([
        torch.autograd.grad(predicted[:, component].sum(), x, retain_graph=True)[0]
        for component in range(3)
    ], dim=1).detach().numpy()
    reference = fields(points, params["end"], params["sigma"])["grad_u"]
    return jacobian - reference


def _decompose_centered_cell(hidden, output, box, params):
    intervals = [arb(lo).union(hi) for lo, hi in box]
    centers = [(lo + hi) / 2 for lo, hi in box]
    center_points = [arb(value) for value in centers]
    center_gradient, _ = _error_jet(
        hidden, output, center_points, time=params["end"],
        sigma=params["sigma"], endpoint=params["end"],
    )
    _, box_hessian = _error_jet(
        hidden, output, intervals, time=params["end"],
        sigma=params["sigma"], endpoint=params["end"],
    )
    deltas = [(interval - center).abs_upper()
              for interval, center in zip(intervals, center_points)]
    center_abs = [[float(center_gradient[i][j].abs_upper())
                   for j in range(3)] for i in range(3)]
    axis_terms = [[[float(box_hessian[i][j][axis].abs_upper() * deltas[axis])
                    for j in range(3)] for i in range(3)] for axis in range(3)]
    component_upper = [[center_abs[i][j] + sum(axis_terms[a][i][j] for a in range(3))
                        for j in range(3)] for i in range(3)]
    frobenius = lambda matrix: math.sqrt(sum(value * value
                                              for row in matrix for value in row))
    return {
        "box": [[float(lo), float(hi)] for lo, hi in box],
        "center": [float(value) for value in centers],
        "center_jacobian_frobenius_upper": frobenius(center_abs),
        "axiswise_hessian_variation_frobenius_bounds": [
            frobenius(axis_terms[axis]) for axis in range(3)
        ],
        "componentwise_combined_frobenius_upper": frobenius(component_upper),
        "quadratic_taylor_frobenius_upper": _frob_upper(
            quadratic_taylor_gradient_error_enclosure(
                hidden, output, box, time=params["end"],
                endpoint=params["end"], sigma=params["sigma"], dps=ctx.dps,
            )
        ),
    }


def audit(archive=DEFAULT_ARCHIVE, divisions=(16,), dps=30, batch_size=128):
    if not divisions or any(not isinstance(n, int) or n < 1 for n in divisions):
        raise ValueError("divisions must contain positive integers")
    raw, weights_bytes, params, state, hidden, output = _load_case(archive)
    torch.set_default_dtype(torch.float64)
    torch.set_num_threads(2)
    old_precision = ctx.prec
    ctx.dps = dps
    rows = []
    started = time.perf_counter()
    try:
        for n in divisions:
            step = 2 * DOMAIN_ENDPOINT / n
            boxes = []
            centers = []
            max_upper = 0.0
            worst_box = None
            for index in np.ndindex((n, n, n)):
                box = [
                    (-DOMAIN_ENDPOINT + axis * step,
                     -DOMAIN_ENDPOINT + (axis + 1) * step)
                    for axis in index
                ]
                enclosure = centered_gradient_error_enclosure(
                    hidden, output, box, time=params["end"],
                    endpoint=params["end"], sigma=params["sigma"], dps=dps,
                )
                boxes.append(enclosure)
                centers.append([(lo + hi) / 2 for lo, hi in box])
                cell_upper = _frob_upper(enclosure)
                if cell_upper > max_upper:
                    max_upper = cell_upper
                    worst_box = box

            max_center_sample = 0.0
            max_component_excess = 0.0
            for start in range(0, len(centers), batch_size):
                points = centers[start:start + batch_size]
                errors = _autograd_error_jacobian(points, state, params)
                max_center_sample = max(
                    max_center_sample,
                    float(np.linalg.norm(errors, axis=(1, 2)).max()),
                )
                for enclosure, error in zip(boxes[start:start + batch_size], errors):
                    for i in range(3):
                        for j in range(3):
                            max_component_excess = max(
                                max_component_excess,
                                float(enclosure[i][j].lower()) - error[i, j],
                                error[i, j] - float(enclosure[i][j].upper()),
                                0.0,
                            )
            rows.append({
                "cells_per_axis": n,
                "cell_count": n**3,
                "domain_endpoint_float": DOMAIN_ENDPOINT,
                "max_centered_cell_frobenius_upper": max_upper,
                "max_autograd_cell_center_sample": max_center_sample,
                "upper_to_center_sample_ratio": max_upper / max_center_sample,
                "max_autograd_sample_excess_outside_component_interval": max_component_excess,
                "all_cell_center_samples_within_1e-8_tolerance": bool(
                    max_component_excess <= 1e-8
                ),
                "worst_cell_decomposition": _decompose_centered_cell(
                    hidden, output, worst_box, params
                ),
            })
    finally:
        ctx.prec = old_precision
    return {
        "scope": "Full periodic-domain centered Arb enclosure for frozen PhysicsNeMo n64-nt17; center autograd checks are diagnostics, not independent global proofs.",
        "archive": Path(archive).name,
        "archive_sha256": _sha(raw),
        "checkpoint_sha256": _sha(weights_bytes),
        "domain": "[-pi, pi]^3, contained in the outward-rounded float cube",
        "domain_endpoint_float": DOMAIN_ENDPOINT,
        "endpoint_is_outward": DOMAIN_ENDPOINT > math.pi,
        "interval_decimal_precision": dps,
        "divisions": rows,
        "environment": {
            "python": platform.python_version(),
            "python_flint": flint_version,
            "torch": torch.__version__,
        },
        "wall_seconds": time.perf_counter() - started,
        "limitations": [
            "Arb/FLINT is not independently verified in a proof assistant.",
            "Cell-center autograd checks validate selected values only, not the complete interval enclosure.",
            "No PhysicsNeMo-specific acceptance threshold is preregistered; quality remains UNCERTAIN.",
        ],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--archive", type=Path, default=DEFAULT_ARCHIVE)
    parser.add_argument("--divisions", type=int, nargs="+", default=[16])
    parser.add_argument("--dps", type=int, default=30)
    parser.add_argument("--batch-size", type=int, default=128)
    parser.add_argument("--output", type=Path,
                        default=Path("evidence/tests/physicsnemo-centered-domain-cover-n16.json"))
    args = parser.parse_args()
    result = audit(args.archive, tuple(args.divisions), args.dps, args.batch_size)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({
        "output": str(args.output),
        "divisions": [
            {"n": row["cells_per_axis"], "cells": row["cell_count"],
             "upper": row["max_centered_cell_frobenius_upper"],
             "center_sample": row["max_autograd_cell_center_sample"]}
            for row in result["divisions"]
        ],
        "wall_seconds": result["wall_seconds"],
    }, indent=2))


if __name__ == "__main__":
    main()
