from pathlib import Path

import pytest

from tools.review_su2_full_horizon_cfl_pair import review


def test_canceled_historical_control_cannot_be_relabelled_as_a_pair():
    root = Path("evidence/su2-full-horizon-run-37160281461/results")
    with pytest.raises(ValueError, match="control execution is incomplete"):
        review(
            None,
            Path("protocols/su2-n32-full-horizon-cfl-control-v1.json"),
            baseline_root=root,
            control_root=root,
        )
