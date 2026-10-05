from pathlib import Path

from tools.verify_su2_cfl_continuation_preconditions import verify


def test_saved_baseline_is_replayed_and_bound_before_the_split_control():
    result = verify(
        Path("protocols/su2-n32-full-horizon-cfl-control-continuation-v3.json"),
        Path("evidence/su2-full-horizon-run-37160281461/results"),
    )
    assert result["status"] == "BASELINE_ARCHIVE_AND_DIAGNOSTIC_REPLAY_PASS"
    assert result["physical_updates"] == 50
    assert result["residual_converged_steps"] == 48
    assert result["baseline_quality"] == "UNCERTAIN"
