"""Reanalyze completed paired raw outputs; keep convergence and quality separate."""
import argparse,json,csv,hashlib,math
from pathlib import Path
from tools.analyze_su2 import analyze
from tools.run_su2_full_horizon_cfl_pair import verify_history
from tools.reference_energy import mean_energy


def review(root,protocol):
    p=json.loads(protocol.read_text());manifest=json.loads((root/'manifest.json').read_text())
    if manifest['status']!='EXECUTION_COMPLETE_QUALITY_SEPARATE' or manifest['completed_cases']!=2:
        raise ValueError('paired execution incomplete')
    if {r['case'] for r in manifest['cases']}!={'baseline','control'} or len(manifest['cases'])!=2:
        raise ValueError('missing or duplicate paired case')
    quality=json.loads(Path(p['quality_protocol']).read_text());rows=[];images=[]
    for label,cfl in [('baseline',10),('control',100)]:
        case=root/label;params=json.loads((case/'parameters.json').read_text())
        if params.get('CFL_NUMBER')!=cfl or any(params[k]!=v for k,v in [('n',32),('dt',.001),('end',.05),('sigma',.5),('nu',.01)]):raise ValueError('case metadata mismatch')
        for filename,key in [('case.cfg',label+'_config_sha256'),('mesh.su2','mesh_sha256')]:
            if hashlib.sha256((case/filename).read_bytes()).hexdigest()!=p[key]:raise ValueError('paired input identity changed')
        with (case/'history.csv').open() as stream:history=list(csv.DictReader(stream))
        verify_history([{k.strip().strip('"'):v for k,v in r.items()} for r in history])
        d=analyze(case);images.append(params['image_id'])
        energy=mean_energy(d['updated_solution_time'],sigma=params['sigma'])
        errors={'velocity_l2':d['velocity_relative_l2'],'energy':abs(d['computed']['mean_kinetic_energy']-energy)/energy,
                'max_gradient':d['gradient_peak_relative_error_samples'],'max_vorticity':d['vorticity_peak_relative_error_samples']}
        if not all(math.isfinite(v) and v>=0 for v in errors.values()):raise ValueError('invalid quality diagnostic')
        rows.append({'case':label,'CFL_NUMBER':cfl,'converged_steps':d['converged_steps'],'expected_steps':50,
                     'all_steps_converged':d['converged_steps']==50,'observed_errors':errors,
                     'observed_quality_checks':{k:v<=quality['relative_error_thresholds'][k] for k,v in errors.items()},
                     'raw_output_sha256':d['sha256']})
    if len(set(images))!=1:raise ValueError('new and old images mixed in pair')
    return {'status':'MATCHED_PAIR_REANALYZED_CONVERGENCE_AND_QUALITY_SEPARATE','image_id':images[0],'cases':rows,
            'limits':['Recomputed grid diagnostics and original thresholds; not continuum peak certification',
                      'Convergence does not by itself imply quality; quality changes do not establish a source defect',
                      'No causal attribution to forcing lag, physical instability or unresolved proof claims']}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,required=True);p.add_argument('--protocol',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    if a.output.exists():raise FileExistsError('preserve prior pair review')
    a.output.write_text(json.dumps(review(a.root,a.protocol),indent=2)+'\n')
