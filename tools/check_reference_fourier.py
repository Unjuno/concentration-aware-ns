"""Reproduce selected phase-corrected Fourier coefficient checks."""
import json
import numpy as np
from scipy.special import ive
from tools.reference import fields
n=64;t=.05;b=4.;axis=(np.arange(n)+.5)*2*np.pi/n
xyz=np.stack(np.meshgrid(axis,axis,axis,indexing='ij'),axis=-1)
f=np.fft.fftn(fields(xyz,t)['u'],axes=(0,1,2))/n**3
rows=[]
for ks in [(1,0,0),(1,2,3),(4,3,2)]:
    k=np.array(ks);psi=np.exp(-t)*np.prod(ive(abs(k),b))*(-1.)**sum(ks)
    coefficient=1j*np.cross(k,[1,2,3])*psi
    sampled=f[ks]*np.exp(-1j*np.sum(k)*np.pi/n)
    error=float(np.abs(sampled-coefficient).max())
    if error>=1e-12:raise ValueError((ks,error))
    rows.append({'mode':ks,'maximum_complex_coefficient_error':error})
print(json.dumps({'scope':'Sample FFT comparison at selected low modes; not an aliasing-free proof for arbitrary modes.','checks':rows},indent=2))
