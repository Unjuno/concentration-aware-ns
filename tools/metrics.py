"""Diagnostics for a verified uniform periodic grid; never an acceptance verdict.

Input layout: (nx, ny, nz, vector_component). Cell spacing must be uniform.
Adapters must explicitly verify ordering/geometry before using these functions.
"""
import numpy as np


def diagnostics(velocity, lengths=(2*np.pi,)*3):
    u = np.asarray(velocity, dtype=float)
    lengths = np.asarray(lengths, dtype=float)
    if u.ndim != 4 or u.shape[-1] != 3 or min(u.shape[:3]) < 4:
        raise ValueError('expected (nx,ny,nz,3), each spatial dimension >=4')
    if lengths.shape != (3,) or not np.isfinite(lengths).all() or np.any(lengths <= 0):
        raise ValueError('three finite positive domain lengths required')
    if not np.isfinite(u).all():
        raise ValueError('velocity contains nonfinite values')
    grad = np.stack([(np.roll(u,-1,axis=j)-np.roll(u,1,axis=j))/(2*lengths[j]/u.shape[j])
                     for j in range(3)],axis=-1)
    omega = np.stack((grad[...,2,1]-grad[...,1,2],
                      grad[...,0,2]-grad[...,2,0],
                      grad[...,1,0]-grad[...,0,1]),axis=-1)
    # Full FFT avoids half-spectrum multiplicity errors. Parseval normalization.
    modes = np.fft.fftn(u,axes=(0,1,2))/np.prod(u.shape[:3])
    modal_energy = 0.5*np.sum(np.abs(modes)**2,axis=-1)
    wave_axes = [2*np.pi*np.fft.fftfreq(u.shape[j],d=lengths[j]/u.shape[j]) for j in range(3)]
    waves = np.meshgrid(*wave_axes,indexing='ij')
    magnitude = np.sqrt(sum(w*w for w in waves))
    shell_width = float(min(2*np.pi/lengths))
    shell_index = np.floor(magnitude/shell_width+0.5).astype(int)
    spectrum = np.bincount(shell_index.ravel(),weights=modal_energy.ravel())
    grad_norm = np.linalg.norm(grad,axis=(-2,-1))
    omega_norm = np.linalg.norm(omega,axis=-1)
    return {
        'mean_kinetic_energy': float(0.5*np.mean(np.sum(u*u,axis=-1))),
        'max_gradient_fd2': float(grad_norm.max()),
        'max_vorticity_fd2': float(omega_norm.max()),
        'max_divergence_fd2': float(np.abs(np.trace(grad,axis1=-2,axis2=-1)).max()),
        'gradient_peak_index': list(map(int,np.unravel_index(grad_norm.argmax(),u.shape[:3]))),
        'vorticity_peak_index': list(map(int,np.unravel_index(omega_norm.argmax(),u.shape[:3]))),
        'shell_width': shell_width,
        'shell_energy': spectrum.tolist(),
        'spectrum_energy': float(spectrum.sum()),
        'method': 'periodic centered FD2; full FFT; uniform-grid samples only',
        'acceptance': 'NOT_EVALUATED',
    }
