"""Verify that the n=128 AMR runner sources match the run's recorded commit."""

import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence/of13-amr-same-run-map-v8-n128"
MANIFEST = EVIDENCE / "manifest.json"
PROTOCOL = ROOT / "protocols/high-gradient-of13-amr-same-run-map-v8-n128.json"
SOURCES = (
    "tools/run_amr_stage_snapshot_v4.py",
    "tools/openfoam_amr_case.py",
    "tools/package_amr_stage_evidence.py",
    "tools/run_high_gradient_openfoam.py",
)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def verify():
    manifest = json.loads(MANIFEST.read_text())
    commit = manifest["source_commit"]
    dirty_lines = manifest["harness_worktree_porcelain"].splitlines()
    protocol_line = "?? protocols/high-gradient-of13-amr-same-run-map-v8-n128.json"
    if dirty_lines != [protocol_line]:
        raise ValueError(f"unexpected recorded harness changes: {dirty_lines!r}")
    protocol_sha = digest(PROTOCOL.read_bytes())
    if protocol_sha != manifest["protocol_sha256"]:
        raise ValueError("protocol hash differs from run manifest")

    rows = []
    for relative in SOURCES:
        worktree_bytes = (ROOT / relative).read_bytes()
        committed = subprocess.run(
            ["git", "show", f"{commit}:{relative}"], cwd=ROOT,
            capture_output=True, check=True,
        ).stdout
        if worktree_bytes != committed:
            raise ValueError(f"worktree source differs from run commit: {relative}")
        rows.append({
            "path": relative,
            "sha256": digest(committed),
            "matches_recorded_commit_blob": True,
        })

    result = {
        "status": "PASS_RECORDED_HARNESS_SOURCES_MATCH_COMMIT",
        "run_manifest": str(MANIFEST.relative_to(ROOT)),
        "run_source_commit": commit,
        "captured_startup_porcelain": dirty_lines,
        "protocol_sha256": protocol_sha,
        "tracked_harness_sources": rows,
        "scope": "The runner's captured startup status contains only the untracked frozen protocol. These tracked source blobs are therefore recoverable from the recorded commit; this verifies provenance, not solver-stack source equivalence or scientific validity.",
    }
    output = EVIDENCE / "harness-provenance-a1.json"
    output.write_text(json.dumps(result, indent=2) + "\n")
    return result


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2))
