"""Coordinate-level cone symmetry; not a reflected PDE construction."""
import json
from pathlib import Path
import sympy as s
a=s.symbols('a',positive=True)
b,p,q=s.symbols('b p q',real=True)
shear=a*(1+(b/a)**2)
projection=p+q*b/a
transverse=q-p*b/a
flip={b:-b,q:-q}
checks={
 'shear_even':s.simplify(shear.xreplace(flip)-shear)==0,
 'projection_preserved':s.simplify(projection.xreplace(flip)-projection)==0,
 'transverse_reversed':s.simplify(transverse.xreplace(flip)+transverse)==0,
}
P,J=s.symbols('P J',real=True)
bound=P+J**2/4-s.Abs(J)*s.sqrt((P-2)/2+J**2/16)
checks['bound_even']=s.simplify(bound.subs(J,-J)-bound)==0
assert all(checks.values())
examples=[]
for sign in (1,-1):
    values={a:s.Integer(1),b:s.Integer(2*sign),p:s.Integer(2),q:s.Integer(4*sign)}
    sh,pr,tr=[expr.subs(values) for expr in (shear,projection,transverse)]
    cb=bound.subs({P:pr,J:tr})
    assert 0<values[a] and 2<pr and 2<sh<cb
    examples.append({'a':str(values[a]),'b':str(values[b]),'p':str(values[p]),'q':str(values[q]),'shearSize':str(sh),'projection':str(pr),'transverse':str(tr),'coneBound':str(cb)})
result={'sympy':s.__version__,'checks':checks,'true_cone_coordinate_examples':examples,
 'scope':'Exact coordinate algebra from ActivationContinuation and ConeAlgebra. Does not realize either tuple as an actual profile or prove whole-assembly sign symmetry.',
 'actual_profile_pressure_gap_resolved':False}
Path('evidence/tests/cone-sign-symmetry.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
