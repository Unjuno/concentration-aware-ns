"""Verify archived AMR cases against their raw-tree hashes in the manifests."""
import hashlib
import json
import tarfile
from pathlib import Path


MANIFESTS = (
    Path("evidence/of13-high-gradient-amr-v2-manifest-2026-09-30.json"),
    Path("evidence/of13-high-gradient-remap-control-v2-manifest-2026-09-30.json"),
)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def verify(manifests=MANIFESTS):
    rows = []
    for path in manifests:
        data = json.loads(Path(path).read_text())
        for case in data["cases"]:
            archive = Path(case["raw_archive"])
            if sha(archive.read_bytes()) != case["raw_archive_sha256"]:
                raise ValueError(f"archive hash mismatch: {archive}")
            entries = []
            with tarfile.open(archive, "r:gz") as tf:
                for member in tf.getmembers():
                    if member.isdir():
                        continue
                    rel = member.name.split("/", 1)[1] if "/" in member.name else member.name
                    if member.issym():
                        entries.append({"path": rel, "type": "symlink", "target": member.linkname})
                    elif member.isfile():
                        entries.append({"path": rel, "type": "file", "sha256": sha(tf.extractfile(member).read())})
                    else:
                        raise ValueError(f"unsupported archive entry: {member.name}")
            entries.sort(key=lambda row: row["path"])
            tree_hash = sha(json.dumps(entries, separators=(",", ":"), sort_keys=True).encode())
            if len(entries) != case["raw_archive_file_count"] or tree_hash != case["source_tree_sha256"]:
                raise ValueError(f"source-tree mismatch: {archive}")
            rows.append({
                "case": case["case"],
                "archive": archive.as_posix(),
                "archive_sha256": case["raw_archive_sha256"],
                "archive_file_count": len(entries),
                "source_tree_sha256": tree_hash,
                "verified": True,
            })
    return {
        "cases": rows,
        "scope": "Verifies archive byte hashes and canonical per-entry tree hashes for archived AMR and fixed-final-mesh cases; does not re-execute OpenFOAM or certify numerical quality.",
    }


if __name__ == "__main__":
    result = verify()
    output = Path("evidence/tests/openfoam-amr-archive-integrity-2026-09-30.json")
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
