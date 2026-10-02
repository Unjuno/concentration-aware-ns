"""Verify that the compact n=128 review package preserves audited source bytes."""

import hashlib
import json
import tarfile
import tempfile
from pathlib import Path

from tools.reconstruct_amr_published_archive import reconstruct

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence/of13-amr-same-run-map-v8-n128"
PARTS = EVIDENCE / "amr-stage-snapshot-n128-review.tar.gz.zst.parts.json"
MANIFEST = EVIDENCE / "manifest.json"


def hash_stream(stream):
    digest = hashlib.sha256()
    size = 0
    for block in iter(lambda: stream.read(1 << 20), b""):
        digest.update(block)
        size += len(block)
    return size, digest.hexdigest()


def verify():
    manifest = json.loads(MANIFEST.read_text())
    case = manifest["case_directory"]
    expected = {
        f"{case}/postProcessing/amrStages/0.002/preMap_cells.csv": manifest["snapshot_sha256"]["postProcessing/amrStages/0.002/preMap_cells.csv"],
        f"{case}/postProcessing/amrStages/0.002/mapped_cells.csv": manifest["snapshot_sha256"]["postProcessing/amrStages/0.002/mapped_cells.csv"],
        f"{case}/postProcessing/amrStages/0.002/mapped_faces.csv": manifest["snapshot_sha256"]["postProcessing/amrStages/0.002/mapped_faces.csv"],
    }
    with tempfile.TemporaryDirectory(prefix="cans-amr-v8-n128-review-") as temp:
        archive_path = Path(temp) / "review.tar.gz"
        reconstructed = reconstruct(PARTS, archive_path)
        verified = []
        with tarfile.open(archive_path, "r:gz") as archive:
            for member, expected_sha in expected.items():
                source = archive.extractfile(member)
                if source is None:
                    raise ValueError(f"missing required audit member: {member}")
                with source:
                    size, actual_sha = hash_stream(source)
                if actual_sha != expected_sha:
                    raise ValueError(f"snapshot hash differs from as-run manifest: {member}")
                verified.append({"member": member, "bytes": size, "sha256": actual_sha})
    result = {
        "status": "PASS_REVIEW_PACKAGE_MEMBERS_MATCH_AS_RUN_SNAPSHOTS",
        "parts_manifest": str(PARTS.relative_to(ROOT)),
        "reconstructed_archive_sha256": reconstructed["sha256"],
        "verified_members": verified,
        "scope": "The compact package contains byte-identical same-run cell and mapped-face snapshots used by the map and Gauss audits. This integrity check does not recompute their numerical diagnostics or certify the solver stack.",
    }
    output = EVIDENCE / "review-archive-members-verification.json"
    output.write_text(json.dumps(result, indent=2) + "\n")
    return result


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2))
