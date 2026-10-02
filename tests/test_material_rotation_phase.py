from pathlib import Path
import math
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools.check_material_rotation_phase import (  # noqa: E402
    phase_sensitivity,
    symbolic_identity,
)


def test_integrated_tangent_rotation_identity_and_dimensionless_sensitivity():
    assert symbolic_identity()["symbolic_derivative_check"] == "PASS"
    data = phase_sensitivity()
    assert data["dimensionless_scale"] == "K = f_star*d_star^(1+h)*tau0^(-h)"
    rows = data["cumulative_tangent_rotation_sensitivity"]
    assert len(rows) == 9
    assert all(row["turns_per_K"] > 0 for row in rows)
    thresholds = data["unit_scale_one_turn_thresholds"]
    assert [row["h"] for row in thresholds] == [0.0, 0.005, 0.0099]
    assert all(0 < row["Q_for_one_turn"] < 1 for row in thresholds)
    by_h_q = {(row["h"], row["Q_tau_over_tau0"]): row["turns_per_K"]
              for row in rows}
    assert by_h_q[(0.0, "1e-15")] > by_h_q[(0.0, "1e-05")]
    assert abs(by_h_q[(0.0, "1e-15")] - 15 * math.log(10) / (2 * math.pi)) < 1e-12
    assert by_h_q[(0.005, "1e-15")] > by_h_q[(0.005, "1e-05")]
