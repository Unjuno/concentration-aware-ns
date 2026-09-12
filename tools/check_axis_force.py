"""Algebra checks for the hand-derived axial force; not a Lean proof."""
import json
from pathlib import Path
import sympy as s

x,y,z,t=s.symbols('x y z t',real=True)
r=s.symbols('r',real=True)
H=s.Function('H')
radial=(x*x+y*y)/2
uz=(H(t,r,z)+r*s.diff(H(t,r,z),r)).subs(r,radial)
lap=s.simplify(sum(s.diff(uz,v,2) for v in (x,y,z)).subs({x:0,y:0}))
expected=s.diff(H(t,0,z),z,2)+4*s.Subs(s.diff(H(t,r,z),r),r,0)
assert s.simplify(lap-expected)==0

h,e,j,P,Pprime=s.symbols('h eta j P Pprime',real=True)
A=s.Rational(1,2)+h;D=s.Rational(1,2)-h
d=1-e**2;L=1-2*h*e**2;U=4*e+j
transport=D*e+d*U
Z=-A*(1-2*e*U)*U-4*transport-d*Pprime+4*A*e*P
axial_rhs=A*(1-2*e*U)*U+4*transport+d*Pprime-4*A*e*P
assert s.expand(axial_rhs+Z)==0

# Direct fixed-time z derivative: q_z=2 eta q^A/L, eta_z=d q^-D/L.
q=s.symbols('q',positive=True)
Hz=q**(-1)*(4*d-2*A*e*U)/L
Hzz=s.diff(Hz,q)*2*e*q**A/L+s.diff(Hz,e)*d*q**(-D)/L
coefficient=s.simplify(Hzz*q**(A+2*D))
assert q not in coefficient.free_symbols
assert s.simplify((A+1)-(A+2*D)-2*h)==0

# Independent Eulerian material derivative, rather than differentiating a
# presumed trajectory twice. The implicit chart tau=q-z²*q^(2h) gives
# q_t=-1/L and eta_t=D*eta/(q*L), with z held fixed.
axis_velocity=q**(-A)*U
qt=-1/L
etat=D*e/(q*L)
qz=2*e*q**A/L
etaz=d*q**(-D)/L
material=s.diff(axis_velocity,q)*(qt+axis_velocity*qz)+s.diff(axis_velocity,e)*(etat+axis_velocity*etaz)
expected_acceleration=A*U/d*q**(-A-1)
root_j=-D*e/d-4*e
acceleration_residual=s.simplify(s.expand_power_base((material-expected_acceleration).subs(j,root_j),force=True))
assert acceleration_residual==0

# Compare coefficients after substituting q=tau/d along the trajectory.
nu,Zstar,Lstar,Astar,Ustar,dstar=s.symbols('nu Zstar Lstar Astar Ustar dstar',positive=True)
B=-Zstar/(2*Lstar)
radial_force=2*nu*B*q**(-Astar-1)
material_acceleration=Astar*Ustar/dstar*q**(-Astar-1)
ratio=s.simplify(radial_force/material_acceleration)
assert ratio==-nu*Zstar*dstar/(Lstar*Astar*Ustar)
result={'scope':'Symbolic algebra and exponent checks only. Does not verify source hypothesis transfer, the tail theorem application, or physical applicability.','sympy':s.__version__,'cartesian_laplacian_axis_identity':True,'natural_axis_equation_equals_negative_Z':True,'eulerian_material_acceleration_matches_root_trajectory':True,'axis_acceleration':'A*U/d*q^(-A-1)','Hzz_q_exponent':'-A-2D','Hzz_coefficient':str(coefficient),'axial_Hzz_relative_decay_exponent':'2h','leading_signed_force_ratio':str(ratio)}
Path('evidence/tests/openai-axis-force-symbolic.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
