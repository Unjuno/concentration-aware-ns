"""Compare same-image BDF2 continuation with a two-state restart."""
import csv,hashlib,json,shutil,subprocess,tarfile
from pathlib import Path
import numpy as np
from tools.su2_case import generate
p=json.loads(Path('protocols/su2-restart-time-pilot-v1.json').read_text())
root=Path('work/su2-restart-time-pilot-v1');root.mkdir(exist_ok=False)
out=Path('evidence/su2-restart-time-pilot-v1');out.mkdir(exist_ok=False)
results=[]
for variant,suffix in [('original',''),('shifted','-corrected')]:
 image='concentration-aware-ns:su2-time-control'+suffix
 identity=subprocess.check_output(['docker','image','inspect',image,'--format','{{.Id}}'],text=True).strip()
 prefix=Path('evidence/su2-boundary-time-pilot-v1')/(variant+'.tar.gz')
 prefixhash=hashlib.sha256(prefix.read_bytes()).hexdigest()
 for mode in ['continuous','resumed']:
  case=root/f'{variant}-{mode}';generate(case,n=p['n'],dt=p['dt'],end=p['end'],inner=p['inner_cap'])
  cfg=case/'case.cfg';cfg.write_text('\n'.join('MARKER_CUSTOM= (x0, x1, y0, y1, z0, z1)' if x.startswith('MARKER_PERIODIC=') else x.replace('DUAL_TIME_STEPPING-1ST_ORDER',p['scheme']) for x in cfg.read_text().splitlines())+'\n')
  if mode=='resumed':
   with tarfile.open(prefix) as tar:
    params=json.load(tar.extractfile('parameters.json'));assert params['image_id']==identity
    for k in [0,1]:
     name=f'restart_{k:05d}.csv';(case/name).write_bytes(tar.extractfile(name).read())
   with cfg.open('a') as f:f.write('RESTART_SOL= YES\nRESTART_ITER= 2\nREAD_BINARY_RESTART= NO\nSOLUTION_FILENAME= restart\n')
  (case/'parameters.json').write_text(json.dumps({**p,'variant':variant,'mode':mode,'image_id':identity,'prefix_sha256':prefixhash},indent=2)+'\n')
  cmd=['docker','run','--rm','--network','none','--cpus=2','--memory=4g','--user','501:20','-e','OMP_NUM_THREADS=2','-v',f'{case.resolve()}:/case',image,'SU2_CFD','case.cfg']
  (case/'command.json').write_text(json.dumps(cmd)+'\n')
  with (case/'solver.log').open('w') as f:run=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT)
  (case/'exit_code').write_text(str(run.returncode)+'\n')
  archive=out/f'{variant}-{mode}.tar.gz'
  with tarfile.open(archive,'w:gz') as tar:
   for f in sorted(case.iterdir()):tar.add(f,arcname=f.name)
  results.append({'variant':variant,'mode':mode,'exit_code':run.returncode,'archive_sha256':hashlib.sha256(archive.read_bytes()).hexdigest()})
  (out/'runs.json').write_text(json.dumps(results,indent=2)+'\n')
  print(variant,mode,run.returncode,flush=True)
  if run.returncode:raise SystemExit(run.returncode)
 comparisons=[]
 for k in [2,3]:
  left=np.genfromtxt(root/f'{variant}-continuous'/f'restart_{k:05d}.csv',delimiter=',',names=True)
  right=np.genfromtxt(root/f'{variant}-resumed'/f'restart_{k:05d}.csv',delimiter=',',names=True)
  assert np.array_equal(left['PointID'],right['PointID'])
  errors={name:float(np.max(abs(left[name]-right[name]))) for name in ['Pressure','Velocity_x','Velocity_y','Velocity_z']}
  comparisons.append({'saved_index':k,'max_differences':errors,'within_tolerance':all(np.isfinite(v) and v<p['comparison_absolute_tolerance'] for v in errors.values())})
 (out/f'{variant}-comparison.json').write_text(json.dumps({'scope':p['scope'],'comparisons':comparisons},indent=2)+'\n')
 print(variant,comparisons,flush=True)
