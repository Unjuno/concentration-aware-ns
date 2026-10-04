"""Uniform MMS diagnostics from OpenFOAM ASCII fields; no acceptance assertion."""
import argparse
import hashlib
import json
import re
from pathlib import Path
import numpy as np
from tools.reference import fields
from tools.high_gradient_reference import fields as high_gradient_fields
from tools.forced_periodic_reference import fields as forced_periodic_fields
from tools.metrics import diagnostics
from tools.high_gradient_acceptance import local_quality, standard_acceptance


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


def scalars(path, count):
    text=Path(path).read_text()
    text=re.sub(r'/\*.*?\*/|//[^\n]*','',text,flags=re.S)
    if re.search(r'format\s+binary',text):
        raise ValueError('ASCII only')
    match=re.search(r'internalField\s+nonuniform\s+List<scalar>\s+(\d+)\s*\((.*?)\)\s*;',text,re.S)
    if not match or int(match[1]) != count:
        raise ValueError('expected matching nonuniform scalar field')
    values=np.fromstring(match[2],sep=' ')
    if values.size != count or not np.isfinite(values).all():
        raise ValueError('invalid scalar data')
    return values


def analyze(case, protocol=None):
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
    if profile == 'high-gradient':
        ref=high_gradient_fields(centers,N=params['frequency'],nu=params['nu'],time=t)
    elif profile == 'forced-periodic':
        ref=forced_periodic_fields(centers,time=t,nu=params['nu'])
    else:
        ref=fields(centers,t,sigma=params['sigma'],nu=params['nu'])
    def grid(v):
        return v.reshape(n,n,n,3).transpose(2,1,0,3)
    actual=diagnostics(grid(u)); sampled=diagnostics(grid(ref['u']))
    exact_g=float(np.linalg.norm(ref['grad_u'],axis=(-2,-1)).max())
    exact_w=float(np.linalg.norm(ref['vorticity'],axis=-1).max())
    continuum_peak_certified = profile == 'high-gradient' and params.get('frequency') == 4
    continuum_gradient_peak = float(np.sqrt(65) / 8 * np.exp(-t)) if continuum_peak_certified else None
    continuum_vorticity_peak = float(9 / 8 * np.exp(-t)) if continuum_peak_certified else None
    if profile == 'high-gradient':
        grad_fd2=np.stack([(np.roll(grid(u),-1,axis=j)-np.roll(grid(u),1,axis=j))/(4*np.pi/n)
                           for j in range(3)],axis=-1)
        selected_peak=float(np.abs(grad_fd2[...,1,0]).max())
        selected_reference_sample=float(np.abs(ref['grad_u'][:,1,0]).max())
        selected_reference_continuous=float(np.exp(-t))
    else:
        selected_peak=None
        selected_reference_sample=None
        selected_reference_continuous=None
    velocity_error=float(np.linalg.norm(u-ref['u'])/np.linalg.norm(ref['u']))
    energy_error=abs(actual['mean_kinetic_energy']-sampled['mean_kinetic_energy'])/max(sampled['mean_kinetic_energy'],1e-300)
    actual_spectrum=np.asarray(actual['shell_energy']); reference_spectrum=np.asarray(sampled['shell_energy'])
    bins=max(actual_spectrum.size,reference_spectrum.size)
    actual_spectrum=np.pad(actual_spectrum,(0,bins-actual_spectrum.size))
    reference_spectrum=np.pad(reference_spectrum,(0,bins-reference_spectrum.size))
    shell_spectrum_error=float(np.abs(actual_spectrum-reference_spectrum).sum()/max(reference_spectrum.sum(),1e-300))
    gradient_error=abs(actual['max_gradient_fd2']-exact_g)/exact_g
    vorticity_error=abs(actual['max_vorticity_fd2']-exact_w)/exact_w
    result={'parameters':params,'quality':'UNCERTAIN','standard_acceptance':'UNCERTAIN',
            'note':'Diagnostics only. Sampled reference peaks and certified N=4 continuum peaks are separate; acceptance denominators remain unchanged.',
            'velocity_relative_l2':velocity_error,
            'energy_relative_error_cell_samples':energy_error,
            'shell_spectrum_relative_l1_error':shell_spectrum_error,
            'gradient_peak_relative_error_cell_samples':gradient_error,
            'vorticity_peak_relative_error_cell_samples':vorticity_error,
            'reference_gradient_peak_cell_samples':exact_g,'reference_vorticity_peak_cell_samples':exact_w,
            'reference_continuum_peak_certified':continuum_peak_certified,
            'reference_gradient_peak_continuum_certified':continuum_gradient_peak,
            'reference_vorticity_peak_continuum_certified':continuum_vorticity_peak,
            'reference_gradient_peak_sampling_fraction_of_continuum':(
                exact_g / continuum_gradient_peak if continuum_peak_certified else None),
            'reference_vorticity_peak_sampling_fraction_of_continuum':(
                exact_w / continuum_vorticity_peak if continuum_peak_certified else None),
            'selected_gradient_component_fd2_peak':selected_peak,
            'selected_gradient_component_reference_sample_peak':selected_reference_sample,
            'selected_gradient_component_reference_continuous_peak':selected_reference_continuous,
            'continuous_full_gradient_peak_certified':False if selected_peak is not None else None,
            'computed':actual,'reference_sampled_fd2':sampled,
            'sha256':{str(p.relative_to(case)):hashlib.sha256(p.read_bytes()).hexdigest()
                      for p in [case/'parameters.json',case/'log.foamRun',time_dir/'U',time_dir/'C']}}
    if protocol is not None:
        thresholds=protocol['local_quality_relative_error_thresholds']
        quality=local_quality({
            'velocity_l2':velocity_error,
            'energy':energy_error,
            'max_gradient':gradient_error,
            'max_vorticity':vorticity_error,
            'shell_spectrum':shell_spectrum_error,
        },thresholds)
        standard=protocol['standard_acceptance']
        result['local_quality']=quality
        result['quality']=quality['status']
        result['standard_acceptance']=standard_acceptance(
            (case/'log.foamRun').read_text(),t,params['dt'],
            standard['outer_corrector_residual_absolute'],
            standard['maximum_outer_correctors'],
            (case/'system/fvSolution').read_text())
    if profile == 'forced-periodic':
        pressure=scalars(time_dir/'p',n**3)
        pressure_difference=pressure-ref['pressure']
        gauge_offset=float(np.mean(pressure_difference))
        result['pressure_gauge_offset_relative_to_reference']=gauge_offset
        result['pressure_relative_l2_gauge_invariant']=float(
            np.linalg.norm(pressure_difference-gauge_offset)/np.linalg.norm(ref['pressure']))
        result['sha256'][str((time_dir/'p').relative_to(case))]=hashlib.sha256(
            (time_dir/'p').read_bytes()).hexdigest()
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('case'); args=parser.parse_args()
    print(json.dumps(analyze(args.case),indent=2,allow_nan=False))
