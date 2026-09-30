"""Exploratory one-point interval/AD cross-check for one frozen PhysicsNeMo run.

This checks a local derivative enclosure implementation at a sampled point. It
does not cover the periodic domain and is not a continuous-extremum certificate.
"""
import hashlib
import io
import json
import tarfile
from pathlib import Path

import numpy as np
import torch
from mpmath import iv
from physicsnemo.models.mlp.fully_connected import FullyConnected

from tools.physicsnemo_local_interval_probe import gradient_error_enclosure
from tools.reference import fields


ARCHIVE = Path("evidence/physicsnemo-study-v1/n64-nt17.tar.gz")


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def audit(archive=ARCHIVE):
    archive = Path(archive)
    raw_archive = archive.read_bytes()
    with tarfile.open(fileobj=io.BytesIO(raw_archive), mode="r:gz") as tar:
        params = json.load(tar.extractfile("parameters.json"))
        weights_bytes = tar.extractfile("weights.pt").read()
        eval_bytes = tar.extractfile("evaluation.npz").read()
    state = torch.load(io.BytesIO(weights_bytes), map_location="cpu", weights_only=True)
    with np.load(io.BytesIO(eval_bytes)) as saved:
        coordinates = saved["coordinates"].copy()

    torch.set_default_dtype(torch.float64)
    torch.set_num_threads(2)
    net = FullyConnected(in_features=7, out_features=4, num_layers=3,
                         layer_size=32, activation_fn="tanh")
    net.load_state_dict(state)
    net = net.double().eval()

    best_norm = -1.0
    best_point = None
    for start in range(0, len(coordinates), 512):
        points = coordinates[start:start + 512]
        x = torch.tensor(points, requires_grad=True)
        t = torch.full((len(x), 1), params["end"])
        psi = torch.exp(((torch.cos(x - torch.pi) - 1) / params["sigma"]**2).sum(dim=1, keepdim=True))
        grad_psi = -psi * torch.sin(x - torch.pi) / params["sigma"]**2
        u0 = torch.linalg.cross(grad_psi, torch.tensor([1.0, 2.0, 3.0]).expand_as(grad_psi))
        output = net(torch.cat((torch.sin(x), torch.cos(x), t / params["end"]), dim=1))
        velocity = u0 + t * output[:, :3]
        jac = torch.stack([
            torch.autograd.grad(velocity[:, i].sum(), x, retain_graph=True)[0]
            for i in range(3)
        ], dim=1).detach().numpy()
        error = jac - fields(points, params["end"], params["sigma"])["grad_u"]
        norms = np.linalg.norm(error, axis=(1, 2))
        idx = int(np.argmax(norms))
        if float(norms[idx]) > best_norm:
            best_norm, best_point = float(norms[idx]), points[idx].copy()

    # Re-evaluate AD at the selected point; never reuse a batch-local tensor.
    x = torch.tensor(best_point[None, :], requires_grad=True)
    t = torch.full((1, 1), params["end"])
    psi = torch.exp(((torch.cos(x - torch.pi) - 1) / params["sigma"]**2).sum(dim=1, keepdim=True))
    grad_psi = -psi * torch.sin(x - torch.pi) / params["sigma"]**2
    u0 = torch.linalg.cross(grad_psi, torch.tensor([1.0, 2.0, 3.0]).expand_as(grad_psi))
    output = net(torch.cat((torch.sin(x), torch.cos(x), t / params["end"]), dim=1))
    velocity = u0 + t * output[:, :3]
    jac = np.stack([
        torch.autograd.grad(velocity[:, i].sum(), x, retain_graph=True)[0][0].detach().numpy()
        for i in range(3)
    ])

    hidden = [
        (state[f"layers.{i}.linear.weight"].numpy().tolist(),
         state[f"layers.{i}.linear.bias"].numpy().tolist())
        for i in range(3)
    ]
    output_layer = (
        state["final_layer.linear.weight"][:3].numpy().tolist(),
        state["final_layer.linear.bias"][:3].numpy().tolist(),
    )
    enclosure = gradient_error_enclosure(
        hidden, output_layer, [(float(v), float(v)) for v in best_point],
        time=params["end"], endpoint=params["end"], sigma=params["sigma"], dps=60,
    )
    ref_jac = fields(best_point, params["end"], params["sigma"])["grad_u"]
    discrepancies = []
    widths = []
    for i in range(3):
        for j in range(3):
            lower, upper = float(enclosure[i][j].a), float(enclosure[i][j].b)
            midpoint = (lower + upper) / 2
            discrepancies.append(abs(midpoint - (jac[i, j] - ref_jac[i, j])))
            widths.append(float(enclosure[i][j].delta))
    max_discrepancy = max(discrepancies)
    if max_discrepancy > 1e-8:
        raise AssertionError(f"interval midpoint disagrees with independent AD by {max_discrepancy}")
    return {
        "scope": "One sampled point from a frozen PhysicsNeMo checkpoint; local exploratory cross-check only, no full-domain cover or continuous-extremum certificate.",
        "case": archive.name.removesuffix(".tar.gz"),
        "archive_sha256": sha256(raw_archive),
        "checkpoint_sha256": sha256(weights_bytes),
        "evaluation_sha256": sha256(eval_bytes),
        "sample_count": int(len(coordinates)),
        "candidate_point_from_saved_evaluation_grid": best_point.tolist(),
        "largest_sampled_gradient_error_frobenius": best_norm,
        "max_interval_midpoint_vs_autograd_error": max_discrepancy,
        "max_point_interval_width": max(widths),
        "interval_decimal_precision": 60,
        "comparison_tolerance": 1e-8,
        "verdict": "EXPLORATORY_POINT_CHECK_PASS",
        "quality": "UNCERTAIN",
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2))
