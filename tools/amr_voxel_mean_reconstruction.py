"""Smooth Fourier reconstruction of imposed finest-voxel averages.

Parent constants are imposed on children before reconstruction. This preserves
native cell averages but adds subcell constraints not supplied by the solver.
"""
import numpy as np

from tools.amr_p0_spectrum import reference_coefficients


def reconstruct(transformed):
    transformed=np.asarray(transformed,dtype=complex)
    m=transformed.shape[0]
    if (transformed.shape!=(m,m,m,3) or m<4 or m%2 or m**3>2**24
            or not np.isfinite(transformed).all()):
        raise ValueError('bounded even cubic three-component FFT required')
    axis=np.arange(-m//2,m//2+1)
    residues=axis%m
    coefficients=transformed[np.ix_(residues,residues,residues)]
    # At each Nyquist coordinate both signs give the same voxel averages.
    # Equal half weights select a real symmetric representative.
    weights=np.ones(m+1);weights[[0,-1]]=.5
    factor=weights*np.exp(-1j*np.pi*axis/m)/np.sinc(axis/m)
    coefficients*=factor[:,None,None,None]*factor[None,:,None,None]*factor[None,None,:,None]
    residual=float(np.max(np.abs(coefficients-coefficients[::-1,::-1,::-1].conj())))
    if residual>2e-12*max(1.,float(np.max(np.abs(coefficients)))):
        raise ValueError('real reconstruction conjugacy failed')
    return axis,coefficients,{'voxel_count_per_axis':m,'mode_count':(m+1)**3,
                             'maximum_conjugacy_residual':residual}


def recovered_voxel_averages(axis,coefficients):
    m=len(axis)-1
    if not np.array_equal(axis,np.arange(-m//2,m//2+1)):
        raise ValueError('complete symmetric even-grid mode axis required')
    factor=np.sinc(axis/m)*np.exp(1j*np.pi*axis/m)
    folded=coefficients*factor[:,None,None,None]*factor[None,:,None,None]*factor[None,None,:,None]
    for j in range(3):
        first=[slice(None)]*4;last=first.copy();first[j]=0;last[j]=-1
        folded[tuple(first)]+=folded[tuple(last)]
        cut=[slice(None)]*4;cut[j]=slice(0,m)
        folded=folded[tuple(cut)].copy()
    values=np.fft.ifftn(np.fft.ifftshift(folded,axes=(0,1,2)),axes=(0,1,2))*m**3
    return values.real,float(np.max(np.abs(values.imag)))


def cube_averages(axis,coefficients,centers,widths):
    """Independent tensor-product analytic integrals over selected native cubes."""
    centers=np.asarray(centers);widths=np.broadcast_to(widths,(len(centers),))
    result=[]
    for center,width in zip(centers,widths):
        factors=np.exp(1j*axis[:,None]*center[None,:])*np.sinc(axis[:,None]*width/(2*np.pi))
        result.append(np.einsum('i,j,k,ijkc->c',factors[:,0],factors[:,1],factors[:,2],coefficients,optimize=True))
    return np.asarray(result)


def reference_tensor(axis,frequency,time):
    if max(frequency,4)>=max(axis):
        raise ValueError('reference support must lie strictly below Nyquist')
    modes=np.array([(x,y,z) for x in (-frequency,frequency) for y in range(-4,5) for z in range(-4,5)])
    values=reference_coefficients(modes,frequency,time)
    result=np.zeros((len(axis),len(axis),len(axis),3),complex)
    indices=modes-axis[0]
    result[indices[:,0],indices[:,1],indices[:,2]]=values
    return result


def norm_metrics(axis,coefficients):
    k=[axis[:,None,None],axis[None,:,None],axis[None,None,:]]
    squared=np.sum(np.abs(coefficients)**2,axis=-1)
    velocity=float(squared.sum())
    gradient=float(np.sum((k[0]**2+k[1]**2+k[2]**2)*squared))
    curl=0.
    for j in range(3):
        a,b=(j+1)%3,(j+2)%3
        curl+=float(np.sum(np.abs(k[a]*coefficients[...,b]-k[b]*coefficients[...,a])**2))
    divergence=float(np.sum(np.abs(sum(k[j]*coefficients[...,j] for j in range(3)))**2))
    if abs(gradient-curl-divergence)>2e-12*max(gradient,1e-300):
        raise ValueError('independent curl/divergence identity failed')
    return {'velocity_mean_square':velocity,'gradient_mean_square':gradient,
            'curl_mean_square':curl,'divergence_mean_square':divergence,
            'gradient_curl_divergence_identity_residual':gradient-curl-divergence}


def errors(axis,coefficients,frequency,time):
    reference=reference_tensor(axis,frequency,time)
    norms=norm_metrics(axis,reference);error=norm_metrics(axis,coefficients-reference)
    return {'reference':norms,'error':error,
            'relative_l2':{kind:float(np.sqrt(error[kind+'_mean_square']/norms[kind+'_mean_square']))
                           for kind in ('velocity','gradient','curl')}}
