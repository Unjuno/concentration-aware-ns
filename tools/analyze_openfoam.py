"""Uniform MMS diagnostics from OpenFOAM ASCII fields; no acceptance assertion."""
import argparse
import hashlib
import json
import re
from pathlib import Path
import numpy as np
from tools.reference import fields
from tools.high_gradient_reference import fields as high_gradient_fields
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
    profile=params.get('profile','gaussian')
    if profile=='gaussian':
        ref=fields(centers,t,sigma=params['sigma'],nu=params['nu'])
    elif profile=='high-gradient':
        ref=high_gradient_fields(centers,N=params['frequency'],nu=params['nu'],time=t)
    else:
        raise ValueError(f'unsupported reference profile: {profile!r}')
    def grid(v):
        return v.reshape(n,n,n,3).transpose(2,1,0,3)
    actual=diagnostics(grid(u)); sampled=diagnostics(grid(ref['u']))
    exact_g=float(np.linalg.norm(ref['grad_u'],axis=(-2,-1)).max())
    exact_w=float(np.linalg.norm(ref['vorticity'],axis=-1).max())
    energy_actual=actual['mean_kinetic_energy']
    energy_reference=sampled['mean_kinetic_energy']
    spectrum_actual=np.asarray(actual['shell_energy'],dtype=float)
    spectrum_reference=np.asarray(sampled['shell_energy'],dtype=float)
    width=max(len(spectrum_actual),len(spectrum_reference))
    spectrum_actual=np.pad(spectrum_actual,(0,width-len(spectrum_actual)))
    spectrum_reference=np.pad(spectrum_reference,(0,width-len(spectrum_reference)))
    spectrum_l1=float(np.abs(spectrum_actual-spectrum_reference).sum()
                      /spectrum_reference.sum()) if spectrum_reference.sum()>0 else float('nan')
    gradient_difference=abs(actual['max_gradient_fd2']-exact_g)/exact_g
    vorticity_difference=abs(actual['max_vorticity_fd2']-exact_w)/exact_w
    result={'parameters':params,'reference_profile':profile,'quality':'UNCERTAIN','standard_acceptance':'UNCERTAIN',
            'note':('Diagnostics only. The computed FD2 peak is compared with the analytic reference peak '
                    'sampled at cell centers; this combines solution and postprocessing differences. '
                    'FD2 operator error on the sampled reference is reported separately. Neither sampled '
                    'quantity certifies a continuous-domain extremum.'),
            'velocity_relative_l2':float(np.linalg.norm(u-ref['u'])/np.linalg.norm(ref['u'])),
            'energy_relative_error_cell_samples':abs(energy_actual-energy_reference)/energy_reference if energy_reference>0 else float('nan'),
            'shell_spectrum_relative_l1_cell_samples':spectrum_l1,
            'gradient_peak_relative_error_cell_samples':gradient_difference,
            'vorticity_peak_relative_error_cell_samples':vorticity_difference,
            'gradient_peak_fd2_vs_analytic_sampled_reference_relative_difference':gradient_difference,
            'vorticity_peak_fd2_vs_analytic_sampled_reference_relative_difference':vorticity_difference,
            'gradient_peak_fd2_operator_relative_error':abs(actual['max_gradient_fd2']-sampled['max_gradient_fd2'])/sampled['max_gradient_fd2'] if sampled['max_gradient_fd2']>0 else float('nan'),
            'vorticity_peak_fd2_operator_relative_error':abs(actual['max_vorticity_fd2']-sampled['max_vorticity_fd2'])/sampled['max_vorticity_fd2'] if sampled['max_vorticity_fd2']>0 else float('nan'),
            'reference_gradient_peak_cell_samples':exact_g,'reference_vorticity_peak_cell_samples':exact_w,
            'reference_continuous_gradient_lower_bound':(float(np.exp(-t)) if profile=='high-gradient' else None),
            'reference_continuous_vorticity_lower_bound':(float(np.exp(-t)*(1+2/params['frequency']**2)) if profile=='high-gradient' else None),
            'computed':actual,'reference_sampled_fd2':sampled,
            'sha256':{str(p.relative_to(case)):hashlib.sha256(p.read_bytes()).hexdigest()
                      for p in [case/'parameters.json',case/'log.foamRun',time_dir/'U',time_dir/'C']}}
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('case'); args=parser.parse_args()
    print(json.dumps(analyze(args.case),indent=2,allow_nan=False))
