"""Symbolic viscous stress and dissipation for the derived trajectory strain."""
import json
from pathlib import Path
import sympy as s

tau,C,nu,omega=s.symbols('tau C nu omega',positive=True)
G=s.Matrix([[-C/(2*tau),-omega,0],[omega,-C/(2*tau),0],[0,0,C/tau]])
S=(G+G.T)/2
stress=2*nu*S
dissipation=s.simplify(sum(stress[i,j]*G[i,j] for i in range(3) for j in range(3)))
assert s.simplify(dissipation-3*nu*C**2/tau**2)==0
assert s.trace(S)==0
out={'scope':'Conditional incompressible Newtonian dissipation per unit mass for the hand-derived trajectory Jacobian. Does not compute the viscous force nu*Laplacian(u) or its ratio to inertia.','sympy':s.__version__,'strain':str(S),'viscous_stress_per_unit_density':str(stress),'dissipation_per_unit_mass':str(dissipation),'rotation_cancels':omega not in dissipation.free_symbols}
Path('evidence/tests/openai-axis-dissipation.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
