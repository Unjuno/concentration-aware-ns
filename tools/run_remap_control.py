"""Fixed refined-mesh controls initialized with analytic velocity at t=0."""
import hashlib,json,os,re,shutil,subprocess
from pathlib import Path
import numpy as np
from tools.openfoam_case import generate
from tools.reference import fields
from tools.analyze_openfoam import vectors
from tools.analyze_amr import values


def main():
    protocol_path=Path(os.environ.get('CANS_REMAP_PROTOCOL','protocols/of13-remap-control-v1.json'))
    spec=json.loads(protocol_path.read_text())
    root=Path(os.environ.get('CANS_OF13_REMAP_RUN_ROOT','work/of13-remap-control-v1')).expanduser().resolve();root.mkdir(exist_ok=False)
    source_study=Path(spec.get('source_study','work/of13-amr-v1'))
    if not source_study.is_absolute():
        source_study=Path('work')/source_study
    for name in spec['source_cases']:
        source=source_study/name
        d=json.loads((source/'diagnostics.json').read_text());count=d['cells']
        original=source/'0.05';centers=vectors(original/'C',count)
        params=json.loads((source/'parameters.json').read_text())
        profile=params.get('profile','gaussian')
        case=root/name;generate(case,n=16,dt=spec['dt'],end=spec['end'],profile=profile,frequency=params.get('frequency',8))
        shutil.copytree(original/'polyMesh',case/'constant/polyMesh')
        # Never run blockMesh on this case: that would replace the refined mesh.
        (case/'system/blockMeshDict').unlink()
        if profile == 'high-gradient':
            from tools.high_gradient_reference import fields as high_gradient_fields
            u=high_gradient_fields(centers,N=params['frequency'],nu=params['nu'],time=0)['u']
        else:
            u=fields(centers,0,sigma=params['sigma'],nu=params['nu'])['u']
        field=case/'0/U';text=field.read_text()
        data='\n'.join('('+ ' '.join(f'{v:.17g}' for v in row)+')' for row in u)
        text=re.sub(r'internalField.*?boundaryField',f'internalField nonuniform List<vector>\n{count}\n(\n{data}\n);\nboundaryField',text,flags=re.S)
        field.write_text(text)
        params=json.loads((case/'parameters.json').read_text())
        params.update(purpose=spec['purpose'],mesh_cells=count,source_case=name,adaptation=False)
        (case/'parameters.json').write_text(json.dumps(params,indent=2))
        hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (case/'constant/polyMesh').iterdir() if p.is_file()}
        (case/'mesh-hashes.json').write_text(json.dumps(hashes,indent=2))
        docker=os.environ.get('CANS_DOCKER_CLI','docker')
        context=os.environ.get('CANS_DOCKER_CONTEXT')
        prefix=[docker]+(['--context',context] if context else [])
        docker_cli=subprocess.run([*prefix,'--version'],capture_output=True,text=True,timeout=8,check=True).stdout.strip()
        docker_image=subprocess.run([*prefix,'image','inspect','concentration-aware-ns:of13','--format','{{.Id}}'],capture_output=True,text=True,timeout=8,check=True).stdout.strip()
        if docker_image != os.environ.get('CANS_EXPECTED_IMAGE_ID',docker_image):
            raise ValueError(f'unexpected OpenFOAM image ID: {docker_image}')
        command=[*prefix,'run','--rm','--name',f'cans-remap-{name}','--entrypoint','/bin/bash','-v',f'{case}:/case',docker_image,'-c',
                 'useradd -o -u "$1" -m runner && su runner -s /bin/bash -c "source /opt/openfoam13/etc/bashrc && cd /case && checkMesh > log.checkMesh 2>&1 && foamRun > log.foamRun 2>&1 && foamPostProcess -func writeCellCentres -latestTime > log.centres 2>&1 && foamPostProcess -func writeCellVolumes -latestTime > log.volumes 2>&1"','--',str(os.getuid())]
        print(f'START {name}',flush=True)
        (case/'command.json').write_text(json.dumps(command,indent=2))
        with (case/'log.container').open('w') as stream:
            run=subprocess.run(command,stdout=stream,stderr=subprocess.STDOUT)
        (case/'exit.json').write_text(json.dumps({'exit_code':run.returncode}))
        if run.returncode:raise RuntimeError(str(case))
        final=case/'0.05'
        if not (case/'log.foamRun').read_text().rstrip().endswith('End'):raise ValueError('incomplete solver')
        observed_c=vectors(final/'C',count)
        np.testing.assert_allclose(observed_c,centers,atol=1e-12,rtol=0)
        got=vectors(final/'U',count);volumes=values(final/'Vc',count)
        if np.any(volumes<=0) or not np.isclose(volumes.sum(),(2*np.pi)**3,rtol=1e-10):raise ValueError('invalid volumes')
        if params.get('profile') == 'high-gradient':
            ref=high_gradient_fields(centers,N=params['frequency'],nu=params['nu'],time=spec['end'])['u']
        else:
            ref=fields(centers,spec['end'],sigma=params['sigma'],nu=params['nu'])['u']
        error=float(np.sqrt(np.sum(volumes*np.sum((got-ref)**2,axis=1))/np.sum(volumes*np.sum(ref**2,axis=1))))
        result={'case':name,'cells':count,'velocity_relative_volume_l2':error,
                'original_amr_velocity_error':d['velocity_relative_volume_l2'],
                'centers_match':True,'quality':'UNCERTAIN','parameters':params}
        (case/'diagnostics.json').write_text(json.dumps(result,indent=2))
        print(f'END {name} error={error}',flush=True)
    (root/'run-environment.json').write_text(json.dumps({
        'source_commit':subprocess.run(['git','rev-parse','HEAD'],capture_output=True,text=True,check=True).stdout.strip(),
        'protocol_sha256':hashlib.sha256(protocol_path.read_bytes()).hexdigest(),
        'source_study':str(source_study), 'docker_cli':docker,
        'docker_context':context, 'docker_cli_version':docker_cli,
        'container_image_id':docker_image,
        'scope':'High-gradient fixed-final-mesh remap controls; see per-case input hashes and command records.'
    },indent=2)+'\n')


if __name__=='__main__':main()
