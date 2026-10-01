"""Replay the preregistered synthetic controls for diagnostic decomposition."""
import hashlib
import json
from pathlib import Path

from tools.audit_openfoam_gradient_reconstruction import synthetic_controls


def check():
    protocol_path = Path("protocols/openfoam-derivative-diagnostics-v3.json")
    protocol = json.loads(protocol_path.read_text())
    result = synthetic_controls(
        n=protocol["synthetic_controls"]["grid_cells_per_axis"],
        frequency=4,
        perturbation_amplitude=0.01,
    )
    exact = result["exact_sample_control"]
    injected = result["injected_perturbation_control"]
    if exact["computed_vs_stencil_matched_reference_gradient_relative_l2"] != 0:
        raise AssertionError("exact-sample control must have zero matched-stencil difference")
    if exact["stencil_matched_reference_vs_analytic_gradient_relative_l2"] <= 0:
        raise AssertionError("control must expose nonzero FD2 truncation floor")
    if abs(injected["computed_vs_stencil_matched_reference_gradient_relative_l2"]
           - injected["injected_field_error_expected_relative_l2"]) > 1e-14:
        raise AssertionError("injected discrete gradient difference disagrees with analytic expectation")
    result["protocol"] = str(protocol_path)
    result["protocol_sha256"] = hashlib.sha256(protocol_path.read_bytes()).hexdigest()
    result["analysis_source_sha256"] = hashlib.sha256(
        Path("tools/audit_openfoam_gradient_reconstruction.py").read_bytes()
    ).hexdigest()
    output = Path("evidence/tests/openfoam-fd2-synthetic-controls-v3.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n")
    return result


if __name__ == "__main__":
    print(json.dumps(check(), indent=2))
