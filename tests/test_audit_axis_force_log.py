import hashlib
import json

from tools.audit_axis_force_log import audit


def fixture():
    source = b"""namespace ConcentrationAware
theorem first : True := trivial
#print axioms first
theorem second : True := trivial
#print axioms second
end ConcentrationAware
"""
    log = (b"'ConcentrationAware.first' depends on axioms: [propext]\n"
           b"'ConcentrationAware.second' depends on axioms: [Classical.choice]\n")
    manifest = {"sha256": {
        "verification/AxisForceSign.lean": hashlib.sha256(source).hexdigest(),
        "evidence/lean-verification/axis-volume-covariance-2026-10-01.log": hashlib.sha256(log).hexdigest(),
    }}
    return source, log, manifest


def test_exact_source_and_complete_allowed_axiom_log_pass():
    source, log, manifest = fixture()
    result = audit(source, log, manifest, "verification/AxisForceSign.lean",
                   "evidence/lean-verification/axis-volume-covariance-2026-10-01.log")
    assert result["success"]
    assert result["printed_declaration_count"] == 2
    assert result["axiom_report_count"] == 2
    assert result["execution_clean_exit"] is None


def test_abnormal_exit_is_preserved_as_not_clean_even_when_log_matches():
    source, log, manifest = fixture()
    manifest["execution"] = {"exit_code": -5}
    result = audit(source, log, manifest, "verification/AxisForceSign.lean",
                   "evidence/lean-verification/axis-volume-covariance-2026-10-01.log")
    assert result["success"]
    assert result["execution_exit_code"] == -5
    assert result["execution_clean_exit"] is False


def test_changed_log_hash_fails_even_when_prints_look_valid():
    source, log, manifest = fixture()
    result = audit(source, log + b"extra\n", manifest, "verification/AxisForceSign.lean",
                   "evidence/lean-verification/axis-volume-covariance-2026-10-01.log")
    assert not result["checks"]["log_sha256_matches_manifest"]


def test_missing_print_and_unapproved_axiom_fail():
    source, log, manifest = fixture()
    bad_log = b"'ConcentrationAware.first' depends on axioms: [sorryAx]\n"
    result = audit(source, bad_log, manifest, "verification/AxisForceSign.lean",
                   "evidence/lean-verification/axis-volume-covariance-2026-10-01.log")
    assert not result["checks"]["printed_declarations_have_axiom_reports"]
    assert not result["checks"]["all_axioms_allowed"]
    assert not result["checks"]["no_sorryAx"]
