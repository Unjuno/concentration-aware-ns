"""Reconcile the compact n=128 review archive with the recorded Gauss audit."""

import contextlib
import io
import json
import os
import tempfile
from pathlib import Path

from tools.reconstruct_amr_published_archive import reconstruct


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence/of13-amr-same-run-map-v8-n128"
PROTOCOL = "protocols/high-gradient-of13-amr-same-run-map-v8-n128.json"
PARTS = EVIDENCE / "amr-stage-snapshot-n128-review.tar.gz.zst.parts.json"


def verify():
    manifest = json.loads((EVIDENCE / "manifest.json").read_text())
    recorded = json.loads((EVIDENCE / "gauss-gradient-audit.json").read_text())
    with tempfile.TemporaryDirectory(prefix="cans-amr-v8-n128-gauss-") as temp:
        temp = Path(temp)
        archive = temp / "review.tar.gz"
        temp_evidence = temp / "evidence"
        temp_evidence.mkdir()
        archive_info = reconstruct(PARTS, archive)
        replay_manifest = dict(manifest)
        replay_manifest["archive_sha256"] = archive_info["sha256"]
        (temp_evidence / "manifest.json").write_text(
            json.dumps(replay_manifest)
        )
        os.environ["CANS_AMR_STAGE_EVIDENCE"] = str(temp_evidence)
        os.environ["CANS_AMR_STAGE_PROTOCOL"] = PROTOCOL
        os.environ["CANS_AMR_STAGE_RAW_ARCHIVE"] = str(archive)

        # Import only after configuring module-level paths from the environment.
        from tools.analyze_amr_gauss_gradient import analyze

        with contextlib.redirect_stdout(io.StringIO()):
            replayed = analyze()

    recorded_stages = {row["stage"]: row for row in recorded["stages"]}
    replayed_stages = {row["stage"]: row for row in replayed["stages"]}
    replay_scope = {
        "status": "PASS_MAPPED_STAGE_REPLAY_WITH_DECLARED_PREMAP_FALLBACK",
        "compact_archive_sha256": archive_info["sha256"],
        "as_run_archive_sha256": manifest["archive_sha256"],
        "mapped_stage_exact_json_match": (
            recorded_stages["mapped"] == replayed_stages["mapped"]
        ),
        "same_parent_face_audit_exact_match": (
            recorded["same_parent_face_audit"]
            == replayed["same_parent_face_audit"]
        ),
        "preMap_as_run_gradient_method": recorded_stages["preMap"]["gradient_method"],
        "preMap_compact_replay_gradient_method": replayed_stages["preMap"]["gradient_method"],
        "preMap_gradient_relative_l2_as_run": recorded_stages["preMap"][
            "interior_gauss_gradient_relative_l2_vs_exact_point_gradient"
        ],
        "preMap_gradient_relative_l2_compact_replay": replayed_stages["preMap"][
            "interior_gauss_gradient_relative_l2_vs_exact_point_gradient"
        ],
        "preMap_vorticity_relative_l2_as_run": recorded_stages["preMap"][
            "interior_gauss_vorticity_relative_l2_vs_exact_point_vorticity"
        ],
        "preMap_vorticity_relative_l2_compact_replay": replayed_stages["preMap"][
            "interior_gauss_vorticity_relative_l2_vs_exact_point_vorticity"
        ],
        "explanation": (
            "The public compact archive omits preMap_faces.csv. Its preMap result "
            "therefore uses the documented periodic centered-difference fallback; "
            "the original as-run audit used captured preMap face data. The mapped "
            "stage and same-parent face audit replay exactly."
        ),
        "scope": (
            "Replays numerical postprocessing from the compact archive; does not "
            "re-run or certify OpenFOAM or imply continuum or physical behavior."
        ),
    }
    if not (replay_scope["mapped_stage_exact_json_match"]
            and replay_scope["same_parent_face_audit_exact_match"]):
        raise AssertionError("published mapped-stage diagnostics did not replay exactly")
    output = EVIDENCE / "compact-gauss-replay-verification.json"
    output.write_text(json.dumps(replay_scope, indent=2) + "\n")
    return replay_scope


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2))
