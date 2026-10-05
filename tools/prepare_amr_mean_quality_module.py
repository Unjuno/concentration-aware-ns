"""Add three cell-only derivative snapshots to the pinned diagnostic module."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def prepare(source, output, spec):
    source, output = Path(source).resolve(), Path(output).resolve()
    module = source/"applications/modules/incompressibleFluid"
    expected = spec["target"]["module_source_sha256"]
    actual = {p.relative_to(module).as_posix(): sha(p) for p in sorted(module.rglob("*")) if p.is_file()}
    if actual != expected:
        raise ValueError("complete pinned module file map differs from protocol")
    model = spec["model"]
    if model["frequency"] != 3 or model["pre_map_time"] != .002 or model["end"] != .05:
        raise ValueError("unexpected model for this frozen instrumentation")
    subprocess.run([sys.executable, str(ROOT/"runtime/openfoam13/instrumentation/prepare_amr_stage_module.py"),
                    str(source), str(output), "--include-pre-map", "--pre-map-time", ".002",
                    "--solver-stage-time", ".05"], check=True, capture_output=True, text=True)
    path = output/"incompressibleFluid.C"
    text = path.read_text()
    anchor = "void Foam::solvers::incompressibleFluid::writeAmrSnapshot\n("
    if text.count(anchor) != 1:
        raise ValueError("snapshot function anchor differs")
    start = text.index(anchor)
    stop = text.index("\n}\n\n\n", start)+2
    method = r'''void Foam::solvers::incompressibleFluid::writeAmrSnapshot
(
    const word& stage
) const
{
    if (getEnv("CANS_AMR_CAPTURE_DISABLED") == "1") return;
    if (stage != "preMap" && stage != "mapped" && stage != "postSolve") return;
    const scalar expectedTime = stage == "postSolve" ? 0.05 : 0.002;
    if (mag(runTime.value() - expectedTime) > 1e-12) return;

    const vectorField& C = mesh.C();
    const tmp<volTensorField> tGradient = fvc::grad(U_);
    const volTensorField& gradient = tGradient();
    volVectorField referenceU
    (
        IOobject("amrQualityReferenceU", runTime.name(), mesh,
                 IOobject::NO_READ, IOobject::NO_WRITE, false), U_
    );
    const scalar decay = exp(-expectedTime);
    forAll(referenceU, celli)
    {
        const scalar x = C[celli].x(), y = C[celli].y(), z = C[celli].z();
        const scalar ay = (1 + cos(y))/2, az = (1 + cos(z))/2;
        const scalar gy = sqr(sqr(ay)), gz = sqr(sqr(az));
        const scalar dy = -2*sin(y)*sqr(ay)*ay;
        referenceU.primitiveFieldRef()[celli] = decay*vector
        (
            sin(3*x)*dy*gz/9, -cos(3*x)*gy*gz/3, 0
        );
    }
    referenceU.correctBoundaryConditions();
    const tmp<volTensorField> tReferenceGradient = fvc::grad(referenceU);
    const volTensorField& referenceGradient = tReferenceGradient();
    const fileName dir(runTime.path()/"postProcessing/amrStages"/runTime.name());
    mkDir(dir);
    OFstream cells(dir/(stage + "_cells.csv"));
    cells.precision(17);
    cells << "cell,cx,cy,cz,V,Ux,Uy,Uz,p,g00,g01,g02,g10,g11,g12,g20,g21,g22,"
             "r00,r01,r02,r10,r11,r12,r20,r21,r22\n";
    forAll(U_, celli)
    {
        const tensor& g = gradient[celli];
        const tensor& r = referenceGradient[celli];
        cells << celli << ',' << C[celli].x() << ',' << C[celli].y() << ','
              << C[celli].z() << ',' << mesh.V()[celli] << ','
              << U_[celli].x() << ',' << U_[celli].y() << ',' << U_[celli].z()
              << ',' << p_[celli] << ','
              << g.xx() << ',' << g.yx() << ',' << g.zx() << ','
              << g.xy() << ',' << g.yy() << ',' << g.zy() << ','
              << g.xz() << ',' << g.yz() << ',' << g.zz() << ','
              << r.xx() << ',' << r.yx() << ',' << r.zx() << ','
              << r.xy() << ',' << r.yy() << ',' << r.zy() << ','
              << r.xz() << ',' << r.yz() << ',' << r.zz() << '\n';
    }
    Info<< "AMR_MEAN_QUALITY_SNAPSHOT stage=" << stage << " time="
        << runTime.name() << " cells=" << mesh.nCells() << endl;
}'''
    text = text[:start]+method+text[stop:]
    text = text.replace('#include "OFstream.H"', '#include "OFstream.H"\n#include "fvcGrad.H"', 1)
    path.write_text(text)
    provenance = {
        "foundation_source_commit": spec["target"]["foundation_source_commit"],
        "original_module_file_sha256": actual,
        "instrumented_module_file_sha256": {p.relative_to(output).as_posix(): sha(p)
            for p in sorted(output.rglob("*")) if p.is_file() and p.name != "instrumentation-provenance.json"},
        "stages": ["preMap", "mapped", "postSolve"],
        "state_times": [.002, .002, .05],
        "tensor_convention": "Export transposed native tensors: gij=du_i/dx_j",
        "equation_assembly_modified": False,
        "measurement_noninterference": "UNVERIFIED until disabled-capture final U/p control matches",
        "reference_evaluation": "Real-space g=((1+cos(q))/2)^4 and g'=-2*sin(q)*((1+cos(q))/2)^3; independent of forcing Fourier implementation.",
    }
    (output/"instrumentation-provenance.json").write_text(json.dumps(provenance, indent=2)+"\n")
    return provenance


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path); parser.add_argument("output", type=Path)
    parser.add_argument("--protocol", type=Path, default=ROOT/"protocols/of13-amr-mean-quality-v1.json")
    args = parser.parse_args()
    print(json.dumps(prepare(args.source, args.output, json.loads(args.protocol.read_text())), indent=2))


if __name__ == "__main__":
    main()
