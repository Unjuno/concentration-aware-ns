"""Arb enclosures for derivative suprema of a specified trig interpolant.

This certifies the explicit real trigonometric interpolant through archived
cell values against the analytic MMS. It does not certify the OpenFOAM
finite-volume field between cells.
"""
import hashlib
import json
import platform
import re
import sys
import tarfile
from pathlib import Path

import numpy as np
import flint
from flint import acb, acb_mat, arb, ctx


ROOT = Path(__file__).resolve().parents[1]
CASES = (
    (16, "evidence/of13-high-gradient-v2/n16-dt0.001.tar.gz"),
    (32, "evidence/of13-high-gradient-v2/n32-dt0.001.tar.gz"),
    (64, "evidence/of13-high-gradient-v2/n64-dt0.001.tar.gz"),
)


def _complex_magnitude_upper(value):
    """Return an outward ball upper bound for the Euclidean complex modulus."""
    real_upper = value.real.abs_upper()
    imag_upper = value.imag.abs_upper()
    return (real_upper**2 + imag_upper**2).sqrt()


def fourier_gradient_l1_bound(coefficients):
    """Bound sup ||grad e||_F by sum_k |k| ||e_hat_k||_2.

    ``coefficients`` contains (kx, ky, kz, (u0, u1, u2)) entries. Each
    coefficient may be a point or an Arb complex ball. Nyquist coefficients
    may be split between their real sine aliases; the total coefficient l1
    norm and |k| are unchanged by that split.
    """
    total = arb(0)
    for kx, ky, kz, vector in coefficients:
        radius2 = kx*kx + ky*ky + kz*kz
        if not radius2:
            continue
        vector_norm2 = arb(0)
        for coefficient in vector:
            magnitude = _complex_magnitude_upper(acb(coefficient))
            vector_norm2 += magnitude**2
        total += arb(radius2).sqrt() * vector_norm2.sqrt()
    return total


def _parse_vectors_exact(data, expected_count):
    text = data.decode("ascii")
    text = re.sub(r"/\*.*?\*/|//[^\n]*", "", text, flags=re.S)
    match = re.search(
        r"internalField\s+nonuniform\s+List<vector>\s+(\d+)\s*\((.*?)\)\s*;",
        text, re.S,
    )
    if not match or int(match.group(1)) != expected_count:
        raise ValueError("expected a matching ASCII nonuniform vector field")
    tokens = re.findall(r"[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?", match.group(2))
    if len(tokens) != expected_count * 3:
        raise ValueError("invalid vector token count")
    return [arb(token) for token in tokens]


def _envelope(q):
    return (35 + 56*q.cos() + 28*(2*q).cos() + 8*(3*q).cos() + (4*q).cos()) / 128


def _envelope_d1(q):
    return -(56*q.sin() + 56*(2*q).sin() + 24*(3*q).sin() + 4*(4*q).sin()) / 128


def _envelope_d2(q):
    return -(56*q.cos() + 112*(2*q).cos() + 72*(3*q).cos() + 16*(4*q).cos()) / 128


def _reference_samples(n, frequency, end):
    _validate_reference_mode(frequency, n)
    pi = arb.pi()
    coordinates = [pi * arb(2*j + 1) / n for j in range(n)]
    env = [_envelope(q) for q in coordinates]
    env1 = [_envelope_d1(q) for q in coordinates]
    env2 = [_envelope_d2(q) for q in coordinates]
    sx = [(frequency*q).sin() for q in coordinates]
    cx = [(frequency*q).cos() for q in coordinates]
    decay = (-arb(str(end))).exp()
    values = np.empty((n, n, n, 3), dtype=object)
    gradient_denominator_lower = arb(0)
    vorticity_denominator_lower = arb(0)
    for iz in range(n):
        for iy in range(n):
            chi = env[iy] * env[iz]
            chi_y = env1[iy] * env[iz]
            chi_yy = env2[iy] * env[iz]
            for ix in range(n):
                values[iz, iy, ix, 0] = chi_y * sx[ix] / (frequency**2) * decay
                values[iz, iy, ix, 1] = -chi * cx[ix] / frequency * decay
                values[iz, iy, ix, 2] = arb(0)
                grad_component = (chi * sx[ix] * decay).abs_lower()
                if grad_component > gradient_denominator_lower:
                    gradient_denominator_lower = grad_component
                omega_z = ((chi - chi_yy/(frequency**2)) * sx[ix] * decay).abs_lower()
                if omega_z > vorticity_denominator_lower:
                    vorticity_denominator_lower = omega_z
    return values, gradient_denominator_lower, vorticity_denominator_lower


def _dft_matrix(n):
    pi = arb.pi()
    return acb_mat(n, n, [
        acb(0, -2*pi*arb(mode*sample)/n).exp() / n
        for mode in range(n) for sample in range(n)
    ])


def _transform_axis(values, axis, matrix):
    n = values.shape[axis]
    moved = np.moveaxis(values, axis, -1)
    rows = moved.reshape(-1, n)
    rhs = acb_mat(n, rows.shape[0], [
        acb(rows[group, sample])
        for sample in range(n) for group in range(rows.shape[0])
    ])
    transformed = matrix * rhs
    output = np.empty((rows.shape[0], n), dtype=object)
    for mode in range(n):
        for group in range(rows.shape[0]):
            output[group, mode] = transformed[mode, group]
    return np.moveaxis(output.reshape(moved.shape), -1, axis)


def _fourier_coefficients(error_samples):
    n = error_samples.shape[0]
    matrix = _dft_matrix(n)
    coefficients = np.empty(error_samples.shape, dtype=object)
    for index in np.ndindex(error_samples.shape):
        coefficients[index] = acb(error_samples[index])
    for axis in range(3):
        coefficients = _transform_axis(coefficients, axis, matrix)
    return coefficients


def _mode_number(index, n):
    # Odd grids have no Nyquist singleton: floor(n/2) is a positive mode.
    # Keep the existing negative representative for the even-grid singleton.
    return index if index < (n+1)//2 else index-n


def _validate_reference_mode(frequency, n):
    """Require a positive mode strictly below Nyquist for exact sampling."""
    if not isinstance(frequency, int) or not isinstance(n, int) or n < 2:
        raise ValueError("frequency and grid size must be integers, with n >= 2")
    if frequency <= 0 or 2*frequency >= n:
        raise ValueError(
            f"reference mode {frequency} is not strictly below Nyquist for n={n}"
        )


def _coefficient_rows(coefficients):
    n = coefficients.shape[0]
    rows = []
    for iz, iy, ix in np.ndindex(n, n, n):
        vector = tuple(coefficients[iz, iy, ix, component] for component in range(3))
        rows.append((_mode_number(ix, n), _mode_number(iy, n), _mode_number(iz, n), vector))
    return rows


def _vector_error_l1_bound(coefficients):
    total = arb(0)
    for index in np.ndindex(coefficients.shape[:3]):
        norm2 = arb(0)
        for component in range(3):
            magnitude = _complex_magnitude_upper(coefficients[index + (component,)])
            norm2 += magnitude**2
        total += norm2.sqrt()
    return total


def _load_case(root, n, relative_path, expected_hash):
    archive_path = root / relative_path
    raw = archive_path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if digest != expected_hash:
        raise ValueError(f"archive hash mismatch for n={n}: {digest}")
    with tarfile.open(archive_path, "r:gz") as tar:
        members = tar.getmembers()
        case_root = {Path(m.name).parts[0] for m in members if m.name}.pop()
        parameters = json.load(tar.extractfile(f"{case_root}/parameters.json"))
        endpoint = format(parameters["end"], ".15g")
        u_members = [m for m in members if m.name.startswith(f"{case_root}/{endpoint}/")
                     and Path(m.name).name == "U"]
        if len(u_members) != 1:
            raise ValueError(f"expected one endpoint U field for n={n}")
        solver = _parse_vectors_exact(tar.extractfile(u_members[0]).read(), n**3)
        c_members = [m for m in members if m.name.startswith(f"{case_root}/{endpoint}/")
                     and Path(m.name).name == "C"]
        if len(c_members) != 1:
            raise ValueError(f"expected one endpoint C field for n={n}")
        centers = _parse_vectors_exact(tar.extractfile(c_members[0]).read(), n**3)
    if parameters["n"] != n or parameters["frequency"] != 4:
        raise ValueError(f"case parameters do not match protocol for n={n}")
    _validate_reference_mode(parameters["frequency"], n)
    return digest, parameters, solver, centers


def audit(root=ROOT, precision_bits=128):
    """Recompute rigorous coefficient and denominator balls for n=16/32/64."""
    root = Path(root)
    protocol_path = root / "protocols/openfoam-derivative-diagnostics-v3.json"
    protocol = json.loads(protocol_path.read_text())
    frozen_protocol = json.loads((root / "protocols/high-gradient-of13-v2.json").read_text())
    manifest = json.loads((root / "evidence/of13-high-gradient-v2/manifest-current-2026-09-30.json").read_text())
    expected = {row["case"]: row["archive_sha256"] for row in manifest["completed_cases"]}
    previous_precision = ctx.prec
    ctx.prec = precision_bits
    rows = []
    try:
        for n, relative_path in CASES:
            case = f"n{n}-dt0.001"
            digest, parameters, solver_values, center_values = _load_case(
                root, n, relative_path, expected[case]
            )
            reference, gradient_lower, vorticity_lower = _reference_samples(
                n, frozen_protocol["frequency_N"], parameters["end"]
            )
            ideal_axis = [arb.pi() * arb(2*j+1) / n for j in range(n)]
            center_offset_upper = arb(0)
            grid_error = np.empty((n, n, n, 3), dtype=object)
            cursor = 0
            for iz in range(n):
                for iy in range(n):
                    for ix in range(n):
                        for component, coordinate_index in enumerate((ix, iy, iz)):
                            center = center_values[cursor*3 + component]
                            offset = (center - ideal_axis[coordinate_index]).abs_upper()
                            if offset > center_offset_upper:
                                center_offset_upper = offset
                        for component in range(3):
                            grid_error[iz, iy, ix, component] = (
                                solver_values[cursor*3 + component] - reference[iz, iy, ix, component]
                            )
                        cursor += 1
            if center_offset_upper > arb("1e-12"):
                raise ValueError(f"serialized centers are not the declared ideal lattice for n={n}")
            coefficients = _fourier_coefficients(grid_error)
            gradient_error_upper = fourier_gradient_l1_bound(_coefficient_rows(coefficients))
            vorticity_error_upper = (arb(2).sqrt() * gradient_error_upper).upper()
            gradient_ratio_upper = (gradient_error_upper / gradient_lower).upper()
            vorticity_ratio_upper = (vorticity_error_upper / vorticity_lower).upper()
            velocity_error_upper = _vector_error_l1_bound(coefficients).upper()
            if not all(coefficients[index].is_finite() for index in np.ndindex(coefficients.shape)):
                raise ArithmeticError(f"non-finite Arb coefficient enclosure for n={n}")
            rows.append({
                "case": case,
                "n": n,
                "dt": parameters["dt"],
                "archive": relative_path,
                "archive_sha256": digest,
                "max_serialized_center_offset_from_ideal_lattice_upper": str(center_offset_upper.upper()),
                "gradient_error_supremum_upper": str(gradient_error_upper.upper()),
                "gradient_reference_supremum_lower": str(gradient_lower.lower()),
                "gradient_relative_supremum_upper_fraction": str(gradient_ratio_upper.upper()),
                "vorticity_error_supremum_upper": str(vorticity_error_upper.upper()),
                "vorticity_reference_supremum_lower": str(vorticity_lower.lower()),
                "vorticity_relative_supremum_upper_fraction": str(vorticity_ratio_upper.upper()),
                "velocity_error_supremum_upper_for_same_interpolant": str(velocity_error_upper.upper()),
                "within_frozen_v2_gradient_peak_tolerance": gradient_ratio_upper < arb(str(frozen_protocol["local_quality_relative_error_thresholds"]["max_gradient"])),
                "within_frozen_v2_vorticity_peak_tolerance": vorticity_ratio_upper < arb(str(frozen_protocol["local_quality_relative_error_thresholds"]["max_vorticity"])),
            })
    finally:
        ctx.prec = previous_precision
    return {
        "protocol": "protocols/openfoam-derivative-diagnostics-v3.json",
        "protocol_sha256": hashlib.sha256(protocol_path.read_bytes()).hexdigest(),
        "precision_bits": precision_bits,
        "arithmetic": "python-flint Arb/Acb ball enclosures; exact decimal OpenFOAM U/C tokens and Arb-evaluated analytic MMS",
        "environment": {"python": sys.version.split()[0], "implementation": platform.python_implementation(), "numpy": np.__version__, "python_flint": flint.__version__},
        "reconstruction": "real periodic cell-centered trigonometric interpolant through archived U values; tensor Nyquist aliases use real sine representatives",
        "bound": "sup ||grad e||_F <= sum_k |k| ||e_hat_k||_2; sup ||curl e||_2 <= sqrt(2)*sup ||grad e||_F; denominator lower bounds use the maximum absolute analytic component sampled on the grid",
        "finite_volume_field_certified": False,
        "continuous_inter_sample_bound_for_named_reconstruction": True,
        "frozen_v2_verdicts_changed": False,
        "cases": rows,
        "analysis_source_sha256": {
            "tools/audit_openfoam_trig_supremum.py": hashlib.sha256((root / "tools/audit_openfoam_trig_supremum.py").read_bytes()).hexdigest(),
            "tools/high_gradient_reference.py": hashlib.sha256((root / "tools/high_gradient_reference.py").read_bytes()).hexdigest(),
            "protocols/high-gradient-of13-v2.json": hashlib.sha256((root / "protocols/high-gradient-of13-v2.json").read_bytes()).hexdigest(),
        },
        "limitations": [
            "This certifies one explicitly named trigonometric reconstruction of the archived samples, not OpenFOAM's finite-volume field or its face/gradient reconstruction.",
            "The analytic MMS modes are within the represented frequency range for all included grids, so its interpolant reproduces the continuum reference exactly.",
            "The existing frozen quality gate also includes velocity L2, energy and spectrum; derivative bounds alone do not determine overall local quality.",
        ],
    }


if __name__ == "__main__":
    result = audit()
    output = ROOT / "evidence/tests/openfoam-trig-supremum-arb-v3.json"
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
