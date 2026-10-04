"""Reconstruction-independent H1 lower bound from prescribed native averages.

Let a=P_K e be the cell-constant projection of an H1 error e with the
prescribed cell means. Then <e,a-mean(a)>=||a-mean(a)||_2^2.
H1/H-1 duality bounds this by ||grad(e)||_2 ||a-mean(a)||_H-1.
Finite exact P0 coefficients plus its entire L2 tail bound the H-1 norm above.
All numerical formulas are floating evaluations, not interval certificates.
"""
import numpy as np

from tools.amr_p0_spectrum import fft_coefficients


def bound(transformed,mean_square,cutoff):
    transformed=np.asarray(transformed)
    if (transformed.ndim!=4 or transformed.shape[-1]!=3
            or len(set(transformed.shape[:3]))!=1 or not np.isfinite(transformed).all()):
        raise ValueError('finite cubic three-component FFT required')
    if (type(cutoff) is not int or not 1<=cutoff<=63
            or not np.isfinite(mean_square) or mean_square<0):
        raise ValueError('finite P0 norm and bounded positive cutoff required')
    axis=np.arange(-cutoff,cutoff+1)
    modes=np.stack(np.meshgrid(axis,axis,axis,indexing='ij'),axis=-1).reshape(-1,3)
    coefficients=fft_coefficients(transformed,modes)
    norms=np.sum(np.abs(coefficients)**2,axis=1);k2=np.sum(modes**2,axis=1);nz=k2>0
    mean_norm=float(norms[~nz].sum());inside=float(norms.sum())
    if mean_square-inside < -2e-12*max(mean_square,1e-300):
        raise ValueError('P0 band norm exceeds complete norm')
    outside=max(0.,mean_square-inside);centered=max(0.,mean_square-mean_norm)
    partial_hminus=float(np.sum(norms[nz]/k2[nz]))
    upper_hminus=partial_hminus+outside/(cutoff+1)**2
    lower=0. if centered==0 else centered/np.sqrt(upper_hminus)
    return {'cutoff_cube':cutoff,'mode_count':len(modes),'p0_mean_square':mean_square,
        'constant_mode_mean_square':mean_norm,'centered_p0_mean_square':centered,
        'inside_cube_mean_square':inside,'outside_cube_mean_square':outside,
        'minimum_outside_wavevector_square':(cutoff+1)**2,
        'partial_hminus_mean_square':partial_hminus,'upper_hminus_mean_square':upper_hminus,
        'gradient_mean_norm_lower':float(lower),
        'scope':'Any periodic H1 error with these exact native cell averages. Analytical lower-bound formula evaluated in floating point; no outward-rounded certificate.'}
