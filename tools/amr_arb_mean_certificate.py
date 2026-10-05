"""Arb certificates for nominal native-mean constraints on a dyadic torus.

For a P0 voxel test field, alias classes have total Fourier mass |F_r|^2.
Every nonzero physical wavevector in class r has norm >= |wrap(r)|.
Thus sum_r!=0 |F_r|^2/|wrap(r)|^2 bounds its H^-1 norm above.
"""
import math
import numpy as np
from flint import arb,acb

from tools.analyze_amr_mean_quality import verify_cube_coverage


def endpoints(value):
    return {'lower_rational':str(value.lower().fmpq()),'upper_rational':str(value.upper().fmpq()),
            'ball':str(value),'display_lower':float(value.lower()),'display_upper':float(value.upper())}


def dft3(grid,progress=None):
    grid=np.asarray(grid,dtype=object).copy();m=grid.shape[0]
    if grid.shape!=(m,m,m) or m<2 or m>128 or m&(m-1):
        raise ValueError('bounded power-of-two cubic grid required')
    for axis in range(3):
        view=np.moveaxis(grid,axis,-1)
        for i in range(m):
            for j in range(m):view[i,j]=acb.dft(view[i,j])
        if progress:progress('dft_axis_'+str(axis))
    return grid


def voxel_bound(grid,progress=None):
    m=grid.shape[0]
    norm=sum((x*x for x in grid.flat),arb(0))/m**3
    mean=sum(grid.flat,arb(0))/m**3
    transformed=dft3(grid,progress)
    power=arb(0);upper=arb(0)
    axis=np.arange(m);axis[axis>=m//2]-=m
    for i in range(m):
        for j in range(m):
            for k in range(m):
                z=transformed[i,j,k];q=z.real*z.real+z.imag*z.imag
                power+=q
                k2=int(axis[i]**2+axis[j]**2+axis[k]**2)
                if k2:upper+=q/k2
    power/=m**6;upper/=m**6
    norm.intersection(power)
    mean.intersection(transformed[0,0,0].real/m**3)
    if not transformed[0,0,0].imag.contains(0):raise ValueError('constant Fourier mode not real')
    return norm,mean,upper


def average_tables(resolution,time,frequency):
    pi=arb.pi();width=2*pi/resolution;decay=(-arb(time)).exp()
    gx=[];dg=[];sx=[];cx=[]
    for j in range(resolution):
        center=pi*(2*j+1)/resolution
        g=arb(35);derivative=arb(0)
        for mode,amplitude in zip((1,2,3,4),(56,28,8,1)):
            q=mode*width/2;window=q.sin()/q
            g+=amplitude*(mode*center).cos()*window
            derivative-=amplitude*mode*(mode*center).sin()*window
        gx.append(g/128);dg.append(derivative/128)
        q=frequency*width/2;window=q.sin()/q
        sx.append(decay*(frequency*center).sin()*window/frequency**2)
        cx.append(-decay*(frequency*center).cos()*window/frequency)
    return gx,dg,sx,cx


def native_grids(centers,widths,values,n,time,frequency):
    m=2*n;unit=2*np.pi/m
    sizes=np.rint(widths/unit).astype(int)
    starts=np.rint((centers-widths[:,None]/2)/unit).astype(int)
    tables={s:average_tables(m//s,time,frequency) for s in (1,2)}
    for component in range(3):
        grid=np.empty((m,m,m),dtype=object)
        for size in (1,2):
            chosen=np.flatnonzero(sizes==size);base=starts[chosen]
            g,dg,sx,cx=tables[size];deltas=[]
            for cell in chosen:
                x,y,z=starts[cell]//size
                exact=(sx[x]*dg[y]*g[z] if component==0 else
                       cx[x]*g[y]*g[z] if component==1 else arb(0))
                deltas.append(arb(float(values[cell,component]))-exact)
            deltas=np.asarray(deltas,dtype=object)
            for dx in range(size):
                for dy in range(size):
                    for dz in range(size):
                        pos=base+np.array([dx,dy,dz]);grid[pos[:,0],pos[:,1],pos[:,2]]=deltas
        yield grid


def reference_bounds(time,frequency):
    decay=(-arb(time)).exp();norm=arb(0)
    for x in (-frequency,frequency):
        for y in range(-4,5):
            for z in range(-4,5):
                g=arb(math.comb(8,4+y)*math.comb(8,4+z))/256**2
                ux=(1 if x>0 else -1)*y*g/(2*frequency**2);uy=-g/(2*frequency)
                norm+=(x*x+y*y+z*z)*(ux*ux+uy*uy)
    norm*=decay**2
    # g=cos(q/2)^8 satisfies |g|<=1, |g'|<=1, |g''|<=2.
    # Frobenius gradient norm^2 splits into sin(Nx)^2 A+cos(Nx)^2 B.
    a=arb(1)+arb(5)/frequency**4;b=arb(3)/frequency**2
    bound=a if a>b else b
    curl=decay*(arb(1)+arb(4)/frequency**2+arb(5)/frequency**4).sqrt()
    return norm,decay*bound.sqrt(),curl


def certificate(centers,widths,values,n,time,frequency=3,progress=None):
    if (type(n) is not int or not 2<=n<=64 or n&(n-1)
            or type(frequency) is not int or frequency<1
            or values.shape!=centers.shape or not np.isfinite(values).all()):
        raise ValueError('bounded dyadic native data required')
    verify_cube_coverage(centers,widths,n)
    norm=arb(0);constant=arb(0);hminus=arb(0);records=[]
    for component,grid in enumerate(native_grids(centers,widths,values,n,time,frequency)):
        callback=(lambda stage:progress(str(component)+':'+stage)) if progress else None
        if progress:progress(str(component)+':input_balls')
        q,mean,h=voxel_bound(grid,callback);norm+=q;constant+=mean*mean;hminus+=h
        records.append({'component':component,'p0_norm':endpoints(q),'mean':endpoints(mean),'hminus_upper':endpoints(h)})
    centered=norm-constant
    if not centered>0 or not hminus>0:raise ValueError('positive centered error and H-1 upper required')
    lower=(centered.lower()/hminus.upper().sqrt()).lower()
    reference_norm,peak,curl_peak=reference_bounds(time,frequency)
    relative_l2=(lower/reference_norm.upper().sqrt()).lower()
    relative_peak=(lower/peak.upper()).lower()
    relative_curl_peak=(lower/curl_peak.upper()).lower()
    return {'components':records,'p0_norm':endpoints(norm),'constant_mode_norm':endpoints(constant),
        'centered_p0_norm':endpoints(centered),'hminus_upper':endpoints(hminus),
        'gradient_absolute_lower':endpoints(lower),'reference_gradient_mean_square':endpoints(reference_norm),
        'reference_curl_peak_upper':endpoints(curl_peak),'reference_gradient_peak_upper':endpoints(peak),'gradient_relative_l2_lower':endpoints(relative_l2),
        'gradient_relative_peak_error_lower':endpoints(relative_peak),
        'solenoidal_curl_relative_peak_error_lower':endpoints(relative_curl_peak),
        'strictly_above_five_percent_peak_error':bool(relative_peak>arb(1)/20),
        'solenoidal_curl_strictly_above_five_percent_peak_error':bool(relative_curl_peak>arb(1)/20)}
