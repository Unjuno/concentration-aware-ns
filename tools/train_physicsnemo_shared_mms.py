"""Train one PINN against the benchmark's shared localized high-gradient MMS."""
import argparse
import json
import logging
import os
import sys
import time
from pathlib import Path

import numpy as np
import torch

_source_root = Path("work/physicsnemo-source").resolve()
if str(_source_root) not in sys.path:
    sys.path.insert(0, str(_source_root))
from physicsnemo.models.mlp.fully_connected import FullyConnected
from physicsnemo.sym.eq.phy_informer import PhysicsInformer

from tools.high_gradient_reference import fields
from tools.physicsnemo_equations import TransientNS
from tools.physicsnemo_shared_mms import velocity_torch


def train(protocol_path, output_path, smoke_steps=None):
    protocol = json.loads(Path(protocol_path).read_text())
    output = Path(output_path)
    output.mkdir(parents=True, exist_ok=False)
    cfg = protocol["model"]
    case = protocol["_case"]
    seed = protocol["_seed"]
    n, time_nodes = case
    steps = cfg["steps"] if smoke_steps is None else smoke_steps
    if steps < 1 or (smoke_steps is not None and steps >= cfg["steps"]):
        raise ValueError("smoke steps must be positive and less than the frozen training budget")
    run_parameters = {"study_id": protocol["study_id"], "seed": seed,
                      "n": n, "time_nodes": time_nodes, "steps": steps,
                      "frozen_training_budget": cfg["steps"], "smoke_only": smoke_steps is not None}
    (output / "parameters.json").write_text(json.dumps(run_parameters, indent=2) + "\n")

    torch.set_default_dtype(torch.float64)
    torch.set_num_threads(protocol["environment"]["threads"])
    torch.manual_seed(seed)
    rng = np.random.default_rng(seed)
    net = FullyConnected(in_features=7, out_features=4, num_layers=cfg["layers"],
                         layer_size=cfg["width"], activation_fn="tanh")
    equations = TransientNS()
    informer = PhysicsInformer(required_outputs=list(equations.equations), equations=equations,
                               grad_method="autodiff", device="cpu")
    logging.getLogger("physicsnemo.sym.eq.phy_informer").setLevel(logging.ERROR)

    def output_fields(x, t):
        features = torch.cat((torch.sin(x), torch.cos(x), t / 0.05), dim=1)
        raw = net(features)
        velocity = velocity_torch(x, torch.zeros_like(t), frequency=4) + t * raw[:, :3]
        return velocity, raw[:, 3:4]

    def residual(x, t, forcing):
        velocity, pressure = output_fields(x, t)
        values = {"coordinates": x, "p": pressure}
        for i, name in enumerate(("u", "v", "w")):
            values[name] = velocity[:, i:i + 1]
            values[name + "__t"] = torch.autograd.grad(
                velocity[:, i].sum(), t, create_graph=True, retain_graph=True)[0]
        for i, name in enumerate(("x", "y", "z")):
            values["f" + name] = torch.as_tensor(forcing[:, i:i + 1], dtype=x.dtype)
        return informer.forward(values)

    optimizer = torch.optim.Adam(net.parameters(), lr=cfg["learning_rate"])
    end_time = protocol["shared_mms"]["end_time"]
    viscosity = protocol["shared_mms"]["viscosity"]
    started = time.monotonic()
    with (output / "training.jsonl").open("w") as log:
        for step in range(steps):
            ijk = rng.integers(0, n, (cfg["batch_size"], 3))
            xyz = (ijk + 0.5) * (2 * np.pi / n)
            time_index = rng.integers(0, time_nodes)
            at = float(time_index) * end_time / (time_nodes - 1)
            x = torch.tensor(xyz, requires_grad=True)
            t = torch.full((len(x), 1), at, requires_grad=True)
            force = fields(xyz, N=4, nu=viscosity, time=at)["force"]
            residuals = residual(x, t, force)
            loss = sum((value * value).mean() for value in residuals.values())
            if not torch.isfinite(loss):
                raise ValueError("nonfinite training loss")
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            if step % 25 == 0 or step == steps - 1:
                row = {"iteration": step + 1, "loss": float(loss.detach()),
                       "elapsed_seconds": time.monotonic() - started}
                log.write(json.dumps(row) + "\n")
                log.flush()
                print(row, flush=True)

    torch.save(net.state_dict(), output / "weights.pt")
    evaluation = protocol["independent_evaluation"]
    axis = (np.arange(evaluation["spatial_nodes_per_axis"]) + evaluation["fractional_cell_phase"]) * (2 * np.pi / evaluation["spatial_nodes_per_axis"])
    points = np.stack(np.meshgrid(axis, axis, axis, indexing="ij"), axis=-1).reshape(-1, 3)
    predicted_u, predicted_grad = [], []
    reference_u, reference_grad, reference_vort = [], [], []
    for start in range(0, len(points), 256):
        coords = torch.tensor(points[start:start + 256], requires_grad=True)
        t = torch.full((len(coords), 1), evaluation["time"])
        velocity, _pressure = output_fields(coords, t)
        jacobian = torch.stack([
            torch.autograd.grad(velocity[:, i].sum(), coords, retain_graph=i < 2)[0]
            for i in range(3)
        ], dim=1)
        exact = fields(points[start:start + 256], N=4, nu=viscosity,
                       time=evaluation["time"])
        predicted_u.append(velocity.detach().numpy())
        predicted_grad.append(jacobian.detach().numpy())
        reference_u.append(exact["u"])
        reference_grad.append(exact["grad_u"])
        reference_vort.append(exact["vorticity"])

    from tools.physicsnemo_validation_v2 import quality_verdict, sampled_quality_metrics
    grid_n = evaluation["spatial_nodes_per_axis"]
    metrics = sampled_quality_metrics(np.concatenate(predicted_u), np.concatenate(predicted_grad),
                                      np.concatenate(reference_u), np.concatenate(reference_grad),
                                      np.concatenate(reference_vort), (grid_n,) * 3)
    verdict = quality_verdict(metrics, evaluation["thresholds"])
    result = {"study_id": protocol["study_id"], "seed": seed, "case": f"n{n}-nt{time_nodes}",
              "optimizer_steps": steps, "training_integrity": "SMOKE_ONLY" if smoke_steps else "RUN_COMPLETE_ONLY",
              "sampled_quality": verdict, "continuous_local_quality": "UNCERTAIN",
              "metrics": metrics, "elapsed_seconds": time.monotonic() - started}
    (output / "diagnostics.json").write_text(json.dumps(result, indent=2) + "\n")
    (output / "exit_code").write_text("0\n")
    print("COMPLETE", verdict, flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--protocol", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--smoke-steps", type=int)
    args = parser.parse_args()
    train(args.protocol, args.output, args.smoke_steps)


if __name__ == "__main__":
    main()
