"""Reconcile same-run AMR nested cell-average decomposition artifacts."""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNS = (
    (16, "evidence/of13-amr-same-run-map-v4-run3/analysis.json"),
    (32, "evidence/of13-amr-same-run-map-v5-n32/analysis.json"),
    (64, "evidence/of13-amr-same-run-map-v7-n64/analysis.json"),
    (128, "evidence/of13-amr-same-run-map-v8-n128/analysis.json"),
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def audit(root: Path = ROOT) -> dict:
    rows = []
    for n, relative in RUNS:
        path = root / relative
        source = json.loads(path.read_text())
        decomposition = source["exact_cell_average_reference"][
            "same_run_cell_average_error_decomposition"
        ]
        injection = source["parent_value_injection"]
        expected_parent_cells = n**3
        if source["preMap_cells"] != expected_parent_cells:
            raise ValueError(f"n={n}: unexpected preMap cell count")
        if injection["mapped_vs_parent_injection_relative_l2"] != 0:
            raise ValueError(f"n={n}: map is not exact parent injection")
        if abs(decomposition["twice_normalized_cross_term"]) > 1e-12:
            raise ValueError(f"n={n}: decomposition cross term is not negligible")
        residual = decomposition["identity_residual"]
        if abs(residual) > 1e-12:
            raise ValueError(f"n={n}: decomposition identity residual is too large")

        ref = source["exact_cell_average_reference"]
        parent = math.sqrt(
            decomposition["inherited_parent_solution_error_squared_relative"]
        )
        variation = math.sqrt(
            decomposition["exact_child_average_refinement_change_squared_relative"]
        )
        total = math.sqrt(
            decomposition["total_mapped_cell_average_error_squared_relative"]
        )
        rows.append({
            "base_cells_per_axis": n,
            "preMap_cells": source["preMap_cells"],
            "mapped_cells": source["mapped_cells"],
            "parent_dof_error_relative": parent,
            "subcell_average_variation_relative": variation,
            "mapped_dof_error_relative": total,
            "source_preMap_average_error_relative": ref[
                "preMap_velocity_relative_l2_vs_exact_cell_averages"
            ],
            "source_mapped_average_error_relative": ref[
                "mapped_velocity_relative_l2_vs_exact_cell_averages"
            ],
            "map_difference_relative_l2": injection[
                "mapped_vs_parent_injection_relative_l2"
            ],
            "cross_term_normalized": decomposition["twice_normalized_cross_term"],
            "identity_residual": residual,
            "analysis_path": relative,
            "analysis_sha256": _sha256(path),
            "run_archive_sha256": source["archive_sha256"],
        })

    rates = []
    for coarse, fine in zip(rows, rows[1:]):
        ratio = fine["subcell_average_variation_relative"] / coarse[
            "subcell_average_variation_relative"
        ]
        rates.append({
            "from_n": coarse["base_cells_per_axis"],
            "to_n": fine["base_cells_per_axis"],
            "variation_ratio": ratio,
            "observed_order": -math.log2(ratio),
        })

    return {
        "status": "PASS_SOURCE_ARTIFACT_RECONCILIATION",
        "identity": (
            "sum_K |K||a_P-u_K|^2 = |P||a_P-u_P|^2 "
            "+ sum_K |K||u_K-u_P|^2"
        ),
        "identity_scope": (
            "Nested-partition identity for exact child cell averages and a "
            "parent value injected piecewise-constantly; it does not assert "
            "that OpenFOAM volVectorField values are exact cell averages."
        ),
        "source_artifact_checks": {
            "runs": len(rows),
            "all_mapped_fields_equal_parent_injection": all(
                row["map_difference_relative_l2"] == 0 for row in rows
            ),
            "max_abs_identity_residual": max(
                abs(row["identity_residual"]) for row in rows
            ),
            "quality_verdicts_assigned_by_this_audit": False,
            "raw_solver_archives_or_diagnostics_recomputed": False,
        },
        "rows": rows,
        "successive_refinement_scaling": rates,
        "interpretation": (
            "Descriptive cross-resolution reconciliation of previously "
            "captured same-run analyses; not an AMR convergence certificate "
            "or solver validation."
        ),
    }


def main() -> None:
    result = audit()
    output = ROOT / "evidence/tests/openfoam-amr-nested-cell-average-audit-2026-10-03.json"
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
