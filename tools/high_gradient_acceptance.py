"""Separate OpenFOAM run acceptance, local quality, and blind-spot evidence."""
import math
import re


def standard_acceptance(log_text, end_time, delta_t, residual_tolerance, max_outer_correctors,
                        fv_solution_text):
    times = list(re.finditer(r"^Time\s*=\s*([0-9.eE+-]+)s?\s*$", log_text, re.M))
    converged = []
    malformed = False
    for i, match in enumerate(times):
        stop = times[i + 1].start() if i + 1 < len(times) else len(log_text)
        block = log_text[match.end():stop]
        iteration = re.search(r"^PIMPLE:\s*Converged in\s+(\d+)\s+iterations?\s*$", block, re.M)
        converged.append(int(iteration[1]) if iteration else None)
    ratio = end_time / delta_t
    expected_steps = round(ratio)
    aligned = math.isfinite(ratio) and abs(ratio - expected_steps) <= 1e-10
    observed_times = [float(match[1]) for match in times]
    time_tolerance = 1e-9 * max(1.0, abs(end_time))
    time_sequence_mismatches = []
    if aligned:
        for i in range(max(len(observed_times), expected_steps)):
            if (i >= len(observed_times) or i >= expected_steps
                    or abs(observed_times[i] - delta_t * (i + 1)) > time_tolerance):
                time_sequence_mismatches.append(i)
    time_sequence_matches = aligned and not time_sequence_mismatches
    final_time = float(times[-1][1]) if times else None
    complete = log_text.rstrip().endswith("End") and final_time is not None and abs(final_time-end_time) <= 1e-12
    if not times or not aligned:
        malformed = True
    failed_steps = [i for i, n in enumerate(converged) if n is None or n > max_outer_correctors]
    outer_count = re.search(r"\bnOuterCorrectors\s+(\d+)\s*;", fv_solution_text)
    controls = re.search(r"outerCorrectorResidualControl\s*\{\s*p\s*\{\s*tolerance\s+([0-9.eE+-]+)\s*;\s*relTol\s+([0-9.eE+-]+)\s*;\s*\}\s*U\s*\{\s*tolerance\s+([0-9.eE+-]+)\s*;\s*relTol\s+([0-9.eE+-]+)\s*;", fv_solution_text, re.S)
    config_valid = bool(outer_count and int(outer_count[1]) == max_outer_correctors and controls
                        and float(controls[1]) == residual_tolerance and float(controls[2]) == 0
                        and float(controls[3]) == residual_tolerance and float(controls[4]) == 0)
    passed = (complete and len(times) == expected_steps and time_sequence_matches
              and not failed_steps and config_valid)
    status = "PASS" if passed else "FAIL" if complete and not malformed else "UNCERTAIN"
    return {
        "status": status,
        "complete_end_time": complete,
        "observed_time_steps": len(times),
        "expected_time_steps": expected_steps if aligned else None,
        "time_sequence_matches_fixed_delta_t": time_sequence_matches,
        "time_sequence_mismatches_zero_based": time_sequence_mismatches,
        "pimple_convergence_records": sum(n is not None for n in converged),
        "failed_or_missing_convergence_steps_zero_based": failed_steps,
        "maximum_observed_outer_correctors": max((n for n in converged if n is not None), default=None),
        "maximum_allowed_outer_correctors": max_outer_correctors,
        "configured_outer_correctors": int(outer_count[1]) if outer_count else None,
        "configured_residual_tolerance": residual_tolerance,
        "outer_residual_control_configuration_matches_protocol": config_valid,
        "evidence_scope": "OpenFOAM PIMPLE convergence messages, completed time log, and checked fvSolution residual-control settings; these certify the configured numerical stopping criterion, not physical accuracy.",
    }


def local_quality(metrics, thresholds):
    rows = {}
    for name, limit in thresholds.items():
        value = metrics.get(name)
        if type(value) not in (int, float) or not math.isfinite(value) or value < 0:
            rows[name] = {"value": value, "threshold": limit, "status": "UNCERTAIN"}
        else:
            rows[name] = {"value": value, "threshold": limit,
                          "status": "PASS" if value <= limit else "FAIL"}
    states = [row["status"] for row in rows.values()]
    overall = "FAIL" if "FAIL" in states else "PASS" if states and all(s == "PASS" for s in states) else "UNCERTAIN"
    return {"status": overall, "metrics": rows}


def matrix_reproduction(cases, adequately_resolved_counts=(64, 128)):
    """Require a persistent standard-PASS/local-FAIL at two fine grid levels."""
    by_n = {case.get("parameters", {}).get("n"): case for case in cases
            if case.get("parameters", {}).get("dt") == 0.001}
    selected = [by_n.get(n) for n in adequately_resolved_counts]
    if any(case is None for case in selected):
        status = "UNCERTAIN"
    elif all(case.get("standard_acceptance", {}).get("status") == "PASS"
             and case.get("local_quality", {}).get("status") == "FAIL" for case in selected):
        status = "REPRODUCED"
    elif all(case.get("standard_acceptance", {}).get("status") == "PASS"
             and case.get("local_quality", {}).get("status") == "PASS" for case in selected):
        status = "NOT_OBSERVED"
    else:
        status = "UNCERTAIN"
    return {
        "status": status,
        "adequately_resolved_grid_counts": list(adequately_resolved_counts),
        "rule": "REPRODUCED only if both listed fine-grid cases pass standard acceptance and fail local quality; NOT_OBSERVED only if both pass both gates.",
        "scope": "A persistent discrepancy under this frozen MMS matrix; not proof of a general solver defect or physical singularity.",
    }
