"""Compile localized-MMS codedFvModel against OpenFOAM vector types.

The mock evaluates the generated codeAddSup body with non-unit cell volumes and
compares its extracted force to the independent NumPy reference. It does not
run the PDE solver or certify the OpenFOAM equation sign convention.
"""
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path

import numpy as np

from tools.high_gradient_reference import fields
from tools.openfoam_case import generate


def main():
    n, frequency, time = 16, 4, 0.037
    rng = np.random.default_rng(8831)
    points = rng.uniform(0, 2*np.pi, size=(72, 3))
    volumes = rng.uniform(0.1, 2.0, size=len(points))
    with tempfile.TemporaryDirectory(prefix="cans-high-gradient-force-") as tmp:
        root = Path(tmp)
        case = root / "case"
        generate(case, n=n, dt=0.001, end=0.05, nu=0.01,
                 profile="high-gradient", frequency=frequency)
        fvmodels = (case / "constant/fvModels").read_text()
        body = fvmodels.split("#{", 1)[1].split("#};", 1)[0]
        (root/"inputs.txt").write_text(str(len(points))+"\n"+"\n".join(
            " ".join(map(str, [*p, v])) for p, v in zip(points, volumes))+"\n")
        cpp = '''#include "vectorField.H"
#include "scalarField.H"
#include "mathematicalConstants.H"
#include <iostream>
#include <iomanip>
using namespace Foam;
struct Clock { scalar value() const { return TIME_VALUE; } };
struct Mesh {
 vectorField points; scalarField volumes; Clock clock;
 Mesh(label n): points(n), volumes(n) {}
 const vectorField& C() const { return points; }
 const scalarField& V() const { return volumes; }
 const Clock& time() const { return clock; }
};
struct Equation { vectorField values; Equation(label n): values(n,vector::zero) {}
 vectorField& source() { return values; } };
namespace Foam {
int evaluate() {
 label n; std::cin >> n; Mesh m(n); Equation eqn(n);
 forAll(m.points,i) { scalar x,y,z,v; std::cin >> x >> y >> z >> v; m.points[i]=vector(x,y,z); m.volumes[i]=v; }
 auto mesh = [&]() -> const Mesh& { return m; };
BODY
 std::cout << std::setprecision(17);
 forAll(m.points,i) { vector f=-eqn.values[i]/m.volumes[i]; std::cout << f.x() << " " << f.y() << " " << f.z() << "\\n"; }
 return 0;
}
}
int main() { return Foam::evaluate(); }
'''.replace("TIME_VALUE", repr(time)).replace("BODY", body)
        (root/"check.C").write_text(cpp)
        command = ["docker", "run", "--rm", "-v", f"{root}:/case",
                   "concentration-aware-ns:of13", "bash", "-c",
                   'g++ -std=c++14 -DNoRepository -DWM_DP -DWM_LABEL_SIZE=32 '
                   '-I$WM_PROJECT_DIR/src/finiteVolume/lnInclude '
                   '-I$WM_PROJECT_DIR/src/meshTools/lnInclude '
                   '-I$WM_PROJECT_DIR/src/OpenFOAM/lnInclude '
                   '-I$WM_PROJECT_DIR/src/OSspecific/POSIX/lnInclude '
                   'check.C -L$FOAM_LIBBIN -lOpenFOAM -o check && ./check < inputs.txt > output.txt']
        try:
            run = subprocess.run(command, capture_output=True, text=True, timeout=120)
            (root/"compile.log").write_text(run.stdout+run.stderr)
            if run.returncode:
                raise RuntimeError(f"OpenFOAM mock compile failed: {run.stderr[-1000:]}")
        except subprocess.TimeoutExpired as exc:
            raise RuntimeError("Docker/OpenFOAM mock timed out; no compile result") from exc
        actual = np.loadtxt(root/"output.txt")
    expected = fields(points, N=frequency, nu=0.01, time=time)["force"]
    error = float(np.max(np.abs(actual-expected)))
    result = {
        "scope": "Generated codedFvModel source assembly against OpenFOAM vector types; not a solver run.",
        "seed": 8831, "points": len(points), "time": time,
        "N": frequency,
        "fvModels_sha256": hashlib.sha256(fvmodels.encode()).hexdigest(),
        "max_absolute_force_error": error,
        "tolerance": 1e-10,
        "passed": error < 1e-10,
        "limitation": "Mock mesh and equation only; does not verify live solver sign or temporal-discretization behavior.",
    }
    out = Path("evidence/tests/high-gradient-openfoam-force.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(result, indent=2))
    if not result["passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
