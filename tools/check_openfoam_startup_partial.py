"""Inventory completed early-time archives without treating missing cases as pass."""
import hashlib,json,tarfile,tempfile
from pathlib import Path
import numpy as np
from tools.analyze_openfoam import vectors
from tools.analyze_amr import values
from tools.reference import fields
root=Path('evidence/of13-startup-time-v1')
spec=json.loads(Path('protocols/of13-startup-time-v1.json').read_text())
rows=[]
for dt in spec['dt']:
 name=f'n64-dt{dt}';archive=root/(name+'.tar.gz')
 if not archive.exists():continue
 with tarfile.open(archive) as tar,tempfile.TemporaryDirectory() as folder:
  folder=Path(folder)
  def materialize(name):
   p=folder/name;p.parent.mkdir(parents=True,exist_ok=True)
   p.write_bytes(tar.extractfile(name).read());return p
  assert json.load(tar.extractfile('exit.json'))['exit_code']==0
  log=tar.extractfile('log.foamRun').read().decode();assert log.rstrip().endswith('End')
  centers=vectors(materialize('0.001/C'),64**3)
  initial=vectors(materialize('0/U'),64**3)
  times=sorted({float(m.name.split('/')[0]) for m in tar.getmembers() if m.name.endswith('/U') and float(m.name.split('/')[0])>0})
  assert len(times)==round(spec['end']/dt) and times[-1]==spec['end']
  steps=[]
  for time in times:
   prefix=format(time,'.12g');u=vectors(materialize(prefix+'/U'),64**3);p=values(materialize(prefix+'/p'),64**3)
   reference=fields(centers,time)['u']
   assert np.isfinite(p).all()
   steps.append({'time':time,'relative_reference_velocity_error':float(np.linalg.norm(u-reference)/np.linalg.norm(reference)),'relative_velocity_change_from_initial':float(np.linalg.norm(u-initial)/np.linalg.norm(initial)),'pressure_range':float(np.ptp(p)),'dt_times_pressure_range':float(dt*np.ptp(p))})
  rows.append({'case':name,'archive_sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),'steps':steps})
result={'completed_cases':len(rows),'expected_cases':len(spec['dt']),'cases':rows,'three_case_order_evaluated':False,'quality':'UNCERTAIN','scope':'Completed archives only; pressure range is gauge-independent and reference pressure is zero. Neither missing cases nor startup causation are inferred.'}
(root/'partial-step-diagnostics.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
