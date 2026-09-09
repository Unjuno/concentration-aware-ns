"""Independent symbolic differentiation of the potential, not a solver test."""
import json
import numpy as np
import sympy as sp
from tools.reference import fields


def check():
    x,y,z,t=sp.symbols('x y z t',real=True)
    coords=[x,y,z]
    sigma=sp.Rational(1,2); nu=sp.Rational(1,100)
    psi=sp.exp(-t+sum(sp.cos(c-sp.pi)-1 for c in coords)/sigma**2)
    potential=sp.Matrix([psi,2*psi,3*psi])
    u=sp.Matrix([sp.diff(potential[2],y)-sp.diff(potential[1],z),
                 sp.diff(potential[0],z)-sp.diff(potential[2],x),
                 sp.diff(potential[1],x)-sp.diff(potential[0],y)])
    grad=u.jacobian(coords)
    force=sp.diff(u,t)+grad*u-nu*sum((sp.diff(u,c,2) for c in coords),sp.zeros(3,1))
    omega=sp.Matrix([grad[2,1]-grad[1,2],grad[0,2]-grad[2,0],grad[1,0]-grad[0,1]])
    expressions={'u':u,'grad_u':grad,'force':force,'vorticity':omega}
    functions={k:sp.lambdify((x,y,z,t),v,'numpy',cse=True) for k,v in expressions.items()}
    rng=np.random.default_rng(571)
    points=np.concatenate([rng.uniform(0,2*np.pi,(32,3)),np.pi+rng.uniform(-0.7,0.7,(32,3))])
    errors={k:0. for k in expressions}
    for point in points:
        time=float(rng.uniform(0,0.5)); ref=fields(point,time)
        for key,fn in functions.items():
            actual=np.asarray(fn(*point,time),dtype=float).reshape(ref[key].shape)
            errors[key]=max(errors[key],float(np.max(np.abs(actual-ref[key]))))
    result={'method':'symbolic curl, Jacobian, Laplacian and time derivative from vector potential',
            'sympy':sp.__version__,'numpy':np.__version__,'seed':571,'points':len(points),
            'sigma':float(sigma),'nu':float(nu),'max_absolute_errors':errors,
            'tolerance':1e-10,'passed':all(e<1e-10 for e in errors.values()),
            'limitations':'Fixed sigma and nu; not validation of C++ runtime source or arbitrary parameter values.'}
    print(json.dumps(result,indent=2,allow_nan=False))
    if not result['passed']:
        raise SystemExit(1)


if __name__=='__main__': check()
