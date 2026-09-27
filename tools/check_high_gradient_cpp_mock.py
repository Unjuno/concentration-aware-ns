"""Host-compile generated C++ forcing with minimal Foam-like mock types.

This is an offline syntax/algebra check, not an OpenFOAM header or solver test.
"""
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

import numpy as np

from tools.high_gradient_reference import fields
from tools.openfoam_case import generate


def main():
    compiler = shutil.which("c++") or shutil.which("clang++") or shutil.which("g++")
    if not compiler:
        raise RuntimeError("no host C++ compiler found")
    n, frequency, now = 4, 4, 0.037
    rng = np.random.default_rng(8831)
    points = rng.uniform(0, 2*np.pi, (48, 3))
    volumes = rng.uniform(0.1, 2.0, len(points))
    with tempfile.TemporaryDirectory(prefix="cans-high-gradient-cpp-") as temp:
        root = Path(temp)
        case = root/"case"
        generate(case, n=n, dt=0.001, end=0.05, nu=0.01,
                 profile="high-gradient", frequency=frequency)
        source = (case/"constant/fvModels").read_text()
        body = source.split("#{",1)[1].split("#};",1)[0]
        point_rows = ",\n".join("vector("+",".join(format(float(v), ".17g") for v in row)+")" for row in points)
        volume_rows = ",".join(format(float(v), ".17g") for v in volumes)
        cpp = r'''#include <cmath>
#include <iostream>
#include <vector>
#include <iomanip>
namespace Foam {
using scalar=double; using label=int;
class vector { scalar a[3]; public:
 vector(scalar x=0,scalar y=0,scalar z=0):a{x,y,z}{}
 scalar& operator[](label i){return a[i];} scalar operator[](label i) const{return a[i];}
 scalar x()const{return a[0];} scalar y()const{return a[1];} scalar z()const{return a[2];}
 vector& operator-=(const vector& b){for(int i=0;i<3;++i)a[i]-=b[i];return *this;}
};
inline vector operator*(scalar s,const vector& v){return vector(s*v[0],s*v[1],s*v[2]);}
inline vector operator*(const vector& v,scalar s){return s*v;}
using vectorField=std::vector<vector>; using scalarField=std::vector<scalar>;
inline scalar sqr(scalar x){return x*x;}
template<class T> inline T pow(T x,int p){return std::pow(x,p);}
namespace constant { namespace mathematical { constexpr scalar pi=3.14159265358979323846; } }
#define forAll(v,i) for(label i=0;i<static_cast<label>((v).size());++i)
struct Clock { scalar value()const{return TIME;} };
struct Mesh { vectorField p; scalarField v; Clock c;
 const vectorField& C()const{return p;} const scalarField& V()const{return v;}
 const Clock& time()const{return c;} };
struct Equation { vectorField v; explicit Equation(label n):v(n){}
 vectorField& source(){return v;} };
}
int main(){using namespace Foam;
 Mesh m{{POINT_ROWS},{VOLUME_ROWS},Clock{}}; Equation eqn(m.p.size());
 auto mesh=[&]() -> const Mesh& {return m;};
BODY
 std::cout<<std::setprecision(17);
 forAll(m.p,i){const vector f=(-1.0/m.v[i])*eqn.v[i];std::cout<<f.x()<<" "<<f.y()<<" "<<f.z()<<"\n";}
}
'''.replace("TIME",format(now,".17g")).replace("POINT_ROWS",point_rows).replace("VOLUME_ROWS",volume_rows).replace("BODY",body)
        source_path, binary = root/"check.cpp", root/"check"
        source_path.write_text(cpp)
        compile_run = subprocess.run([compiler,"-std=c++14","-O2",str(source_path),"-o",str(binary)],
                                     capture_output=True,text=True,timeout=30)
        if compile_run.returncode:
            raise RuntimeError("mock C++ compile failed: "+compile_run.stderr[-2000:])
        run = subprocess.run([str(binary)],capture_output=True,text=True,timeout=10,check=True)
        actual=np.loadtxt(run.stdout.splitlines())
    expected=fields(points,N=frequency,nu=0.01,time=now)["force"]
    error=float(np.max(np.abs(actual-expected)))
    version=subprocess.run([compiler,"--version"],capture_output=True,text=True,check=True).stdout.splitlines()[0]
    result={"scope":"Generated codeAddSup C++ body with minimal mock types; no OpenFOAM headers or solver.",
            "compiler":version,"seed":8831,"points":len(points),"time":now,"N":frequency,
            "fvModels_sha256":__import__("hashlib").sha256(source.encode()).hexdigest(),
            "max_absolute_force_error":error,"tolerance":1e-10,"passed":error<1e-10,
            "limitations":"Does not establish compatibility with Foundation headers or live solver source sign convention."}
    out=Path("evidence/tests/high-gradient-cpp-mock.json");out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,indent=2)+"\n");print(json.dumps(result,indent=2))
    if not result["passed"]: raise SystemExit(1)


if __name__=="__main__": main()
