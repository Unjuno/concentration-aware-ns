"""Independent dense Sobol/autograd search for PhysicsNeMo gradient errors.

The point scan is empirical, not a continuous-domain proof. The top sampled
point is separately enclosed with Arb to provide a rigorous pointwise lower
bound for the supremum, conditional on the interval implementation.
"""
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
from flint import arb, ctx
from physicsnemo.models.mlp.fully_connected import FullyConnected

from tools.physicsnemo_arb_interval_probe import gradient_error_enclosure
from tools.physicsnemo_gradient_global_cover import frobenius_lower
from tools.reference import fields


ARCHIVE = Path("evidence/physicsnemo-study-v1/n64-nt17.tar.gz")
PRIOR_LATTICE_EVIDENCE = Path("evidence/tests/physicsnemo-local-interval-probe-2026-10-01.json")
SAMPLES = 1_048_576
BATCH = 512
SEED = 20261001


def _sha(data):
    return hashlib.sha256(data).hexdigest()


def audit(archive=ARCHIVE, *, sample_count=SAMPLES, batch_size=BATCH, seed=SEED):
    archive = Path(archive)
    raw_archive = archive.read_bytes()
    prior_raw = PRIOR_LATTICE_EVIDENCE.read_bytes()
    prior = json.loads(prior_raw)
    with tarfile.open(fileobj=io.BytesIO(raw_archive), mode="r:gz") as tar:
        params = json.load(tar.extractfile("parameters.json"))
        weights_bytes = tar.extractfile("weights.pt").read()
    state = torch.load(io.BytesIO(weights_bytes), map_location="cpu", weights_only=True)
    checkpoint_sha = _sha(weights_bytes)
    if prior["checkpoint_sha256"] != checkpoint_sha:
        raise ValueError("prior lattice evidence references a different checkpoint")

    torch.set_default_dtype(torch.float64)
    torch.set_num_threads(2)
    model = FullyConnected(in_features=7, out_features=4, num_layers=3,
                           layer_size=32, activation_fn="tanh")
    model.load_state_dict(state)
    model = model.double().eval()

    engine = torch.quasirandom.SobolEngine(dimension=3, scramble=True, seed=seed)
    best_norm = -1.0
    best_point = None
    top = []
    started = time.monotonic()
    tval = float(params["end"])
    sigma = float(params["sigma"])
    pi = math.pi
    a = torch.tensor([1.0, 2.0, 3.0], dtype=torch.float64)

    for start in range(0, sample_count, batch_size):
        count = min(batch_size, sample_count - start)
        points = engine.draw(count).to(torch.float64) * (2 * pi)
        points.requires_grad_(True)
        t = torch.full((count, 1), tval, dtype=torch.float64)
        psi = torch.exp(((torch.cos(points - pi) - 1) / sigma**2)
                        .sum(dim=1, keepdim=True))
        grad_psi = -psi * torch.sin(points - pi) / sigma**2
        u0 = torch.linalg.cross(grad_psi, a.expand_as(grad_psi), dim=1)
        features = torch.cat((torch.sin(points), torch.cos(points),
                              t / tval), dim=1)
        velocity = u0 + t * model(features)[:, :3]
        jacobian = torch.stack([
            torch.autograd.grad(velocity[:, i].sum(), points,
                                retain_graph=True)[0]
            for i in range(3)
        ], dim=1).detach().cpu().numpy()
        coords = points.detach().cpu().numpy()
        reference_gradient = fields(coords, tval, sigma)["grad_u"]
        error = jacobian - reference_gradient
        norms = np.linalg.norm(error, axis=(1, 2))
        local_top = np.argpartition(norms, -min(8, count))[-min(8, count):]
        for idx in local_top:
            item = (float(norms[idx]), coords[idx].tolist())
            if len(top) < 32:
                top.append(item)
            else:
                worst = min(range(len(top)), key=lambda k: top[k][0])
                if item[0] > top[worst][0]:
                    top[worst] = item
        idx = int(np.argmax(norms))
        if float(norms[idx]) > best_norm:
            best_norm = float(norms[idx])
            best_point = coords[idx].tolist()

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
    ctx.dps = 70
    try:
        point_interval = gradient_error_enclosure(
            hidden, output, [(v, v) for v in best_point], time=tval,
            sigma=sigma, endpoint=tval, dps=70,
        )
        point_lower = frobenius_lower(point_interval)
    finally:
        ctx.prec = old_prec

    top.sort(key=lambda row: row[0], reverse=True)
    return {
        "scope": "Independent scrambled-Sobol sample search with PyTorch autograd; it is empirical and does not cover the continuum. Arb separately encloses the strongest sampled point to produce a pointwise lower bound.",
        "archive": str(archive),
        "archive_sha256": _sha(raw_archive),
        "checkpoint_sha256": checkpoint_sha,
        "prior_lattice_evidence": str(PRIOR_LATTICE_EVIDENCE),
        "prior_lattice_evidence_sha256": _sha(prior_raw),
        "sample_count": sample_count,
        "batch_size": batch_size,
        "sobol_scramble_seed": seed,
        "torch_version": torch.__version__,
        "python_version": platform.python_version(),
        "numpy_version": np.__version__,
        "python_flint_version": __import__("flint").__version__,
        "pointwise_max_sampled_frobenius_error": best_norm,
        "maximum_sampled_point": best_point,
        "arb_pointwise_lower_bound": point_lower,
        "top_sampled_points": [
            {"frobenius_error": norm, "point": point} for norm, point in top
        ],
        "prior_lattice_sample_count": prior["sample_count"],
        "prior_lattice_maximum": prior["largest_sampled_gradient_error_frobenius"],
        "difference_from_prior_lattice_maximum": best_norm - prior["largest_sampled_gradient_error_frobenius"],
        "elapsed_seconds": time.monotonic() - started,
        "interpretation": "A larger Sobol value would show the prior lattice missed a stronger sampled point, not establish a continuous maximum. A matching value is only independent sampling evidence; the previous global interval upper remains too coarse.",
        "continuous_quality_verdict": "UNCERTAIN",
    }


def main():
    result = audit()
    result["tool_sha256"] = _sha(Path(__file__).read_bytes())
    result["reference_source_sha256"] = _sha(Path("tools/reference.py").read_bytes())
    result["repository_commit_at_execution"] = "2630ff2eb01c5849b54db465603a265ef5735cf7"
    result["execution_source_status"] = "untracked working-tree script at the recorded repository commit"
    path = Path("evidence/tests/physicsnemo-sobol-gradient-audit-2026-10-01.json")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
