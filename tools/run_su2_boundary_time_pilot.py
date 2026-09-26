"""Run a bounded boundary time observation with both existing diagnostic images."""
import csv
import hashlib
import json
from pathlib import Path
import subprocess
import tarfile
import numpy as np
from tools.su2_case import generate
p=json.loads(Path('protocols/su2-boundary-time-pilot-v1.json').read_text())
root=Path('work/su2-boundary-time-pilot-v1');root.mkdir(exist_ok=False)
out=Path('evidence/su2-boundary-time-pilot-v1');out.mkdir(exist_ok=False)
rows=[]
for variant,suffix in [('original',''),('shifted','-corrected')]:
 case=root/variant;generate(case,n=p['n'],dt=p['dt'],end=p['end'],inner=p['inner_cap'])
 cfg=case/'case.cfg';lines=cfg.read_text().splitlines()
 cfg.write_text('\n'.join('MARKER_CUSTOM= (x0, x1, y0, y1, z0, z1)' if x.startswith('MARKER_PERIODIC=') else x.replace('DUAL_TIME_STEPPING-1ST_ORDER',p['scheme']) for x in lines)+'\n')
 image='concentration-aware-ns:su2-time-control'+suffix
 identity=subprocess.check_output(['docker','image','inspect',image,'--format','{{.Id}}'],text=True).strip()
 (case/'parameters.json').write_text(json.dumps({**p,'variant':variant,'image_id':identity},indent=2)+'\n')
 cmd=['docker','run','--rm','--network','none','--cpus=2','--memory=4g','--user','501:20','-e','OMP_NUM_THREADS=2','-v',f'{case.resolve()}:/case',image,'SU2_CFD','case.cfg']
 (case/'command.json').write_text(json.dumps(cmd)+'\n')
 with (case/'solver.log').open('w') as log:r=subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT)
 (case/'exit_code').write_text(str(r.returncode)+'\n')
 result={'variant':variant,'exit_code':r.returncode,'image_id':identity,'steps':[]}
 if r.returncode==0:
  with (case/'history.csv').open() as f:history=[{k.strip().strip('"'):float(v) for k,v in row.items()} for row in csv.DictReader(f)]
  for k in range(1,round(p['end']/p['dt'])+1):
   data=np.genfromtxt(case/f'restart_{k-1:05d}.csv',delimiter=',',names=True)
   boundary=np.zeros(len(data),dtype=bool)
   for name in ['x','y','z']:boundary |= np.isclose(data[name],0,atol=1e-12,rtol=0)|np.isclose(data[name],2*np.pi,atol=1e-12,rtol=0)
   assert boundary.sum()==(p['n']+1)**3-(p['n']-1)**3
   ux=data['Velocity_x'][boundary]
   result['steps'].append({'step':k,'boundary_nodes':int(boundary.sum()),'old_time_boundary_max_error':float(np.max(abs(ux-(1+((k-1)*p['dt'])**2)))),'target_time_boundary_max_error':float(np.max(abs(ux-(1+(k*p['dt'])**2)))),'reported_time':history[k-1]['Cur_Time'],'all_inner_residuals_met':all(history[k-1][key]<p['log10_residual_threshold'] for key in ['rms[P]','rms[U]','rms[V]','rms[W]'])})
 (case/'diagnostics.json').write_text(json.dumps(result,indent=2)+'\n')
 archive=out/f'{variant}.tar.gz'
 with tarfile.open(archive,'w:gz') as tar:
  for f in sorted(case.iterdir()):tar.add(f,arcname=f.name)
 rows.append({**result,'archive_sha256':hashlib.sha256(archive.read_bytes()).hexdigest()})
 (out/'summary.json').write_text(json.dumps({'scope':p['scope'],'cases':rows},indent=2)+'\n')
 print(json.dumps(result),flush=True)
 if r.returncode:raise SystemExit(r.returncode)
