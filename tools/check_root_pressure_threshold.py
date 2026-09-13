"""Exact local pressure-jet diagnostic, not a constructed-profile counterexample."""
import json
from pathlib import Path
import sympy as s

h, eta, j, p, dp = s.symbols('h eta j p dp', real=True)
A = s.Rational(1, 2) + h
D = s.Rational(1, 2) - h
d = 1 - eta**2
u = 4*eta + j
root = D*eta + d*u
z = -A*(1-2*eta*u)*u - 4*root - d*dp + 4*A*eta*p
threshold = (1-2*eta*u)*u/(4*eta) + d*dp/(4*A*eta)
assert s.cancel(z + 4*root - 4*A*eta*(p-threshold)) == 0
# Exact small-parameter root; a negative local pressure and negative local derivative.
h0, e0 = s.Rational(1, 1000), -s.Rational(1, 5000)
j0 = -D.subs(h,h0)*e0/(1-e0**2)-4*e0
values = {h:h0, eta:e0, j:j0, p:-s.Rational(1,1000000), dp:-s.Rational(1,1000000000)}
assert 0 < j0 <= s.Rational(1,1000)
assert -j0/4 < e0 < -j0/5
assert root.subs(values) == 0
z0 = s.factor(z.subs(values))
assert z0 < 0
result = {
 'scope': 'Exact local algebra only. The diagnostic pressure jet is not shown to arise from an outgoing, nominal, or actual profile.',
 'sympy': s.__version__,
 'root_identity': 'Z = 4*A*eta*(P-Pcrit) when H=0',
 'Pcrit': '(1-2*eta*U)*U/(4*eta) + d*Pprime/(4*A*eta)',
 'sign_equivalence_under_A_positive_eta_negative': 'Z>0 iff P<Pcrit',
 'weak_pressure_negativity_insufficient_for_local_sign': True,
 'diagnostic': {k:str(v) for k,v in {'h':h0,'eta':e0,'j':j0,'P':values[p],'Pprime':values[dp],'Z':z0,'Pcrit':s.factor(threshold.subs(values))}.items()},
 'upstream_counterexample': False,
}
Path('evidence/tests/root-pressure-threshold.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
