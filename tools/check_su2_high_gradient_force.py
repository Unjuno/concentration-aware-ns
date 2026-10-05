"""Compile the pinned SU2 adapter helper and compare it with the independent NumPy MMS."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import numpy as np
from tools.high_gradient_reference import fields


PATCH = Path("runtime/su2/high_gradient.patch")


def check():
    added = "\n".join(line[1:] for line in PATCH.read_text().splitlines()
                        if line.startswith("+") and not line.startswith("+++"))
    helper = added[added.index("namespace {"):added.index("CUserDefinedSolution::CUserDefinedSolution")]
    with tempfile.TemporaryDirectory(prefix="su2-high-gradient-check-") as directory:
        root = Path(directory)
        source = "#include <cmath>\n#include <iostream>\n#include <iomanip>\nusing su2double=double;\n" + helper + r'''
int main(){ double x[3],t,u[3],f[3]; while(std::cin>>x[0]>>x[1]>>x[2]>>t){ localized(x,t,.01,u,f); std::cout<<std::setprecision(17); for(auto v:u)std::cout<<v<<" "; for(auto v:f)std::cout<<v<<" "; std::cout<<"\n"; }}
'''
        (root / "check.cpp").write_text(source)
        compiler = shutil.which(os.environ.get("CXX", "c++"))
        if compiler is None:
            raise RuntimeError("a C++17 compiler is required (set CXX)")
        subprocess.run([compiler, "-std=c++17", "-O2", str(root / "check.cpp"), "-o", str(root / "check")], check=True)
        rng = np.random.default_rng(20261004)
        points = rng.uniform(0, 2*np.pi, (257, 3))
        t = 0.037
        data = "\n".join(" ".join(map(repr, [*map(float, xyz), t])) for xyz in points) + "\n"
        run = subprocess.run([str(root / "check")], input=data, text=True, capture_output=True, check=True)
    actual = np.fromstring(run.stdout, sep=" ").reshape(len(points), 6)
    expected = fields(points, N=4, nu=.01, time=t)
    errors = {"u": float(np.max(np.abs(actual[:, :3]-expected["u"]))),
              "force": float(np.max(np.abs(actual[:, 3:]-expected["force"]))) }
    if max(errors.values()) > 2e-13:
        raise AssertionError(errors)
    return {"points": len(points), "seed": 20261004, "time": t,
            "max_abs_error": errors, "patch_sha256": hashlib.sha256(PATCH.read_bytes()).hexdigest(),
            "scope": "compiled helper parity only; does not validate SU2 integration or solver time semantics"}


if __name__ == "__main__":
    print(json.dumps(check(), indent=2))
