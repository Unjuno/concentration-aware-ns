"""Prospective held-out evaluation helpers for archived PhysicsNeMo PINNs."""

import math
import argparse
import hashlib
import io
import json
import importlib.metadata
import platform
import subprocess
import tarfile
from pathlib import Path

import numpy as np

from tools.metrics import diagnostics


ROOT = Path(__file__).resolve().parents[1]


def validation_grid(n, phase):
    """Return a periodic n^3 grid at a fixed fractional-cell phase."""
    if not isinstance(n, int) or isinstance(n, bool) or n < 4:
        raise ValueError("n must be an integer >= 4")
    if not isinstance(phase, (int, float)) or not math.isfinite(phase) or not 0 <= phase < 1:
        raise ValueError("phase must be finite and in [0, 1)")
    axis = (np.arange(n, dtype=float) + phase) * (2 * np.pi / n)
    return np.stack(np.meshgrid(axis, axis, axis, indexing="ij"), axis=-1).reshape(-1, 3)


def quality_verdict(metrics, thresholds):
    """Apply inclusive sampled-quality limits; this does not certify extrema."""
    if not isinstance(metrics, dict) or not isinstance(thresholds, dict) or not thresholds:
        raise ValueError("metrics and nonempty thresholds must be mappings")
    missing = sorted(set(thresholds) - set(metrics))
    if missing:
        raise ValueError(f"missing metrics: {missing}")
    for name, threshold in thresholds.items():
        value = metrics[name]
        if (not isinstance(value, (int, float)) or isinstance(value, bool)
                or not math.isfinite(value) or value < 0):
            raise ValueError(f"metric {name} must be finite nonnegative")
        if (not isinstance(threshold, (int, float)) or isinstance(threshold, bool)
                or not math.isfinite(threshold) or threshold < 0):
            raise ValueError(f"threshold {name} must be finite nonnegative")
    return "PASS" if all(metrics[name] <= limit for name, limit in thresholds.items()) else "FAIL"


def sampled_quality_metrics(
    predicted_velocity,
    predicted_gradient,
    reference_velocity,
    reference_gradient,
    reference_vorticity,
    grid_shape,
):
    """Compare sampled fields and spectra on one matched periodic grid."""
    predicted_velocity = np.asarray(predicted_velocity, dtype=float)
    reference_velocity = np.asarray(reference_velocity, dtype=float)
    predicted_gradient = np.asarray(predicted_gradient, dtype=float)
    reference_gradient = np.asarray(reference_gradient, dtype=float)
    reference_vorticity = np.asarray(reference_vorticity, dtype=float)
    size = int(np.prod(grid_shape))
    if (len(grid_shape) != 3 or any(not isinstance(n, int) or n < 4 for n in grid_shape)
            or predicted_velocity.shape != (size, 3)
            or reference_velocity.shape != (size, 3)
            or predicted_gradient.shape != (size, 3, 3)
            or reference_gradient.shape != (size, 3, 3)
            or reference_vorticity.shape != (size, 3)):
        raise ValueError("sample arrays must match the declared 3D grid and vector/tensor shapes")
    arrays = (predicted_velocity, reference_velocity, predicted_gradient,
              reference_gradient, reference_vorticity)
    if any(not np.isfinite(array).all() for array in arrays):
        raise ValueError("sample arrays must be finite")

    pred_grad_norm = np.linalg.norm(predicted_gradient, axis=(-2, -1))
    ref_grad_norm = np.linalg.norm(reference_gradient, axis=(-2, -1))
    pred_vorticity = np.stack((
        predicted_gradient[:, 2, 1] - predicted_gradient[:, 1, 2],
        predicted_gradient[:, 0, 2] - predicted_gradient[:, 2, 0],
        predicted_gradient[:, 1, 0] - predicted_gradient[:, 0, 1],
    ), axis=-1)
    pred_omega_norm = np.linalg.norm(pred_vorticity, axis=-1)
    ref_omega_norm = np.linalg.norm(reference_vorticity, axis=-1)
    ref_energy = 0.5 * np.mean(np.sum(reference_velocity**2, axis=-1))
    ref_grad_peak = float(ref_grad_norm.max())
    ref_omega_peak = float(ref_omega_norm.max())
    if ref_energy <= 0 or ref_grad_peak <= 0 or ref_omega_peak <= 0:
        raise ValueError("reference energy and sampled derivative peaks must be positive")

    pred_grid = predicted_velocity.reshape(*grid_shape, 3)
    ref_grid = reference_velocity.reshape(*grid_shape, 3)
    pred_spectrum = np.asarray(diagnostics(pred_grid)["shell_energy"])
    ref_spectrum = np.asarray(diagnostics(ref_grid)["shell_energy"])
    if pred_spectrum.shape != ref_spectrum.shape:
        raise ValueError("predicted and reference shell spectra have different shapes")

    return {
        "velocity_relative_l2": float(np.linalg.norm(predicted_velocity - reference_velocity)
                                      / np.linalg.norm(reference_velocity)),
        "energy_relative_error": float(abs(0.5 * np.mean(np.sum(predicted_velocity**2, axis=-1))
                                           - ref_energy) / ref_energy),
        "gradient_peak_relative_error_samples": float(abs(pred_grad_norm.max() - ref_grad_peak)
                                                       / ref_grad_peak),
        "vorticity_peak_relative_error_samples": float(abs(pred_omega_norm.max() - ref_omega_peak)
                                                         / ref_omega_peak),
        "shell_spectrum_relative_l1": float(np.abs(pred_spectrum - ref_spectrum).sum()
                                             / ref_spectrum.sum()),
        "divergence_peak_normalized": float(np.abs(np.trace(predicted_gradient, axis1=-2, axis2=-1)).max()
                                             / ref_grad_peak),
    }


def _sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _model_archives(protocol):
    baseline_root = ROOT / protocol["model_artifacts"]["baseline_directory"]
    baseline = json.loads((baseline_root / "summary.json").read_text())
    if baseline.get("completed_cases") != protocol["model_artifacts"]["expected_cases"] and not (
        isinstance(baseline.get("completed_cases"), int)
        and baseline["completed_cases"] == len(protocol["model_artifacts"]["expected_cases"])
    ):
        raise ValueError("baseline model summary does not contain all expected cases")
    control_root = ROOT / protocol["model_artifacts"]["seed_control_directory"]
    control = json.loads((control_root / "summary.json").read_text())
    if control.get("status") != "COMPLETE" or control.get("completed_runs") != 20:
        raise ValueError("paired-seed model summary is incomplete")
    records = []
    for row in baseline["cases"]:
        name = row["case"]
        archive = baseline_root / f"{name}.tar.gz"
        records.append({"seed": 709, "case": name, "archive": archive,
                        "archive_sha256": row["archive_sha256"]})
    for row in control["runs"]:
        name = row["case"]
        archive = control_root / f"{name}.tar.gz"
        records.append({"seed": row["seed"], "case": f"n{row['n']}-nt{row['time_nodes']}",
                        "archive": archive, "archive_sha256": row["archive_sha256"]})
    expected = protocol["model_artifacts"]["expected_models"]
    expected_pairs = {(seed, case) for seed in protocol["model_artifacts"]["expected_seeds"]
                      for case in protocol["model_artifacts"]["expected_cases"]}
    actual_pairs = {(row["seed"], row["case"]) for row in records}
    if len(records) != expected or actual_pairs != expected_pairs:
        raise ValueError("archived models do not match the preregistered seed/case matrix")
    for row in records:
        if _sha256(row["archive"]) != row["archive_sha256"]:
            raise ValueError(f"model archive hash mismatch: {row['archive']}")
    return records


def _read_archive(archive_path):
    with tarfile.open(archive_path, "r:gz") as archive:
        members = {Path(member.name).name: member for member in archive.getmembers()
                   if member.isfile()}
        required = {"parameters.json", "weights.pt", "training.jsonl", "exit_code"}
        if not required.issubset(members):
            raise ValueError(f"model archive missing {sorted(required - set(members))}")
        def read(name):
            stream = archive.extractfile(members[name])
            if stream is None:
                raise ValueError(f"cannot read {name} from model archive")
            return stream.read()
        return {name: read(name) for name in required}


def evaluate_archive(record, protocol, batch_size=512):
    """Evaluate one frozen checkpoint on the preregistered shifted grid."""
    import torch
    from physicsnemo.models.mlp.fully_connected import FullyConnected
    from tools.reference import fields

    files = _read_archive(record["archive"])
    params = json.loads(files["parameters.json"])
    train_rows = [json.loads(line) for line in files["training.jsonl"].splitlines() if line]
    if (files["exit_code"].decode().strip() != "0" or not train_rows
            or train_rows[-1].get("iteration") != protocol["model_artifacts"]["training_budget_steps"]):
        raise ValueError(f"training integrity gate failed: {record['case']} seed={record['seed']}")
    if (params.get("seed") != record["seed"]
            or params.get("n") * 1 != int(record["case"].split("-")[0][1:])
            or params.get("time_nodes") * 1 != int(record["case"].split("nt")[1])):
        raise ValueError(f"model parameters do not match index: {record['case']} seed={record['seed']}")
    final_loss = train_rows[-1].get("loss")
    if not isinstance(final_loss, (int, float)) or not math.isfinite(final_loss):
        raise ValueError("final training loss is not finite")

    torch.set_default_dtype(torch.float64)
    torch.set_num_threads(2)
    net = FullyConnected(in_features=7, out_features=4, num_layers=params["layers"],
                         layer_size=params["width"], activation_fn="tanh")
    state = torch.load(io.BytesIO(files["weights.pt"]), map_location="cpu", weights_only=True)
    if any(not torch.isfinite(value).all() for value in state.values()):
        raise ValueError("checkpoint has a nonfinite tensor")
    net.load_state_dict(state)
    net.eval()

    evaluation = protocol["independent_evaluation"]
    points = validation_grid(evaluation["spatial_nodes_per_axis"],
                             evaluation["fractional_cell_phase"])
    time = evaluation["time"]
    predicted_u, predicted_grad = [], []
    reference_u, reference_grad, reference_vort = [], [], []
    for start in range(0, len(points), batch_size):
        chunk = points[start:start + batch_size]
        x = torch.tensor(chunk, requires_grad=True)
        t = torch.full((len(x), 1), time)
        psi = torch.exp(((torch.cos(x - torch.pi) - 1) / params["sigma"]**2).sum(dim=1, keepdim=True))
        grad_psi = -psi * torch.sin(x - torch.pi) / params["sigma"]**2
        u0 = torch.linalg.cross(grad_psi, torch.tensor([1., 2., 3.]).expand_as(grad_psi))
        raw = net(torch.cat((torch.sin(x), torch.cos(x), t / params["end"]), dim=1))
        velocity = u0 + t * raw[:, :3]
        jacobian = torch.stack([
            torch.autograd.grad(velocity[:, i].sum(), x, retain_graph=(i < 2))[0]
            for i in range(3)
        ], dim=1)
        reference = fields(chunk, time, sigma=params["sigma"], nu=params["nu"])
        predicted_u.append(velocity.detach().numpy())
        predicted_grad.append(jacobian.detach().numpy())
        reference_u.append(reference["u"])
        reference_grad.append(reference["grad_u"])
        reference_vort.append(reference["vorticity"])

    predicted_u = np.concatenate(predicted_u)
    predicted_grad = np.concatenate(predicted_grad)
    reference_u = np.concatenate(reference_u)
    reference_grad = np.concatenate(reference_grad)
    reference_vort = np.concatenate(reference_vort)
    grid_n = evaluation["spatial_nodes_per_axis"]
    thresholds = protocol["sampled_quality_thresholds"]
    metrics = sampled_quality_metrics(predicted_u, predicted_grad, reference_u,
                                      reference_grad, reference_vort,
                                      (grid_n, grid_n, grid_n))
    local_names = ("gradient_peak_relative_error_samples",
                   "vorticity_peak_relative_error_samples", "divergence_peak_normalized")
    global_names = ("velocity_relative_l2", "energy_relative_error",
                    "shell_spectrum_relative_l1")
    local = quality_verdict({name: metrics[name] for name in local_names},
                            {name: thresholds[name] for name in local_names})
    global_quality = quality_verdict({name: metrics[name] for name in global_names},
                                     {name: thresholds[name] for name in global_names})
    return {
        "seed": record["seed"], "case": record["case"],
        "archive": str(record["archive"].relative_to(ROOT)),
        "archive_sha256": record["archive_sha256"],
        "checkpoint_sha256": hashlib.sha256(files["weights.pt"]).hexdigest(),
        "training_integrity": "RUN_COMPLETE_ONLY",
        "optimizer_steps": train_rows[-1]["iteration"],
        "final_training_loss": final_loss,
        "metrics": metrics,
        "global_sampled_quality": global_quality,
        "local_sampled_quality": local,
        "overall_sampled_quality": quality_verdict(metrics, thresholds),
        "sampled_blind_spot": ("REPRODUCED" if global_quality == "PASS" and local == "FAIL"
                                else "NOT_OBSERVED" if global_quality == "PASS" and local == "PASS"
                                else "UNCERTAIN"),
        "continuous_local_quality": "UNCERTAIN",
    }


def run(protocol_path, output_path, batch_size=512):
    protocol_path = Path(protocol_path)
    if not protocol_path.is_absolute():
        protocol_path = ROOT / protocol_path
    protocol_bytes = protocol_path.read_bytes()
    protocol = json.loads(protocol_bytes)
    if protocol.get("status") != "frozen-before-independent-evaluation":
        raise ValueError("protocol is not frozen for evaluation")
    if protocol["source"]["commit"] != "1b961314e42a0625502ba1592d25f706f1e02a24":
        raise ValueError("unexpected pinned PhysicsNeMo source commit")
    if platform.python_version() != protocol["environment"]["python"]:
        raise ValueError("Python version does not match frozen validation environment")
    if importlib.metadata.version("torch") != protocol["environment"]["torch"]:
        raise ValueError("Torch version does not match frozen validation environment")
    if batch_size != protocol["environment"]["batch_size"]:
        raise ValueError("batch size does not match frozen validation environment")
    status = subprocess.run(["git", "status", "--porcelain"], cwd=ROOT,
                            text=True, capture_output=True, check=True).stdout
    if status.strip():
        raise ValueError("repository worktree must be clean before frozen evaluation")
    harness_commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT,
                                    text=True, capture_output=True, check=True).stdout.strip()

    source_archive = ROOT / protocol["source"]["source_archive"]
    source_root = ROOT / protocol["source"]["source_root"]
    from tools.physicsnemo_seed_control import verify_source_tree
    source_check = verify_source_tree(source_archive, source_root,
                                      protocol["source"]["source_archive_sha256"])
    if (source_check["changed_files"] or source_check["missing_files"]
            or source_check["matching_files"] != protocol["source"]["expected_regular_files"]):
        raise ValueError("pinned PhysicsNeMo source tree changed")

    records = _model_archives(protocol)
    results = []
    for index, record in enumerate(records, start=1):
        result = evaluate_archive(record, protocol, batch_size)
        results.append(result)
        print(f"EVALUATED {index}/{len(records)} seed={record['seed']} case={record['case']} "
              f"quality={result['overall_sampled_quality']}", flush=True)
    outcome = {
        "study_id": protocol["study_id"],
        "status": "COMPLETE",
        "protocol_sha256": hashlib.sha256(protocol_bytes).hexdigest(),
        "source_commit": protocol["source"]["commit"],
        "source_archive_sha256": source_check["archive_sha256"],
        "source_tree_check": source_check,
        "harness_commit": harness_commit,
        "evaluator_sha256": _sha256(Path(__file__)),
        "reference_sha256": _sha256(ROOT / "tools/reference.py"),
        "metrics_sha256": _sha256(ROOT / "tools/metrics.py"),
        "environment": {"python": platform.python_version(),
                        "torch": importlib.metadata.version("torch"),
                        "platform": platform.platform(), "device": "cpu"},
        "evaluation_grid": {
            "nodes_per_axis": protocol["independent_evaluation"]["spatial_nodes_per_axis"],
            "phase": protocol["independent_evaluation"]["fractional_cell_phase"],
            "time": protocol["independent_evaluation"]["time"],
            "point_count": protocol["independent_evaluation"]["spatial_nodes_per_axis"]**3,
        },
        "expected_models": protocol["model_artifacts"]["expected_models"],
        "completed_models": len(results),
        "results": results,
        "scope": "Prospective finite-grid validation of frozen archived checkpoints under common preregistered thresholds; does not certify continuous extrema, optimizer convergence, or physical consequences.",
    }
    output_path = Path(output_path)
    if not output_path.is_absolute():
        output_path = ROOT / output_path
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if output_path.exists():
        raise FileExistsError(f"refusing to overwrite frozen evaluation: {output_path}")
    output_path.write_text(json.dumps(outcome, indent=2) + "\n")
    return outcome


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--protocol", default="protocols/physicsnemo-heldout-validation-v2.json")
    parser.add_argument("--output", default="evidence/physicsnemo-heldout-validation-v2/results.json")
    parser.add_argument("--batch-size", type=int, default=512)
    args = parser.parse_args()
    result = run(args.protocol, args.output, args.batch_size)
    print(json.dumps({"status": result["status"], "completed_models": result["completed_models"],
                      "output": args.output}, indent=2))


if __name__ == "__main__":
    main()
