from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools.check_material_rotation_phase import (  # noqa: E402
    illustrative_table,
    symbolic_identity,
)


def test_integrated_tangent_rotation_identity_and_scope_values():
    assert symbolic_identity()["symbolic_derivative_check"] == "PASS"
    rows = illustrative_table()["cumulative_tangent_rotation"]
    assert [row["Q_tau_over_tau0"] for row in rows] == [
        "1e-02", "3e-03", "1e-05", "1e-15"
    ]
    turns = [row["turns"] for row in rows]
    assert turns == sorted(turns)
    assert turns[2] < 1 < turns[3]
