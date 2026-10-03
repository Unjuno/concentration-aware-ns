"""Original-image paired runner; never rebuilds or repairs Docker."""
import argparse,csv,json,os,shutil,subprocess
from pathlib import Path
from tools.verify_su2_cfl_pair_inputs import verify
from tools.analyze_su2 import analyze


def run(root,protocol,output,preflight_only=False):
    if output.exists():raise FileExistsError('preserve previous experiment')
    inputs=verify(root,protocol);p=json.loads(protocol.read_text())
    for label in ('baseline','control'):
        if {x.name for x in (root/label).iterdir()}!={'case.cfg','mesh.su2','parameters.json'}:
            raise ValueError('prepared directory contains non-input files')
    output.mkdir();(output/'input-verification.json').write_text(json.dumps(inputs,indent=2)+'\n')
    manifest={'status':'INCOMPLETE','completed_cases':0,'expected_cases':2,'preflight_only':preflight_only,'cases':[]}
    def save(): (output/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    save()
    command=['docker','image','inspect',p['image_id_required'],'--format','{{json .}}']
    try:
        result=subprocess.run(command,capture_output=True,text=True,timeout=10)
    except subprocess.TimeoutExpired:
        manifest['preflight_status']='OBSERVATION_TIMEOUT';save();raise
    (output/'image-inspect.stdout').write_text(result.stdout);(output/'image-inspect.stderr').write_text(result.stderr)
    if result.returncode:
        manifest['preflight_status']='IMAGE_UNAVAILABLE';save();raise RuntimeError('original image inspection failed; no solver started')
    image=json.loads(result.stdout)
    if image['Id']!=p['image_id_required']:raise ValueError('wrong original image')
    manifest['preflight_status']='ORIGINAL_IMAGE_IDENTITY_VERIFIED';save()
    if preflight_only:return manifest
    for label in ('baseline','control'):
        case=output/label;shutil.copytree(root/label,case)
        params=json.loads((case/'parameters.json').read_text());params['CFL_NUMBER']=10 if label=='baseline' else 100
        (case/'parameters.json').write_text(json.dumps(params,indent=2)+'\n')
        cmd=['docker','run','--rm','--cpus','2','--user',f'{os.getuid()}:{os.getgid()}',
             '-e','OMP_NUM_THREADS=2','-v',f'{case.resolve()}:/case',p['image_id_required'],'SU2_CFD','case.cfg']
        (case/'command.json').write_text(json.dumps(cmd)+'\n')
        with (case/'solver.log').open('w') as log:result=subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT)
        (case/'exit_code').write_text(str(result.returncode)+'\n')
        if result.returncode:save();raise RuntimeError('solver failed; preserve partial case')
        with (case/'history.csv').open() as stream:history=list(csv.DictReader(stream))
        history=[{k.strip().strip('"'):v for k,v in r.items()} for r in history]
        if len(history)!=50 or [int(r['Time_Iter']) for r in history]!=list(range(50)):
            raise ValueError('missing or duplicate physical updates')
        diagnostics=analyze(case);(case/'diagnostics.json').write_text(json.dumps(diagnostics,indent=2)+'\n')
        for filename,key in [('case.cfg',label+'_config_sha256'),('mesh.su2','mesh_sha256')]:
            if diagnostics['sha256'][filename]!=p[key]:raise ValueError('input mutated during solver')
        manifest['cases'].append({'case':label,'converged_steps':diagnostics['converged_steps'],'steps':50,'velocity_relative_l2':diagnostics['velocity_relative_l2']})
        manifest['completed_cases']+=1;save()
    manifest['status']='EXECUTION_COMPLETE_QUALITY_SEPARATE';save();return manifest


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,required=True);p.add_argument('--protocol',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--preflight-only',action='store_true');a=p.parse_args();run(a.root,a.protocol,a.output,a.preflight_only)
