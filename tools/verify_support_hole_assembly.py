"""Verify and hash the selected-stage support-hole assembly implications."""
import hashlib
import json
import re
import subprocess
from pathlib import Path


SOURCE = Path("verification/SupportHoleAssembly.lean")
RUNNER = Path("runtime/lean-verification/check_support_hole_assembly.sh")
UPSTREAM_SHA256 = {
    "NavierStokes/ActualCandidateAssembly.lean": "bba2f74a938039caec486ca6a35576efd21e6fe35c1ba695e4d21609d89b8a94",
    "NavierStokes/ActualCandidateConstruction.lean": "c8ac0ed2cac0390ea16ad9e2fa300e23cbc9950220dba0432f61724a3ea8c20f",
    "NavierStokes/ActualCurrentWaveSupport.lean": "bfe9d89941842402ffd89e18eee0074f0e66e24ddc0bc3c5dd8e984576827bfb",
    "NavierStokes/ActualMeanStageData.lean": "7195488e5bed2a1261067ff7e997c7b1ce230747b235b9178c53da3a7184b471",
    "NavierStokes/ActualMeanExterior.lean": "f9c1d7e1fd4e659185f580112b45941c72c09c54cc92210a07d23764b9ef77ea",
    "NavierStokes/ActualSignedExterior.lean": "459cd2997fb53946e4bcd273b37cb2981de42ef4c6bf50e759dd824a67d38b16",
    "NavierStokes/ActualValidBandWaves.lean": "3e058e7f84b61de977590972218906cdffd387954280a095f830de77164e0991",
}
THEOREMS = (
    "actual_stages_zero_below_active_radius",
    "diagonal_sum_zero_of_stage_germs",
    "actual_stage_zero_germs_below_active_radius",
    "actual_potential_sum_eq_base_germ_inside_hole",
    "actual_direct_sum_zero_germ_inside_hole",
    "actual_candidate_velocity_eq_base_germ_inside_hole",
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify() -> bool:
    result = subprocess.run(["sh", str(RUNNER)], capture_output=True, text=True)
    log = result.stdout + result.stderr
    log_path = Path("evidence/lean-verification/support-hole-assembly.log")
    report_path = Path("evidence/lean-verification/support-hole-assembly.json")
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text(log)
    source_hashes = {
        match.group(2): match.group(1)
        for match in re.finditer(r"^([0-9a-f]{64})  (NavierStokes/\S+\.lean)$", log, re.M)
    }
    reports = {
        theorem: re.findall(
            rf"'ConcentrationAware\.{theorem}' depends on axioms: \[(.*?)\]", log, re.S
        )
        for theorem in THEOREMS
    }
    axioms_by_theorem = {
        theorem: [value.strip() for value in values[0].split(",")] if values else []
        for theorem, values in reports.items()
    }
    allowed = {"propext", "Classical.choice", "Quot.sound"}
    source_match = source_hashes == UPSTREAM_SHA256
    axiom_match = all(values and set(values) <= allowed for values in axioms_by_theorem.values())
    success = result.returncode == 0 and source_match and axiom_match and "sorryAx" not in log
    report = {
        "exit_code": result.returncode,
        "success": success,
        "source": str(SOURCE),
        "source_sha256": digest(SOURCE),
        "runner_sha256": digest(RUNNER),
        "pinned_openai_source_sha256": source_hashes,
        "pinned_source_hashes_match": source_match,
        "theorems": list(THEOREMS),
        "axioms_by_theorem": axioms_by_theorem,
        "only_allowed_axioms": axiom_match,
        "log_sha256": digest(log_path),
        "contains_sorryAx": "sorryAx" in log,
        "scope": "The selected actual stages vanish in the inner support hole; their initialized potential sum and direct angular sum transfer as germs; and the complete activated periodic candidate velocity equals the base germ under explicit physical-domain, cutoff-plateau, late-time, and spatial-localization hypotheses. Uniform verification of those hypotheses on a quantitative tube remains open.",
    }
    report_path.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    return success


if __name__ == "__main__":
    raise SystemExit(0 if verify() else 1)
