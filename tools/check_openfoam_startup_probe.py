"""Compare constructor-observed divergence against independent uniform flux sum."""
import json
from pathlib import Path
import numpy as np
from tools.analyze_openfoam import vectors
from tools.analyze_amr import values
spec=json.loads(Path('protocols/of13-startup-probe-v1.json').read_text())
rows=[]
for n in spec['grids']:
 case=Path(f'work/of13-startup-probe-v1/n{n}')
 assert json.loads((case/'exit.json').read_text())['exit_code']==0
 assert 'STARTUP_PROBE_COMPLETE_NO_TIME_ADVANCE' in (case/'log.probe').read_text()
 assert not any(p.is_dir() and p.name[0].isdigit() and p.name!='0' for p in case.iterdir())
 source=Path(f'work/of13-study-v1/n{n}-dt0.001')
 assert (case/'0/U').read_bytes()==(source/'0/U').read_bytes()
 u=vectors(case/'0/U',n**3).reshape(n,n,n,3).transpose(2,1,0,3)
 expected=sum((np.roll(u[...,j],-1,axis=j)-np.roll(u[...,j],1,axis=j))/(4*np.pi/n) for j in range(3))
 actual=values(case/'0/initialDiv',n**3).reshape(n,n,n).transpose(2,1,0)
 error=float(np.max(abs(actual-expected)))
 assert error < spec['absolute_comparison_tolerance']
 rows.append({'n':n,'max_actual_divergence':float(np.max(abs(actual))),'maximum_cellwise_difference':error,'tolerance_pass':True})
result={'cases':rows,'scope':'Actual solver-constructor output before time advancement agrees with independent arithmetic face-flux divergence; no temporal-error causation claim'}
Path('evidence/of13-startup-probe-v1/comparison.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
