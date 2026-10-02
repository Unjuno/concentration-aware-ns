import json
import tempfile
import unittest
from pathlib import Path

import numpy as np

from tools.analyze_openfoam import analyze
from tools.analyze_amr import analyze as analyze_amr
from tools.high_gradient_reference import fields
from tools.openfoam_amr_case import generate_amr
from tools.openfoam_case import generate
from tools.archive_high_gradient_openfoam import _redact_host_mount


def write_vectors(path, values, object_name):
    values = np.asarray(values, dtype=float)
    rows = "\n".join("(" + " ".join(f"{v:.17g}" for v in row) + ")"
                      for row in values)
    path.write_text(
        "FoamFile { format ascii; class volVectorField; object "
        f"{object_name}; }}\ninternalField nonuniform List<vector>\n"
        f"{len(values)}\n(\n{rows}\n);\n"
    )


def write_components(path, values, object_name, foam_type):
    values = np.asarray(values, dtype=float).reshape(len(values), -1)
    primitive = {"volScalarField": "scalar", "volTensorField": "tensor"}[foam_type]
    rows = "\n".join("(" + " ".join(f"{v:.17g}" for v in row) + ")"
                      for row in values)
    path.write_text(
        f"FoamFile {{ format ascii; class {foam_type}; object {object_name}; }}\n"
        f"internalField nonuniform List<{primitive}>\n"
        f"{len(values)}\n(\n{rows}\n);\n"
    )


class OpenFoamHighGradientAnalysisTests(unittest.TestCase):
    def test_uses_high_gradient_reference_and_separates_fd2_operator_error(self):
        n, end, frequency = 8, 0.005, 4
        with tempfile.TemporaryDirectory() as directory:
            case = Path(directory) / "case"
            generate(case, n=n, dt=0.001, end=end, nu=0.01,
                     profile="high-gradient", frequency=frequency)
            params = json.loads((case / "parameters.json").read_text())
            axis = (np.arange(n) + 0.5) * (2 * np.pi / n)
            z, y, x = np.meshgrid(axis, axis, axis, indexing="ij")
            points = np.stack((x, y, z), axis=-1).reshape(-1, 3)
            reference = fields(points, N=frequency, nu=params["nu"], time=end)
            sensor_from_exact_gradient = reference["grad_u"][:, 1, 0] ** 2
            chi = ((1 + np.cos(points[:, 1])) / 2) ** 4 * ((1 + np.cos(points[:, 2])) / 2) ** 4
            sensor_formula = np.exp(-2 * end) * chi**2 * np.sin(frequency * points[:, 0]) ** 2
            np.testing.assert_allclose(sensor_from_exact_gradient, sensor_formula, atol=1e-14)
            time_dir = case / str(end)
            time_dir.mkdir()
            write_vectors(time_dir / "C", points, "C")
            write_vectors(time_dir / "U", reference["u"], "U")
            (case / "log.foamRun").write_text("End\n")

            result = analyze(case)

        self.assertEqual(result["reference_profile"], "high-gradient")
        self.assertEqual(result["parameters"]["frequency"], frequency)
        self.assertEqual(result["velocity_relative_l2"], 0.0)
        self.assertEqual(result["energy_relative_error_cell_samples"], 0.0)
        self.assertEqual(result["shell_spectrum_relative_l1_cell_samples"], 0.0)
        self.assertEqual(result["gradient_peak_fd2_operator_relative_error"], 0.0)
        self.assertEqual(result["vorticity_peak_fd2_operator_relative_error"], 0.0)
        self.assertAlmostEqual(
            result["reference_continuous_gradient_lower_bound"], np.exp(-end)
        )
        self.assertEqual(result["quality"], "UNCERTAIN")
        self.assertEqual(result["standard_acceptance"], "UNCERTAIN")

    def test_high_gradient_amr_generation_and_analysis_use_matching_profile(self):
        n, end, frequency = 4, 0.005, 4
        with tempfile.TemporaryDirectory() as directory:
            case = Path(directory) / "case"
            generate_amr(case, max_cells=5000, max_level=2, end=end,
                         profile="high-gradient", frequency=frequency, n=n)
            params = json.loads((case / "parameters.json").read_text())
            source = (case / "constant/fvModels").read_text()
            mesh_dict = (case / "constant/dynamicMeshDict").read_text()
            self.assertEqual(params["profile"], "high-gradient")
            self.assertIn("sensor[celli] = sqr(decay*chi*sx)", source)
            self.assertIn("lowerRefineLevel 0.25", mesh_dict)
            self.assertIn("equals (partial_x u_y)^2", params["amr"]["sensor"])

            axis = (np.arange(n) + 0.5) * (2 * np.pi / n)
            z, y, x = np.meshgrid(axis, axis, axis, indexing="ij")
            points = np.stack((x, y, z), axis=-1).reshape(-1, 3)
            reference = fields(points, N=frequency, nu=params["nu"], time=end)
            time_dir = case / str(end)
            time_dir.mkdir()
            write_vectors(time_dir / "C", points, "C")
            write_vectors(time_dir / "U", reference["u"], "U")
            write_components(time_dir / "Vc", np.full((n**3,), (2*np.pi/n)**3),
                             "Vc", "volScalarField")
            write_components(time_dir / "grad(U)", reference["grad_u"],
                             "grad(U)", "volTensorField")
            write_components(time_dir / "cellLevel", np.zeros(n**3),
                             "cellLevel", "volScalarField")
            (case / "log.foamRun").write_text("End\n")

            result = analyze_amr(case)

        self.assertEqual(result["reference_profile"], "high-gradient")
        self.assertAlmostEqual(result["velocity_relative_volume_l2"], 0.0, places=14)
        self.assertEqual(result["quality"], "UNCERTAIN")

    def test_gaussian_amr_generator_keeps_its_analytic_sensor(self):
        with tempfile.TemporaryDirectory() as directory:
            case = Path(directory) / "case"
            generate_amr(case, max_cells=5000, end=0.005)
            source = (case / "constant/fvModels").read_text()
            params = json.loads((case / "parameters.json").read_text())

        self.assertIn("sensor[celli] = exp(exponent+now)", source)
        self.assertIn("exp(sum(cos(x-pi)-1)/sigma^2)", params["amr"]["sensor"])

    def test_public_command_redacts_user_specific_host_mount(self):
        with tempfile.TemporaryDirectory() as directory:
            command_path = Path(directory) / "command.json"
            command_path.write_text(json.dumps([
                "docker", "run", "-v",
                "/Users/private-name/project/work/case:/case", "image-id",
            ]))
            command = _redact_host_mount(command_path)

        self.assertEqual(command[-2], "<HOST_CASE_DIR>:/case")
        self.assertNotIn("private-name", " ".join(command))


if __name__ == "__main__":
    unittest.main()
