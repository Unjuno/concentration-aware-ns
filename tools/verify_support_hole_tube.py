"""Run and hash the pinned-source Lean check for the scalar tube envelope."""
import hashlib
import json
import re
import subprocess
from pathlib import Path


SOURCE = Path("verification/SupportHoleTube.lean")
RUNNER = Path("runtime/lean-verification/check_support_hole_tube.sh")
UPSTREAM_SHA256 = {
    "NavierStokes/SimilarityCoordinates.lean": "de85505217232fed653c70fb73edf5658c1bf995bb36792cab5a4653d063ca1f",
    "NavierStokes/PhysicalWaveSum.lean": "5713536b5d510c2ab2c2151b4b1aa6c8822535169ae0e73ff60d9f7b69e9ea81",
    "NavierStokes/SimilarityProfile.lean": "82ef1138367d9a916ab6a478086a6e308ad24d901e58a62920c6f0095a503cd0",
    "NavierStokes/AxisymmetricFields.lean": "41d403ae4cec8887c17a80f621744399522a3247bddbcab64e577cb296b3020d",
}
THEOREMS = [
    "scalar_sublinear_envelope",
    "similarity_coordinate_upper_of_scaled_axial",
    "sqrt_tau_le_sublinear_power",
    "axial_coordinate_bound_of_tube",
    "similarity_coordinate_upper_of_tube",
    "physicalQ_forwardScalar",
    "physicalQ_ge_elapsed",
    "physicalQ_le_supportHoleScale",
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify() -> bool:
    result = subprocess.run(["sh", str(RUNNER)], capture_output=True, text=True)
    log = result.stdout + result.stderr
    output = Path("evidence/lean-verification/support-hole-tube.log")
    record = Path("evidence/lean-verification/support-hole-tube.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(log)
    source_hash = sha256(SOURCE)
    runner_hash = sha256(RUNNER)
    imported_hashes = {
        match.group(2): match.group(1)
        for match in re.finditer(r"^([0-9a-f]{64})  (NavierStokes/\S+\.lean)$", log, re.M)
    }
    imported_hash_ok = imported_hashes == UPSTREAM_SHA256
    allowed_axioms = {"propext", "Classical.choice", "Quot.sound"}
    axiom_reports = {
        name: [value.strip() for value in body.split(",")]
        for name, body in re.findall(
            r"'ConcentrationAware\.([^']+)' depends on axioms: \[(.*?)\]", log, re.S
        )
    }
    only_allowed_axioms = set(axiom_reports) == set(THEOREMS) and all(
        set(values) <= allowed_axioms for values in axiom_reports.values()
    )
    success = (
        result.returncode == 0
        and imported_hash_ok
        and only_allowed_axioms
        and "sorryAx" not in log
    )
    report = {
        "exit_code": result.returncode,
        "success": success,
        "source": str(SOURCE),
        "source_sha256": source_hash,
        "runner_sha256": runner_hash,
        "imported_source_sha256": imported_hashes,
        "imported_source_hashes_match": imported_hash_ok,
        "axioms": axiom_reports,
        "only_allowed_axioms": only_allowed_axioms,
        "log_sha256": sha256(output),
        "contains_sorryAx": "sorryAx" in log,
        "scope": "Lean checks the sublinear envelope; tube axial-power inequality; actual physicalQ coordinate equation and lower bound; and the resulting q upper bound conditional on a scaled axial bound. The selected-stage hole and full candidate germ transfer are checked separately in support-hole-assembly.json; uniform tube hypotheses and the selected trajectory-center bound remain open.",
    }
    record.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    return success


if __name__ == "__main__":
    raise SystemExit(0 if verify() else 1)
