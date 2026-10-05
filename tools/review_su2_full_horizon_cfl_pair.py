"""Reanalyze completed paired raw outputs; keep convergence and quality separate."""
import argparse,json,csv,hashlib,math
from pathlib import Path
from tools.analyze_su2 import analyze
from tools.run_su2_full_horizon_cfl_pair import verify_history
from tools.reference_energy import mean_energy


def _manifest_case(root,label,allowed_statuses):
    manifest_path=root/'manifest.json'
    manifest=json.loads(manifest_path.read_text())
    if (manifest.get('status') not in allowed_statuses
            or manifest.get('completed_cases')!=1
            or [row.get('case') for row in manifest.get('cases',[])]!=[label]):
        raise ValueError(f'{label} execution is incomplete, duplicated, or mislabeled')
    if manifest.get('preflight_status')!='SUCCESSOR_ACTUAL_PROBE_VERIFIED':
        raise ValueError(f'{label} lacks an actual successor-image probe')
    case=root/label
    receipt=json.loads((root/'successor-receipt.json').read_text())
    return manifest,manifest_path,case,receipt


def review(root,protocol,baseline_root=None,control_root=None):
    p=json.loads(protocol.read_text())
    split=baseline_root is not None or control_root is not None
    if split:
        if baseline_root is None or control_root is None:
            raise ValueError('both baseline_root and control_root are required')
        baseline_root=Path(baseline_root);control_root=Path(control_root)
        bm,bmp,baseline,brec=_manifest_case(
            baseline_root,'baseline',{'INCOMPLETE','SINGLE_CASE_COMPLETE_NOT_PAIRED'})
        cm,cmpath,control,crec=_manifest_case(
            control_root,'control',{'SINGLE_CASE_COMPLETE_NOT_PAIRED'})
        manifests=[(bm,bmp),(cm,cmpath)]
        receipts=[brec,crec]
    else:
        if root is None:
            raise ValueError('root is required for a combined-run review')
        root=Path(root)
        manifest_path=root/'manifest.json'
        manifest=json.loads(manifest_path.read_text())
        if (manifest.get('status')!='EXECUTION_COMPLETE_QUALITY_SEPARATE'
                or manifest.get('completed_cases')!=2
                or [row.get('case') for row in manifest.get('cases',[])]
                   !=['baseline','control']):
            raise ValueError('paired execution incomplete, duplicated, or mislabeled')
        if manifest.get('preflight_status')!='SUCCESSOR_ACTUAL_PROBE_VERIFIED':
            raise ValueError('paired execution lacks an actual successor-image probe')
        baseline=root/'baseline';control=root/'control'
        receipt=json.loads((root/'successor-receipt.json').read_text())
        manifests=[(manifest,manifest_path)]
        receipts=[receipt]
    identity_keys=('image_id','source_commit','architecture','build_inputs_sha256',
                   'binary_sha256','patched_source_sha256','package_versions_sha256',
                   'compiler_version')
    if any(any(receipt.get(key)!=receipts[0].get(key) for key in identity_keys)
           for receipt in receipts[1:]):
        raise ValueError('paired cases were not measured against the same image receipt')
    image_id=receipts[0].get('image_id')
    if not isinstance(image_id,str) or not image_id.startswith('sha256:'):
        raise ValueError('successor receipt lacks an immutable image identity')
    for manifest,_ in manifests:
        selected=manifest.get('selected_image_id')
        if selected is not None and selected!=image_id:
            raise ValueError('run manifest image identity differs from its receipt')
    quality=json.loads(Path(p['quality_protocol']).read_text());rows=[]
    for label,cfl in [('baseline',10),('control',100)]:
        case=baseline if label=='baseline' else control
        params=json.loads((case/'parameters.json').read_text())
        if (params.get('CFL_NUMBER')!=cfl or params.get('image_id')!=image_id
                or any(params[k]!=v for k,v in [('n',32),('dt',.001),('end',.05),('sigma',.5),('nu',.01)])):
            raise ValueError('case metadata or actual image identity mismatch')
        for filename,key in [('case.cfg',label+'_config_sha256'),('mesh.su2','mesh_sha256')]:
            if hashlib.sha256((case/filename).read_bytes()).hexdigest()!=p[key]:raise ValueError('paired input identity changed')
        if (case/'exit_code').read_text().strip()!='0':
            raise ValueError(f'{label} solver did not exit successfully')
        with (case/'history.csv').open() as stream:history=list(csv.DictReader(stream))
        clock=verify_history([{k.strip().strip('"'):v for k,v in r.items()} for r in history])
        if clock['status']!='PHYSICAL_UPDATE_AND_REPORTED_CLOCK_MATCH':
            raise ValueError(f'{label} reported clock gate failed')
        d=analyze(case)
        energy=mean_energy(d['updated_solution_time'],sigma=params['sigma'])
        errors={'velocity_l2':d['velocity_relative_l2'],'energy':abs(d['computed']['mean_kinetic_energy']-energy)/energy,
                'max_gradient':d['gradient_peak_relative_error_samples'],'max_vorticity':d['vorticity_peak_relative_error_samples']}
        if not all(math.isfinite(v) and v>=0 for v in errors.values()):raise ValueError('invalid quality diagnostic')
        rows.append({'case':label,'CFL_NUMBER':cfl,'converged_steps':d['converged_steps'],'expected_steps':50,
                     'all_steps_converged':d['converged_steps']==50,'observed_errors':errors,
                     'observed_quality_checks':{k:v<=quality['relative_error_thresholds'][k] for k,v in errors.items()},
                     'raw_output_sha256':d['sha256']})
    return {'status':'MATCHED_PAIR_REANALYZED_CONVERGENCE_AND_QUALITY_SEPARATE','image_id':image_id,
            'run_manifests':[{'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
                             for _,path in manifests],
            'successor_receipt_sha256':[hashlib.sha256(
                (Path(baseline_root if split else root)/'successor-receipt.json').read_bytes()
                ).hexdigest(), hashlib.sha256(
                (Path(control_root if split else root)/'successor-receipt.json').read_bytes()
                ).hexdigest()],
            'cases':rows,
            'limits':['Recomputed grid diagnostics and original thresholds; not continuum peak certification',
                      'Convergence does not by itself imply quality; quality changes do not establish a source defect',
                      'No causal attribution to forcing lag, physical instability or unresolved proof claims']}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path);p.add_argument('--baseline-root',type=Path);p.add_argument('--control-root',type=Path);p.add_argument('--protocol',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    if a.output.exists():raise FileExistsError('preserve prior pair review')
    a.output.parent.mkdir(parents=True,exist_ok=True)
    result=review(a.root,a.protocol,a.baseline_root,a.control_root)
    a.output.write_text(json.dumps(result,indent=2)+'\n')
