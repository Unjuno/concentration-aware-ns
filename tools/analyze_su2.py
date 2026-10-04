"""Read complete SU2 periodic Cartesian results with explicit time conventions."""
import csv
import hashlib
import json
from pathlib import Path
import numpy as np
from tools.reference import fields
from tools.high_gradient_reference import fields as high_gradient_fields
from tools.metrics import diagnostics


def analyze(case):
    case=Path(case);p=json.loads((case/'parameters.json').read_text());n=p['n'];dt=p['dt'];end=p['end'];steps=round(end/dt)
    if (case/'exit_code').read_text().strip()!='0' or 'Exit Success (SU2_CFD)' not in (case/'solver.log').read_text():raise ValueError('no completed solver')
    with (case/'history.csv').open() as f:
        history=[{k.strip().strip('"'):float(v) for k,v in r.items()} for r in csv.DictReader(f)]
    if len(history)!=steps or [int(r['Time_Iter']) for r in history]!=list(range(steps)):raise ValueError('unexpected time history')
    if abs(history[-1]['Cur_Time']-(steps-1)*dt)>1e-10:raise ValueError('changed reported-time convention')
    path=case/f'restart_{steps-1:05d}.csv';data=np.genfromtxt(path,delimiter=',',names=True)
    xyz=np.stack([data[k] for k in ('x','y','z')],axis=-1)
    u=np.stack([data['Velocity_'+k] for k in ('x','y','z')],axis=-1)
    if not np.isfinite(xyz).all() or not np.isfinite(u).all():raise ValueError('nonfinite fields')
    indices=np.rint(xyz*n/(2*np.pi)).astype(int)
    if np.max(np.abs(xyz-indices*2*np.pi/n))>1e-12 or np.any(indices<0) or np.any(indices>n):raise ValueError('not expected grid')
    keep=np.all(indices<n,axis=1);ids=indices[keep]
    if len(ids)!=n**3 or len(np.unique(ids,axis=0))!=n**3:raise ValueError('incomplete unique periodic grid')
    grid=np.empty((n,n,n,3));grid[tuple(ids.T)]=u[keep]
    mismatch=float(np.abs(u-grid[tuple((indices%n).T)]).max())
    profile=p.get('profile','gaussian')
    if profile=='high-gradient':
        ref=high_gradient_fields(xyz[keep],N=p['frequency'],nu=p['nu'],time=end)
    elif profile=='gaussian':
        ref=fields(xyz[keep],end,sigma=p['sigma'],nu=p['nu'])
    else:
        raise ValueError(f'unsupported SU2 reference profile: {profile}')
    refgrid=np.empty_like(grid);refgrid[tuple(ids.T)]=ref['u']
    computed=diagnostics(grid);sampled=diagnostics(refgrid)
    g=float(np.linalg.norm(ref['grad_u'],axis=(-2,-1)).max());w=float(np.linalg.norm(ref['vorticity'],axis=-1).max())
    energy_error=abs(computed['mean_kinetic_energy']-sampled['mean_kinetic_energy'])/sampled['mean_kinetic_energy']
    shell_error=float(np.abs(np.asarray(computed['shell_energy'])-np.asarray(sampled['shell_energy'])).sum()/sampled['spectrum_energy'])
    thresholds=p.get('quality_thresholds',{})
    metric_errors={'velocity_relative_l2':float(np.linalg.norm(u[keep]-ref['u'])/np.linalg.norm(ref['u'])),
                   'energy_relative_error':energy_error,
                   'max_gradient_relative_error_samples':abs(computed['max_gradient_fd2']-g)/g,
                   'max_vorticity_relative_error_samples':abs(computed['max_vorticity_fd2']-w)/w,
                   'shell_spectrum_relative_l1':shell_error}
    quality_sampled=('PASS' if thresholds and all(metric in thresholds and metric_errors[metric]<=thresholds[metric]
                      for metric in metric_errors) else 'FAIL' if thresholds else 'NOT_EVALUATED')
    history_time=float(history[-1]['Cur_Time'])
    last_source_time=(steps-1)*dt
    return {'parameters':p,'mms_profile':profile,'quality':'UNCERTAIN','quality_sampled':quality_sampled,
            'quality_metric_errors':metric_errors,'updated_solution_time':steps*dt,
            'expected_last_source_time':last_source_time,'reported_history_time':history_time,
            'source_history_time_difference':history_time-last_source_time,
            'reported_and_source_time':history_time,
            'steps':steps,'converged_steps':sum(all(r[k]<-10 for k in ('rms[P]','rms[U]','rms[V]','rms[W]')) for r in history),
            'periodic_duplicate_max_mismatch':mismatch,'unique_points':len(ids),
            'velocity_relative_l2':metric_errors['velocity_relative_l2'],'energy_relative_error':energy_error,
            'computed':computed,'reference_sampled_fd2':sampled,
            'reference_gradient_peak_samples':g,'reference_vorticity_peak_samples':w,
            'gradient_peak_relative_error_samples':abs(computed['max_gradient_fd2']-g)/g,
            'vorticity_peak_relative_error_samples':abs(computed['max_vorticity_fd2']-w)/w,
            'sha256':{f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in (path,case/'case.cfg',case/'mesh.su2',case/'history.csv',case/'solver.log')}}
