"""Arb derivative witnesses for captured idealized barycentric affine pieces."""
import numpy as np
from flint import arb,arb_mat
from tools.amr_point_gradient_bound import exact_float
from tools.amr_arb_mean_certificate import endpoints,reference_bounds


def reference_gradient(position,time='0.05',frequency=3):
    x,y,z=position
    def envelope(q):
        c=(q/2).cos();s=(q/2).sin();c2=c*c;c4=c2*c2;c6=c4*c2;c8=c4*c4
        return c8,-4*c6*c*s,14*c6*s*s-2*c8
    g,dg,ddg=envelope(y);h,dh,_=envelope(z)
    sx=(frequency*x).sin();cx=(frequency*x).cos();decay=(-arb(time)).exp()
    return arb_mat([[decay*dg*h*cx/frequency,decay*ddg*h*sx/frequency**2,decay*dg*dh*sx/frequency**2],
                    [decay*g*h*sx,-decay*dg*h*cx/frequency,-decay*g*dh*cx/frequency],
                    [0,0,0]])


def affine_gradient(vertices,values):
    if np.asarray(vertices).shape!=(4,3) or np.asarray(values).shape!=(4,3):
        raise ValueError('four vector nodes required')
    p=[[exact_float(v) for v in row] for row in vertices]
    u=[[exact_float(v) for v in row] for row in values]
    a=arb_mat([[p[i][j]-p[0][j] for j in range(3)] for i in (1,2,3)])
    determinant=a.det()
    if determinant.contains(0):raise ValueError('nondegenerate enclosed tetrahedron required')
    d=arb_mat([[u[i][j]-u[0][j] for j in range(3)] for i in (1,2,3)])
    gradient=(a.inv()*d).transpose()
    centroid=[sum((row[j] for row in p),arb(0))/4 for j in range(3)]
    return gradient,centroid,determinant


def certificate(vertices,values,time='0.05',frequency=3):
    gradient,centroid,det=affine_gradient(vertices,values)
    error=gradient-reference_gradient(centroid,time,frequency)
    norm=sum((error[i,j]*error[i,j] for i in range(3) for j in range(3)),arb(0)).sqrt()
    curl=[error[2,1]-error[1,2],error[0,2]-error[2,0],error[1,0]-error[0,1]]
    curl_norm=sum((v*v for v in curl),arb(0)).sqrt()
    _,peak,curl_peak=reference_bounds(time,frequency)
    return {'vertices':np.asarray(vertices).tolist(),'nodal_values':np.asarray(values).tolist(),
            'centroid':[endpoints(v) for v in centroid],'determinant':endpoints(det),
            'affine_gradient':[[endpoints(gradient[i,j]) for j in range(3)] for i in range(3)],
            'gradient_error_norm':endpoints(norm),'curl_error_norm':endpoints(curl_norm),
            'reference_gradient_peak_upper':endpoints(peak),'reference_curl_peak_upper':endpoints(curl_peak),
            'gradient_relative_reference_peak_error_lower':endpoints((norm.lower()/peak.upper()).lower()),
            'curl_relative_reference_peak_error_lower':endpoints((curl_norm.lower()/curl_peak.upper()).lower())}
