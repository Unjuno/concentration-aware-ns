"""Run the frozen high-gradient OpenFOAM AMR budget sweep once."""
import hashlib
import json
import os
import subprocess
from pathlib import Path

from tools.analyze_amr import analyze
from tools.openfoam_amr_case import generate_amr


def sha256(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda:stream.read(1<<20),b''):
            h.update(chunk)
    return h.hexdigest()


def main():
    spec=json.loads(Path('protocols/high-gradient-of13-v1.json').read_text())
    amr=spec['amr']; spatial=spec['spatial_matrix']
    root=Path('work/of13-high-gradient-amr-v1').resolve()
    dirty=subprocess.run(['git','status','--porcelain','--untracked-files=all'],
                         capture_output=True,text=True,check=True).stdout.strip()
    if dirty:
        raise RuntimeError('commit the run sources first so the recorded source revision is reproducible')
    git=subprocess.run(['git','rev-parse','HEAD'],capture_output=True,text=True,check=True).stdout.strip()
    image_info=subprocess.run(['docker','image','inspect','concentration-aware-ns:of13',
                               '--format','{{.Id}} {{.Os}}/{{.Architecture}}'],
                              capture_output=True,text=True,timeout=8,check=True).stdout.strip()
    image,platform=image_info.split(maxsplit=1)
    root.mkdir(parents=True,exist_ok=False)
    (root/'run-environment.json').write_text(json.dumps({
        'source_commit':git,'container_image_id':image,'container_platform':platform,
        'protocol_sha256':sha256('protocols/high-gradient-of13-v1.json'),
        'scope':'OpenFOAM Foundation 13 high-gradient AMR sweep'},indent=2)+'\n')
    cases=[]
    for cap in amr['cell_budgets']:
        case=root/f'cap{cap}'
        generate_amr(case,max_cells=cap,max_level=amr['max_refinement'],end=spec['end_time'],
                     profile='high-gradient',frequency=spec['frequency_N'],
                     n=amr['baseline_cell_count'],dt=spatial['delta_t'],
                     refine_interval=amr['refine_interval'])
        hashes={str(p.relative_to(case)):sha256(p) for p in sorted(case.rglob('*')) if p.is_file()}
        (case/'input-hashes.json').write_text(json.dumps(hashes,indent=2)+'\n')
        command=['docker','run','--rm','--name',f'cans-hg-amr-{cap}','--entrypoint','/bin/bash',
                 '-v',f'{case}:/case',image,'-c',
                 'useradd -o -u "$1" -m runner && su runner -s /bin/bash -c "source /opt/openfoam13/etc/bashrc && cd /case && blockMesh > log.blockMesh 2>&1 && foamRun > log.foamRun 2>&1 && foamPostProcess -func writeCellCentres -latestTime > log.centres 2>&1 && foamPostProcess -func writeCellVolumes -latestTime > log.volumes 2>&1 && foamPostProcess -func \'grad(U)\' -latestTime > log.gradient 2>&1"',
                 '--',str(os.getuid())]
        (case/'command.json').write_text(json.dumps(command,indent=2)+'\n')
        with (case/'log.container').open('w') as log:
            run=subprocess.run(command,stdout=log,stderr=subprocess.STDOUT)
        (case/'exit.json').write_text(json.dumps({'exit_code':run.returncode})+'\n')
        if run.returncode:
            raise RuntimeError(f"AMR case cap={cap} failed; preserve case and logs at {case}")
        result=analyze(case)
        (case/'diagnostics.json').write_text(json.dumps(result,indent=2)+'\n')
        cases.append(result)
    summary={'protocol':'protocols/high-gradient-of13-v1.json','cases':cases,
             'scope':'AMR and uniform-grid comparison inputs; no blind-spot verdict without all quality gates.'}
    (root/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps({'completed':len(cases),'root':str(root)},indent=2))


if __name__=='__main__':
    main()
