import pytest

from tools.audit_su2_localized_source_lag import audit


def test_source_lag_audit_is_archive_locked_and_first_order():
    result = audit()
    assert len(result["cases"]) == 3
    assert [case["dt"] for case in result["cases"]] == [0.001, 0.0005, 0.00025]
    assert len({case["archive_sha256"] for case in result["cases"]}) == 3
    assert all(case["sample_count"] == 4096 for case in result["cases"])
    assert all(0.99 < order < 1.01
               for order in result["successive_halving_force_difference_orders"])
    assert "not a PDE solution-error attribution" in result["scope"]


def test_source_lag_audit_rejects_changed_archive_hash(monkeypatch):
    import tools.audit_su2_localized_source_lag as module

    class WrongDigest:
        def hexdigest(self):
            return "0" * 64

    monkeypatch.setattr(module.hashlib, "sha256", lambda _: WrongDigest())
    with pytest.raises(ValueError, match="archive hash mismatch"):
        audit()
