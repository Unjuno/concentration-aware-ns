"""Generate AMR cases with analytic Gaussian or localized-envelope sensors."""
import argparse
import json
from pathlib import Path
from tools.openfoam_case import generate


def generate_amr(path, max_cells=5000, max_level=1, end=0.01,
                 profile='gaussian', frequency=4, n=16, dt=0.001):
    generate(path,n=n,dt=dt,end=end,profile=profile,frequency=frequency)
    path=Path(path)
    model=path/'constant/fvModels'
    body=model.read_text()
    if profile == 'gaussian':
        body=body.replace('const scalar now = mesh().time().value();','''const scalar now = mesh().time().value();
 if (!mesh().foundObject<volScalarField>("refineSensor")) {
   auto* sensor = new volScalarField(
     IOobject("refineSensor", mesh().time().name(), mesh(), IOobject::NO_READ, IOobject::AUTO_WRITE),
     mesh(), dimensionedScalar("zero", dimless, 0), "cyclic");
   sensor->store();
 }
 volScalarField& sensor = mesh().lookupObjectRef<volScalarField>("refineSensor");''')
        body=body.replace('const scalar psi = exp(exponent);','const scalar psi = exp(exponent);\n   sensor[celli] = exp(exponent+now);')
        body=body.replace('\n #};','\n sensor.correctBoundaryConditions();\n #};')
    else:
        body=body.replace(' const vectorField& centers = mesh().C();',''' const vectorField& centers = mesh().C();
 if (!mesh().foundObject<volScalarField>("refineSensor")) {
   auto* sensorField = new volScalarField(
     IOobject("refineSensor", mesh().time().name(), mesh(), IOobject::NO_READ, IOobject::AUTO_WRITE),
     mesh(), dimensionedScalar("zero", dimless, 0), "cyclic");
   sensorField->store();
 }
 volScalarField& sensor = mesh().lookupObjectRef<volScalarField>("refineSensor");''')
        body=body.replace('const scalar chi = gy[0]*hz[0];','const scalar chi = gy[0]*hz[0];\n   sensor[celli] = chi;')
        body=body.replace('\n #};','\n sensor.correctBoundaryConditions();\n #};')
    model.write_text(body)
    solution=path/'system/fvSolution'
    solution.write_text(solution.read_text().replace('pFinal { $p; }','pFinal { $p; }\npcorr { $p; }\npcorrFinal { $p; }'))
    (path/'constant/dynamicMeshDict').write_text(f'''FoamFile {{ format ascii; class dictionary; object dynamicMeshDict; }}
topoChanger {{
 type refiner; libs ("libfvMeshTopoChangers.so");
 refineInterval 2; field refineSensor;
 lowerRefineLevel 0.01; upperRefineLevel 1.1;
 nBufferLayers 1; maxRefinement {max_level}; maxCells {max_cells};
 dumpLevel true;
}}
''')
    p=json.loads((path/'parameters.json').read_text())
    p.update(purpose='AMR integration pilot, not production',amr={'maxCells':max_cells,'maxRefinement':max_level,'refineInterval':2,
        'sensor':'analytic Gaussian concentration' if profile=='gaussian' else 'analytic localized envelope chi(y,z), recomputed by source hook before adaptation'},
        profile=profile,frequency=frequency)
    (path/'parameters.json').write_text(json.dumps(p,indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('path');parser.add_argument('--max-cells',type=int,default=5000)
    args=parser.parse_args();generate_amr(args.path,args.max_cells)
