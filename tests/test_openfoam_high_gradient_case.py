import json
import tempfile
import unittest
from pathlib import Path

import numpy as np

from tools.high_gradient_reference import fields
from tools.analyze_openfoam import analyze
from tools.openfoam_case import generate
from tools.openfoam_amr_case import generate_amr


class OpenFoamHighGradientCaseTests(unittest.TestCase):
    @staticmethod
    def write_vectors(path, values):
        body = "FoamFile { format ascii; class volVectorField; object field; }\n"
        body += f"internalField nonuniform List<vector>\n{len(values)}\n(\n"
        body += "\n".join("(" + " ".join(f"{x:.17g}" for x in row) + ")"
                             for row in values)
        path.write_text(body + "\n);\n")

    def test_case_generation_uses_exact_profile_and_transient_forcing(self):
        with tempfile.TemporaryDirectory() as directory:
            case = Path(directory) / "case"
            generate(case, n=4, dt=0.001, end=0.005, nu=0.01,
                     profile="high-gradient", frequency=4)
            params = json.loads((case / "parameters.json").read_text())
            self.assertEqual(params["profile"], "high-gradient")
            self.assertEqual(params["frequency"], 4)
            code = (case / "constant/fvModels").read_text()
            self.assertIn("sqr(decay)*conv", code)
            self.assertIn("viscosity*decay*lapU", code)
            self.assertIn("source[celli] -= volumes[celli]*forcing", code)

            text = (case / "0/U").read_text()
            count_pos = text.index("internalField nonuniform List<vector>")
            payload = text[count_pos:].split("(", 1)[1].split(");", 1)[0]
            actual = np.array([[float(v) for v in line.strip(" ()").split()]
                               for line in payload.splitlines() if line.strip()])
            coordinates = (np.arange(4)+0.5)*2*np.pi/4
            z, y, x = np.meshgrid(coordinates, coordinates, coordinates, indexing="ij")
            points = np.stack((x,y,z), axis=-1).reshape(-1,3)
            expected = fields(points, N=4, nu=0.01, time=0)["u"]
            np.testing.assert_allclose(actual, expected, rtol=0, atol=1e-15)

    def test_amr_generator_uses_analytic_envelope_sensor(self):
        with tempfile.TemporaryDirectory() as directory:
            case=Path(directory)/"amr"
            generate_amr(case,max_cells=5000,max_level=2,end=0.005,
                         profile="high-gradient",frequency=4,n=4,dt=0.001)
            model=(case/"constant/fvModels").read_text()
            self.assertIn('volScalarField& sensor =',model)
            self.assertIn('sensor[celli] = chi;',model)
            self.assertIn('sensor.correctBoundaryConditions();',model)
            mesh=(case/"constant/dynamicMeshDict").read_text()
            self.assertIn('field refineSensor;',mesh)
            self.assertIn('maxCells 5000;',mesh)
            params=json.loads((case/"parameters.json").read_text())
            self.assertEqual(params['profile'],'high-gradient')
            self.assertIn('localized envelope chi',params['amr']['sensor'])

    def test_analyzer_separates_fd2_peak_from_continuous_reference(self):
        n, frequency, end = 8, 2, 0.05
        with tempfile.TemporaryDirectory() as directory:
            case = Path(directory)
            time_dir = case / str(end)
            time_dir.mkdir()
            axis = (np.arange(n) + 0.5) * 2 * np.pi / n
            z, y, x = np.meshgrid(axis, axis, axis, indexing="ij")
            centers = np.stack((x, y, z), axis=-1).reshape(-1, 3)
            velocity = fields(centers, N=frequency, time=end)["u"]
            self.write_vectors(time_dir / "C", centers)
            self.write_vectors(time_dir / "U", velocity)
            (case / "parameters.json").write_text(json.dumps({
                "n": n, "end": end, "nu": 0.01, "profile": "high-gradient",
                "frequency": frequency,
            }))
            (case / "log.foamRun").write_text("End\n")

            result = analyze(case)
            sinc = np.sin(frequency * 2 * np.pi / n) / (frequency * 2 * np.pi / n)
            self.assertAlmostEqual(
                result["selected_gradient_component_fd2_peak"] /
                result["selected_gradient_component_reference_sample_peak"],
                sinc, places=13,
            )
            self.assertAlmostEqual(
                result["selected_gradient_component_reference_continuous_peak"],
                np.exp(-end), places=15,
            )
            self.assertFalse(result["continuous_full_gradient_peak_certified"])
            self.assertEqual(result["quality"], "UNCERTAIN")


if __name__ == "__main__":
    unittest.main()
