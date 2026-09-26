"""Check follow-up-paper operators by implicit differentiation, not simulation."""
import json
from pathlib import Path
import sympy as s

q = s.symbols('q', positive=True)
h, e, X, b, r = s.symbols('h eta X b r', real=True)
D = s.Rational(1, 2)-h
A = s.Rational(1, 2)+h
d = 1-e**2
L = 1-2*h*e**2
# Physical coordinates t, z, squared cylindrical radius as functions of q,eta,X.
physical = s.Matrix([1-q*(1-e**2), e*q**D, 2*q*X])
jacobian = physical.jacobian([q,e,X])
time_rates = jacobian.inv()*s.Matrix([1,0,0])
axial_rates = jacobian.inv()*s.Matrix([0,1,0])
expected_time = s.Matrix([-1/L,D*e/(q*L),X/(q*L)])
expected_axial = s.Matrix([2*e*q**A/L,d*q**(-D)/L,-2*e*X*q**(-D)/L])
assert all(s.simplify(x)==0 for x in time_rates-expected_time)
assert all(s.simplify(x)==0 for x in axial_rates-expected_axial)
f=s.Function('f')(X,e)
field=q**b*f
partials=s.Matrix([s.diff(field,v) for v in (q,e,X)])
time_expected=q**(b-1)*(-b*f+D*e*s.diff(f,e)+X*s.diff(f,X))/L
axial_expected=q**(b-D)*(2*b*e*f+d*s.diff(f,e)-2*e*X*s.diff(f,X))/L
assert s.simplify(partials.dot(time_rates)-time_expected)==0
assert s.simplify(partials.dot(axial_rates)-axial_expected)==0
second_axial=s.Matrix([s.diff(axial_expected,v) for v in (q,e,X)]).dot(axial_rates)
normalized_second=s.simplify(second_axial/q**(b-2*D))
assert q not in normalized_second.free_symbols
# Cylindrical scalar radial Laplacian, with q and eta fixed under radial differentiation.
radial_field=field.subs(X,r**2/(2*q))
radial_laplacian=s.diff(radial_field,r,2)+s.diff(radial_field,r)/r
radial_expected=(2*q**(b-1)*(s.diff(f,X)+X*s.diff(f,X,2))).subs(X,r**2/(2*q))
assert s.simplify(radial_laplacian-radial_expected)==0
assert s.simplify((b-2*D)-(b-1)-2*h)==0
result={
 'scope':'Exact chain-rule and scalar radial-Laplacian checks. Not verification of the paper, its simulations, or the sign of our actual-profile force ratio.',
 'source':'https://arxiv.org/html/2609.17642v1',
 'source_equations':'(1), (3), and radial operator in (4b)',
 'sympy':s.__version__,
 'time_operator_matches':True,'axial_operator_matches':True,
 'scalar_radial_laplacian_matches':True,'second_axial_scaling_matches':True,
 'time_operator':'q^(b-1)/L * (-b*f + D*eta*f_eta + X*f_X)',
 'axial_operator':'q^(b-D)/L * (2*b*eta*f + d*f_eta - 2*eta*X*f_X)',
 'scalar_radial_laplacian':'2*q^(b-1)*(f_X + X*f_XX)',
 'axial_to_radial_power_difference':'2h',
 'domain':'q>0, L!=0; cylindrical computation r!=0 with axis limit only where smooth extension exists',
 'interpretation':'Positive h suppresses the axial power relative to the radial power for fixed bounded profile derivatives. It does not show vanishing total viscosity or a nonzero radial coefficient.'}
Path('evidence/tests/similarity-operators.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
