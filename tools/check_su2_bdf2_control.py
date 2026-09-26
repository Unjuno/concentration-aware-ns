"""Replay archive identities and exact recurrence predictions for BDF2 control."""
from fractions import Fraction as F
import csv
import io
import numpy as np
import hashlib
import json
import math
from pathlib import Path
import tarfile

protocol=json.loads(Path('protocols/su2-bdf2-control-v1.json').read_text())
results=[]
for suffix in ('','-corrected'):
    root=Path('evidence/su2-bdf2-control-v1'+suffix)
    summary=json.loads((root/'summary.json').read_text())
    assert [case['dt'] for case in summary['cases']]==protocol['dt']
    cases=[]
    for case in summary['cases']:
        archive=root/f"dt{case['dt']}.tar.gz"
        assert hashlib.sha256(archive.read_bytes()).hexdigest()==case['archive_sha256']
        assert [step['step'] for step in case['steps']]==list(range(1,round(protocol['end']/case['dt'])+1))
        endpoint_error=None
        with tarfile.open(archive) as tar:
            diag=json.load(tar.extractfile('diagnostics.json'))
            assert diag['steps']==case['steps']
            assert tar.extractfile('exit_code').read().strip()==b'0'
            assert b'DUAL_TIME_STEPPING-2ND_ORDER' in tar.extractfile('case.cfg').read()
            history=list(csv.DictReader(io.StringIO(tar.extractfile('history.csv').read().decode())))
            assert len(history)==len(case['steps'])
            for step,row in zip(case['steps'],history):
                values=np.genfromtxt(tar.extractfile(f"restart_{step['step']-1:05d}.csv"),delimiter=',',names=True)['Velocity_x']
                assert values.size>0 and np.isfinite(values).all()
                target_time=step['step']*case['dt']
                endpoint_error=float(np.max(np.abs(values-(1+target_time**2))))
                assert abs(endpoint_error-step['max_error_continuous_at_target'])<1e-14
                assert abs(float(values.mean())-step['mean_ux'])<1e-14
                assert abs(float(np.ptp(values))-step['spatial_spread'])<1e-14
                row={key.strip().strip('\"'):float(value) for key,value in row.items()}
                assert all(row[key]<-10 for key in ['rms[P]','rms[U]','rms[V]','rms[W]'])
        h=F(str(case['dt']))
        def error(k):
            return h*h*(F(1,2)*(1-F(3)**(-k)) if suffix else -2*k+F(3,2)*(1-F(3)**(-k)))
        def solution(k):
            return 1+(k*h)**2+error(k)
        assert solution(-1)==solution(0)==1
        discrepancies=[]
        for step in case['steps']:
            k=step['step']
            assert 3*solution(k)-4*solution(k-1)+solution(k-2)==4*h*h*(k if suffix else k-1)
            discrepancy=abs(step['mean_ux']-float(solution(k)))+step['spatial_spread']
            assert discrepancy<1e-7
            assert step['all_residuals_met']
            discrepancies.append(discrepancy)
        cases.append({'dt':float(h),'endpoint_error':endpoint_error,
                      'max_bound_on_formula_discrepancy':max(discrepancies),'all_step_residuals_met':True,
                      'archive_sha256':case['archive_sha256']})
    errors=[c['endpoint_error'] for c in cases]
    results.append({'variant':'target-time intervention' if suffix else 'original driver', 'cases':cases,
                    'observed_orders':[math.log(a/b,2) for a,b in zip(errors,errors[1:])]})
output={'success':True,'initial_history':'U[-1]=U[0]=1 (confirmed by all-step recurrence match)',
        'exact_error_original':'-2*k*h^2 + 3*h^2/2*(1-3^(-k))',
        'exact_error_target':'h^2/2*(1-3^(-k))',
        'scope':'Uniform MMS on pinned v8.5.0 source; not a general restart/multizone/boundary fix.', 'results':results}
Path('evidence/tests/su2-bdf2-control.json').write_text(json.dumps(output,indent=2)+'\n')
print(json.dumps(output,indent=2))
