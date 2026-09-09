"""AMR integration pilot using an analytic, fixed spatial concentration sensor."""
import argparse
import json
from pathlib import Path
from tools.openfoam_case import generate


def generate_amr(path, max_cells=5000, max_level=1, end=0.01):
    generate(path,n=16,dt=0.001,end=end)
    path=Path(path)
    model=path/'constant/fvModels'
    body=model.read_text()
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
    p.update(purpose='AMR integration pilot, not production',amr={'maxCells':max_cells,'maxRefinement':max_level,'refineInterval':2,'sensor':'analytic exp(sum(cos(x-pi)-1)/sigma^2); recomputed by source hook before next adaptation'})
    (path/'parameters.json').write_text(json.dumps(p,indent=2))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('path');parser.add_argument('--max-cells',type=int,default=5000)
    args=parser.parse_args();generate_amr(args.path,args.max_cells)
