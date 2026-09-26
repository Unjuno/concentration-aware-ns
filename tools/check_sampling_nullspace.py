"""Exact smooth observation-nullspace control; not an upstream solver defect."""
import json
from math import lcm
from pathlib import Path
import sympy as s

resolutions=[16,32,64]
m=2*lcm(*resolutions)
x,y,z,nu=s.symbols('x y z nu',real=True)
a=s.Rational(1,m)
uvec=s.Matrix([0,a*s.sin(m*x),0])
coordinates=(x,y,z)
grad=uvec.jacobian(coordinates)
assert s.trace(grad)==0
assert grad*uvec==s.zeros(3,1)
force=nu*m*m*uvec
lap=uvec.applyfunc(lambda f:sum(s.diff(f,v,2) for v in coordinates))
assert s.simplify(nu*lap+force)==s.zeros(3,1)
for n in resolutions:
    for k in range(n):
        assert s.simplify(uvec.subs(x,2*s.pi*k/n))==s.zeros(3,1)
        assert s.simplify(uvec.subs(x,2*s.pi*(s.Rational(k)+s.Rational(1,2))/n))==s.zeros(3,1)
        assert s.integrate(uvec[1],(x,2*s.pi*k/n,2*s.pi*(k+1)/n))==0
energy=s.integrate(uvec.dot(uvec)/2,(x,0,2*s.pi))/(2*s.pi)
assert energy==s.Rational(1,4*m*m)
assert grad[1,0]==s.cos(m*x)
result={'scope':'Exact auxiliary stationary solution and observation identities. Not the current manufactured case, a numerical solver run, or a singular solution.',
 'resolutions':resolutions,'frequency':m,'velocity':'(0,sin(m*x)/m,0)',
 'pressure':0,'forcing':'(0,nu*m*sin(m*x),0)',
 'divergence_zero':True,'advection_zero':True,'steady_NS_balance':True,
 'nodal_samples_zero':True,'cell_center_samples_zero':True,'cell_averages_zero':True,
 'continuous_gradient_frobenius_max':1,'continuous_vorticity_max':1,
 'mean_kinetic_energy':str(energy),'sympy':s.__version__,
 'interpretation':'Finite samples and cell averages alone cannot upper-bound continuous derivative maxima without additional regularity, spectral or reconstruction assumptions. Force and initial data differ from the main benchmark.'}
Path('evidence/tests/sampling-nullspace.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
