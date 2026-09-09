"""Continuum Fourier energy from the separable analytic potential, no FFT input."""
import math
import numpy as np
from scipy.special import ive
from tools.reference_energy import mean_energy


def spectrum(time=.05,sigma=.5,cutoff=32):
    if type(cutoff)!=int or cutoff<1:raise ValueError('positive integer cutoff')
    axis=np.arange(-cutoff,cutoff+1);k=np.stack(np.meshgrid(axis,axis,axis,indexing='ij'),axis=-1)
    factors=ive(np.abs(axis),1/sigma**2)
    psi2=math.exp(-2*time)*np.einsum('i,j,k->ijk',factors*factors,factors*factors,factors*factors)
    cross=np.cross(k,np.array([1.,2.,3.]));energy=.5*np.sum(cross*cross,axis=-1)*psi2
    shells=np.floor(np.linalg.norm(k,axis=-1)+.5).astype(int)
    values=np.bincount(shells.ravel(),weights=energy.ravel())
    total=mean_energy(time,sigma)
    return {'time':time,'sigma':sigma,'mode_cube_cutoff':cutoff,'shell_energy':values.tolist(),
            'truncated_energy':float(energy.sum()),'continuum_energy':total,
            'signed_energy_remainder_float':total-float(energy.sum()),
            'scope':'Analytic Fourier coefficients evaluated in floating point; remainder is not an interval-certified tail bound.'}
