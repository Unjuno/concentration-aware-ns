"""Conservative report triage; flags require independent evidence review."""
import json
import math
import sys


def evaluate(report):
    result = dict(standard_acceptance="UNCERTAIN", local_quality="UNCERTAIN",
                  hypothesis="UNCERTAIN")
    if not isinstance(report, dict):
        return result
    standard = report.get("standard_acceptance")
    if standard in ("PASS", "FAIL"):
        result["standard_acceptance"] = standard
    evidence = report.get("evidence")
    required = ("reference_verified", "forcing_verified", "derivatives_verified",
                "space_time_study_verified", "thresholds_preregistered",
                "raw_artifacts_reviewed", "evaluation_time_verified")
    if not isinstance(evidence, dict) or any(evidence.get(k) is not True for k in required):
        return result
    metrics = report.get("metrics")
    if not isinstance(metrics, list) or not metrics:
        return result
    failures = []
    names = set()
    for metric in metrics:
        if not isinstance(metric, dict):
            return result
        name = metric.get("name")
        if not isinstance(name, str) or not name or name in names:
            return result
        names.add(name)
        values = [metric.get(k) for k in ("error", "tolerance")]
        if any(type(v) not in (int, float) or not math.isfinite(v) or v < 0 for v in values):
            return result
        failures.append(values[0] > values[1])
    if not {"max_gradient", "max_vorticity"}.issubset(names):
        return result
    result["local_quality"] = "FAIL" if any(failures) else "PASS"
    if standard == "PASS":
        result["hypothesis"] = "REPRODUCED" if any(failures) else "NOT_OBSERVED"
    return result


if __name__ == "__main__":
    try:
        with open(sys.argv[1]) as stream:
            result = evaluate(json.load(stream))
    except (IndexError, OSError, ValueError):
        result = evaluate(None)
    print(json.dumps(result, indent=2))
    sys.exit({"PASS": 0, "FAIL": 1, "UNCERTAIN": 2}[result["local_quality"]])
