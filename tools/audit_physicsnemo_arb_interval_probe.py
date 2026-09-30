"""Audit exploratory Arb mean-value enclosures on a frozen PhysicsNeMo run."""
import hashlib
import io
import itertools
import json
import math
import platform
import tarfile
from pathlib import Path

import numpy as np
import torch
from flint import __version__ as flint_version
from flint import ctx
from physicsnemo.models.mlp.fully_connected import FullyConnected

from tools.physicsnemo_arb_interval_probe import (
    centered_gradient_error_enclosure,
    gradient_error_enclosure,
)
from tools.arb_local_branch_cover import adaptive_axis_bisect_cover
from tools.reference import fields


ARCHIVE = Path("evidence/physicsnemo-study-v1/n64-nt17.tar.gz")


def _sha(data):
    return hashlib.sha256(data).hexdigest()


def _frob_upper(enclosure):
    return math.sqrt(sum(
        float(enclosure[i][j].abs_upper()) ** 2
        for i in range(3) for j in range(3)
    ))


def _max_radius(enclosure):
    return max(float(enclosure[i][j].rad().upper())
               for i in range(3) for j in range(3))


def audit(archive=ARCHIVE):
    archive = Path(archive)
    archive_bytes = archive.read_bytes()
    with tarfile.open(fileobj=io.BytesIO(archive_bytes), mode="r:gz") as tar:
        params = json.load(tar.extractfile("parameters.json"))
        weights_bytes = tar.extractfile("weights.pt").read()
        evaluation_bytes = tar.extractfile("evaluation.npz").read()
    state = torch.load(io.BytesIO(weights_bytes), map_location="cpu", weights_only=True)
    with np.load(io.BytesIO(evaluation_bytes)) as saved:
        coordinates = saved["coordinates"].copy()

    torch.set_default_dtype(torch.float64)
    torch.set_num_threads(2)
    net = FullyConnected(in_features=7, out_features=4, num_layers=3,
                         layer_size=32, activation_fn="tanh")
    net.load_state_dict(state)
    net = net.double().eval()
    hidden = [
        (state[f"layers.{layer}.linear.weight"].numpy().tolist(),
         state[f"layers.{layer}.linear.bias"].numpy().tolist())
        for layer in range(3)
    ]
    output = (
        state["final_layer.linear.weight"][:3].numpy().tolist(),
        state["final_layer.linear.bias"][:3].numpy().tolist(),
    )

    def autograd_error_jacobian(points):
        points = np.asarray(points, dtype=np.float64)
        x = torch.tensor(points, requires_grad=True)
        t = torch.full((len(x), 1), params["end"])
        psi = torch.exp(((torch.cos(x - torch.pi) - 1) / params["sigma"]**2)
                        .sum(dim=1, keepdim=True))
        grad_psi = -psi * torch.sin(x - torch.pi) / params["sigma"]**2
        u0 = torch.linalg.cross(grad_psi, torch.tensor([1., 2., 3.]).expand_as(grad_psi))
        raw = net(torch.cat((torch.sin(x), torch.cos(x), t / params["end"]), dim=1))
        predicted = u0 + t * raw[:, :3]
        jacobian = torch.stack([
            torch.autograd.grad(predicted[:, i].sum(), x, retain_graph=True)[0]
            for i in range(3)
        ], dim=1).detach().numpy()
        reference = fields(points, params["end"], params["sigma"])["grad_u"]
        return jacobian - reference

    best_norm = -1.0
    candidate = None
    for start in range(0, len(coordinates), 512):
        points = coordinates[start:start + 512]
        errors = autograd_error_jacobian(points)
        norms = np.linalg.norm(errors, axis=(1, 2))
        local = int(np.argmax(norms))
        if float(norms[local]) > best_norm:
            best_norm = float(norms[local])
            candidate = points[local].copy()

    old_prec = ctx.prec
    ctx.dps = 60
    try:
        point_box = [(float(value), float(value)) for value in candidate]
        point_direct = gradient_error_enclosure(
            hidden, output, point_box, time=params["end"], endpoint=params["end"],
            sigma=params["sigma"], dps=60,
        )
        point_centered = centered_gradient_error_enclosure(
            hidden, output, point_box, time=params["end"], endpoint=params["end"],
            sigma=params["sigma"], dps=60,
        )
    finally:
        ctx.prec = old_prec
    point_autograd = autograd_error_jacobian(candidate[None, :])[0]
    point_discrepancy = max(
        abs((float(point_direct[i][j].lower()) + float(point_direct[i][j].upper())) / 2
            - point_autograd[i, j])
        for i in range(3) for j in range(3)
    )

    neighborhood_rows = []
    for radius in (0.0, 1e-4, 1e-3, 1e-2, 0.025, 0.05):
        box = [(float(value - radius), float(value + radius)) for value in candidate]
        direct = gradient_error_enclosure(
            hidden, output, box, time=params["end"], endpoint=params["end"],
            sigma=params["sigma"], dps=60,
        )
        centered = centered_gradient_error_enclosure(
            hidden, output, box, time=params["end"], endpoint=params["end"],
            sigma=params["sigma"], dps=60,
        )
        sample_points = [candidate + radius * np.asarray(signs)
                         for signs in itertools.product((-1, 0, 1), repeat=3)]
        sample_errors = autograd_error_jacobian(sample_points)
        max_sample_excess = 0.0
        for sample_error in sample_errors:
            for i in range(3):
                for j in range(3):
                    lower = float(centered[i][j].lower())
                    upper = float(centered[i][j].upper())
                    max_sample_excess = max(
                        max_sample_excess,
                        lower - sample_error[i, j], sample_error[i, j] - upper, 0.0,
                    )
        neighborhood_rows.append({
            "half_width": radius,
            "direct_frobenius_error_upper": _frob_upper(direct),
            "centered_frobenius_error_upper": _frob_upper(centered),
            "centered_max_component_radius": _max_radius(centered),
            "autograd_sample_count": len(sample_points),
            "max_autograd_excess_outside_centered_bound": max_sample_excess,
            "samples_within_1e-8_float_tolerance": bool(max_sample_excess <= 1e-8),
        })

    subdivision_rows = []
    parent_half_width = 0.01
    for divisions in (1, 2, 4, 8):
        step = 2 * parent_half_width / divisions
        cell_bounds = []
        centers = []
        max_cell_upper = 0.0
        max_cell_radius = 0.0
        for index in itertools.product(range(divisions), repeat=3):
            bounds = [
                (float(candidate[axis] - parent_half_width + index[axis] * step),
                 float(candidate[axis] - parent_half_width + (index[axis] + 1) * step))
                for axis in range(3)
            ]
            center = np.array([(lo + hi) / 2 for lo, hi in bounds])
            enclosure = centered_gradient_error_enclosure(
                hidden, output, bounds, time=params["end"], endpoint=params["end"],
                sigma=params["sigma"], dps=40,
            )
            cell_bounds.append(enclosure)
            centers.append(center)
            max_cell_upper = max(max_cell_upper, _frob_upper(enclosure))
            max_cell_radius = max(max_cell_radius, _max_radius(enclosure))
        center_errors = autograd_error_jacobian(centers)
        max_excess = 0.0
        for enclosure, error in zip(cell_bounds, center_errors):
            for i in range(3):
                for j in range(3):
                    max_excess = max(
                        max_excess,
                        float(enclosure[i][j].lower()) - error[i, j],
                        error[i, j] - float(enclosure[i][j].upper()),
                        0.0,
                    )
        subdivision_rows.append({
            "parent_half_width": parent_half_width,
            "equal_subdivisions_per_axis": divisions,
            "cell_count": divisions**3,
            "max_centered_cell_frobenius_error_upper": max_cell_upper,
            "max_centered_cell_component_radius": max_cell_radius,
            "autograd_cell_center_count": len(centers),
            "max_autograd_excess_outside_centered_bound": max_excess,
            "cell_centers_within_1e-8_float_tolerance": bool(max_excess <= 1e-8),
        })

    adaptive_rows = []
    target_upper = 0.26  # exploratory comparator, not a preregistered gate
    evaluation_budget = 2049
    for half_width in (0.01, 0.025, 0.05):
        parent = [
            (float(value - half_width), float(value + half_width))
            for value in candidate
        ]

        def cell_upper(bounds):
            enclosure = centered_gradient_error_enclosure(
                hidden, output, bounds, time=params["end"],
                endpoint=params["end"], sigma=params["sigma"], dps=40,
            )
            return _frob_upper(enclosure)

        cover = adaptive_axis_bisect_cover(
            parent, cell_upper, target=target_upper,
            max_evaluations=evaluation_budget,
        )
        centers = [
            [(lo + hi) / 2 for lo, hi in leaf["box"]]
            for leaf in cover["leaves"]
        ]
        center_errors = autograd_error_jacobian(centers)
        max_center_excess = 0.0
        for leaf, error in zip(cover["leaves"], center_errors):
            bounds = leaf["box"]
            enclosure = centered_gradient_error_enclosure(
                hidden, output, bounds, time=params["end"],
                endpoint=params["end"], sigma=params["sigma"], dps=40,
            )
            for i in range(3):
                for j in range(3):
                    max_center_excess = max(
                        max_center_excess,
                        float(enclosure[i][j].lower()) - error[i, j],
                        error[i, j] - float(enclosure[i][j].upper()), 0.0,
                    )
        cover.update({
            "parent_half_width": half_width,
            "autograd_leaf_center_count": len(centers),
            "max_autograd_excess_at_leaf_centers": max_center_excess,
            "leaf_centers_within_1e-8_float_tolerance": bool(
                max_center_excess <= 1e-8
            ),
        })
        adaptive_rows.append(cover)

    return {
        "scope": "Exploratory local Arb mean-value enclosures for one frozen PhysicsNeMo checkpoint; no full periodic-domain cover or global-extremum certificate.",
        "case": archive.name.removesuffix(".tar.gz"),
        "archive_sha256": _sha(archive_bytes),
        "checkpoint_sha256": _sha(weights_bytes),
        "evaluation_sha256": _sha(evaluation_bytes),
        "sample_count": len(coordinates),
        "candidate_point_from_saved_grid": candidate.tolist(),
        "largest_sampled_gradient_error_frobenius": best_norm,
        "max_point_centered_interval_midpoint_vs_autograd": point_discrepancy,
        "point_direct_frobenius_error_upper": _frob_upper(point_direct),
        "point_centered_frobenius_error_upper": _frob_upper(point_centered),
        "point_centered_max_component_radius": _max_radius(point_centered),
        "neighborhood_sweep": neighborhood_rows,
        "local_equal_subdivision_sweep": subdivision_rows,
        "adaptive_local_cover_sweep": {
            "target_frobenius_upper": target_upper,
            "target_status": "exploratory, not preregistered acceptance gate",
            "max_evaluations_per_parent": evaluation_budget,
            "cases": adaptive_rows,
        },
        "environment": {
            "python": platform.python_version(),
            "python_flint": flint_version,
            "torch": torch.__version__,
            "interval_decimal_precision_neighborhood": 60,
            "interval_decimal_precision_subdivision": 40,
        },
        "limitations": [
            "Autograd sample checks are diagnostic, not proofs of the enclosure.",
            "No cover outside the single local parent box is built.",
            "Arb/FLINT library assurance is taken from upstream contracts and is not independently proved here.",
            "No PhysicsNeMo quality acceptance threshold is preregistered; quality remains UNCERTAIN.",
        ],
        "quality": "UNCERTAIN",
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2))
