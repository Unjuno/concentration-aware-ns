"""Check the N=3 uniform reference operator before prospective AMR runs."""
import hashlib
import json
from pathlib import Path

import numpy as np

from tools.amr_derivative_projection import split_derivative_error
from tools.analyze_amr_gauss_gradient import periodic_uniform_gauss_gradient
from tools.high_gradient_reference import fields
from tools.high_gradient_cell_average import exact_cell_average_velocity
from tools.amr_projection_decomposition import exact_mms_mean_square_velocity
from tools.run_amr_mean_quality import PROTOCOL, ROOT


def audit():
    spec = json.loads(PROTOCOL.read_text()); model = spec["model"]
    rows = []
    for n in sorted({c["n"] for c in spec["cases"]}):
        h = 2*np.pi/n; axis = (np.arange(n)+.5)*h
        z, y, x = np.meshgrid(axis, axis, axis, indexing="ij")
        centers = np.stack((x, y, z), axis=-1).reshape(-1, 3)
        velocity = fields(centers, N=model["frequency"], time=model["pre_map_time"])["u"]
        gradient = periodic_uniform_gauss_gradient(centers, velocity)
        split = split_derivative_error(centers, np.full(n**3, h), np.full(n**3, h**3),
                                      gradient, model["pre_map_time"], model["frequency"])
        means = exact_cell_average_velocity(centers, h, model["pre_map_time"], model["frequency"])
        velocity_error = float(np.sqrt(np.mean(np.sum((velocity-means)**2, axis=1))
            /exact_mms_mean_square_velocity(model["pre_map_time"], model["frequency"])))
        adequate = all(split[kind]["mean_mismatch_relative_l2"] <= spec["quality"][kind+"_mean_mismatch_relative_l2"]
                       for kind in ("gradient", "curl"))
        adequate = adequate and velocity_error <= spec["quality"]["velocity_mean_mismatch_relative_l2"]
        rows.append({"n": n, "reference_fd2_mean_gradient_error": split["gradient"]["mean_mismatch_relative_l2"],
                     "reference_fd2_mean_curl_error": split["curl"]["mean_mismatch_relative_l2"],
                     "reference_p0_gradient_floor": split["gradient"]["projection_floor_relative_l2"],
                     "reference_center_velocity_vs_mean_error": velocity_error,
                     "within_new_reference_mean_gate": adequate})
    if any(not row["within_new_reference_mean_gate"] for row in rows
           if row["n"] in spec["reproduction"]["adequate_counts"]):
        raise ValueError("selected fine grids fail the prospective reference-operator gate")
    return {"status": "PASS_SELECTED_REFERENCE_GRID_PRECHECK", "rows": rows,
            "protocol_sha256": hashlib.sha256(PROTOCOL.read_bytes()).hexdigest(),
            "source_sha256": {p: hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in (
                "tools/audit_amr_mean_reference_precheck.py", "tools/amr_derivative_projection.py",
                "tools/high_gradient_reference.py", "tools/analyze_amr_gauss_gradient.py",
                "tools/high_gradient_cell_average.py", "tools/amr_projection_decomposition.py")},
            "scope": "Analytic N=3 uniform centered/Gauss reference-operator precheck; no solver or mapped-mesh execution. Native captured reference operator must still verify adequacy on each actual mesh/stage."}


if __name__ == "__main__":
    result = audit()
    output = ROOT/"evidence/tests/amr-mean-quality-reference-precheck-v1.json"
    output.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(result, indent=2))
