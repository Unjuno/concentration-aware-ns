"""Compare cell-centre and cell-volume integration for the OpenFOAM matrix."""
import hashlib
import json
from pathlib import Path

import numpy as np
from numpy.polynomial.legendre import leggauss

from tools.analyze_amr import values
from tools.analyze_openfoam import vectors
from tools.high_gradient_reference import fields


ROOT = Path("work/of13-high-gradient-v2")
EVIDENCE = Path("evidence/of13-high-gradient-v2")
N_VALUES = (16, 32, 64, 128)
LENGTH = 2 * np.pi
NU = 0.01
FREQUENCY = 4


def sha256(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _read_case(n):
    case = ROOT / f"n{n}-dt0.001"
    time = 0.05
    time_dir = case / "0.05"
    centers = vectors(time_dir / "C", n ** 3)
    velocity = vectors(time_dir / "U", n ** 3)
    axis = (np.arange(n) + 0.5) * LENGTH / n
    z, y, x = np.meshgrid(axis, axis, axis, indexing="ij")
    expected = np.stack((x, y, z), axis=-1).reshape(-1, 3)
    if not np.allclose(centers, expected, atol=1e-12, rtol=0):
        raise ValueError(f"unexpected structured mesh ordering for n={n}")
    if not (case / "log.foamRun").read_text().rstrip().endswith("End"):
        raise ValueError(f"case n={n} is not a completed run")
    return case, centers, velocity, LENGTH / n


def center_sample_error(centers, velocity, n, time):
    reference = fields(centers, N=FREQUENCY, nu=NU, time=time)["u"]
    volume = (LENGTH / n) ** 3
    return float(np.sqrt(
        volume * np.sum((velocity - reference) ** 2)
        / (volume * np.sum(reference ** 2))
    ))


def periodic_gauss_gradient(velocity, n, width):
    """Reproduce Gauss-linear FV gradients on the uniform orthogonal periodic mesh."""
    grid = velocity.reshape(n, n, n, 3).transpose(2, 1, 0, 3)
    gradient = np.stack([
        (np.roll(grid, -1, axis=axis) - np.roll(grid, 1, axis=axis))
        / (2 * width)
        for axis in range(3)
    ], axis=-1)
    return gradient.transpose(2, 1, 0, 3, 4).reshape(-1, 3, 3)


def exact_cell_average_velocity(centers, width, time):
    """Closed-form cell averages using the MMS Fourier polynomial factors."""
    modes = np.array((1.0, 2.0, 3.0, 4.0))
    amplitudes = np.array((56.0, 28.0, 8.0, 1.0))
    x, y, z = centers.T
    widths = np.broadcast_to(np.asarray(width, dtype=float), x.shape)
    sinc = np.sinc(widths[:, None] * modes[None, :] / (2 * np.pi))
    average_g_y = (35.0 + np.sum(
        amplitudes * np.cos(y[:, None] * modes) * sinc, axis=1
    )) / 128.0
    average_g_z = (35.0 + np.sum(
        amplitudes * np.cos(z[:, None] * modes) * sinc, axis=1
    )) / 128.0
    average_g_prime_y = -np.sum(
        amplitudes * modes * np.sin(y[:, None] * modes) * sinc, axis=1
    ) / 128.0
    average_sin = np.sin(FREQUENCY * x) * np.sinc(
        FREQUENCY * widths / (2 * np.pi)
    )
    average_cos = np.cos(FREQUENCY * x) * np.sinc(
        FREQUENCY * widths / (2 * np.pi)
    )
    decay = np.exp(-time)
    return np.stack((
        decay * average_g_prime_y * average_g_z * average_sin / FREQUENCY**2,
        -decay * average_g_y * average_g_z * average_cos / FREQUENCY,
        np.zeros_like(x),
    ), axis=1)


def verify_cell_average_formula():
    """Compare the closed form with independent tensor Gauss quadrature."""
    case, centers, _, width = _read_case(16)
    del case
    centers = centers[[0, 17, 511, 2048, -1]]
    exact_average = exact_cell_average_velocity(centers, width, 0.05)
    nodes, weights = leggauss(10)
    numerical_average = np.zeros_like(exact_average)
    for ix, wx in zip(nodes, weights):
        for iy, wy in zip(nodes, weights):
            for iz, wz in zip(nodes, weights):
                offset = np.array((ix, iy, iz)) * (width / 2)
                numerical_average += (wx * wy * wz / 8) * fields(
                    centers + offset, N=FREQUENCY, nu=NU, time=0.05
                )["u"]
    return float(np.max(np.abs(exact_average - numerical_average)))


def integrated_error(centers, velocity, width, time, order, gradient=None,
                     chunk_size=50000):
    """Integrate P0 or linear-gradient U against exact MMS over each cube."""
    nodes, weights = leggauss(order)
    numerator = 0.0
    denominator = 0.0
    cell_volume = width ** 3
    for start in range(0, len(centers), chunk_size):
        stop = min(start + chunk_size, len(centers))
        cell_centers = centers[start:stop]
        cell_velocity = velocity[start:stop]
        for ix, wx in zip(nodes, weights):
            for iy, wy in zip(nodes, weights):
                for iz, wz in zip(nodes, weights):
                    offset = np.array((ix, iy, iz)) * (width / 2)
                    reconstructed = cell_velocity
                    if gradient is not None:
                        reconstructed = cell_velocity + np.einsum(
                            "nij,j->ni", gradient[start:stop], offset
                        )
                    exact = fields(cell_centers + offset, N=FREQUENCY, nu=NU,
                                   time=time)["u"]
                    weight = cell_volume * wx * wy * wz / 8
                    numerator += weight * np.sum((reconstructed - exact) ** 2)
                    denominator += weight * np.sum(exact ** 2)
    return float(np.sqrt(numerator / denominator))


def audit():
    # The two rules bracket expected spatial quadrature needs for this smooth
    # frequency-4 MMS; convergence is explicitly checked per resolution.
    orders = {16: (8, 10), 32: (5, 6), 64: (3, 4), 128: (3, 4)}
    rows = []
    crosscheck = {}
    for n in N_VALUES:
        case, centers, velocity, width = _read_case(n)
        gradient = periodic_gauss_gradient(velocity, n, width)
        if n == 16:
            probe = Path("work/of13-amr-first-refinement-v1/uniform-n16/0.002")
            probe_velocity = vectors(probe / "U", n ** 3)
            probe_gradient = periodic_gauss_gradient(
                probe_velocity, n, LENGTH / n
            )
            saved = values(probe / "grad(U)", n ** 3, 9).reshape(
                n, n, n, 3, 3
            ).swapaxes(-1, -2).reshape(-1, 3, 3)
            maximum_difference = float(np.max(np.abs(probe_gradient - saved)))
            if maximum_difference > 1e-12:
                raise ValueError("periodic gradient does not match OpenFOAM grad(U)")
            crosscheck = {
                "saved_field": str(probe / "grad(U)"),
                "max_abs_difference": maximum_difference,
                "saved_field_sha256": sha256(probe / "grad(U)"),
            }
        p0 = {str(order): integrated_error(
            centers, velocity, width, 0.05, order
        ) for order in orders[n]}
        p1 = {str(order): integrated_error(
            centers, velocity, width, 0.05, order, gradient=gradient
        ) for order in orders[n]}
        exact_average = exact_cell_average_velocity(centers, width, 0.05)
        rows.append({
            "n": n,
            "case": case.name,
            "end_time": 0.05,
            "cell_count": int(len(centers)),
            "center_sample_relative_l2": center_sample_error(
                centers, velocity, n, 0.05
            ),
            "exact_cell_average_relative_l2": float(np.linalg.norm(
                velocity - exact_average
            ) / np.linalg.norm(exact_average)),
            "piecewise_constant_cell_volume_relative_l2_by_gauss_order": p0,
            "cellwise_gauss_linear_cell_volume_relative_l2_by_gauss_order": p1,
            "quadrature_abs_difference": {
                "piecewise_constant": abs(p0[str(orders[n][0])] - p0[str(orders[n][1])]),
                "gauss_linear": abs(p1[str(orders[n][0])] - p1[str(orders[n][1])]),
            },
            "field_sha256": {
                "C": sha256(case / "0.05" / "C"),
                "U": sha256(case / "0.05" / "U"),
                "parameters": sha256(case / "parameters.json"),
                "solver_log": sha256(case / "log.foamRun"),
            },
        })
    result = {
        "scope": "Post-hoc exact-MMS velocity-error audit of the four completed OpenFOAM uniform spatial cases at dt=0.001, t=0.05.",
        "reconstructions": [
            "Stored cell-centre U held constant within each verified uniform Cartesian cell.",
            "Cellwise linear field U + grad(U) dot (x-C), with periodic Gauss gradient from the uniform orthogonal finite-volume stencil.",
        ],
        "gradient_method": "Periodic central difference, cross-checked against the saved OpenFOAM grad(U) postprocessing field from the AMR probe with the tensor index order normalized.",
        "gradient_crosscheck": crosscheck,
        "cell_average_formula_crosscheck_max_abs_difference":
            verify_cell_average_formula(),
        "not_claimed": [
            "This is not the solver's unique reconstructed field or a continuous pointwise bound.",
            "It does not recompute gradient, vorticity or spectrum gates.",
            "It does not change the frozen acceptance protocol; it tests how much its centre-sampled velocity norm depends on spatial quadrature.",
        ],
        "cases": rows,
    }
    output = EVIDENCE / "uniform-cell-center-quadrature-audit.json"
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    return result


if __name__ == "__main__":
    audit()
