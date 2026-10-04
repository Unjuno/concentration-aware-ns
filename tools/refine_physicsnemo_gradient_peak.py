"""Locally refine the strongest Sobol gradient-error candidate.

SciPy optimization proposes a candidate only. Arb point and box enclosures
then report pointwise lower and local-neighborhood upper bounds; neither is a
global maximum certificate.
"""
import hashlib
import io
import json
import math
import tarfile
import time
from pathlib import Path

import numpy as np
import torch
from flint import ctx
from physicsnemo.models.mlp.fully_connected import FullyConnected

from tools.physicsnemo_arb_interval_probe import (
    gradient_error_enclosure,
    quadratic_taylor_gradient_error_enclosure,
)
from tools.physicsnemo_gradient_global_cover import frobenius_lower, frobenius_upper


ARCHIVE = Path("evidence/physicsnemo-study-v1/n64-nt17.tar.gz")
SOBOL_EVIDENCE = Path("evidence/tests/physicsnemo-sobol-gradient-audit-2026-10-01.json")


def _sha(value):
    return hashlib.sha256(value).hexdigest()


def audit(archive=ARCHIVE, sobol_evidence=SOBOL_EVIDENCE, *, dps=50):
    raw_archive = Path(archive).read_bytes()
    sobol_raw = Path(sobol_evidence).read_bytes()
    sobol = json.loads(sobol_raw)
    with tarfile.open(fileobj=io.BytesIO(raw_archive), mode="r:gz") as tar:
        params = json.load(tar.extractfile("parameters.json"))
        weight_bytes = tar.extractfile("weights.pt").read()
    if _sha(weight_bytes) != sobol["checkpoint_sha256"]:
        raise ValueError("Sobol record and selected archive use different checkpoints")
    state = torch.load(io.BytesIO(weight_bytes), map_location="cpu", weights_only=True)
    torch.set_default_dtype(torch.float64)
    torch.set_num_threads(2)
    model = FullyConnected(in_features=7, out_features=4, num_layers=3,
                           layer_size=32, activation_fn="tanh")
    model.load_state_dict(state)
    model = model.double().eval()
    tval, sigma = float(params["end"]), float(params["sigma"])
    a = torch.tensor([1.0, 2.0, 3.0], dtype=torch.float64)

    def value_and_gradient(point):
        x = torch.tensor(np.asarray(point).reshape(1, 3), dtype=torch.float64,
                         requires_grad=True)
        d = x - math.pi
        psi = torch.exp(((torch.cos(d) - 1) / sigma**2).sum(dim=1, keepdim=True))
        grad_psi = -psi * torch.sin(d) / sigma**2
        u0 = torch.linalg.cross(grad_psi, a.expand_as(grad_psi), dim=1)
        features = torch.cat((torch.sin(x), torch.cos(x),
                              torch.ones((1, 1), dtype=torch.float64)), dim=1)
        velocity = u0 + tval * model(features)[:, :3]
        jac = torch.stack([
            torch.autograd.grad(velocity[:, i].sum(), x, create_graph=True,
                                retain_graph=True)[0][0]
            for i in range(3)
        ])
        q = -torch.sin(d[0]) / sigma**2
        r = -torch.cos(d[0]) / sigma**2
        psi_ref = torch.exp(-tval + ((torch.cos(d[0]) - 1) / sigma**2).sum())
        hessian_psi = psi_ref * (q[:, None] * q[None, :] + torch.diag(r))
        grad_ref = torch.stack([
            torch.linalg.cross(hessian_psi[:, j], a, dim=0) for j in range(3)
        ], dim=1)
        error = jac - grad_ref
        norm = torch.linalg.vector_norm(error)
        gradient = torch.autograd.grad(norm, x)[0][0]
        return float(norm.detach()), gradient.detach().cpu().numpy()

    starts = [row["point"] for row in sobol["top_sampled_points"][:16]]
    bounds = [(2.4, 3.7), (2.4, 3.7), (2.8, 3.8)]
    started = time.monotonic()
    optima = []
    lower = torch.tensor([pair[0] for pair in bounds], dtype=torch.float64)
    upper = torch.tensor([pair[1] for pair in bounds], dtype=torch.float64)
    for start in starts:
        start_tensor = torch.tensor(np.asarray(start), dtype=torch.float64)
        fraction = ((start_tensor - lower) / (upper - lower)).clamp(1e-8, 1 - 1e-8)
        unconstrained = torch.nn.Parameter(torch.logit(fraction))
        optimizer = torch.optim.LBFGS(
            [unconstrained], lr=0.8, max_iter=250, tolerance_grad=1e-10,
            tolerance_change=1e-14, line_search_fn="strong_wolfe",
        )
        iterations = 0

        def closure():
            nonlocal iterations
            optimizer.zero_grad()
            point = lower + (upper - lower) * torch.sigmoid(unconstrained)
            # Keep the objective connected to LBFGS parameters through the
            # bounded logistic coordinate transform.
            x = point
            d = x - math.pi
            psi = torch.exp(((torch.cos(d) - 1) / sigma**2).sum())
            grad_psi = -psi * torch.sin(d) / sigma**2
            u0 = torch.linalg.cross(grad_psi, a, dim=0)
            features = torch.cat((torch.sin(x), torch.cos(x), torch.ones(1, dtype=x.dtype)))
            velocity = u0 + tval * model(features.reshape(1, -1))[0, :3]
            jac = torch.stack([
                torch.autograd.grad(velocity[i], x, create_graph=True, retain_graph=True)[0]
                for i in range(3)
            ])
            q = -torch.sin(d) / sigma**2
            r = -torch.cos(d) / sigma**2
            psi_ref = torch.exp(-tval + ((torch.cos(d) - 1) / sigma**2).sum())
            hessian_psi = psi_ref * (q[:, None] * q[None, :] + torch.diag(r))
            grad_ref = torch.stack([
                torch.linalg.cross(hessian_psi[:, j], a, dim=0) for j in range(3)
            ], dim=1)
            objective = -torch.linalg.vector_norm(jac - grad_ref)
            objective.backward()
            iterations += 1
            return objective

        optimizer.step(closure)
        point = (lower + (upper - lower) * torch.sigmoid(unconstrained)).detach().numpy()
        value, grad = value_and_gradient(point)
        optima.append({
            "point": point.tolist(),
            "frobenius_error": value,
            "optimizer_success": bool(np.linalg.norm(grad) < 1e-7),
            "optimizer_message": "PyTorch LBFGS completed; success means only the final gradient met the recorded tolerance.",
            "gradient_norm": float(np.linalg.norm(grad)),
            "iterations": iterations,
        })
    best = max(optima, key=lambda item: item["frobenius_error"])

    hidden = [
        (state[f"layers.{i}.linear.weight"].numpy().tolist(),
         state[f"layers.{i}.linear.bias"].numpy().tolist())
        for i in range(3)
    ]
    output = (
        state["final_layer.linear.weight"][:3].numpy().tolist(),
        state["final_layer.linear.bias"][:3].numpy().tolist(),
    )
    old_prec = ctx.prec
    ctx.dps = dps
    try:
        point_interval = gradient_error_enclosure(
            hidden, output, [(x, x) for x in best["point"]], time=tval,
            sigma=sigma, endpoint=tval, dps=dps,
        )
        lower = frobenius_lower(point_interval)
        neighborhood = []
        for radius in (1e-4, 5e-4, 1e-3, 2e-3, 5e-3, 1e-2):
            box = [(x - radius, x + radius) for x in best["point"]]
            direct = gradient_error_enclosure(
                hidden, output, box, time=tval, sigma=sigma,
                endpoint=tval, dps=dps,
            )
            taylor = quadratic_taylor_gradient_error_enclosure(
                hidden, output, box, time=tval, sigma=sigma,
                endpoint=tval, dps=dps,
            )
            neighborhood.append({
                "half_width": radius,
                "direct_interval_frobenius_upper": frobenius_upper(direct),
                "quadratic_taylor_frobenius_upper": frobenius_upper(taylor),
            })
    finally:
        ctx.prec = old_prec

    return {
        "scope": "Local multi-start refinement of the strongest Sobol candidate, followed by an Arb point lower bound and Arb local-box upper bounds. It is not a global maximum proof.",
        "archive_sha256": _sha(raw_archive),
        "checkpoint_sha256": _sha(weight_bytes),
        "sobol_evidence_sha256": _sha(sobol_raw),
        "sobol_sampled_maximum": sobol["pointwise_max_sampled_frobenius_error"],
        "optimizer_start_count": len(starts),
        "optimizer_bounds": bounds,
        "highest_refined_candidate": best,
        "all_refined_starts": optima,
        "arb_pointwise_lower_bound_at_candidate": lower,
        "local_neighborhood_enclosures": neighborhood,
        "interval_decimal_precision": dps,
        "elapsed_seconds": time.monotonic() - started,
        "limitations": [
            "L-BFGS-B outcomes are candidate searches, not proofs of stationarity or local maximality.",
            "The box upper bounds cover only small neighborhoods around the selected candidate.",
            "No global quality threshold was preregistered; the verdict remains UNCERTAIN.",
        ],
    }


def main():
    result = audit()
    result["tool_sha256"] = _sha(Path(__file__).read_bytes())
    result["repository_commit_at_execution"] = "c4cd47741c5459d7cf822178b0b0332da550eb8b"
    result["execution_source_status"] = "untracked working-tree script at the recorded repository commit"
    path = Path("evidence/tests/physicsnemo-local-peak-refinement-2026-10-01.json")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
