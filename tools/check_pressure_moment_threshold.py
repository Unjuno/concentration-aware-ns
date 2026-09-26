"""Exact pressure-moment algebra; no actual-profile moment estimate is asserted."""
import json
from pathlib import Path
import sympy as s
h, e, m0, m1, b = s.symbols('h eta M0 M1 amplitude', real=True)
A, D, d = s.Rational(1,2)+h, s.Rational(1,2)-h, 1-e**2
u = -D*e/d  # the root equation
p, dp = -m0/2, 2*e*m1/(1+e**2)
z = -A*(1-2*e*u)*u-d*dp+4*A*e*p
threshold = D/(2*d)*(1+2*D*e**2/d)
weighted = m0+d*m1/(A*(1+e**2))
assert s.cancel(z-(-2*A*e)*(weighted-threshold)) == 0
# An outgoing ideal prefix gives M0 >= 5*b^2/(1+eta^2)^2.
amplitude_threshold = s.factor(threshold*(1+e**2)**2/5)
assert s.cancel(5*amplitude_threshold/(1+e**2)**2-threshold) == 0
# Correlated jets with a constant shape exponent: exact algebra controls only.
point = {h:s.Rational(1,1000),e:-s.Rational(1,5000)}
controls=[]
for mass in (s.Rational(1,100),s.Rational(1,2)):
    value=s.factor(z.subs(point).subs({m0:mass,m1:mass}))
    controls.append({'M0':str(mass),'M1':str(mass),'Z':str(value)})
assert s.Rational(controls[0]['Z']) < 0 < s.Rational(controls[1]['Z'])
result={'sympy':s.__version__,'identity_checked':True,
 'identity':'Z = -2*A*eta*(M0 + d*M1/(A*(1+eta^2)) - T)',
 'T':str(s.factor(threshold)), 'sufficient_amplitude_squared_threshold':str(amplitude_threshold),
 'controls':controls,'actual_profile_bound_proved':False,
 'scope':'Exact algebra with the root equation and pressure moment formulas; integral differentiation and prefix inequalities rely on separately identified source results. Controls are not realized complete profiles.'}
Path('evidence/tests/pressure-moment-threshold.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
