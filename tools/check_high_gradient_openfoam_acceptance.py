"""Check the frozen OpenFOAM outer-residual and endpoint acceptance contract."""
import hashlib
import json
import math
import re
import subprocess
from pathlib import Path

IMAGE = "sha256:dd2b2eb63b12896a9b6e7a46563ed96b26d1c78c3e3749536d40d456895f722b"
ROOT = Path("work/of13-high-gradient-v2")
PROTOCOL = json.loads(Path("protocols/high-gradient-of13-v1.json").read_text())
CASES = (
    "n16-dt0.001", "n32-dt0.001", "n64-dt0.001", "n128-dt0.001",
    "n64-dt0.0005-rerun-20261002", "n64-dt0.00025-rerun-20261002",
    "amr-cap4096", "amr-cap5000", "amr-cap100000",
)
SOURCES = {
    "momentumPredictor.C": "/opt/openfoam13/applications/modules/incompressibleFluid/momentumPredictor.C",
    "fvMatrix.C": "/opt/openfoam13/src/finiteVolume/fvMatrices/fvMatrix/fvMatrix.C",
    "pimpleLoop.C": "/opt/openfoam13/src/finiteVolume/cfdTools/general/solutionControl/pimpleControl/pimpleLoop/pimpleLoop.C",
    "singleRegionCorrectorConvergenceControl.C": "/opt/openfoam13/src/finiteVolume/cfdTools/general/solutionControl/convergenceControl/singleRegionCorrectorConvergenceControl/singleRegionCorrectorConvergenceControl.C",
}


def image_sources():
    commands = [f"printf '\\n__CANS_SOURCE_{name}__\\n'; cat {path}"
                for name, path in SOURCES.items()]
    result = subprocess.run(
        ["docker", "run", "--rm", "--network", "none", "--entrypoint", "/bin/bash",
         IMAGE, "-c", "; ".join(commands)], capture_output=True, text=True, timeout=60,
    )
    if result.returncode:
        raise RuntimeError(f"cannot read runtime acceptance sources: {result.stderr[-1000:]}")
    cursor = result.stdout
    found = {}
    names = list(SOURCES)
    for index, name in enumerate(names):
        marker = f"__CANS_SOURCE_{name}__\n"
        if marker not in cursor:
            raise RuntimeError(f"source file missing from image output: {name}")
        remainder = cursor.split(marker, 1)[1]
        if index + 1 < len(names):
            next_marker = f"\n__CANS_SOURCE_{names[index + 1]}__\n"
            content = remainder.split(next_marker, 1)[0]
        else:
            content = remainder
        found[name] = content
        cursor = remainder
    return found


def audit_runtime_semantics(source):
    loop = source["pimpleLoop.C"]
    convergence = source["singleRegionCorrectorConvergenceControl.C"]
    matrix = source["fvMatrix.C"]
    momentum = source["momentumPredictor.C"]
    checks = {
        "momentum_rhs_is_fvModels_source": re.search(
            r"momentumTransport->divDevSigma\(U\)\s*==\s*fvModels\(\)\.source\(U\)", momentum
        ) is not None,
        "matrix_equality_subtracts_rhs_matrix": "return (A - B);" in matrix,
        "pimple_loop_uses_outer_convergence_predicate":
            "!firstIter() && convergence.corrCriteriaSatisfied()" in loop,
        "convergence_requires_abs_or_relative_residual_for_all_controlled_fields":
            "achieved = achieved && (absCheck || relCheck);" in convergence
            and "return checked && achieved;" in convergence,
    }
    if not all(checks.values()):
        raise AssertionError(f"pinned-image acceptance semantics changed: {checks}")
    return checks


def _tolerance(block, field):
    match = re.search(
        rf"\b{field}\s*\{{\s*tolerance\s+([0-9.eE+-]+)\s*;\s*relTol\s+([0-9.eE+-]+)\s*;\s*\}}",
        block,
    )
    if not match:
        return None
    return float(match.group(1)), float(match.group(2))


def inspect_case(name):
    case = ROOT / name
    params = json.loads((case / "parameters.json").read_text())
    log = (case / "log.foamRun").read_text()
    control = (case / "system/controlDict").read_text()
    solution = (case / "system/fvSolution").read_text()
    exit_code = json.loads((case / "exit.json").read_text()).get("exit_code")
    n_outer = re.search(r"\bnOuterCorrectors\s+(\d+)\s*;", solution)
    dt = float(params["dt"])
    end = float(params["end"])
    expected_steps = round(end / dt)
    time_values = [float(value) for value in re.findall(r"^Time\s*=\s*([0-9.eE+-]+)", log, re.M)]
    converged_iters = [int(value) for value in re.findall(r"^PIMPLE: Converged in (\d+) iterations$", log, re.M)]
    expected_times = [k * dt for k in range(1, expected_steps + 1)]
    time_sequence_ok = (len(time_values) == expected_steps and len(expected_times) == expected_steps
                        and all(math.isclose(a, b, rel_tol=0, abs_tol=1e-10)
                                for a, b in zip(time_values, expected_times)))
    end_name = format(end, ".12g")
    end_candidates = [path for path in case.iterdir()
                      if path.is_dir() and re.fullmatch(r"[0-9.eE+-]+", path.name)
                      and math.isclose(float(path.name), end, rel_tol=0, abs_tol=1e-12)]
    checks = {
        "exit_code_zero": exit_code == 0,
        "terminal_end_marker": log.rstrip().endswith("End"),
        "exact_physical_time_sequence": time_sequence_ok,
        "every_step_reports_pimple_convergence": len(converged_iters) == expected_steps,
        "outer_iterations_within_frozen_maximum": bool(n_outer) and max(converged_iters, default=10**9) <= int(n_outer.group(1)) <= PROTOCOL["standard_acceptance"]["maximum_outer_correctors"],
        "no_nonconvergence_message": "Not converged within" not in log,
        "no_fatal_error": (
            "FOAM FATAL ERROR" not in log
            and re.search(r"Floating point exception(?! trapping - not supported)", log) is None
        ),
        "endpoint_velocity_present": any((path / "U").is_file() for path in end_candidates),
        "delta_t_matches_case_parameters": re.search(rf"\bdeltaT\s+{re.escape(format(dt, '.12g'))}\s*;", control) is not None,
        "end_time_matches_case_parameters": re.search(rf"\bendTime\s+{re.escape(format(end, '.12g'))}\s*;", control) is not None,
        "p_abs_tolerance_matches_protocol": _tolerance(solution, "p") == (PROTOCOL["standard_acceptance"]["outer_corrector_residual_absolute"], 0.0),
        "U_abs_tolerance_matches_protocol": _tolerance(solution, "U") == (PROTOCOL["standard_acceptance"]["outer_corrector_residual_absolute"], 0.0),
    }
    return {
        "case": name,
        "parameters": {"n": params["n"], "dt": dt, "end": end, "profile": params["profile"]},
        "expected_time_steps": expected_steps,
        "observed_time_steps": len(time_values),
        "converged_outer_iterations": {
            "count": len(converged_iters),
            "minimum": min(converged_iters) if converged_iters else None,
            "maximum": max(converged_iters) if converged_iters else None,
        },
        "checks": checks,
        "standard_acceptance": "PASS" if all(checks.values()) else "UNCERTAIN",
        "input_hashes": {
            filename: hashlib.sha256((case / filename).read_bytes()).hexdigest()
            for filename in ("system/controlDict", "system/fvSolution", "log.foamRun", "exit.json")
        },
    }


def main():
    source = image_sources()
    runtime_checks = audit_runtime_semantics(source)
    cases = [inspect_case(name) for name in CASES]
    source_hashes = {name: hashlib.sha256(content.encode()).hexdigest()
                     for name, content in source.items()}
    complete = all(row["standard_acceptance"] == "PASS" for row in cases)
    report = {
        "schema_version": 1,
        "scope": "Frozen OpenFOAM standard acceptance contract: completion, time sequence, and per-step outer residual convergence",
        "protocol": "protocols/high-gradient-of13-v1.json",
        "protocol_sha256": hashlib.sha256(Path("protocols/high-gradient-of13-v1.json").read_bytes()).hexdigest(),
        "runtime_image": IMAGE,
        "runtime_source_hashes": source_hashes,
        "runtime_semantics_checks": runtime_checks,
        "cases": cases,
        "matrix_standard_acceptance": "PASS" if complete else "UNCERTAIN",
        "limitations": [
            "PIMPLE convergence lines are accepted as the runtime's configured corrector-residual decision; raw debug residual values were not enabled.",
            "The runtime log reports that floating-point exception trapping is not supported on this platform; exit success does not replace such checks.",
            "This gate says the requested numerical solve completed and met its configured outer-corrector condition; it does not establish local numerical accuracy.",
            "The image source files are inspected directly, but source-to-binary identity remains unverified.",
        ],
    }
    out = Path("evidence/tests/of13-high-gradient-standard-acceptance.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    if not complete:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
