import json,os,subprocess
from pathlib import Path
from tools.openfoam_amr_case import generate_amr
from tools.analyze_amr import analyze


def main():
    spec=json.loads(Path('protocols/of13-amr-v1.json').read_text())
    root=Path('work/of13-amr-v1').resolve();root.mkdir(exist_ok=False)
    for cap in spec['maxCells']:
        case=root/f'cap{cap}';generate_amr(case,cap,spec['maxRefinement'],spec['end'])
        print(f'START cap{cap}',flush=True)
        command=['docker','run','--rm','--name',f'cans-amr-{cap}','--entrypoint','/bin/bash','-v',f'{case}:/case','concentration-aware-ns:of13','-c',
         'useradd -o -u "$1" -m runner && su runner -s /bin/bash -c "source /opt/openfoam13/etc/bashrc && cd /case && blockMesh > log.blockMesh 2>&1 && foamRun > log.foamRun 2>&1 && foamPostProcess -func writeCellCentres -latestTime > log.centres 2>&1 && foamPostProcess -func writeCellVolumes -latestTime > log.volumes 2>&1 && foamPostProcess -func \'grad(U)\' -latestTime > log.gradient 2>&1"','--',str(os.getuid())]
        (case/'command.json').write_text(json.dumps(command))
        with (case/'log.container').open('w') as stream:
            p=subprocess.run(command,stdout=stream,stderr=subprocess.STDOUT)
        (case/'exit.json').write_text(json.dumps({'exit_code':p.returncode}))
        if p.returncode: raise RuntimeError(str(case))
        d=analyze(case);(case/'diagnostics.json').write_text(json.dumps(d,indent=2))
        print(f'END cap{cap} cells={d["cells"]} velocity_error={d["velocity_relative_volume_l2"]}',flush=True)


if __name__=='__main__':main()
