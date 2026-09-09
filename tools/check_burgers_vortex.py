"""Independent symbolic substitution; no molecular or finite-energy claim."""
import json
import sympy as s

r,z,t=s.symbols('r z t', real=True)
nu,G=s.symbols('nu Gamma', positive=True)
a=s.Function('a')(t); q=s.Function('q')(t)
ur=-a*r/2; uz=a*z
v=G*(1-s.exp(-r*r/q))/(2*s.pi*r)
# Derivatives of the proposed pressure divided by density.
pr=(s.diff(a,t)/2-a*a/4)*r+v*v/r
pz=-(s.diff(a,t)+a*a)*z
res={
 'continuity':s.diff(r*ur,r)/r+s.diff(uz,z),
 'radial':s.diff(ur,t)+ur*s.diff(ur,r)-v*v/r+pr-nu*(s.diff(ur,r,2)+s.diff(ur,r)/r-ur/r**2),
 'axial':s.diff(uz,t)+uz*s.diff(uz,z)+pz-nu*s.diff(uz,z,2),
 'azimuthal':s.diff(v,t)+ur*s.diff(v,r)+ur*v/r-nu*(s.diff(v,r,2)+s.diff(v,r)/r-v/r**2),
 'vorticity':s.diff(r*v,r)/r-G*s.exp(-r*r/q)/(s.pi*q)}
res={k:s.simplify(x.subs(s.diff(q,t),4*nu-a*q)) for k,x in res.items()}
assert all(x==0 for x in res.values()),res
center=s.simplify(s.limit(v/r,r,0))
assert center==G/(2*s.pi*q)
print(json.dumps({'sympy_version':s.__version__,'residuals':{k:str(v) for k,v in res.items()},'axis_limit_u_theta_over_r':str(center),'assumptions':'nu>0, Gamma>0, q(t)>0, smooth a and q, qdot=4nu-aq; cylindrical expressions evaluated for r>0 with smooth axis extension','scope':'Algebraic consistency of specified continuum ansatz only; no proof of finite energy, self-generated strain, molecular alignment, or observability.'},indent=2))
