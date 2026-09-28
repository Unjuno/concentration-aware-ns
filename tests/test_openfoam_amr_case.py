import tempfile
import unittest
from pathlib import Path

from tools.openfoam_amr_case import generate_amr


class OpenFoamAmrCaseTests(unittest.TestCase):
    def test_high_gradient_sensor_is_created_updated_and_bounded(self):
        with tempfile.TemporaryDirectory() as temp:
            case = Path(temp) / "case"
            generate_amr(case, max_cells=5000, max_level=2, end=0.05,
                         profile="high-gradient", frequency=4, n=16, dt=0.001,
                         refine_interval=2)
            model = (case / "constant/fvModels").read_text()
            mesh = (case / "constant/dynamicMeshDict").read_text()
            parameters = (case / "parameters.json").read_text()

            self.assertIn('foundObject<volScalarField>("refineSensor")', model)
            self.assertIn('lookupObjectRef<volScalarField>("refineSensor")', model)
            self.assertIn("sensor[celli] = chi;", model)
            self.assertIn("sensor.correctBoundaryConditions();", model)
            self.assertIn("refineInterval 2;", mesh)
            self.assertIn("maxRefinement 2;", mesh)
            self.assertIn("maxCells 5000;", mesh)
            self.assertIn('"profile": "high-gradient"', parameters)

    def test_refine_interval_must_allow_sensor_initialization(self):
        with tempfile.TemporaryDirectory() as temp:
            case = Path(temp) / "case"
            with self.assertRaisesRegex(ValueError, "refine_interval"):
                generate_amr(case, refine_interval=1)
            self.assertFalse(case.exists())

    def test_gaussian_sensor_path_is_still_generated(self):
        with tempfile.TemporaryDirectory() as temp:
            case = Path(temp) / "case"
            generate_amr(case, profile="gaussian", n=8)
            model = (case / "constant/fvModels").read_text()
            self.assertIn("sensor[celli] = exp(exponent+now);", model)
            self.assertIn("sensor.correctBoundaryConditions();", model)


if __name__ == "__main__":
    unittest.main()
