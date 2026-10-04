import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

import numpy as np

from tools.high_gradient_reference import fields
from tools.forced_periodic_reference import fields as forced_periodic_fields
from tools.analyze_openfoam import analyze
from tools.openfoam_case import generate
from tools.openfoam_amr_case import generate_amr
from tools.check_high_gradient_fd2_floor import audit


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

    def test_case_generation_supports_pressure_bearing_periodic_control(self):
        n = 4
        with tempfile.TemporaryDirectory() as directory:
            case = Path(directory) / "case"
            generate(case, n=n, dt=0.001, end=0.005, nu=0.01,
                     profile="forced-periodic")
            params = json.loads((case / "parameters.json").read_text())
            self.assertEqual(params["profile"], "forced-periodic")
            self.assertEqual(params["reference"], "arXiv:2609.38210v1")
            code = (case / "constant/fvModels").read_text()
            self.assertIn("const vector gradp", code)
            self.assertIn("exp(-4*viscosity*now)", code)
            self.assertIn("source[celli] -= volumes[celli]*forcing", code)

            coordinates = (np.arange(n) + 0.5) * 2 * np.pi / n
            z, y, x = np.meshgrid(coordinates, coordinates, coordinates, indexing="ij")
            points = np.stack((x, y, z), axis=-1).reshape(-1, 3)
            expected = forced_periodic_fields(points, time=0, nu=0.01)
            velocity_text = (case / "0/U").read_text()
            velocity_start = velocity_text.index("internalField nonuniform List<vector>")
            velocity_payload = velocity_text[velocity_start:].split("(", 1)[1].split(");", 1)[0]
            velocity = np.array([[float(v) for v in line.strip(" ()").split()]
                                 for line in velocity_payload.splitlines() if line.strip()])
            np.testing.assert_allclose(velocity, expected["u"], rtol=0, atol=1e-15)

            pressure_text = (case / "0/p").read_text()
            pressure_start = pressure_text.index("internalField nonuniform List<scalar>")
            pressure_payload = pressure_text[pressure_start:].split("(", 1)[1].split(");", 1)[0]
            pressure = np.array([float(v) for v in pressure_payload.split()])
            np.testing.assert_allclose(pressure, expected["pressure"], rtol=0, atol=1e-15)

    @unittest.skipUnless(shutil.which("g++") or shutil.which("clang++"),
                         "a C++ compiler is required for generated C++ control")
    def test_forced_periodic_generated_cpp_matches_independent_reference(self):
        points = np.array([[0.2, 1.1, 2.2], [2.4, 3.1, 5.2],
                           [5.8, 0.7, 4.1], [1.7, 5.2, 0.4]])
        volumes = np.array([0.25, 0.7, 1.3, 2.0])
        now, nu = 0.31, 0.07
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            case = root / "case"
            generate(case, n=4, dt=0.001, end=0.005, nu=nu,
                     profile="forced-periodic")
            body = (case / "constant/fvModels").read_text().split("#{", 1)[1].split("#};", 1)[0]
            rows = ",\n".join(f"vector({x:.17g},{y:.17g},{z:.17g})" for x, y, z in points)
            weights = ",".join(f"{v:.17g}" for v in volumes)
            cpp = f'''#include <cmath>
#include <iostream>
#include <iomanip>
#include <vector>
using scalar=double;
struct vector {{ scalar v[3]; vector(scalar x=0,scalar y=0,scalar z=0):v{{x,y,z}}{{}}
 scalar x()const{{return v[0];}} scalar y()const{{return v[1];}} scalar z()const{{return v[2];}}
 vector& operator-=(const vector& b){{for(int i=0;i<3;++i)v[i]-=b.v[i];return *this;}}
}};
vector operator+(vector a,const vector& b){{for(int i=0;i<3;++i)a.v[i]+=b.v[i];return a;}}
vector operator*(scalar a,vector b){{for(double& x:b.v)x*=a;return b;}}
using vectorField=std::vector<vector>; using scalarField=std::vector<scalar>;
#define forAll(field,index) for(std::size_t index=0;index<(field).size();++index)
struct Clock {{ scalar value()const{{return {now:.17g};}} }};
struct Mesh {{ vectorField c{{{rows}}}; scalarField v{{{weights}}}; Clock t;
 const vectorField& C()const{{return c;}} const scalarField& V()const{{return v;}}
 const Clock& time()const{{return t;}} }};
struct Equation {{ vectorField s=vectorField(4); vectorField& source(){{return s;}} }};
int main(){{
 const Mesh m; Equation eqn;
 auto mesh=[&]() -> const Mesh& {{return m;}};
{body}
 std::cout<<std::setprecision(17);
 forAll(m.c,i) std::cout<<-eqn.s[i].x()/m.v[i]<<" "<<-eqn.s[i].y()/m.v[i]<<" "<<-eqn.s[i].z()/m.v[i]<<"\\n";
}}'''.replace("NU", repr(nu))
            source, executable = root / "check.cpp", root / "check"
            source.write_text(cpp)
            compiler = shutil.which("g++") or shutil.which("clang++")
            try:
                subprocess.run([compiler, "-std=c++17", str(source), "-o", str(executable)],
                               check=True, capture_output=True, text=True)
            except subprocess.CalledProcessError as error:
                if "Xcode license agreements" in error.stderr:
                    self.skipTest("Apple compiler unavailable until its Xcode license is accepted")
                raise
            completed = subprocess.run([str(executable)], check=True, capture_output=True, text=True)
            actual = np.loadtxt(completed.stdout.splitlines())
        expected = forced_periodic_fields(points, time=now, nu=nu)["force"]
        np.testing.assert_allclose(actual, expected, rtol=0, atol=2e-15)

    def test_amr_generator_uses_analytic_envelope_sensor(self):
        with tempfile.TemporaryDirectory() as directory:
            case=Path(directory)/"amr"
            generate_amr(case,max_cells=5000,max_level=2,end=0.005,
                         profile="high-gradient",frequency=4,n=4,dt=0.001,
                         refine_interval=4)
            model=(case/"constant/fvModels").read_text()
            self.assertIn('volScalarField& sensor =',model)
            self.assertIn('sensor[celli] = chi;',model)
            self.assertIn('sensor.correctBoundaryConditions();',model)
            mesh=(case/"constant/dynamicMeshDict").read_text()
            self.assertIn('field refineSensor;',mesh)
            self.assertIn('maxCells 5000;',mesh)
            self.assertIn('refineInterval 4;',mesh)
            params=json.loads((case/"parameters.json").read_text())
            self.assertEqual(params['profile'],'high-gradient')
            self.assertEqual(params['amr']['refineInterval'],4)
            self.assertIn('localized envelope chi',params['amr']['sensor'])

    def test_amr_interval_must_allow_sensor_initialization_before_refinement(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(ValueError, "integer >= 2"):
                generate_amr(Path(directory) / "amr", refine_interval=1)

    def test_analyzer_separates_fd2_peak_from_continuous_reference(self):
        n, frequency, end = 8, 4, 0.05
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
                "n": n, "dt": 0.001, "end": end, "nu": 0.01, "profile": "high-gradient",
                "frequency": frequency,
            }))
            log = "".join(f"Time = {i * 0.001:.3f}s\nPIMPLE: Converged in 4 iterations\n"
                          for i in range(1, 51)) + "End\n"
            (case / "log.foamRun").write_text(log)

            protocol = json.loads(Path("protocols/high-gradient-of13-v2.json").read_text())
            (case / "system").mkdir()
            (case / "system/fvSolution").write_text(
                "PIMPLE { nOuterCorrectors 12; outerCorrectorResidualControl "
                "{ p { tolerance 1e-8; relTol 0; } U { tolerance 1e-8; relTol 0; } } }"
            )
            result = analyze(case, protocol)
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
            self.assertTrue(result["reference_continuum_peak_certified"])
            self.assertAlmostEqual(
                result["reference_gradient_peak_continuum_certified"],
                np.sqrt(65) / 8 * np.exp(-end), places=14,
            )
            self.assertAlmostEqual(
                result["reference_vorticity_peak_continuum_certified"],
                9 / 8 * np.exp(-end), places=14,
            )
            self.assertLessEqual(
                result["reference_gradient_peak_sampling_fraction_of_continuum"], 1.0,
            )
            self.assertLessEqual(
                result["reference_vorticity_peak_sampling_fraction_of_continuum"], 1.0,
            )
            self.assertLess(
                result["reference_gradient_peak_sampling_fraction_of_continuum"], 1.0,
            )
            params = json.loads((case / "parameters.json").read_text())
            params["frequency"] = 2
            (case / "parameters.json").write_text(json.dumps(params))
            other_frequency = analyze(case)
            self.assertFalse(other_frequency["reference_continuum_peak_certified"])
            self.assertIsNone(other_frequency["reference_gradient_peak_continuum_certified"])
            self.assertIsNone(other_frequency["reference_vorticity_peak_continuum_certified"])
            self.assertIsNone(other_frequency["reference_gradient_peak_sampling_fraction_of_continuum"])
            self.assertIsNone(other_frequency["reference_vorticity_peak_sampling_fraction_of_continuum"])
            self.assertEqual(result["standard_acceptance"]["status"], "PASS")
            self.assertEqual(result["quality"], "FAIL")
            self.assertIn("shell_spectrum", result["local_quality"]["metrics"])

    def test_analyzer_compares_forced_periodic_velocity_and_gauge_free_pressure(self):
        n, end, nu = 4, 0.005, 0.01
        with tempfile.TemporaryDirectory() as directory:
            case = Path(directory)
            time_dir = case / str(end)
            time_dir.mkdir()
            axis = (np.arange(n) + 0.5) * 2 * np.pi / n
            z, y, x = np.meshgrid(axis, axis, axis, indexing="ij")
            centers = np.stack((x, y, z), axis=-1).reshape(-1, 3)
            expected = forced_periodic_fields(centers, time=end, nu=nu)
            self.write_vectors(time_dir / "C", centers)
            self.write_vectors(time_dir / "U", expected["u"])
            scalar_text = "FoamFile { format ascii; class volScalarField; object p; }\n"
            scalar_text += f"internalField nonuniform List<scalar>\n{n**3}\n(\n"
            scalar_text += "\n".join(f"{v:.17g}" for v in expected["pressure"])
            (time_dir / "p").write_text(scalar_text + "\n);\n")
            (case / "parameters.json").write_text(json.dumps({
                "n": n, "dt": 0.001, "end": end, "nu": nu,
                "sigma": 0.5, "profile": "forced-periodic",
                "reference": "arXiv:2609.38210v1",
            }))
            (case / "log.foamRun").write_text("Time = 0.005s\nPIMPLE: Converged in 3 iterations\nEnd\n")
            result = analyze(case)
            self.assertLess(result["velocity_relative_l2"], 1e-15)
            self.assertLess(result["pressure_relative_l2_gauge_invariant"], 1e-15)
            self.assertEqual(result["quality"], "UNCERTAIN")
            self.assertEqual(result["standard_acceptance"], "UNCERTAIN")

    def test_frozen_matrix_has_two_fine_grids_below_reference_fd2_floor(self):
        result = audit()
        rows = {row["n"]: row for row in result["rows"]}
        self.assertGreater(rows[16]["exact_solution_fd2_gradient_peak_relative_error"], 0.05)
        self.assertGreater(rows[32]["exact_solution_fd2_gradient_peak_relative_error"], 0.05)
        self.assertLess(rows[64]["exact_solution_fd2_gradient_peak_relative_error"], 0.05)
        self.assertLess(rows[128]["exact_solution_fd2_gradient_peak_relative_error"], 0.05)
        self.assertTrue(result["at_least_two_finer_grids_meet_both_derivative_thresholds"])


if __name__ == "__main__":
    unittest.main()
