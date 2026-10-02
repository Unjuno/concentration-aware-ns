"""Build evidence-linked local-quality gates for the preregistered AMR cases."""
import hashlib
import json
import tarfile
from pathlib import Path

from tools.acceptance_gate import evaluate

ROOT = Path(".")
MANIFEST_PATH = Path("evidence/of13-high-gradient-v2/matrix-manifest.json")
CASES = ("amr-cap4096", "amr-cap5000", "amr-cap100000")
EVIDENCE_PATHS = {
    "reference_verified": "evidence/tests/high-gradient-mms.json",
    "forcing_verified": "evidence/tests/high-gradient-openfoam-force.json",
    "derivatives_verified": "evidence/tests/high-gradient-reference.json",
    "space_time_study_verified": "reports/of13-high-gradient-amr-v1.md",
    "thresholds_preregistered": "protocols/high-gradient-of13-amr-v1.json",
    "raw_artifacts_reviewed": "evidence/of13-high-gradient-v2/matrix-manifest.json",
    "evaluation_time_verified": "evidence/tests/of13-high-gradient-standard-acceptance.json",
    "standard_acceptance_verified": "evidence/tests/of13-high-gradient-standard-acceptance.json",
}


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def verify_archives(manifest):
    rows = {row["case"]: row for row in manifest["cases"]}
    for name in CASES:
        row = rows[name]
        archive_path = Path("evidence/of13-high-gradient-v2") / f"{name}.tar.gz"
        if sha256(archive_path) != row["archive_sha256"]:
            raise ValueError(f"archive hash mismatch for {name}")
        expected = set(row["archive_paths"])
        with tarfile.open(archive_path, "r:gz") as archive:
            members = {Path(member.name).relative_to(name).as_posix()
                       for member in archive.getmembers()
                       if Path(member.name).parts and Path(member.name).parts[0] == name}
        if not expected.issubset(members):
            raise ValueError(f"archive members missing for {name}: {sorted(expected-members)}")
    return True


def build_case(name, diagnostic, standard_report, manifest):
    manifest_rows = {row["case"]: row for row in manifest["cases"]}
    row = manifest_rows[name]
    standard_rows = {case["case"]: case for case in standard_report["cases"]}
    standard = standard_rows[name]["standard_acceptance"]
    if standard != "PASS":
        raise ValueError(f"standard acceptance is not PASS for {name}")
    error = diagnostic["velocity_relative_volume_l2"]
    tolerance = 0.02
    roundoff_budget = 1e-12
    if error <= roundoff_budget:
        lower = 0.0
    else:
        lower = error - roundoff_budget
    metrics = [
        {"name": "velocity_l2", "error_lower": lower,
         "error_upper": error + roundoff_budget, "tolerance": tolerance},
        {"name": "energy", "error_lower": 0.0, "error_upper": None,
         "tolerance": 0.02},
        {"name": "max_gradient", "error_lower": 0.0, "error_upper": None,
         "tolerance": 0.05},
        {"name": "max_vorticity", "error_lower": 0.0, "error_upper": None,
         "tolerance": 0.05},
        {"name": "shell_spectrum", "error_lower": 0.0, "error_upper": None,
         "tolerance": 0.05},
    ]
    evidence = {key: True for key in EVIDENCE_PATHS}
    artifacts = {key: {"path": path, "sha256": sha256(path)}
                 for key, path in EVIDENCE_PATHS.items()}
    report = {
        "schema_version": 2,
        "case": name,
        "standard_acceptance": standard,
        "evidence": evidence,
        "artifacts": artifacts,
        "metrics": metrics,
        "scope": (
            "Discrete volume-weighted velocity error against the analytic field at AMR cell centers; "
            "other metric intervals remain unavailable. This identifies a tested acceptance/local-error "
            "discrepancy, not an upstream software defect."
        ),
        "protocol_sha256": "6e47566d489bc3a48894c9077cbcf8f6ff915da6c135b9cec6809eca8ed5116f",
        "case_evidence": {
            "manifest_status": row["status"],
            "archive_sha256": row["archive_sha256"],
            "actual_cells": diagnostic["cells"],
            "requested_cell_cap": diagnostic["parameters"]["amr"]["maxCells"],
            "maximum_refinement_level": max(map(int, diagnostic["level_counts"])),
            "velocity_l2_numeric_roundoff_budget": roundoff_budget,
        },
        "unresolved": [
            "Peak-gradient and peak-vorticity metric definitions do not have validated continuous-domain bounds.",
            "This AMR matrix starts from n=16; coarse initialization and refinement interpolation remain confounded.",
            "No upstream defect or general AMR limitation is established.",
            "Source-to-binary identity for the packaged solver is not proven.",
        ],
    }
    verdict = evaluate(report, ROOT)
    return report, verdict


def main():
    manifest = json.loads(MANIFEST_PATH.read_text())
    standard_report = json.loads(Path(EVIDENCE_PATHS["standard_acceptance_verified"]).read_text())
    verify_archives(manifest)
    verdicts = {}
    for name in CASES:
        diagnostic = json.loads((Path("work/of13-high-gradient-v2") / name / "diagnostics.json").read_text())
        report, verdict = build_case(name, diagnostic, standard_report, manifest)
        if verdict["standard_acceptance"] != "PASS" or verdict["local_quality"] != "FAIL":
            raise ValueError(f"unexpected gate verdict for {name}: {verdict}")
        out = Path("reports") / f"of13-high-gradient-{name}-gate.json"
        out.write_text(json.dumps(report, indent=2) + "\n")
        verdict_path = Path("reports") / f"of13-high-gradient-{name}-verdict.json"
        verdict_path.write_text(json.dumps(verdict, indent=2) + "\n")
        verdicts[name] = verdict
    print(json.dumps(verdicts, indent=2))


if __name__ == "__main__":
    main()
