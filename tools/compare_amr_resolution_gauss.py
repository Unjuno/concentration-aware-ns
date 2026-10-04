"""Compare same-run AMR gradient/curl diagnostics on one shared physical mask.

This is a reconstruction diagnostic, not a solver-quality certificate. It
recomputes archived n=16/n=32/n=64 first-map stages on the n=16 two-cell-wide
interior region so the physical support is identical across resolutions.
"""

import hashlib
import json
import math
from pathlib import Path
import tempfile

from tools.analyze_amr_gauss_gradient import _stage
from tools.reconstruct_amr_published_archive import reconstruct


ROOT = Path(__file__).resolve().parents[1]
CASES = (
    (16, "evidence/of13-amr-same-run-map-v4-run3",
     "protocols/high-gradient-of13-amr-same-run-map-v4.json"),
    (32, "evidence/of13-amr-same-run-map-v5-n32",
     "protocols/high-gradient-of13-amr-same-run-map-v5-n32.json"),
    (64, "evidence/of13-amr-same-run-map-v7-n64",
     "protocols/high-gradient-of13-amr-same-run-map-v7-n64.json"),
)
DOMAIN_LENGTH = 2 * math.pi
COMMON_MARGIN = 2 * DOMAIN_LENGTH / 16


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def compare_case(n, evidence_rel, protocol_rel, expected_fraction):
    evidence = ROOT / evidence_rel
    protocol_path = ROOT / protocol_rel
    manifest = json.loads((evidence / "manifest.json").read_text())
    protocol = json.loads(protocol_path.read_text())
    archive = evidence / manifest["archive"]
    archive_label = str(archive.relative_to(ROOT))
    if not archive.is_file():
        parts_manifest = evidence / "amr-stage-snapshot-n64-review.tar.gz.zst.parts.json"
        with tempfile.TemporaryDirectory(prefix="cans-amr-resolution-") as temp:
            archive = Path(temp) / manifest["archive"]
            reconstruct(parts_manifest, archive)
            return _compare_case_data(
                n, evidence, protocol_path, manifest, protocol, archive,
                expected_fraction, archive_label,
            )
    return _compare_case_data(
        n, evidence, protocol_path, manifest, protocol, archive,
        expected_fraction, archive_label,
    )


def _compare_case_data(n, evidence, protocol_path, manifest, protocol,
                       archive, expected_fraction, archive_label):
    if sha256(archive) != manifest["archive_sha256"]:
        raise ValueError(f"archive SHA-256 mismatch for n={n}")
    case = protocol["case"]
    if case["initial_grid_cells_per_axis"] != n:
        raise ValueError(f"protocol resolution mismatch for n={n}")
    if manifest.get("foundation_source_commit") != \
            "18870c24d21c6b982e2cdec27b2f59738cca5f90":
        raise ValueError(f"Foundation source pin mismatch for n={n}")
    case_dir = manifest.get("case_directory", "amr-cap5000")
    pre_time = f"{case.get('pre_map_time', 0.002):g}"
    frequency = case["frequency"]
    pre = _stage(archive, case_dir, "preMap", pre_time,
                 frequency, COMMON_MARGIN,
                 force_uniform_centered_pre_map=True)
    mapped = _stage(archive, case_dir, "mapped", pre_time,
                    frequency, COMMON_MARGIN,
                    force_uniform_centered_pre_map=True)
    for stage in (pre, mapped):
        if not math.isclose(stage["interior_volume_fraction"],
                            expected_fraction, rel_tol=0, abs_tol=1e-10):
            raise ValueError(
                f"common-mask volume fraction mismatch for n={n}, "
                f"stage={stage['stage']}: "
                f"{stage['interior_volume_fraction']} != {expected_fraction}"
            )
    return {
        "n": n,
        "protocol": protocol_path.relative_to(ROOT).as_posix(),
        "protocol_sha256_current": sha256(protocol_path),
        "protocol_sha256_at_run": manifest.get(
            "protocol_sha256_at_execution", manifest.get("protocol_sha256")
        ),
        "protocol_hash_at_run_limitation": manifest.get("protocol_hash_limitation"),
        "archive": archive_label,
        "archive_sha256": manifest["archive_sha256"],
        "case_directory": case_dir,
        "stages": [pre, mapped],
    }


def compare():
    expected_fraction = ((DOMAIN_LENGTH - 2 * COMMON_MARGIN) / DOMAIN_LENGTH) ** 3
    rows = [compare_case(n, evidence, protocol, expected_fraction)
            for n, evidence, protocol in CASES]
    return {
        "status": "PASS_COMMON_PHYSICAL_INTERIOR_REPLAY",
        "analyzer": {
            "path": Path(__file__).relative_to(ROOT).as_posix(),
            "sha256": sha256(Path(__file__)),
            "operator_implementation": "tools/analyze_amr_gauss_gradient.py",
            "operator_implementation_sha256": sha256(
                ROOT / "tools/analyze_amr_gauss_gradient.py"
            ),
        },
        "scope": (
            "Archived first-refinement Gauss-gradient and vorticity diagnostics "
            "recomputed on one shared physical interior subdomain. This is not "
            "a continuous-field bound, AMR convergence certificate, or solver-defect verdict."
        ),
        "mask": {
            "definition": "cell centers whose distance from every periodic boundary exceeds pi/4",
            "physical_margin": COMMON_MARGIN,
            "equivalent_to_two_base_cell_widths_at": "n=16",
            "expected_volume_fraction": expected_fraction,
            "same_support_across_resolutions": True,
        },
        "cases": rows,
        "limitations": [
            "Mapped values are compared through a specified finite-volume Gauss reconstruction using captured face Uf and S.",
            "The exact gradient and vorticity are evaluated at cell centers, not integrated over cells.",
            "The preMap stage uses centered periodic differences, equivalent to arithmetic-midpoint Gauss interpolation on its uniform orthogonal grid.",
            "The n=16 v4 run manifest records a post-hoc protocol-hash limitation; its raw archive hash is verified, and the current protocol is separately hashed.",
            "These are exploratory single-run map events with no preregistered AMR quality threshold; no OpenFOAM defect or physical consequence is inferred.",
        ],
    }


if __name__ == "__main__":
    result = compare()
    output = ROOT / "evidence/of13-amr-resolution-comparison-2026-10-02.json"
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
