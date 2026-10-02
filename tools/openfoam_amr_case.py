"""AMR integration pilots with an analytic profile-matched sensor."""
import argparse
import json
from pathlib import Path

from tools.openfoam_case import generate


SENSOR_INIT = '''
 if (!mesh().foundObject<volScalarField>("refineSensor")) {
   auto* sensor = new volScalarField(
     IOobject("refineSensor", mesh().time().name(), mesh(), IOobject::NO_READ, IOobject::AUTO_WRITE),
     mesh(), dimensionedScalar("zero", dimless, 0), "cyclic");
   sensor->store();
 }
 volScalarField& sensor = mesh().lookupObjectRef<volScalarField>("refineSensor");'''


def generate_amr(path, max_cells=5000, max_level=1, end=0.01, *,
                 profile='gaussian', frequency=8, n=16, dt=0.001, nu=0.01):
    generate(path, n=n, dt=dt, end=end, nu=nu,
             profile=profile, frequency=frequency)
    path = Path(path)
    model = path/'constant/fvModels'
    body = model.read_text()
    if profile == 'gaussian':
        marker = 'const scalar now = mesh().time().value();'
        if marker not in body:
            raise ValueError('Gaussian source-hook insertion point not found')
        body = body.replace(marker, marker+SENSOR_INIT, 1)
        marker = 'const scalar psi = exp(exponent);'
        if marker not in body:
            raise ValueError('Gaussian sensor expression insertion point not found')
        body = body.replace(marker, marker+'\n   sensor[celli] = exp(exponent+now);', 1)
        lower_refine_level = 0.01
        sensor_description = 'exp(sum(cos(x-pi)-1)/sigma^2)'
    elif profile == 'high-gradient':
        marker = 'const scalar decay = exp(-mesh().time().value());'
        if marker not in body:
            raise ValueError('high-gradient source-hook insertion point not found')
        body = body.replace(marker, marker+SENSOR_INIT, 1)
        marker = 'const scalar sx = sin(frequency*x), cx = cos(frequency*x);'
        if marker not in body:
            raise ValueError('high-gradient sensor expression insertion point not found')
        # The selected component is u_y = -exp(-t)*chi*cos(N*x)/N,
        # hence (d_x u_y)^2 = exp(-2t)*chi^2*sin(N*x)^2.
        body = body.replace(marker, marker+'\n   sensor[celli] = sqr(decay*chi*sx);', 1)
        lower_refine_level = 0.25
        sensor_description = ('exp(-2*time)*chi(y,z)^2*sin(frequency*x)^2; '
                              'equals (partial_x u_y)^2')
    else:
        raise ValueError(f'unsupported AMR profile {profile!r}')
    if '\n #};' not in body:
        raise ValueError('source-hook closing marker not found')
    body = body.replace('\n #};', '\n sensor.correctBoundaryConditions();\n #};', 1)
    model.write_text(body)
    solution = path/'system/fvSolution'
    solution.write_text(solution.read_text().replace(
        'pFinal { $p; }', 'pFinal { $p; }\npcorr { $p; }\npcorrFinal { $p; }'))
    (path/'constant/dynamicMeshDict').write_text(f'''FoamFile {{ format ascii; class dictionary; object dynamicMeshDict; }}
topoChanger {{
 type refiner; libs ("libfvMeshTopoChangers.so");
 refineInterval 2; field refineSensor;
 lowerRefineLevel {lower_refine_level}; upperRefineLevel 1.1;
 nBufferLayers 1; maxRefinement {max_level}; maxCells {max_cells};
 dumpLevel true;
}}
''')
    params = json.loads((path/'parameters.json').read_text())
    params.update(purpose='AMR integration pilot, not production', amr={
        'maxCells': max_cells,
        'maxRefinement': max_level,
        'refineInterval': 2,
        'sensor': sensor_description,
        'lowerRefineLevel': lower_refine_level,
        'upperRefineLevel': 1.1,
    })
    (path/'parameters.json').write_text(json.dumps(params, indent=2)+'\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    parser.add_argument('--max-cells', type=int, default=5000)
    parser.add_argument('--max-level', type=int, default=1)
    parser.add_argument('--profile', choices=['gaussian', 'high-gradient'], default='gaussian')
    parser.add_argument('--frequency', type=int, default=8)
    parser.add_argument('--n', type=int, default=16)
    parser.add_argument('--dt', type=float, default=0.001)
    parser.add_argument('--end', type=float, default=0.01)
    parser.add_argument('--nu', type=float, default=0.01)
    args = parser.parse_args()
    generate_amr(args.path, args.max_cells, args.max_level, args.end,
                 profile=args.profile, frequency=args.frequency,
                 n=args.n, dt=args.dt, nu=args.nu)
