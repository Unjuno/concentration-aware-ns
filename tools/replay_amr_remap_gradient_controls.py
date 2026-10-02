"""Replay Foundation-13 gradient/curl diagnostics on matched AMR controls.

The archived dynamic-AMR case and its fixed-final-mesh control are extracted
from their source archives, post-processed with the recorded OpenFOAM image,
then compared with the same analytic point derivatives and interior mask.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tarfile

import numpy as np

from tools.analyze_amr import values
from tools.analyze_amr_gauss_gradient import (
    interior_periodic_mask,
    relative_volume_l2,
    vorticity_from_gradient,
)
from tools.analyze_openfoam import vectors
from tools.high_gradient_reference import fields


ROOT = Path(__file__).resolve().parents[1]
IMAGE = "sha256:dd2b2eb63b12896a9b6e7a46563ed96b26d1c78c3e3749536d40d456895f722b"
SOURCE_COMMIT = "18870c24d21c6b982e2cdec27b2f59738cca5f90"
SOURCE_FILE_SHA256 = {
    "src/finiteVolume/finiteVolume/gradSchemes/gaussGrad/gaussGrad.C":
        "9e419df4d574a4dc48ccd4eba02007e995ece0ef21e98895d16adc67bcc39380",
    "src/finiteVolume/finiteVolume/fvc/fvcCurl.C":
        "57532eaee1ddeed718675d2351c0d3186db2128c1500d15471780027f01c0e17",
    "src/OpenFOAM/primitives/Tensor/TensorI.H":
        "689d7ab3c086d28284155d3173b7ae986ac823414af3f23b7e5bc363f3fdd30d",
}
CASES = {
    "dynamic-cap5000": (
        "cap5000",
        "evidence/of13-high-gradient-amr-v2-2026-09-30/cap5000.tar.gz",
        "evidence/of13-high-gradient-amr-v2-manifest-2026-09-30.json",
        "evidence/of13-high-gradient-amr-v2-2026-09-30/cap5000.tar.gz",
    ),
    "control-cap5000": (
        "cap5000",
        "evidence/of13-high-gradient-remap-control-v2-2026-09-30/cap5000.tar.gz",
        "evidence/of13-high-gradient-remap-control-v2-manifest-2026-09-30.json",
        "evidence/of13-high-gradient-remap-control-v2-2026-09-30/cap5000.tar.gz",
    ),
    "dynamic-cap100000": (
        "cap100000",
        "evidence/of13-high-gradient-amr-v2-2026-09-30/cap100000.tar.gz",
        "evidence/of13-high-gradient-amr-v2-manifest-2026-09-30.json",
        "evidence/of13-high-gradient-amr-v2-2026-09-30/cap100000.tar.gz",
    ),
    "control-cap100000": (
        "cap100000",
        "evidence/of13-high-gradient-remap-control-v2-2026-09-30/cap100000.tar.gz",
        "evidence/of13-high-gradient-remap-control-v2-manifest-2026-09-30.json",
        "evidence/of13-high-gradient-remap-control-v2-2026-09-30/cap100000.tar.gz",
    ),
}
EVIDENCE_OUT = Path("evidence/of13-amr-remap-gradient-controls-2026-10-02")
DOMAIN_LENGTH = 2 * np.pi
BASE_N = 16
END_TIME = 0.05
FREQUENCY = 4
VISCOSITY = 0.01
PROTOCOL = Path("protocols/high-gradient-of13-v2.json")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def openfoam_gradient_to_math_convention(gradient: np.ndarray) -> np.ndarray:
    """Convert OpenFOAM's derivative-index-first tensor to dU_i/dx_j."""
    gradient = np.asarray(gradient, dtype=float)
    if gradient.ndim != 3 or gradient.shape[1:] != (3, 3):
        raise ValueError("gradient must have shape (cells, 3, 3)")
    return gradient.transpose(0, 2, 1)


def _manifest_archive_hash(manifest_path: Path, case_name: str) -> str:
    manifest = json.loads(manifest_path.read_text())
    rows = manifest.get("cases", [])
    row = next((item for item in rows if item.get("case") == case_name), None)
    if row is None:
        raise ValueError(f"{case_name} missing from {manifest_path}")
    return row["raw_archive_sha256"]


def _extract(archive: Path, destination: Path, expected_root: str) -> Path:
    destination.mkdir(parents=True, exist_ok=False)
    with tarfile.open(archive, "r:gz") as tf:
        members = tf.getmembers()
        for member in members:
            path = Path(member.name)
            if path.is_absolute() or ".." in path.parts:
                raise ValueError(f"unsafe archive member: {member.name}")
            if path.parts and path.parts[0] != expected_root:
                raise ValueError(f"unexpected archive root: {member.name}")
        tf.extractall(destination, members=members, filter="data")
    case = destination / expected_root
    if not case.is_dir():
        raise ValueError(f"missing extracted case root {case}")
    return case


def _mesh_path(case: Path, time: str, name: str) -> Path:
    candidates = (case / time / "polyMesh" / name,
                  case / "constant" / "polyMesh" / name)
    return next((path for path in candidates if path.is_file()), candidates[0])


def _check_matching_mesh(dynamic: Path, control: Path, time: str) -> dict:
    names = ("points", "faces", "owner", "neighbour", "boundary")
    hashes = {}
    for name in names:
        left = _mesh_path(dynamic, time, name)
        right = _mesh_path(control, time, name)
        if not left.is_file() or not right.is_file():
            raise ValueError(f"missing mesh file {name}")
        left_hash, right_hash = sha256_file(left), sha256_file(right)
        if left_hash != right_hash:
            raise ValueError(f"dynamic/control mesh differs at {name}")
        hashes[name] = left_hash
    dynamic_schemes = dynamic / "system" / "fvSchemes"
    control_schemes = control / "system" / "fvSchemes"
    schemes_hash = sha256_file(dynamic_schemes)
    if schemes_hash != sha256_file(control_schemes):
        raise ValueError("dynamic/control fvSchemes differ")
    hashes["system/fvSchemes"] = schemes_hash
    return hashes


def _case_metrics(case: Path, interior_mask: np.ndarray | None = None) -> tuple[dict, dict]:
    folder = case / f"{END_TIME:g}"
    volume_path = folder / "Vc"
    count_match = re.search(r"List<vector>\s+(\d+)", (folder / "C").read_text())
    if count_match is None:
        raise ValueError(f"cannot read cell count from {folder / 'C'}")
    count = int(count_match.group(1))
    volumes = values(volume_path, count=count)
    centers = vectors(folder / "C", count)
    velocity = vectors(folder / "U", count)
    if not np.isclose(volumes.sum(), DOMAIN_LENGTH**3, rtol=1e-10, atol=1e-10):
        raise ValueError("cell volumes do not cover the periodic domain")
    if interior_mask is None:
        interior_mask = interior_periodic_mask(
            centers, volumes, domain_length=DOMAIN_LENGTH,
            boundary_margin=2 * DOMAIN_LENGTH / BASE_N,
        )
    exact = fields(centers, N=FREQUENCY, nu=VISCOSITY, time=END_TIME)
    foam_gradient = values(folder / "grad(U)", count, 9).reshape(-1, 3, 3)
    gradient = openfoam_gradient_to_math_convention(foam_gradient)
    vorticity = vectors(folder / "vorticity", count)
    reconstructed_vorticity = vorticity_from_gradient(gradient)
    curl_agreement = relative_volume_l2(
        vorticity, reconstructed_vorticity, volumes, interior_mask
    )
    if curl_agreement > 1e-12:
        raise ValueError(f"OpenFOAM vorticity disagrees with grad(U): {curl_agreement}")
    metrics = {
        "cells": count,
        "interior_cells": int(interior_mask.sum()),
        "interior_volume_fraction": float(
            volumes[interior_mask].sum() / volumes.sum()
        ),
        "velocity_relative_l2_all": float(np.sqrt(
            np.sum(volumes * np.sum((velocity - exact["u"])**2, axis=1))
            / np.sum(volumes * np.sum(exact["u"]**2, axis=1))
        )),
        "gradient_relative_l2_interior": relative_volume_l2(
            gradient, exact["grad_u"], volumes, interior_mask
        ),
        "vorticity_relative_l2_interior": relative_volume_l2(
            vorticity, exact["vorticity"], volumes, interior_mask
        ),
        "gradient_max_abs_component_error_interior": float(np.max(np.abs(
            gradient[interior_mask] - exact["grad_u"][interior_mask]
        ))),
        "vorticity_max_abs_component_error_interior": float(np.max(np.abs(
            vorticity[interior_mask] - exact["vorticity"][interior_mask]
        ))),
        "foam_vorticity_vs_curl_of_transposed_grad_relative_l2": curl_agreement,
        "grad_U_sha256": sha256_file(folder / "grad(U)"),
        "vorticity_sha256": sha256_file(folder / "vorticity"),
    }
    return metrics, interior_mask


def replay(work_root: Path) -> dict:
    docker = shutil.which("docker")
    if docker is None:
        raise RuntimeError("docker CLI is required for pinned Foundation post-processing")
    inspect = subprocess.run(
        [docker, "image", "inspect", IMAGE, "--format", "{{.Id}} {{.Os}}/{{.Architecture}}"],
        check=True, capture_output=True, text=True, timeout=15,
    ).stdout.strip()
    image_id, platform = inspect.split(maxsplit=1)
    if image_id != IMAGE or platform != "linux/arm64":
        raise RuntimeError(f"runtime mismatch: {inspect}")
    work_root.mkdir(parents=True, exist_ok=True)
    extracted = {}
    archive_info = {}
    for key, (case_name, archive_rel, manifest_rel, tracked_archive_rel) in CASES.items():
        archive = ROOT / archive_rel
        manifest_path = ROOT / manifest_rel
        actual_hash = sha256_file(archive)
        expected_hash = _manifest_archive_hash(manifest_path, case_name)
        if actual_hash != expected_hash:
            raise ValueError(f"archive hash differs from manifest: {archive_rel}")
        case = _extract(archive, work_root / key, case_name)
        extracted[key] = case
        archive_info[key] = {
            "path": tracked_archive_rel,
            "sha256": actual_hash,
            "manifest": manifest_rel,
        }
    uid = str(os.getuid())
    gid = str(os.getgid())
    for key, case in extracted.items():
        case = case.resolve()
        command = [
            docker, "run", "--rm", "--network", "none", "--user", f"{uid}:{gid}",
            "-v", f"{case}:/case", "--entrypoint", "/bin/bash", IMAGE,
            "-lc", "source /opt/openfoam13/etc/bashrc && "
            'foamPostProcess -case /case -time 0.05 -funcs "(grad(U) vorticity)"',
        ]
        proc = subprocess.run(command, capture_output=True, text=True, timeout=120)
        log = (proc.stdout + proc.stderr).rstrip() + "\n"
        (work_root / key / "postprocess.log").write_text(log)
        if proc.returncode or not log.rstrip().endswith("End"):
            raise RuntimeError(f"post-processing failed for {key}: {log[-2000:]}")

    comparisons = {}
    for cap in ("cap5000", "cap100000"):
        dynamic_key, control_key = f"dynamic-{cap}", f"control-{cap}"
        dynamic, control = extracted[dynamic_key], extracted[control_key]
        mesh_hashes = _check_matching_mesh(dynamic, control, "0.05")
        dynamic_metrics, mask = _case_metrics(dynamic)
        control_metrics, control_mask = _case_metrics(control)
        if not np.array_equal(mask, control_mask):
            raise ValueError(f"dynamic/control interior masks differ for {cap}")
        dynamic_centers = vectors(dynamic / "0.05" / "C", dynamic_metrics["cells"])
        control_centers = vectors(control / "0.05" / "C", control_metrics["cells"])
        if not np.array_equal(dynamic_centers, control_centers):
            raise ValueError(f"dynamic/control cell centers differ for {cap}")
        dynamic_volumes = values(dynamic / "0.05" / "Vc", dynamic_metrics["cells"])
        control_volumes = values(control / "0.05" / "Vc", control_metrics["cells"])
        if not np.array_equal(dynamic_volumes, control_volumes):
            raise ValueError(f"dynamic/control cell volumes differ for {cap}")
        comparisons[cap] = {
            "mesh_file_sha256": mesh_hashes,
            "cell_centers_and_volumes_exactly_equal": True,
            "dynamic": dynamic_metrics,
            "fixed_final_mesh_control": control_metrics,
        }
        # Reprocessing the dynamic case must reproduce its archived solver field.
        _, archive_rel, _, _ = CASES[dynamic_key]
        archive = ROOT / archive_rel
        with tarfile.open(archive, "r:gz") as tf:
            original = tf.extractfile(f"{cap}/0.05/grad(U)")
            if original is None:
                raise ValueError(f"missing archived grad(U) for {cap}")
            original_bytes = original.read()
        post_bytes = (dynamic / "0.05" / "grad(U)").read_bytes()
        comparisons[cap]["dynamic"]["original_solver_grad_byte_identical"] = (
            original_bytes == post_bytes
        )
        if original_bytes != post_bytes:
            raise ValueError(f"post-process grad(U) differs from archived field for {cap}")

    docker_context = subprocess.run(
        [docker, "context", "show"], check=True, capture_output=True,
        text=True, timeout=15,
    ).stdout.strip()
    result = {
        "status": "REPLAYED_SAME_MESH_AMR_DERIVATIVE_COMPARISON",
        "scope": "Two Foundation-13 n=16 AMR endpoint meshes, each compared with its analytic-initialized fixed-final-mesh control; archived cases only, no solver integration rerun.",
        "runtime": {
            "image_id": image_id,
            "platform": platform,
            "docker_context": docker_context,
            "postprocess": "foamPostProcess -time 0.05 -funcs '(grad(U) vorticity)'",
            "postprocess_log_normalization": "Captured output trailing whitespace is trimmed and exactly one final LF is retained.",
            "openfoam_package": "Foundation 13, package 20260624, arm64",
            "package_sha256": "6da0f6460fbc33c8995cbc97caba52c6cb0342f52ed02ff57530d9d62e9ef360",
            "runtime_dockerfile_sha256": sha256_file(ROOT / "runtime/openfoam13/Dockerfile"),
            "protocol": PROTOCOL.as_posix(),
            "protocol_sha256": sha256_file(ROOT / PROTOCOL),
            "source_commit": SOURCE_COMMIT,
            "source_files_sha256": SOURCE_FILE_SHA256,
            "tensor_convention": "OpenFOAM grad(U) is outerProduct<vector,vector> from Sf * U; transpose the derivative-index-first storage to compare against dU_i/dx_j. OpenFOAM vorticity is checked against the curl of that transposed tensor.",
        },
        "inputs": archive_info,
        "comparisons": comparisons,
        "limitations": [
            "The fixed-final-mesh controls begin with the analytic field on the already-refined mesh. They do not isolate mapping alone from the subsequent evolution in the dynamic-AMR cases.",
            "Gradient and vorticity compare Gauss-linear cell fields with exact point derivatives at cell centers on a common interior mask; no continuous maximum or cell-average derivative norm is certified.",
            "This is a reproduced benchmark-path difference, not an upstream defect verdict. AMR quality attribution remains UNCERTAIN; no physical, singularity, or molecular inference follows.",
        ],
    }
    EVIDENCE_OUT.mkdir(parents=True, exist_ok=True)
    for key in CASES:
        log_path = work_root / key / "postprocess.log"
        if log_path.is_file():
            shutil.copy2(log_path, ROOT / EVIDENCE_OUT / f"{key}-postprocess.log")
            result.setdefault("postprocess_logs_sha256", {})[key] = sha256_file(log_path)
    output = ROOT / EVIDENCE_OUT / "comparison.json"
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--work-root", type=Path,
        default=Path("work/of13-amr-remap-gradient-replay"),
        help="existing empty path where archived cases are extracted",
    )
    args = parser.parse_args()
    if args.work_root.exists() and any(args.work_root.iterdir()):
        parser.error("work-root must be empty or absent; choose a fresh path")
    result = replay(args.work_root)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
