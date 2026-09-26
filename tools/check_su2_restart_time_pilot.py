"""Replay archived same-variant continuation comparisons and time/residual checks."""
import csv,hashlib,io,json,math,tarfile
from pathlib import Path
import numpy as np
root=Path('evidence/su2-restart-time-pilot-v1')
p=json.loads(Path('protocols/su2-restart-time-pilot-v1.json').read_text())
rows=[];fields={}
runs=json.loads((root/'runs.json').read_text())
assert {(r['variant'],r['mode']) for r in runs}=={(v,m) for v in ['original','shifted'] for m in ['continuous','resumed']}
assert len(runs)==4
for run in runs:
 path=root/(run['variant']+'-'+run['mode']+'.tar.gz')
 assert hashlib.sha256(path.read_bytes()).hexdigest()==run['archive_sha256']
 with tarfile.open(path) as tar:
  assert tar.extractfile('exit_code').read().strip()==b'0'
  params=json.load(tar.extractfile('parameters.json'));assert all(params[k]==v for k,v in p.items())
  prefix=Path('evidence/su2-boundary-time-pilot-v1')/(run['variant']+'.tar.gz')
  assert hashlib.sha256(prefix.read_bytes()).hexdigest()==params['prefix_sha256']
  if run['mode']=='resumed':
   with tarfile.open(prefix) as pre:
    for k in [0,1]:
     name=f'restart_{k:05d}.csv';assert tar.extractfile(name).read()==pre.extractfile(name).read()
  name='history.csv' if run['mode']=='continuous' else 'history_00002.csv'
  history=[{k.strip().strip('"'):float(v) for k,v in row.items()} for row in csv.DictReader(io.StringIO(tar.extractfile(name).read().decode()))]
  expected=[0,.1,.2,.3] if run['mode']=='continuous' else [.2,.3]
  assert len(history)==len(expected)
  time_matches=all(abs(r['Cur_Time']-t)<1e-12 for r,t in zip(history,expected))
  residuals=[r[k] for r in history for k in ['rms[P]','rms[U]','rms[V]','rms[W]']]
  assert all(math.isfinite(x) and x<p['log10_residual_threshold'] for x in residuals)
  rows.append({'variant':run['variant'],'mode':run['mode'],'times':[r['Cur_Time'] for r in history],'worst_log10_residual':max(residuals),'expected_continuous_times':expected,'history_time_matches':time_matches})
  for k in [2,3]:fields[run['variant'],run['mode'],k]=np.genfromtxt(io.BytesIO(tar.extractfile(f'restart_{k:05d}.csv').read()),delimiter=',',names=True)
comparisons=[]
for variant in ['original','shifted']:
 for k in [2,3]:
  left,right=[fields[variant,mode,k] for mode in ['continuous','resumed']]
  assert np.array_equal(left['PointID'],right['PointID']) and len(left)==125
  errors={name:float(np.max(abs(left[name]-right[name]))) for name in ['Pressure','Velocity_x','Velocity_y','Velocity_z']}
  assert all(math.isfinite(v) and v<p['comparison_absolute_tolerance'] for v in errors.values())
  comparisons.append({'variant':variant,'saved_index':k,'max_differences':errors})
result={'success':all(r['history_time_matches'] for r in rows),'field_comparison_pass':True,'scope':p['scope'],'history':rows,'comparisons':comparisons}
(root/'replay-review.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))

raise SystemExit(0 if result["success"] else 1)
