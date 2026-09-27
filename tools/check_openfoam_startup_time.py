"""Early-time field comparison, without attributing its cause."""
import hashlib,json
from pathlib import Path
import numpy as np
from tools.analyze_openfoam import vectors
from tools.analyze_amr import values
from tools.reference import fields
from tools.compare_openfoam_iteration_sensitivity import alignment,completed_times
spec=json.loads(Path('protocols/of13-startup-time-v1.json').read_text())
root=Path('work/of13-startup-time-v1');rows=[];us=[];common_centers=None
for dt in spec['dt']:
 name=f'n64-dt{dt}';case=root/name;source=Path('work/of13-iteration-sensitivity-v1')/name
 assert json.loads((case/'exit.json').read_text())['exit_code']==0
 log=(case/'log.foamRun').read_text();times=completed_times(log)
 assert log.rstrip().endswith('End') and len(times)==round(spec['end']/dt) and times[-1]==spec['end']
 assert log.count('PIMPLE: Converged in')==len(times)
 assert (case/'0/U').read_bytes()==(source/'0/U').read_bytes()
 assert (case/'system/fvSolution').read_bytes()==(source/'system/fvSolution').read_bytes()
 u=vectors(case/'0.001/U',64**3);centers=vectors(case/'0.001/C',64**3)
 if common_centers is not None:assert np.array_equal(common_centers,centers)
 common_centers=centers;us.append(u)
 reference=fields(centers,.001)['u'];initial=vectors(case/'0/U',64**3)
 pressure=values(case/'0.001/p',64**3)
 assert np.isfinite(pressure).all()
 rows.append({'case':name,'velocity_relative_reference_error':float(np.linalg.norm(u-reference)/np.linalg.norm(reference)),'relative_change_from_initial':float(np.linalg.norm(u-initial)/np.linalg.norm(initial)),'pressure_range':float(np.ptp(pressure)),'endpoint_U_sha256':hashlib.sha256((case/'0.001/U').read_bytes()).hexdigest()})
result={'cases':rows,'temporal_differences':alignment(us),'scope':'Common early endpoint t=0.001, original initial U, tightened iteration settings; finite triple is not proof of asymptotic order or startup causation','quality':'UNCERTAIN'}
Path('evidence/of13-startup-time-v1/comparison.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
