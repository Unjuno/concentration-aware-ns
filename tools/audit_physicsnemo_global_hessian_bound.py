"""Quantify a deliberately coarse continuous-gradient Lipschitz certificate."""
import argparse
import hashlib
import io
import json
import tarfile
from fractions import Fraction
from pathlib import Path

import torch

from tools.physicsnemo_global_hessian_bound import (
    best_case_uniform_grid_nodes,
    network_hessian_entry_bound,
    total_error_hessian_entry_bound,
)


def _sha(data):
    return hashlib.sha256(data).hexdigest()


def _weights(data):
    state = torch.load(io.BytesIO(data), map_location="cpu", weights_only=True)
    hidden = [state[f"layers.{i}.linear.weight"].numpy() for i in range(3)]
    output = state["final_layer.linear.weight"].numpy()[:3]
    return state, hidden, output


def _sampled_hessian_max(state, coordinates):
    """Check the envelope against AD at fixed points; not a global proof."""
    x = torch.tensor(coordinates, dtype=torch.float64, requires_grad=True)
    features = torch.cat((torch.sin(x), torch.cos(x), torch.ones((len(x), 1), dtype=x.dtype)), dim=1)
    value = features
    for i in range(3):
        value = torch.tanh(torch.nn.functional.linear(
            value, state[f"layers.{i}.linear.weight"], state[f"layers.{i}.linear.bias"]))
    value = float(Fraction(1, 20)) * torch.nn.functional.linear(
        value, state["final_layer.linear.weight"][:3], state["final_layer.linear.bias"][:3])
    maximum = 0.0
    for component in range(3):
        gradient = torch.autograd.grad(value[:, component].sum(), x, create_graph=True, retain_graph=True)[0]
        for axis in range(3):
            hessian_row = torch.autograd.grad(gradient[:, axis].sum(), x, retain_graph=True)[0]
            maximum = max(maximum, float(hessian_row.abs().max()))
    return maximum


def audit(root=Path(".")):
    root = Path(root)
    protocol = json.loads((root / "protocols/physicsnemo-study-v1.json").read_text())
    expected_source_commit = protocol["base"]["source_commit"]
    frozen_source_protocol = json.loads((root / "protocols/physicsnemo-seed-control-v1.json").read_text())
    source_summary = json.loads((root / "evidence/physicsnemo-seed-control-v1/summary.json").read_text())
    tree_check = source_summary["source_tree_check"]
    if frozen_source_protocol["source"]["commit"] != expected_source_commit:
        raise ValueError("PhysicsNeMo study and seed-control source pins differ")
    if source_summary["source_commit"] != expected_source_commit:
        raise ValueError("PhysicsNeMo frozen run summary has a different source pin")
    if tree_check["archive_sha256"] != frozen_source_protocol["source"]["archive_sha256"] or tree_check["missing_files"] or tree_check["changed_files"]:
        raise ValueError("PhysicsNeMo frozen source-tree verification is incomplete")
    source_commit = expected_source_commit
    model_source = root / "work/physicsnemo-source/physicsnemo/models/mlp/fully_connected.py"
    trainer_source = root / "tools/train_physicsnemo_pilot.py"
    paths = sorted((root / "evidence/physicsnemo-study-v1").glob("n*-nt*.tar.gz"))
    paths += sorted((root / "evidence/physicsnemo-seed-control-v1").glob("seed*-n*-nt*.tar.gz"))
    if len(paths) != 25:
        raise ValueError(f"expected 25 frozen runs, found {len(paths)}")

    rows = []
    generator = torch.Generator(device="cpu").manual_seed(2609)
    sample_points = (torch.rand((8, 3), generator=generator, dtype=torch.float64) * (2 * torch.pi) - torch.pi).tolist()
    for archive in paths:
        raw = archive.read_bytes()
        with tarfile.open(fileobj=io.BytesIO(raw), mode="r:gz") as tar:
            parameters = json.load(tar.extractfile("parameters.json"))
            weights_data = tar.extractfile("weights.pt").read()
        if (parameters["layers"], parameters["width"], parameters["end"], parameters["sigma"], parameters["dtype"]) != (3, 32, 0.05, 0.5, "float64"):
            raise ValueError(f"unexpected architecture or endpoint in {archive.name}")
        state, hidden, output = _weights(weights_data)
        network_bound = network_hessian_entry_bound(hidden, output)
        total_bound = total_error_hessian_entry_bound(network_bound)
        nodes = best_case_uniform_grid_nodes(total_bound)
        sampled_hessian = _sampled_hessian_max(state, sample_points)
        if sampled_hessian > float(network_bound):
            raise AssertionError(f"sampled Hessian exceeds exact envelope: {archive.name}")
        rows.append({
            "case": archive.stem.removesuffix(".tar"),
            "archive_sha256": _sha(raw),
            "weights_sha256": _sha(weights_data),
            "network_hessian_entry_bound_exact": str(network_bound),
            "network_hessian_entry_bound_approx": float(network_bound),
            "sampled_hessian_entry_max_8_points": sampled_hessian,
            "sampled_to_bound_ratio": sampled_hessian / float(network_bound) if network_bound else 0.0,
            "derivative_error_hessian_entry_bound_exact": str(total_bound),
            "optimistic_nodes_per_axis": nodes,
            "optimistic_uniform_points": nodes ** 3,
        })
    nodes = [row["optimistic_nodes_per_axis"] for row in rows]
    return {
        "scope": "Exact-rational global Hessian envelope for the frozen 3-layer tanh MLP and analytic reference, used only to assess a uniform-grid Lipschitz cover. No solver is rerun and no quality verdict is assigned.",
        "source": {
            "repository": "https://github.com/NVIDIA/physicsnemo",
            "commit": source_commit,
            "archive_sha256": frozen_source_protocol["source"]["archive_sha256"],
            "frozen_run_source_tree_check": tree_check,
            "fully_connected_py_sha256": _sha(model_source.read_bytes()),
            "trainer_py_sha256": _sha(trainer_source.read_bytes()),
        },
        "method": {
            "float_weights": "Each stored binary64 parameter is converted to its exact Fraction value; all envelope propagation is rational arithmetic.",
            "network": "For each tanh layer use |tanh'|<=1 and |tanh''|<=1; propagate absolute first- and second-derivative envelopes through the three hidden affine maps and final linear map, then multiply by endpoint t=1/20.",
            "reference": "For beta=4, each third derivative of exp(beta*(cos(y)-1)) is bounded by beta+3*beta^2+beta^3=116; cross product with a=(1,2,3) gives a velocity-Hessian component bound of 580.",
            "cover": "A uniform N^3 periodic grid gives sup gradient-error <= grid-sample max + 9*pi*B/N for component Hessian bound B. The reported optimistic N assumes the grid-sample error is zero, uses pi<22/7, exact reference peak >19, and an illustrative 5% comparator only.",
            "limitations": ["The 5% value is not a preregistered PhysicsNeMo threshold and does not change old verdicts.", "This global envelope is intentionally coarse; the large N diagnoses this proof route, not the true error or impossibility of adaptive interval certification.", "An actual certificate still requires evaluating every node and outward-certified arithmetic for sampled values."]
        },
        "expected_cases": 25,
        "cases": rows,
        "nodes_per_axis_range": [min(nodes), max(nodes)],
        "optimistic_point_count_range": [min(row["optimistic_uniform_points"] for row in rows), max(row["optimistic_uniform_points"] for row in rows)],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--output", type=Path, default=Path("evidence/tests/physicsnemo-global-hessian-coverage.json"))
    args = parser.parse_args()
    result = audit(args.root)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({
        "output": str(args.output),
        "expected_cases": result["expected_cases"],
        "nodes_per_axis_range": result["nodes_per_axis_range"],
        "optimistic_point_count_range": result["optimistic_point_count_range"],
        "max_sampled_to_bound_ratio": max(row["sampled_to_bound_ratio"] for row in result["cases"]),
        "scope": result["scope"],
    }, indent=2))


if __name__ == "__main__":
    main()
