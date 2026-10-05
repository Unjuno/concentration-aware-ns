"""Read generated inputs independently and check their Couette geometry/physics."""

import hashlib
import json
from pathlib import Path
import re
import tempfile
import unittest

import numpy as np

from tools.build_interface_operator_cases import build_cases, generate


def read_internal_field(path):
    text = path.read_text()
    match = re.search(
        r"internalField\s+nonuniform\s+List<(scalar|vector)>\s+(\d+)\s*\((.*?)\)\s*;",
        text, re.DOTALL,
    )
    if match is None:
        raise AssertionError(f"missing nonuniform field in {path}")
    kind, count, body = match.groups()
    if kind == "vector":
        values = np.array([[float(value) for value in row.split()]
                           for row in re.findall(r"\(([^()]*)\)", body)])
    else:
        values = np.array([float(value) for value in body.split()])
    if len(values) != int(count):
        raise AssertionError(f"field count mismatch in {path}")
    return text, values


def read_named_block(text, name):
    """Read one balanced dictionary block, without depending on line formatting."""
    match = re.search(r"\b" + re.escape(name) + r"\s*\{", text)
    if match is None:
        raise AssertionError(f"missing block {name}")
    start = match.end()
    depth = 1
    for end in range(start, len(text)):
        depth += (text[end] == "{") - (text[end] == "}")
        if depth == 0:
            return text[start:end]
    raise AssertionError(f"unclosed block {name}")


def read_entry(text, name):
    match = re.search(r"\b" + re.escape(name) + r"\s+([^;]+);", text)
    if match is None:
        raise AssertionError(f"missing entry {name}")
    return " ".join(match.group(1).split())


class InterfaceOperatorCasesTests(unittest.TestCase):
    def assert_case_physics(self, case, nx, mu_left, mu_right, traction):
        mesh_text = (case / "system/blockMeshDict").read_text()
        vertices_block = re.search(r"vertices\s*\((.*?)\)\s*;", mesh_text,
                                   re.DOTALL).group(1)
        vertices = np.array([[float(value) for value in row.split()]
                             for row in re.findall(r"\(([^()]*)\)", vertices_block)])
        np.testing.assert_array_equal(vertices.min(axis=0), [-1, 0, 0])
        np.testing.assert_array_equal(vertices.max(axis=0), [1, 1, 1])
        blocks = re.findall(r"hex\s*\(([^()]*)\)\s*\(([^()]*)\)\s*"
                            r"simpleGrading\s*\(([^()]*)\)", mesh_text)
        self.assertEqual(len(blocks), 1)
        labels, counts, grading = blocks[0]
        self.assertEqual([int(value) for value in labels.split()], list(range(8)))
        self.assertEqual([int(value) for value in counts.split()], [nx, 2, 2])
        self.assertEqual([float(value) for value in grading.split()], [1, 1, 1])
        self.assertEqual(read_entry(mesh_text, "scale"), "1")

        # Reconstruct an independent cell lattice from the parsed mesh extents.
        faces_x = np.linspace(vertices[:, 0].min(), vertices[:, 0].max(), nx + 1)
        self.assertEqual(faces_x[nx // 2], 0)
        axes = [(faces_x[:-1] + faces_x[1:]) / 2, np.array([0.25, 0.75]),
                np.array([0.25, 0.75])]
        z, y, x = np.meshgrid(axes[2], axes[1], axes[0], indexing="ij")
        centres = np.column_stack((x.ravel(), y.ravel(), z.ravel()))
        metadata = json.loads((case / "case_metadata.json").read_text())
        np.testing.assert_allclose(metadata["mesh"]["cell_centres"], centres,
                                   rtol=0, atol=2 * np.finfo(float).eps)
        self.assertEqual(metadata["mesh"]["interface"]["face_index_along_x"], nx // 2)
        self.assertEqual(metadata["mesh"]["cell_count"], 4 * nx)
        self.assertEqual(metadata["inputs"]["density"], 1)

        u_text, velocity = read_internal_field(case / "0/U")
        shear_text, shear = read_internal_field(case / "0/shear")
        mu_text, mu = read_internal_field(case / "0/mu")
        self.assertEqual(velocity.shape, (4 * nx, 3))
        np.testing.assert_array_equal(velocity[:, 0], 0)
        np.testing.assert_array_equal(velocity[:, 2], 0)
        np.testing.assert_array_equal(velocity[:, 1], shear)
        self.assertEqual(read_entry(u_text, "dimensions"), "[0 1 -1 0 0 0 0]")
        self.assertEqual(read_entry(shear_text, "dimensions"), "[0 1 -1 0 0 0 0]")
        self.assertEqual(read_entry(mu_text, "dimensions"), "[0 2 -1 0 0 0 0]")
        np.testing.assert_array_equal(mu[centres[:, 0] < 0], mu_left)
        np.testing.assert_array_equal(mu[centres[:, 0] > 0], mu_right)

        patch_faces = {}
        for name in ("xm", "xp", "ym", "yp", "zm", "zp"):
            patch = read_named_block(mesh_text, name)
            indices = [int(value) for value in re.search(
                r"faces\s*\(\(([^()]*)\)\)\s*;", patch).group(1).split()]
            patch_faces[name] = vertices[indices]
            normal = np.cross(patch_faces[name][1] - patch_faces[name][0],
                              patch_faces[name][2] - patch_faces[name][1])
            axis = "xyz".index(name[0])
            other_axes = [index for index in range(3) if index != axis]
            np.testing.assert_array_equal(normal[other_axes], 0)
            self.assertGreater(normal[axis] * (-1 if name[1] == "m" else 1), 0)
            self.assertEqual(np.linalg.norm(normal), 1 if axis == 0 else 2)

            if name in ("xm", "xp"):
                self.assertEqual(read_entry(patch, "type"), "wall")
                wall_x = -1 if name == "xm" else 1
                wall_mu = mu_left if wall_x < 0 else mu_right
                wall_velocity = traction * wall_x / wall_mu
                for field_text, expected in (
                    (u_text, f"uniform (0 {wall_velocity:.17g} 0)"),
                    (shear_text, f"uniform {wall_velocity:.17g}"),
                    (mu_text, f"uniform {wall_mu:.17g}"),
                ):
                    field_patch = read_named_block(read_named_block(field_text, "boundaryField"), name)
                    self.assertEqual(read_entry(field_patch, "type"), "fixedValue")
                    self.assertEqual(read_entry(field_patch, "value"), expected)
            else:
                self.assertEqual(read_entry(patch, "type"), "cyclic")
                peer = name[0] + ("p" if name[1] == "m" else "m")
                self.assertEqual(read_entry(patch, "neighbourPatch"), peer)
                for field_text in (u_text, shear_text, mu_text):
                    field_patch = read_named_block(read_named_block(field_text, "boundaryField"), name)
                    self.assertEqual(read_entry(field_patch, "type"), "cyclic")

        # Each stripe is constant tangentially.  Recover each one-sided slope
        # using the generated wall and cell values, then extrapolate its trace.
        values = shear.reshape(2, 2, nx)
        for row in values.reshape(4, nx):
            np.testing.assert_array_equal(row, values[0, 0])
            traces = []
            for side, wall_x, wall_mu in (
                (slice(0, nx // 2), -1, mu_left),
                (slice(nx // 2, nx), 1, mu_right),
            ):
                samples_x = np.r_[wall_x, axes[0][side]]
                samples_u = np.r_[traction * wall_x / wall_mu, row[side]]
                slopes = np.diff(samples_u) / np.diff(samples_x)
                np.testing.assert_allclose(wall_mu * slopes, traction, rtol=2e-14,
                                           atol=2e-14 * abs(traction))
                traces.append(samples_u[-1] - slopes[-1] * samples_x[-1])
            np.testing.assert_allclose(traces, [0, 0], rtol=0,
                                       atol=2e-14 * abs(traction))

        # The exact sampled kink has the intended scalar interface behaviour:
        # harmonic interpolation gives the continuum flux, while arithmetic
        # interpolation gives the analytically predicted large nodal mismatch.
        i, j = nx // 2 - 1, nx // 2
        secant = (values[0, 0, j] - values[0, 0, i]) / (axes[0][j] - axes[0][i])
        harmonic_flux = 2 * mu_left * mu_right / (mu_left + mu_right) * secant
        arithmetic_flux = (mu_left + mu_right) / 2 * secant
        self.assertAlmostEqual(harmonic_flux / traction, 1, places=13)
        self.assertAlmostEqual(arithmetic_flux / traction,
                               (mu_left + mu_right) ** 2 / (4 * mu_left * mu_right),
                               places=12)

    def test_preregistered_meshes_have_compatible_exact_fields_and_boundaries(self):
        with tempfile.TemporaryDirectory() as directory:
            collection = Path(directory) / "cases"
            build_cases(collection)
            self.assertEqual(sorted(path.name for path in collection.iterdir()),
                             ["nx16", "nx32", "nx64"])
            for nx in (16, 32, 64):
                with self.subTest(nx=nx):
                    self.assert_case_physics(collection / f"nx{nx}", nx, 1, 100, 1)

    def test_general_coefficients_negative_traction_and_minimal_grid(self):
        with tempfile.TemporaryDirectory() as directory:
            for nx in (2, 6):
                with self.subTest(nx=nx):
                    case = Path(directory) / f"nx{nx}"
                    generate(case, nx=nx, mu_left=3, mu_right=17, traction=-2.5)
                    self.assert_case_physics(case, nx, 3, 17, -2.5)

    def test_discretization_and_solver_settings_match_scalar_probe_contract(self):
        with tempfile.TemporaryDirectory() as directory:
            case = Path(directory) / "case"
            generate(case)
            schemes = (case / "system/fvSchemes").read_text()
            for name, default in (
                ("gradSchemes", "Gauss linear"),
                ("laplacianSchemes", "Gauss linear orthogonal"),
                ("interpolationSchemes", "linear"),
                ("snGradSchemes", "orthogonal"),
            ):
                self.assertEqual(read_entry(read_named_block(schemes, name), "default"), default)
            flux_required = read_named_block(schemes, "fluxRequired")
            for name in ("shear", "constantControl"):
                self.assertRegex(flux_required, r"\b" + name + r"\s*;")
            solver = read_named_block((case / "system/fvSolution").read_text(), "shear")
            self.assertEqual(read_entry(solver, "solver"), "PCG")
            self.assertEqual(read_entry(solver, "preconditioner"), "DIC")
            self.assertEqual(float(read_entry(solver, "tolerance")), 1e-12)
            self.assertEqual(float(read_entry(solver, "relTol")), 0)
            control = (case / "system/controlDict").read_text()
            self.assertEqual(read_entry(control, "application"), "interfaceOperatorProbe")
            self.assertEqual(read_entry(control, "startTime"), "0")

    def test_constant_control_is_the_diffusion_null_mode_on_every_patch(self):
        with tempfile.TemporaryDirectory() as directory:
            case = Path(directory) / "case"
            generate(case)
            text = (case / "0/constantControl").read_text()
            self.assertEqual(read_entry(text, "class"), "volScalarField")
            self.assertEqual(read_entry(text, "dimensions"), "[0 1 -1 0 0 0 0]")
            internal = read_entry(text, "internalField")
            self.assertEqual(internal.split()[0], "uniform")
            internal_value = float(internal.split()[1])
            self.assertEqual(internal_value, 1)
            boundary = read_named_block(text, "boundaryField")
            for name in ("xm", "xp", "ym", "yp", "zm", "zp"):
                patch = read_named_block(boundary, name)
                if name in ("xm", "xp"):
                    self.assertEqual(read_entry(patch, "type"), "fixedValue")
                    value = read_entry(patch, "value").split()
                    self.assertEqual(value[0], "uniform")
                    # A uniform field with these wall values has zero normal
                    # derivative at both half-cell walls, as at internal and
                    # cyclic faces; its physical diffusion flux is zero.
                    self.assertEqual(float(value[1]) - internal_value, 0)
                else:
                    self.assertEqual(read_entry(patch, "type"), "cyclic")

    def test_metadata_identifies_inputs_and_all_generated_files_deterministically(self):
        with tempfile.TemporaryDirectory() as directory:
            first, second = Path(directory) / "first", Path(directory) / "second"
            first_metadata = generate(first)
            self.assertEqual(first_metadata, generate(second))
            self.assertEqual(first_metadata["execution_status"], "NOT_RUN")
            inputs_bytes = json.dumps(first_metadata["inputs"], sort_keys=True,
                                      separators=(",", ":"), allow_nan=False).encode()
            self.assertEqual(first_metadata["inputs_sha256"],
                             hashlib.sha256(inputs_bytes).hexdigest())
            self.assertEqual(set(first_metadata["files_sha256"]),
                             {path.relative_to(first).as_posix() for path in first.rglob("*")
                              if path.is_file() and path.name != "case_metadata.json"})
            for name, digest in first_metadata["files_sha256"].items():
                self.assertEqual(digest, hashlib.sha256((first / name).read_bytes()).hexdigest())
                self.assertEqual((first / name).read_bytes(), (second / name).read_bytes())
            changed = generate(Path(directory) / "changed", traction=-1)
            self.assertNotEqual(first_metadata["inputs_sha256"], changed["inputs_sha256"])

    def test_malformed_parameters_fail_before_writing_a_case(self):
        invalid = [{"nx": value} for value in (True, 0, -2, 1, 3, 16.0, "16", None)]
        invalid.extend({name: value} for name in ("mu_left", "mu_right")
                       for value in (True, 0, -1, float("nan"), float("inf"), 1j, "1"))
        invalid.extend({"traction": value}
                       for value in (True, 0, -0.0, float("nan"), float("inf"), 1j, "1"))
        invalid.append({"mu_left": 1e-308, "traction": 1e308})
        with tempfile.TemporaryDirectory() as directory:
            for index, parameters in enumerate(invalid):
                with self.subTest(parameters=parameters):
                    case = Path(directory) / f"invalid{index}"
                    with self.assertRaises(ValueError):
                        generate(case, **parameters)
                    self.assertFalse(case.exists())

    def test_existing_destinations_and_dangling_symlinks_are_preserved(self):
        with tempfile.TemporaryDirectory() as directory:
            case = Path(directory) / "case"
            case.mkdir()
            sentinel = case / "keep"
            sentinel.write_bytes(b"existing evidence\n")
            with self.assertRaisesRegex(ValueError, "refusing to overwrite"):
                generate(case)
            self.assertEqual(sentinel.read_bytes(), b"existing evidence\n")
            self.assertEqual(list(case.iterdir()), [sentinel])
            existing_file = Path(directory) / "file"
            existing_file.write_bytes(b"keep file")
            with self.assertRaisesRegex(ValueError, "refusing to overwrite"):
                generate(existing_file)
            self.assertEqual(existing_file.read_bytes(), b"keep file")
            symlink = Path(directory) / "dangling"
            symlink.symlink_to(Path(directory) / "absent")
            with self.assertRaisesRegex(ValueError, "refusing to overwrite"):
                generate(symlink)
            self.assertTrue(symlink.is_symlink())

    def test_collection_validates_every_grid_and_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as directory:
            for index, resolutions in enumerate(((), (16, 16), (16, 3), (16, False))):
                case = Path(directory) / f"invalid{index}"
                with self.assertRaises(ValueError):
                    build_cases(case, nx_values=resolutions)
                self.assertFalse(case.exists())
            existing = Path(directory) / "existing"
            existing.mkdir()
            with self.assertRaisesRegex(ValueError, "refusing to overwrite"):
                build_cases(existing)
            self.assertEqual(list(existing.iterdir()), [])


if __name__ == "__main__":
    unittest.main()
