"""Review completed SU2 artifacts without treating process success as accuracy."""
import hashlib
import json
from pathlib import Path
import tarfile


def review(root=Path('.')):
    summary=json.loads((root/'evidence/su2-study-v1/summary.json').read_text())
    rows=[]
    for entry in summary['cases']:
        path=root/'evidence/su2-study-v1'/(entry['case']+'.tar.gz')
        digest=hashlib.sha256(path.read_bytes()).hexdigest()
        if digest!=entry['archive_sha256']:raise ValueError(f'Archive hash: {path}')
        with tarfile.open(path) as archive:
            def read(name):
                f=archive.extractfile(name)
                if f is None:raise ValueError(f'Missing file: {name}')
                return f.read()
            if read('exit_code').strip()!=b'0' or b'Exit Success' not in read('solver.log'):
                raise ValueError(f'Unsuccessful run: {path}')
            d=json.loads(read('diagnostics.json'))
            for name,expected in d['sha256'].items():
                if hashlib.sha256(read(name)).hexdigest()!=expected:
                    raise ValueError(f'Input hash: {path}/{name}')
            for key in ('velocity_relative_l2','converged_steps','steps'):
                if d[key]!=entry[key]:raise ValueError(f'Summary mismatch: {key}')
            p=d['parameters'];tol=p['relative_error_thresholds']['velocity_l2']
            if d['steps']!=round(p['end']/p['dt']):raise ValueError('Incomplete steps')
            rows.append({'case':entry['case'],'archive_sha256':digest,
                         'termination_and_input_hashes_verified':True,
                         'converged_steps':d['converged_steps'],'steps':d['steps'],
                         'velocity_relative_l2':d['velocity_relative_l2'],
                         'velocity_tolerance':tol,
                         'observed_velocity_threshold':'PASS' if d['velocity_relative_l2']<=tol else 'FAIL',
                         'all_step_residual_thresholds':'PASS' if d['converged_steps']==d['steps'] else 'FAIL'})
    return {'scope':'Archived diagnostics and integrity review; does not independently recompute fields, certify continuous peaks, or complete the full acceptance gate.',
            'expected_cases':summary['expected_cases'],'reviewed_cases':len(rows),'cases':rows}


if __name__=='__main__':
    result=review()
    Path('evidence/su2-study-v1/archive-review.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
