"""Sequential frozen study runner. Existing cases are never overwritten."""
import json
import os
import subprocess
from pathlib import Path
from tools.openfoam_case import generate
from tools.analyze_openfoam import analyze


def main():
    spec=json.loads(Path('protocols/of13-study-v1.json').read_text())
    root=Path('work/of13-study-v1').resolve()
    root.mkdir(exist_ok=False)
    cases=[(n,spec['spatial_dt']) for n in spec['spatial_n']]
    cases += [(spec['temporal_n'],dt) for dt in spec['temporal_dt'] if (spec['temporal_n'],dt) not in cases]
    for n,dt in cases:
        case=root/f'n{n}-dt{dt}'
        generate(case,n=n,dt=dt,end=spec['end'],sigma=spec['sigma'],nu=spec['nu'])
        print(f'START {case.name}',flush=True)
        command=['docker','run','--rm','--name',f'cans-{case.name}', '--entrypoint','/bin/bash',
                 '-v',f'{case}:/case','concentration-aware-ns:of13','-c',
                 'useradd -o -u "$1" -m runner && su runner -s /bin/bash -c "source /opt/openfoam13/etc/bashrc && cd /case && blockMesh > log.blockMesh 2>&1 && foamRun > log.foamRun 2>&1 && foamPostProcess -func writeCellCentres -latestTime > log.centres 2>&1"','--',str(os.getuid())]
        (case/'command.json').write_text(json.dumps(command,indent=2))
        with (case/'log.container').open('w') as out:
            result=subprocess.run(command,stdout=out,stderr=subprocess.STDOUT)
        (case/'exit.json').write_text(json.dumps({'exit_code':result.returncode}))
        if result.returncode:
            raise RuntimeError(f'{case.name} failed: inspect logs, do not overwrite')
        d=analyze(case)
        (case/'diagnostics.json').write_text(json.dumps(d,indent=2,allow_nan=False))
        print(f'END {case.name} velocity_relative_l2={d["velocity_relative_l2"]}',flush=True)


if __name__=='__main__':
    main()
