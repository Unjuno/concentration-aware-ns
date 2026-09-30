"""Analyze saved OpenFOAM endpoint continuity residuals on AMR/control meshes."""
import hashlib
import json
import re
from pathlib import Path

import numpy as np

from tools.analyze_amr import values
from tools.analyze_openfoam import vectors


CASES = {
    "amr-cap5000": Path("work/of13-high-gradient-amr-v2-20260930/cap5000"),
    "amr-cap100000": Path("work/of13-high-gradient-amr-v2-20260930/cap100000"),
    "fixed-cap5000-mesh": Path("work/of13-high-gradient-remap-control-v2-20260930e/cap5000"),
    "fixed-cap100000-mesh": Path("work/of13-high-gradient-remap-control-v2-20260930e/cap100000"),
}
ENDPOINT = "0.05"
DOMAIN_LENGTH = 2 * np.pi


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def analyze_case(name, case):
    endpoint = case / ENDPOINT
    c_path, u_path = endpoint / "C", endpoint / "U"
    v_path, div_path = endpoint / "Vc", endpoint / "div(phi)"
    diagnostics_path = case / "diagnostics.json"
    diagnostics = json.loads(diagnostics_path.read_text()) if diagnostics_path.is_file() else {}
    count = int(diagnostics.get("cells", 0))
    if not count:
        count = int(json.loads(case.joinpath("parameters.json").read_text()).get("mesh_cells", 0))
    if not count:
        count = int(re.search(r"List<vector>\s+(\d+)", c_path.read_text())[1])
    centers = vectors(c_path, count)
    velocity = vectors(u_path, count)
    volumes = values(v_path, count)
    div_phi = values(div_path, count)
    if not (centers.shape == velocity.shape == (count, 3)):
        raise ValueError(f"unexpected vector field shape: {name}")
    if np.any(volumes <= 0) or not np.isfinite(div_phi).all():
        raise ValueError(f"invalid volume or div(phi) value: {name}")
    domain_volume = (2 * np.pi) ** 3
    if not np.isclose(volumes.sum(), domain_volume, rtol=1e-10, atol=1e-10):
        raise ValueError(f"volume sum does not match periodic box: {name}")
    total_volume = float(volumes.sum())
    rms_div = float(np.sqrt(np.sum(volumes * div_phi**2) / total_volume))
    mean_abs_div = float(np.sum(volumes * np.abs(div_phi)) / total_volume)
    net_integral = float(np.sum(volumes * div_phi))
    rms_velocity = float(np.sqrt(np.sum(volumes * np.sum(velocity**2, axis=1)) / total_volume))
    characteristic_rate = rms_velocity / DOMAIN_LENGTH
    log_path = case / "log.foamRun"
    log_text = log_path.read_text(errors="replace")
    continuity = [
        (float(local), float(global_))
        for local, global_ in re.findall(
            r"time step continuity errors\s*:\s*sum local\s*=\s*([0-9.eE+-]+),\s*global\s*=\s*([0-9.eE+-]+)",
            log_text,
        )
    ]
    if not continuity:
        raise ValueError(f"solver continuity history is missing: {name}")
    return {
        "case": name,
        "cell_count": count,
        "domain_volume": total_volume,
        "rms_velocity": rms_velocity,
        "div_phi_volume_weighted_rms_per_second": rms_div,
        "div_phi_volume_weighted_mean_abs_per_second": mean_abs_div,
        "div_phi_max_abs_per_second": float(np.max(np.abs(div_phi))),
        "integrated_div_phi": net_integral,
        "characteristic_velocity_over_box_length_per_second": characteristic_rate,
        "rms_div_phi_over_characteristic_rate": float(rms_div / characteristic_rate),
        "mean_abs_div_phi_over_characteristic_rate": float(mean_abs_div / characteristic_rate),
        "solver_log_continuity_records": len(continuity),
        "solver_log_max_sum_local": max(local for local, _ in continuity),
        "solver_log_max_abs_global": max(abs(global_) for _, global_ in continuity),
        "solver_log_final_sum_local": continuity[-1][0],
        "solver_log_final_global": continuity[-1][1],
        "field_sha256": {
            str(path.relative_to(case)): sha256(path)
            for path in (c_path, u_path, v_path, div_path, endpoint / "phi")
        },
        "postprocess_log_sha256": sha256(case / "log.divphi-container"),
        "solver_log_sha256": sha256(log_path),
        "interpretation_scope": "Endpoint face-flux continuity diagnostic only; it does not measure momentum error, temporal divergence history, or identify a particular remapping defect.",
    }


def main():
    results = [analyze_case(name, case) for name, case in CASES.items()]
    output = {
        "source_commit": "18870c24d21c6b982e2cdec27b2f59738cca5f90",
        "container_image_id": "sha256:dd2b2eb63b12896a9b6e7a46563ed96b26d1c78c3e3749536d40d456895f722b",
        "postprocess": "OpenFOAM Foundation 13 foamPostProcess -func div(phi) -latestTime",
        "weighting": "Cell-volume-weighted endpoint metrics on the saved periodic meshes.",
        "cases": results,
        "scope": "Read-only post-processing of completed AMR and fixed-final-mesh runs; not a new solver execution or an acceptance verdict.",
    }
    target = Path("evidence/of13-high-gradient-amr-flux-balance-2026-09-30.json")
    target.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
