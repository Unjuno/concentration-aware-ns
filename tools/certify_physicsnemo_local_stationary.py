"""Interval-certify one strict local maximum for a frozen PhysicsNeMo checkpoint.

The conclusion is local to a small box around a numerical candidate. It is not
a global extremum certificate or a formally verified Arb-kernel result.
"""
from __future__ import annotations

import hashlib
import io
import json
import math
import sys
import tarfile
from pathlib import Path

import numpy as np
from flint import arb, ctx

from tools.physicsnemo_arb_interval_probe import (
    _error_jet,
    quadratic_taylor_gradient_error_enclosure,
)
from tools.physicsnemo_gradient_global_cover import frobenius_lower, frobenius_upper


ARCHIVE = Path("evidence/physicsnemo-study-v1/n64-nt17.tar.gz")
CANDIDATE = Path("evidence/tests/physicsnemo-local-peak-refinement-2026-10-01.json")


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _objective_jet(gradient, hessian, third):
    """Return interval value derivatives of f=||D(u_pred-u_ref)||_F^2."""
    grad_f = [
        2 * sum((gradient[i][j] * hessian[i][j][k]
                 for i in range(3) for j in range(3)), arb(0))
        for k in range(3)
    ]
    hess_f = [[
        2 * sum((hessian[i][j][k] * hessian[i][j][ell]
                 + gradient[i][j] * third[i][j][k][ell]
                 for i in range(3) for j in range(3)), arb(0))
        for ell in range(3)] for k in range(3)]
    return grad_f, hess_f


def _det3(matrix):
    a, b, c = matrix[0]
    d, e, f = matrix[1]
    g, h, i = matrix[2]
    return a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)


def _autograd_objective_jet(state, point, *, time, sigma):
    """Independent floating-point AD sanity check, not part of the certificate."""
    import torch
    from physicsnemo.models.mlp.fully_connected import FullyConnected

    torch.set_default_dtype(torch.float64)
    torch.set_num_threads(2)
    model = FullyConnected(in_features=7, out_features=4, num_layers=3,
                           layer_size=32, activation_fn="tanh")
    model.load_state_dict(state)
    model = model.double().eval()
    direction = torch.tensor([1.0, 2.0, 3.0], dtype=torch.float64)
    x = torch.tensor(point, dtype=torch.float64, requires_grad=True)
    delta = x - torch.pi
    psi = torch.exp(((torch.cos(delta) - 1) / sigma**2).sum())
    grad_psi = -psi * torch.sin(delta) / sigma**2
    base = torch.linalg.cross(grad_psi, direction, dim=0)
    features = torch.cat((torch.sin(x), torch.cos(x), torch.ones(1, dtype=x.dtype)))
    prediction = base + time * model(features.reshape(1, 7))[0, :3]
    reference = math.exp(-time) * base
    error_gradient = torch.stack([
        torch.autograd.grad((prediction - reference)[i], x, create_graph=True,
                            retain_graph=True)[0]
        for i in range(3)
    ])
    objective = (error_gradient**2).sum()
    grad = torch.autograd.grad(objective, x, create_graph=True)[0]
    hessian = torch.stack([
        torch.autograd.grad(grad[i], x, retain_graph=True)[0]
        for i in range(3)
    ])
    return (float(objective.detach()), grad.detach().numpy(), hessian.detach().numpy())


def certify(archive=ARCHIVE, candidate=CANDIDATE, *, radius=1e-4, dps=50):
    import torch

    archive, candidate = Path(archive), Path(candidate)
    archive_bytes, candidate_bytes = archive.read_bytes(), candidate.read_bytes()
    with tarfile.open(fileobj=io.BytesIO(archive_bytes), mode="r:gz") as stream:
        parameters = json.load(stream.extractfile("parameters.json"))
        weights_bytes = stream.extractfile("weights.pt").read()
    candidate_data = json.loads(candidate_bytes)
    x0 = np.asarray(candidate_data["highest_refined_candidate"]["point"], dtype=float)
    if radius <= 0 or not math.isfinite(radius) or dps < 30:
        raise ValueError("radius must be positive and precision at least 30 dps")

    state = torch.load(io.BytesIO(weights_bytes), map_location="cpu", weights_only=True)
    if len(state["final_layer.linear.bias"]) < 3:
        raise ValueError("the frozen model has fewer than three velocity outputs")
    hidden = [
        (state[f"layers.{layer}.linear.weight"].numpy().tolist(),
         state[f"layers.{layer}.linear.bias"].numpy().tolist())
        for layer in range(3)
    ]
    output = (
        state["final_layer.linear.weight"][:3].numpy().tolist(),
        state["final_layer.linear.bias"][:3].numpy().tolist(),
    )
    time_value, sigma = float(parameters["end"]), float(parameters["sigma"])
    bounds = [(float(value - radius), float(value + radius)) for value in x0]
    old_prec = ctx.prec
    ctx.dps = dps
    try:
        box = [arb(lo).union(hi) for lo, hi in bounds]
        g_box, h_box, t_box = _error_jet(
            hidden, output, box, time=time_value, sigma=sigma,
            endpoint=time_value, include_third=True,
        )
        grad_box, hess_box = _objective_jet(g_box, h_box, t_box)
        point = [arb(float(value)) for value in x0]
        g_point, h_point, t_point = _error_jet(
            hidden, output, point, time=time_value, sigma=sigma,
            endpoint=time_value, include_third=True,
        )
        grad_point, hess_point = _objective_jet(g_point, h_point, t_point)

        midpoint_hessian = np.asarray(
            [[float(value.mid()) for value in row] for row in hess_point], dtype=float
        )
        preconditioner_float = np.linalg.inv(midpoint_hessian)
        if not np.isfinite(preconditioner_float).all():
            raise ArithmeticError("non-finite Krawczyk preconditioner")
        preconditioner = [
            [arb(float(preconditioner_float[i, j])) for j in range(3)]
            for i in range(3)
        ]
        determinant = _det3(preconditioner)
        determinant_lower = math.nextafter(float(determinant.abs_lower()), -math.inf)
        if determinant_lower <= 0:
            raise ArithmeticError("the preconditioner determinant was not separated from zero")

        displacement = [(arb(lo) - arb(float(x0[i]))).union(
                            arb(hi) - arb(float(x0[i])))
                        for i, (lo, hi) in enumerate(bounds)]
        image = []
        contraction_rows = []
        for i in range(3):
            center = arb(float(x0[i])) - sum(
                (preconditioner[i][j] * grad_point[j] for j in range(3)), arb(0)
            )
            row_sum = arb(0)
            correction = arb(0)
            for j in range(3):
                entry = (arb(1) if i == j else arb(0)) - sum(
                    (preconditioner[i][k] * hess_box[k][j] for k in range(3)), arb(0)
                )
                row_sum += entry.abs_upper()
                correction += entry * displacement[j]
            image.append(center + correction)
            contraction_rows.append(math.nextafter(float(row_sum.upper()), math.inf))

        image_bounds = []
        strict_inclusion = True
        for interval, (lo, hi) in zip(image, bounds):
            image_lo = math.nextafter(float(interval.lower()), -math.inf)
            image_hi = math.nextafter(float(interval.upper()), math.inf)
            image_bounds.append([image_lo, image_hi])
            strict_inclusion &= image_lo > lo and image_hi < hi
        contraction = max(contraction_rows)

        diagonal_upper = [math.nextafter(float(hess_box[i][i].upper()), math.inf)
                          for i in range(3)]
        diagonal_dominance_lower = []
        for i in range(3):
            margin = -hess_box[i][i] - sum(
                (hess_box[i][j].abs_upper() for j in range(3) if j != i), arb(0)
            )
            diagonal_dominance_lower.append(
                math.nextafter(float(margin.lower()), -math.inf)
            )
        negative_definite = (
            all(value < 0 for value in diagonal_upper)
            and all(value > 0 for value in diagonal_dominance_lower)
        )
        lower = frobenius_lower(g_box)
        upper = frobenius_upper(g_box)
        taylor_box = quadratic_taylor_gradient_error_enclosure(
            hidden, output, bounds, time=time_value, sigma=sigma,
            endpoint=time_value, dps=dps,
        )
        taylor_upper = frobenius_upper(taylor_box)
        candidate_lower = frobenius_lower(g_point)
        candidate_upper = frobenius_upper(g_point)
        autograd_value, autograd_grad, autograd_hessian = _autograd_objective_jet(
            state, x0, time=time_value, sigma=sigma
        )
        interval_grad_mid = np.asarray([float(value.mid()) for value in grad_point])
        interval_hess_mid = np.asarray([
            [float(value.mid()) for value in row] for row in hess_point
        ])
        autograd_value_discrepancy = abs(autograd_value - candidate_lower**2)
        autograd_gradient_discrepancy = float(
            np.max(np.abs(autograd_grad - interval_grad_mid))
        )
        autograd_hessian_discrepancy = float(
            np.max(np.abs(autograd_hessian - interval_hess_mid))
        )
        autograd_check_tolerance = 1e-6
        autograd_check_success = max(
            autograd_value_discrepancy,
            autograd_gradient_discrepancy,
            autograd_hessian_discrepancy,
        ) < autograd_check_tolerance
        result = {
            "scope": "Interval-arithmetic certificate of a unique strict local maximum of the squared gradient-error norm inside one candidate-centered box. It is not a global maximum certificate; Arb is not independently proof-kernel checked.",
            "archive_sha256": _sha(archive_bytes),
            "checkpoint_sha256": _sha(weights_bytes),
            "candidate_evidence_sha256": _sha(candidate_bytes),
            "tool_sha256": _sha(Path(__file__).read_bytes()),
            "environment": {
                "python": sys.version,
                "python_flint": "0.9.0",
                "pytorch": str(torch.__version__),
                "physicsnemo_release": "2.2.1",
                "physicsnemo_source_commit": "1b961314e42a0625502ba1592d25f706f1e02a24",
            },
            "candidate": [float(value) for value in x0],
            "box_radius": radius,
            "box": bounds,
            "precision_decimal_digits": dps,
            "objective": "f(x) = ||D_x(u_pred-u_ref)||_F^2",
            "krawczyk_image": image_bounds,
            "krawczyk_strict_inclusion": strict_inclusion,
            "krawczyk_contraction_infinity_norm_upper": contraction,
            "preconditioner_determinant_abs_lower": determinant_lower,
            "hessian_diagonal_upper_bounds": diagonal_upper,
            "hessian_strict_diagonal_dominance_margin_lower": diagonal_dominance_lower,
            "objective_hessian_negative_definite_on_box": negative_definite,
            "gradient_error_frobenius_lower_on_box": lower,
            "gradient_error_frobenius_upper_on_box": upper,
            "gradient_error_frobenius_taylor_upper_on_box": taylor_upper,
            "candidate_point_frobenius_lower": candidate_lower,
            "candidate_point_frobenius_upper": candidate_upper,
            "unique_local_maximum_value_enclosure": [candidate_lower, taylor_upper],
            "candidate_point_objective_gradient_midpoint": [
                float(value.mid()) for value in grad_point
            ],
            "independent_torch_autograd_sanity_check": {
                "objective_value": autograd_value,
                "max_objective_value_discrepancy": autograd_value_discrepancy,
                "max_objective_gradient_discrepancy": autograd_gradient_discrepancy,
                "max_objective_hessian_discrepancy": autograd_hessian_discrepancy,
                "absolute_tolerance": autograd_check_tolerance,
                "passed": autograd_check_success,
            },
            "certified_statement": "The Krawczyk map is a contraction from the box strictly into itself and its preconditioner is nonsingular, so the squared gradient-error norm has exactly one stationary point in the box. The Hessian is strictly diagonally dominant with negative diagonal throughout, so this point is the unique strict maximum in the box.",
            "success": (
                strict_inclusion and contraction < 1 and determinant_lower > 0
                and negative_definite and lower > 0 and upper >= lower
                and taylor_upper >= candidate_lower > 0
                and autograd_check_success
            ),
        }
        return result
    finally:
        ctx.prec = old_prec


def main():
    result = certify()
    target = Path("evidence/tests/physicsnemo-local-stationary-certificate-2026-10-01.json")
    target.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    return 0 if result["success"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
