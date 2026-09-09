"""Read complete SU2 periodic Cartesian results with explicit time conventions."""
import csv
import hashlib
import json
from pathlib import Path
import numpy as np
from tools.reference import fields
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
    ref=fields(xyz[keep],end,sigma=p['sigma'],nu=p['nu'])
    refgrid=np.empty_like(grid);refgrid[tuple(ids.T)]=ref['u']
    computed=diagnostics(grid);sampled=diagnostics(refgrid)
    g=float(np.linalg.norm(ref['grad_u'],axis=(-2,-1)).max());w=float(np.linalg.norm(ref['vorticity'],axis=-1).max())
    return {'parameters':p,'quality':'UNCERTAIN','updated_solution_time':steps*dt,'reported_and_source_time':history[-1]['Cur_Time'],
            'steps':steps,'converged_steps':sum(all(r[k]<-10 for k in ('rms[P]','rms[U]','rms[V]','rms[W]')) for r in history),
            'periodic_duplicate_max_mismatch':mismatch,'unique_points':len(ids),
            'velocity_relative_l2':float(np.linalg.norm(u[keep]-ref['u'])/np.linalg.norm(ref['u'])),
            'computed':computed,'reference_sampled_fd2':sampled,
            'reference_gradient_peak_samples':g,'reference_vorticity_peak_samples':w,
            'gradient_peak_relative_error_samples':abs(computed['max_gradient_fd2']-g)/g,
            'vorticity_peak_relative_error_samples':abs(computed['max_vorticity_fd2']-w)/w,
            'sha256':{f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in (path,case/'case.cfg',case/'mesh.su2',case/'history.csv',case/'solver.log')}}
