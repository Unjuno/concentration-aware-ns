"""Compare archived shell spectra against continuum Fourier coefficients."""
import json
from pathlib import Path
import tarfile
import numpy as np
from tools.reference_spectrum import spectrum
rows=[];ref=spectrum();expected=np.array(ref['shell_energy'])
for group in ('of13-study-v1','physicsnemo-study-v1'):
    for archive in sorted((Path('evidence')/group).glob('*.tar.gz')):
        with tarfile.open(archive) as tar:
            d=json.load(tar.extractfile('diagnostics.json'))
            p=d.get('parameters') or json.load(tar.extractfile('parameters.json'))
        if p['end']!=ref['time'] or p['sigma']!=ref['sigma']:raise ValueError('reference mismatch')
        observed=np.array(d['computed']['shell_energy']);size=max(len(observed),len(expected))
        obs=np.pad(observed,(0,size-len(observed)));ex=np.pad(expected,(0,size-len(expected)))
        rows.append({'group':group,'case':archive.name,'normalized_shell_l1_difference':float(np.abs(obs-ex).sum()/ref['continuum_energy']),
                     'computed_mean_energy':d['computed']['mean_kinetic_energy']})
print(json.dumps({'reference':ref,'scope':'Numerical sample FFT versus continuum shells truncated to |k_i|<=32; combines solution, sampling and aliasing effects.','cases':rows},indent=2))
