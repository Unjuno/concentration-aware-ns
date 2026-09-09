"""Compile the actual generated codeAddSup body against OpenFOAM vector types.

A mock mesh/equation supplies sample coordinates, non-unit volumes and time.
This tests formula and source assembly, not the solver's equation conventions.
"""
import hashlib
import json
from pathlib import Path
import subprocess
import numpy as np
from tools.reference import fields


def main():
    path=Path('work/of13-study-v1/n16-dt0.001/constant/fvModels')
    body=path.read_text().split('#{',1)[1].split('#};',1)[0]
    root=Path('work/force-check').resolve(); root.mkdir(exist_ok=True)
    rng=np.random.default_rng(719)
    points=np.pi+rng.uniform(-1,1,(48,3)); volumes=rng.uniform(0.1,2,48)
    (root/'inputs.txt').write_text('48\n'+'\n'.join(' '.join(map(str,[*p,v])) for p,v in zip(points,volumes)))
    cpp='''#include "vectorField.H"
#include "scalarField.H"
#include "mathematicalConstants.H"
#include <iostream>
#include <iomanip>
using namespace Foam;
struct Clock { scalar value() const { return 0.05; } };
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
 label n; std::cin >> n;
 Mesh m(n); Equation eqn(n);
 forAll(m.points,i) { scalar x,y,z,v; std::cin >> x >> y >> z >> v; m.points[i]=vector(x,y,z); m.volumes[i]=v; }
 auto mesh = [&]() -> const Mesh& { return m; };
'''+body+'''
 std::cout << std::setprecision(17);
 forAll(m.points,i) { vector f=-eqn.values[i]/m.volumes[i]; std::cout << f.x() << " " << f.y() << " " << f.z() << "\\n"; }
 return 0;
}
}
int main() { return Foam::evaluate(); }
'''
    (root/'check.C').write_text(cpp)
    command=['docker','run','--rm','-v',f'{root}:/case','concentration-aware-ns:of13','bash','-c',
             'g++ -std=c++14 -DNoRepository -DWM_DP -DWM_LABEL_SIZE=32 -I$WM_PROJECT_DIR/src/finiteVolume/lnInclude -I$WM_PROJECT_DIR/src/meshTools/lnInclude -I$WM_PROJECT_DIR/src/OpenFOAM/lnInclude -I$WM_PROJECT_DIR/src/OSspecific/POSIX/lnInclude check.C -L$FOAM_LIBBIN -lOpenFOAM -o check && ./check < inputs.txt > output.txt']
    with (root/'compile.log').open('w') as out:
        subprocess.run(command,stdout=out,stderr=subprocess.STDOUT,check=True)
    got=np.loadtxt(root/'output.txt'); expected=fields(points,0.05)['force']
    error=float(np.max(np.abs(got-expected)))
    result={'seed':719,'points':48,'time':0.05,'source_file_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
            'max_absolute_error':error,'tolerance':1e-10,'passed':error<1e-10,
            'limitations':'Mock mesh/equation; does not independently verify solver force sign convention.'}
    print(json.dumps(result,indent=2))
    if not result['passed']: raise SystemExit(1)


if __name__=='__main__': main()
