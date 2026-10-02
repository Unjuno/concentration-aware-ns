"""Audit grid-dependent quadrature in the AMR early-time probe.

This reads archived finite-volume cell values and integrates piecewise-constant
and cellwise gradient-linear reconstructions against the exact MMS with tensor-product
Gauss-Legendre quadrature inside each axis-aligned cubical cell. It is a
post-hoc metric audit, not a solver acceptance test or a claim that the solver
uses either reconstruction for every operation.
"""
import json
import re
from pathlib import Path

import numpy as np
from numpy.polynomial.legendre import leggauss

from tools.analyze_amr import values
from tools.analyze_openfoam import vectors
from tools.high_gradient_reference import fields
from tools.audit_uniform_cell_center_quadrature import exact_cell_average_velocity


ROOT = Path("work/of13-amr-first-refinement-v1")
EVIDENCE = Path("evidence/of13-amr-first-refinement-v1")
LENGTH = 2 * np.pi
BASE_N = 16
NU = 0.01
FREQUENCY = 4


def _read_case(case, time):
    folder = ROOT / case / time
    text = (folder / "C").read_text()
    count = int(re.search(r"List<vector>\s+(\d+)", text)[1])
    centers = vectors(folder / "C", count)
    velocity = vectors(folder / "U", count)
    volume = values(folder / "Vc", count)
    widths = np.cbrt(volume)
    levels = np.rint(np.log2((LENGTH / BASE_N) / widths)).astype(int)
    expected_widths = (LENGTH / BASE_N) / (2.0 ** levels)
    if np.any(levels < 0) or np.any(levels > 2) or not np.allclose(
            widths, expected_widths, rtol=2e-10, atol=2e-12):
        raise ValueError(f"non-cubic or unsupported cell sizes in {case}/{time}")
    if not np.isclose(volume.sum(), LENGTH ** 3, rtol=2e-12, atol=2e-12):
        raise ValueError(f"domain volume mismatch in {case}/{time}")
    center_index = centers / widths[:, None] - 0.5
    if not np.allclose(center_index, np.rint(center_index), rtol=0, atol=2e-9):
        raise ValueError(f"cell centres are not on the expected Cartesian hierarchy in {case}/{time}")
    return centers, velocity, volume, widths


def _integrated_error(centers, velocity, volume, widths, time, order,
                      gradient=None):
    """Integrate cellwise-constant or linear-reconstructed velocity error."""
    nodes, weights = leggauss(order)
    numerator = 0.0
    denominator = 0.0
    # Iterate quadrature nodes, vectorizing across all cells to keep memory low.
    for ix, wx in zip(nodes, weights):
        for iy, wy in zip(nodes, weights):
            for iz, wz in zip(nodes, weights):
                offset = np.stack(np.broadcast_arrays(
                    ix * widths / 2, iy * widths / 2, iz * widths / 2
                ), axis=-1)
                reconstructed = velocity
                if gradient is not None:
                    reconstructed = velocity + np.einsum(
                        "nij,nj->ni", gradient, offset
                    )
                exact = fields(centers + offset, N=FREQUENCY, nu=NU,
                               time=time)["u"]
                point_weight = volume * (wx * wy * wz / 8)
                numerator += np.sum(point_weight * np.sum(
                    (reconstructed - exact) ** 2, axis=1
                ))
                denominator += np.sum(point_weight * np.sum(exact ** 2, axis=1))
    return float(np.sqrt(numerator / denominator))


def _center_sample_error(centers, velocity, volume, time):
    exact = fields(centers, N=FREQUENCY, nu=NU, time=time)["u"]
    return float(np.sqrt(np.sum(volume * np.sum((velocity - exact) ** 2, axis=1))
                         / np.sum(volume * np.sum(exact ** 2, axis=1))))


def _parent_indices(centers):
    width = LENGTH / BASE_N
    ijk = np.floor(centers / width).astype(int) % BASE_N
    # The reference generator flattens a z,y,x meshgrid: x is fastest.
    return ijk[:, 2] * BASE_N * BASE_N + ijk[:, 1] * BASE_N + ijk[:, 0]


def audit():
    cases = {
        "amr-cap5000-t002": ("amr-cap5000", "0.002", 0.002),
        "uniform-n16-t002": ("uniform-n16", "0.002", 0.002),
        "amr-cap5000-t003": ("amr-cap5000", "0.003", 0.003),
        "uniform-n16-t003": ("uniform-n16", "0.003", 0.003),
    }
    metrics = {}
    loaded = {}
    for name, (case, time, exact_time) in cases.items():
        centers, velocity, volume, widths = _read_case(case, time)
        grad = values(ROOT / case / time / "grad(U)", len(centers), 9).reshape(
            -1, 3, 3
        )
        exact_average = exact_cell_average_velocity(centers, widths, exact_time)
        cell_average_error = float(np.sqrt(
            np.sum(volume * np.sum((velocity - exact_average) ** 2, axis=1))
            / np.sum(volume * np.sum(exact_average ** 2, axis=1))
        ))
        loaded[name] = (centers, velocity, volume, widths, grad)
        metrics[name] = {
            "cell_count": len(centers),
            "cell_center_weighted_relative_l2": _center_sample_error(
                centers, velocity, volume, exact_time
            ),
            "relative_l2_to_exact_cell_averages": cell_average_error,
            "piecewise_constant_volume_l2_by_gauss_order": {
                str(order): _integrated_error(
                    centers, velocity, volume, widths, exact_time, order
                ) for order in (2, 4, 8)
            },
            "gradient_linear_reconstruction_volume_l2_by_gauss_order": {
                str(order): _integrated_error(
                    centers, velocity, volume, widths, exact_time, order,
                    gradient=grad
                ) for order in (2, 4, 8)
            },
        }

    # Reconstruct the direct parent-value mapping implied by a pure refinement
    # of the n=16 mesh; compare that mapped field on the actual AMR child cells.
    _, coarse_u, _, _, _ = loaded["amr-cap5000-t002"]
    fine_c, _, fine_v, fine_h, _ = loaded["amr-cap5000-t003"]
    parent = _parent_indices(fine_c)
    mapped_u = coarse_u[parent]
    exact_average_t002 = exact_cell_average_velocity(fine_c, fine_h, 0.002)
    exact_average_t003 = exact_cell_average_velocity(fine_c, fine_h, 0.003)
    mapped_cell_average_error_t002 = float(np.sqrt(
        np.sum(fine_v * np.sum((mapped_u - exact_average_t002) ** 2, axis=1))
        / np.sum(fine_v * np.sum(exact_average_t002 ** 2, axis=1))
    ))
    mapped_cell_average_error_t003 = float(np.sqrt(
        np.sum(fine_v * np.sum((mapped_u - exact_average_t003) ** 2, axis=1))
        / np.sum(fine_v * np.sum(exact_average_t003 ** 2, axis=1))
    ))
    map_metric = {
        "mapped_parent_count": int(len(np.unique(parent))),
        "child_cell_count": int(len(parent)),
        "parent_multiplicity_counts": {
            str(int(k)): int(v) for k, v in zip(*np.unique(
                np.bincount(parent, minlength=len(coarse_u)), return_counts=True
            ))
        },
        "cell_center_weighted_relative_l2_against_exact_t002":
            _center_sample_error(fine_c, mapped_u, fine_v, 0.002),
        "cell_center_weighted_relative_l2_against_exact_t003":
            _center_sample_error(fine_c, mapped_u, fine_v, 0.003),
        "relative_l2_to_exact_cell_averages_at_t002": mapped_cell_average_error_t002,
        "relative_l2_to_exact_cell_averages_at_t003": mapped_cell_average_error_t003,
        "integrated_relative_l2_against_exact_t002_by_gauss_order": {
            str(order): _integrated_error(
                fine_c, mapped_u, fine_v, fine_h, 0.002, order
            ) for order in (2, 4, 8)
        },
        "integrated_relative_l2_against_exact_t003_by_gauss_order": {
            str(order): _integrated_error(
                fine_c, mapped_u, fine_v, fine_h, 0.003, order
            ) for order in (2, 4, 8)
        },
        "mapped_to_solved_relative_l2_change": float(np.sqrt(
            np.sum(fine_v * np.sum((loaded["amr-cap5000-t003"][1] - mapped_u) ** 2,
                                   axis=1))
            / np.sum(fine_v * np.sum(mapped_u ** 2, axis=1))
        )),
    }
    result = {
        "method": "Tensor-product Gauss-Legendre integration of cellwise-constant U and cellwise gradient-linear U + grad(U) dot (x-C) reconstructions over validated axis-aligned cubes.",
        "interpretation": "The original center-sample norm uses a different quadrature rule on each mesh. Refinement adds sample points and can reveal intra-cell MMS variation even when mapped parent values are unchanged. The mapped field is a counterfactual transfer reconstruction, not a saved instantaneous solver state. Exact cell-average DOF errors are also reported; they rise when coarse parent values are copied to children because the finer exact cell averages resolve subcell variation.",
        "cases": metrics,
        "parent_value_mapping_counterfactual": map_metric,
        "limits": [
            "P0 and gradient-linear integrated norms are reconstruction-dependent and are not continuous pointwise bounds.",
            "The exact cell-average DOF comparison does not prove that the packaged solver's stored U is an exact volume average.",
            "Does not isolate pressure/flux correction or post-remap timestep effects.",
            "Source inspection is against public Foundation commit 18870c24d21c6b982e2cdec27b2f59738cca5f90; equivalence to the packaged binary is not established.",
        ],
    }
    output = EVIDENCE / "cell-center-quadrature-audit.json"
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    return result


if __name__ == "__main__":
    audit()
