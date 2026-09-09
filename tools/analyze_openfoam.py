"""Uniform MMS diagnostics from OpenFOAM ASCII fields; no acceptance assertion."""
import argparse
import hashlib
import json
import re
from pathlib import Path
import numpy as np
from tools.reference import fields
from tools.metrics import diagnostics


def vectors(path, count):
    text=Path(path).read_text()
    text=re.sub(r'/\*.*?\*/|//[^\n]*','',text,flags=re.S)
    if re.search(r'format\s+binary',text):
        raise ValueError('ASCII only')
    match=re.search(r'internalField\s+nonuniform\s+List<vector>\s+(\d+)\s*\((.*?)\)\s*;',text,re.S)
    if not match or int(match[1]) != count:
        raise ValueError('expected matching nonuniform vector field')
    values=np.fromstring(match[2].replace('(',' ').replace(')',' '),sep=' ')
    if values.size != count*3 or not np.isfinite(values).all():
        raise ValueError('invalid vector data')
    return values.reshape(count,3)


def analyze(case):
    case=Path(case)
    params=json.loads((case/'parameters.json').read_text())
    n=params['n']; t=params['end']
    time_dir=next((p for p in case.iterdir() if p.is_dir() and p.name not in ('constant','system','dynamicCode','0')
                   and re.fullmatch(r'[0-9.eE+-]+',p.name) and abs(float(p.name)-t)<1e-12),None)
    if time_dir is None or not (case/'log.foamRun').read_text().rstrip().endswith('End'):
        raise ValueError('completed evaluation time not found')
    axis=(np.arange(n)+0.5)*2*np.pi/n
    z,y,x=np.meshgrid(axis,axis,axis,indexing='ij')
    points=np.stack((x,y,z),axis=-1).reshape(-1,3)
    centers=vectors(time_dir/'C',n**3)
    if not np.allclose(centers,points,atol=1e-12,rtol=0):
        raise ValueError('unverified mesh ordering/geometry')
    u=vectors(time_dir/'U',n**3)
    ref=fields(centers,t,sigma=params['sigma'],nu=params['nu'])
    def grid(v):
        return v.reshape(n,n,n,3).transpose(2,1,0,3)
    actual=diagnostics(grid(u)); sampled=diagnostics(grid(ref['u']))
    exact_g=float(np.linalg.norm(ref['grad_u'],axis=(-2,-1)).max())
    exact_w=float(np.linalg.norm(ref['vorticity'],axis=-1).max())
    result={'parameters':params,'quality':'UNCERTAIN','standard_acceptance':'UNCERTAIN',
            'note':'Diagnostics only. Analytic peaks are evaluated at cell centers, not continuous extrema.',
            'velocity_relative_l2':float(np.linalg.norm(u-ref['u'])/np.linalg.norm(ref['u'])),
            'gradient_peak_relative_error_cell_samples':abs(actual['max_gradient_fd2']-exact_g)/exact_g,
            'vorticity_peak_relative_error_cell_samples':abs(actual['max_vorticity_fd2']-exact_w)/exact_w,
            'reference_gradient_peak_cell_samples':exact_g,'reference_vorticity_peak_cell_samples':exact_w,
            'computed':actual,'reference_sampled_fd2':sampled,
            'sha256':{str(p.relative_to(case)):hashlib.sha256(p.read_bytes()).hexdigest()
                      for p in [case/'parameters.json',case/'log.foamRun',time_dir/'U',time_dir/'C']}}
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('case'); args=parser.parse_args()
    print(json.dumps(analyze(args.case),indent=2,allow_nan=False))
