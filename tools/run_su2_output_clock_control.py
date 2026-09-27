"""Run output-only intervention with archived original inputs and history states."""
import csv,hashlib,io,json,subprocess,tarfile
from pathlib import Path
import numpy as np
p=json.loads(Path('protocols/su2-output-clock-control-v1.json').read_text())
root=Path('work/su2-output-clock-control-v1');root.mkdir(exist_ok=False)
out=Path('evidence/su2-output-clock-control-v1');out.mkdir(exist_ok=False)
identity=subprocess.check_output(['docker','image','inspect',p['image'],'--format','{{.Id}}'],text=True).strip()
rows=[]
for mode in ['continuous','resumed']:
 case=root/mode;case.mkdir()
 baseline=Path('evidence/su2-restart-time-pilot-v1')/f'original-{mode}.tar.gz'
 with tarfile.open(baseline) as tar:
  names=['case.cfg','mesh.su2']+(['restart_00000.csv','restart_00001.csv'] if mode=='resumed' else [])
  for name in names:(case/name).write_bytes(tar.extractfile(name).read())
 command=['docker','run','--rm','--network','none','--cpus=2','--memory=4g','--user','501:20','-e','OMP_NUM_THREADS=2','-v',f'{case.resolve()}:/case',p['image'],'SU2_CFD','case.cfg']
 (case/'command.json').write_text(json.dumps(command)+'\n')
 (case/'parameters.json').write_text(json.dumps({**p,'mode':mode,'image_id':identity,'baseline_sha256':hashlib.sha256(baseline.read_bytes()).hexdigest()},indent=2)+'\n')
 with (case/'solver.log').open('w') as f:run=subprocess.run(command,stdout=f,stderr=subprocess.STDOUT)
 (case/'exit_code').write_text(str(run.returncode)+'\n')
 archive=out/f'{mode}.tar.gz'
 with tarfile.open(archive,'w:gz') as tar:
  for f in sorted(case.iterdir()):tar.add(f,arcname=f.name)
 assert run.returncode==0
 historyfile='history.csv' if mode=='continuous' else 'history_00002.csv'
 with (case/historyfile).open() as f:history=[{k.strip().strip('"'):float(v) for k,v in row.items()} for row in csv.DictReader(f)]
 indices=list(range(4)) if mode=='continuous' else [2,3]
 assert len(history)==len(indices)
 assert all(abs(row['Cur_Time']-.1*k)<1e-12 for row,k in zip(history,indices))
 assert all(row[key]<-10 for row in history for key in ['rms[P]','rms[U]','rms[V]','rms[W]'])
 differences=[]
 with tarfile.open(baseline) as tar:
  for k in indices:
   name=f'restart_{k:05d}.csv';a=np.genfromtxt(io.BytesIO(tar.extractfile(name).read()),delimiter=',',names=True);b=np.genfromtxt(case/name,delimiter=',',names=True)
   assert np.array_equal(a['PointID'],b['PointID'])
   error=max(float(np.max(abs(a[field]-b[field]))) for field in ['Pressure','Velocity_x','Velocity_y','Velocity_z'])
   assert np.isfinite(error) and error<p['comparison_absolute_tolerance'];differences.append(error)
 rows.append({'mode':mode,'exit_code':0,'times':[r['Cur_Time'] for r in history],'same_mode_field_max_difference':max(differences),'archive_sha256':hashlib.sha256(archive.read_bytes()).hexdigest()})
 (out/'summary.json').write_text(json.dumps({'scope':p['scope'],'image_id':identity,'cases':rows},indent=2)+'\n')
 print(rows[-1],flush=True)
