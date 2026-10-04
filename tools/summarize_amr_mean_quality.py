"""Aggregate complete frozen AMR results without promoting missing controls."""
import argparse
import json
from pathlib import Path

from tools.run_amr_mean_quality import PROTOCOL, sha


def summarize(results, spec, protocol_sha256):
    expected = {c["id"] for c in spec["cases"]}
    by_id = {}
    for result in results:
        key = result.get("case_id")
        if key not in expected or key in by_id:
            raise ValueError("unknown or duplicate matrix case")
        by_id[key] = result
    integrity = set(by_id) == expected and all(
        r.get("status") == "COMPLETE_SPECIFIED_MEAN_GATE_ANALYSIS"
        and r.get("protocol_sha256") == protocol_sha256
        and r.get("case") == next(c for c in spec["cases"] if c["id"] == key)
        and r.get("model") == spec["model"]
        and {s.get("stage"): s.get("time") for s in r.get("stages", [])}
            == spec["measurements"]["state_times"]
        and len(r.get("stages", [])) == 3 for key, r in by_id.items())
    commits = {r.get("source_commit") for r in results}
    integrity = integrity and len(commits) == 1 and None not in commits
    controls = integrity and all(by_id[c["id"]].get("instrumentation_control")
        == "BYTE_IDENTICAL_FINAL_U_AND_P" for c in spec["cases"] if c["capture_disabled_control"])
    standard = controls and all(r.get("standard_acceptance", {}).get("status") == "PASS" for r in results)
    selected = [by_id.get(c["id"]) for c in spec["cases"]
                if c["n"] in spec["reproduction"]["adequate_counts"] and c["dt"] == .001]
    adequate = standard and len(selected) == 2 and all(
        all(s.get("reference_operator_quality", {}).get("status") == "PASS" for s in r["stages"])
        for r in selected)
    status = "UNCERTAIN"
    if adequate:
        final = [next(s for s in r["stages"] if s["stage"] == "postSolve") for r in selected]
        if all(s.get("local_mean_quality", {}).get("status") == "FAIL" for s in final):
            status = "REPRODUCED_SPECIFIED_MEAN_GATE_DISCREPANCY"
        elif all(s.get("local_mean_quality", {}).get("status") == "PASS"
                 for r in selected for s in r["stages"]):
            status = "NOT_OBSERVED"
    return {"schema": "of13-amr-mean-quality-matrix/v1", "status": status,
            "expected_cases": sorted(expected), "missing_cases": sorted(expected-set(by_id)),
            "complete_same_source_protocol_and_stage_identity": bool(integrity),
            "disabled_capture_control_verified": bool(controls),
            "all_case_standard_acceptance_pass": bool(standard),
            "both_fine_cases_reference_operator_adequate_at_all_stages": bool(adequate),
            "protocol_sha256": protocol_sha256, "source_commits": sorted(str(c) for c in commits),
            "rule": spec["reproduction"]["rule"],
            "original_AMR_peak_spectrum_gate": "UNCERTAIN_SEPARATE_OPEN_OBLIGATIONS",
            "limits": spec["limits"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("analyses", nargs="+", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    result = summarize([json.loads(p.read_text()) for p in args.analyses],
                       json.loads(PROTOCOL.read_text()), sha(PROTOCOL))
    args.output.write_text(json.dumps(result, indent=2, allow_nan=False)+"\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
