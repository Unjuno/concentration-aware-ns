"""Check the Bessel expression by independent one-dimensional quadrature."""
import json
import math
from scipy.integrate import quad
from tools.reference_energy import mean_energy
rows=[]
for sigma in (.25,.5,1.):
    b=1/sigma**2;t=.05
    z,ez=quad(lambda d:math.exp(2*b*(math.cos(d)-1)),-math.pi,math.pi,epsabs=1e-13,epsrel=1e-13)
    v,ev=quad(lambda d:math.sin(d)**2*math.exp(2*b*(math.cos(d)-1)),-math.pi,math.pi,epsabs=1e-13,epsrel=1e-13)
    direct=14*b*b*math.exp(-2*t)*(v/(2*math.pi))*(z/(2*math.pi))**2
    exact=mean_energy(t,sigma)
    if abs(direct-exact)>1e-12:raise ValueError('formula mismatch')
    rows.append({'sigma':sigma,'time':t,'bessel_value':exact,'quadrature_value':direct,'absolute_difference':abs(direct-exact),'quadrature_estimated_errors':[ez,ev]})
print(json.dumps({'scope':'Closed-form continuum integral; ordinary floating point, not interval-certified Bessel evaluation.','checks':rows},indent=2))
