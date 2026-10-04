"""Original-image paired runner; never rebuilds or repairs Docker."""
import argparse,csv,json,os,shutil,subprocess,math,sys
from pathlib import Path
import hashlib
from tools.verify_su2_cfl_pair_inputs import verify
from tools.analyze_su2 import analyze


def verify_history(history,steps=50,dt=.001):
    if len(history)!=steps or [int(r['Time_Iter']) for r in history]!=list(range(steps)):
        raise ValueError('missing or duplicate physical updates')
    # Recorded CSV times are decimal diagnostics, not exact binary state.
    for k,row in enumerate(history):
        step=float(row['Time_Step']);time=float(row['Cur_Time'])
        if not (math.isfinite(step) and math.isfinite(time)):
            raise ValueError('nonfinite history clock')
        if abs(step-dt)>1e-12 or abs(time-k*dt)>1e-12:
            raise ValueError('history does not match frozen old-time clock')
    return {'status':'PHYSICAL_UPDATE_AND_REPORTED_CLOCK_MATCH',
            'steps':steps,'CSV_absolute_clock_tolerance':1e-12,
            'scope':'Recorded history only, not source callback or internal floating clock proof'}


def normalize_case_labels(case_labels):
    labels=('baseline','control') if case_labels is None else tuple(case_labels)
    if (not labels or len(set(labels))!=len(labels)
            or set(labels)-{'baseline','control'}):
        raise ValueError('case_labels must be unique baseline/control selections')
    return labels


def verify_successor_probe(successor,measured):
    keys={'binary_sha256','patched_source_sha256','package_versions_sha256','compiler_version'}
    if set(measured)!=keys:raise ValueError('missing or unexpected successor probe fields')
    for key in keys:
        value=measured[key]
        if not isinstance(value,str) or not value or successor.get(key)!=value:
            raise ValueError('actual successor image evidence differs from receipt')
        if key.endswith('_sha256') and (len(value)!=64 or any(c not in '0123456789abcdef' for c in value)):
            raise ValueError('invalid successor measured digest')


def run_logged_command(command, log_path):
    """Save child output verbatim while streaming a readable copy to stdout."""
    with Path(log_path).open('wb') as log:
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            bufsize=0,
        )
        try:
            while chunk := process.stdout.read(8192):
                log.write(chunk)
                log.flush()
                sys.stdout.write(chunk.decode('utf-8', errors='replace'))
                sys.stdout.flush()
            return subprocess.CompletedProcess(command, process.wait())
        finally:
            process.stdout.close()


def run(root,protocol,output,preflight_only=False,successor_receipt=None,
        case_labels=None):
    if output.exists():raise FileExistsError('preserve previous experiment')
    case_labels=normalize_case_labels(case_labels)
    inputs=verify(root,protocol);p=json.loads(protocol.read_text())
    image_id=p['image_id_required']
    successor=None
    if successor_receipt is not None:
        successor=json.loads(Path(successor_receipt).read_text())
        frozen=json.loads(Path('protocols/su2-n32-full-horizon-cfl-successor-v2.json').read_text())
        if successor.get('source_commit')!=frozen['source_commit'] or successor.get('architecture')!=frozen['architecture']:
            raise ValueError('successor source or architecture mismatch')
        for path,digest in frozen['build_inputs_sha256'].items():
            if hashlib.sha256(Path(path).read_bytes()).hexdigest()!=digest or successor.get('build_inputs_sha256',{}).get(path)!=digest:
                raise ValueError('successor recipe identity mismatch')
        for key in ('binary_sha256','patched_source_sha256','package_versions_sha256'):
            value=successor.get(key,'')
            if len(value)!=64 or any(c not in '0123456789abcdef' for c in value):raise ValueError('missing successor identity evidence')
        image_id=successor.get('image_id','')
        if not image_id.startswith('sha256:') or len(image_id)!=71 or any(c not in '0123456789abcdef' for c in image_id[7:]):raise ValueError('invalid successor image identity')

    for label in ('baseline','control'):
        if {x.name for x in (root/label).iterdir()}!={'case.cfg','mesh.su2','parameters.json'}:
            raise ValueError('prepared directory contains non-input files')
    output.mkdir()
    if successor is not None:(output/'successor-receipt.json').write_text(json.dumps(successor,indent=2)+'\n')
    (output/'input-verification.json').write_text(json.dumps(inputs,indent=2)+'\n')
    manifest={'status':'INCOMPLETE','completed_cases':0,
              'expected_cases':len(case_labels),'case_labels':list(case_labels),
              'preflight_only':preflight_only,'cases':[]}
    manifest['selected_image_id']=image_id
    if successor_receipt is not None:
        manifest['successor_receipt_sha256']=hashlib.sha256(
            Path(successor_receipt).read_bytes()).hexdigest()
    def save(): (output/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    save()
    command=['docker','image','inspect',image_id,'--format','{{json .}}']
    try:
        result=subprocess.run(command,capture_output=True,text=True,timeout=10)
    except subprocess.TimeoutExpired:
        manifest['preflight_status']='OBSERVATION_TIMEOUT';save();raise
    (output/'image-inspect.stdout').write_text(result.stdout);(output/'image-inspect.stderr').write_text(result.stderr)
    if result.returncode:
        manifest['preflight_status']='IMAGE_UNAVAILABLE';save();raise RuntimeError('original image inspection failed; no solver started')
    image=json.loads(result.stdout)
    if image['Id']!=image_id:raise ValueError('wrong selected image')
    if successor is not None and (image.get('Architecture')!='arm64' or image.get('Os')!='linux'):raise ValueError('wrong successor platform')
    manifest['preflight_status']='SELECTED_IMAGE_IDENTITY_VERIFIED';save()
    if successor is not None:
        probe_code="import json,hashlib,subprocess; from pathlib import Path; paths={'binary_sha256':'/opt/su2-install/bin/SU2_CFD','patched_source_sha256':'/opt/SU2/Common/src/toolboxes/MMS/CUserDefinedSolution.cpp','package_versions_sha256':'/opt/package-versions.txt'}; r={k:hashlib.sha256(Path(v).read_bytes()).hexdigest() for k,v in paths.items()}; r['compiler_version']=subprocess.check_output(['g++','--version'],text=True); print(json.dumps(r))"
        probe=subprocess.run(['docker','run','--rm','--cpus','1','--entrypoint','python3',image_id,'-c',probe_code],capture_output=True,text=True,timeout=30)
        (output/'successor-probe.stdout').write_text(probe.stdout);(output/'successor-probe.stderr').write_text(probe.stderr)
        if probe.returncode:raise ValueError('successor identity probe failed')
        measured=json.loads(probe.stdout)
        verify_successor_probe(successor,measured)
        manifest['preflight_status']='SUCCESSOR_ACTUAL_PROBE_VERIFIED';save()

    if preflight_only:return manifest
    for label in case_labels:
        case=output/label;shutil.copytree(root/label,case)
        params=json.loads((case/'parameters.json').read_text());params['CFL_NUMBER']=10 if label=='baseline' else 100
        params['predecessor_image_id']=params['image_id'];params['image_id']=image_id
        (case/'parameters.json').write_text(json.dumps(params,indent=2)+'\n')
        cmd=['docker','run','--rm','--cpus','2','--user',f'{os.getuid()}:{os.getgid()}',
             '-e','OMP_NUM_THREADS=2','-v',f'{case.resolve()}:/case',image_id,'SU2_CFD','case.cfg']
        (case/'command.json').write_text(json.dumps(cmd)+'\n')
        result=run_logged_command(cmd,case/'solver.log')
        (case/'exit_code').write_text(str(result.returncode)+'\n')
        if result.returncode:save();raise RuntimeError('solver failed; preserve partial case')
        with (case/'history.csv').open() as stream:history=list(csv.DictReader(stream))
        history=[{k.strip().strip('"'):v for k,v in r.items()} for r in history]
        clock=verify_history(history)
        (case/'history-verification.json').write_text(json.dumps(clock,indent=2)+'\n')
        diagnostics=analyze(case);(case/'diagnostics.json').write_text(json.dumps(diagnostics,indent=2)+'\n')
        for filename,key in [('case.cfg',label+'_config_sha256'),('mesh.su2','mesh_sha256')]:
            if diagnostics['sha256'][filename]!=p[key]:raise ValueError('input mutated during solver')
        manifest['cases'].append({'case':label,'converged_steps':diagnostics['converged_steps'],'steps':50,'velocity_relative_l2':diagnostics['velocity_relative_l2']})
        manifest['completed_cases']+=1;save()
    manifest['status']=('EXECUTION_COMPLETE_QUALITY_SEPARATE'
                        if set(case_labels)=={'baseline','control'}
                        else 'SINGLE_CASE_COMPLETE_NOT_PAIRED')
    save();return manifest


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,required=True);p.add_argument('--protocol',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--preflight-only',action='store_true');p.add_argument('--successor-receipt',type=Path);p.add_argument('--case',choices=('baseline','control'),action='append',dest='case_labels');a=p.parse_args();run(a.root,a.protocol,a.output,a.preflight_only,a.successor_receipt,a.case_labels)
