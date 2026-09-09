"""Execute the preregistered uniform-in-space MMS time-indexing control."""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import subprocess
import tarfile
import numpy as np
from tools.su2_case import generate

parser=argparse.ArgumentParser();parser.add_argument('--corrected',action='store_true');args=parser.parse_args()
suffix='-corrected' if args.corrected else ''
p=json.loads(Path('protocols/su2-time-control-v1.json').read_text())
root=Path('work/su2-time-control-v1'+suffix);root.mkdir(exist_ok=False)
out=Path('evidence/su2-time-control-v1'+suffix);out.mkdir(exist_ok=False)
image='concentration-aware-ns:su2-time-control'+suffix
identity=subprocess.check_output(['docker','image','inspect',image,'--format','{{.Id}}'],text=True).strip()
rows=[]
for dt in p['dt']:
    case=root/f'dt{dt}';generate(case,n=p['n'],dt=dt,end=p['end'],inner=p['inner_cap'])
    (case/'parameters.json').write_text(json.dumps({**p,'dt':dt,'image_id':identity},indent=2)+'\n')
    cmd=['docker','run','--rm','--user','501:20','-e','OMP_NUM_THREADS=2','-v',f'{case.resolve()}:/case',image,'SU2_CFD','case.cfg']
    (case/'command.json').write_text(json.dumps(cmd)+'\n')
    with (case/'solver.log').open('w') as log:proc=subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT)
    (case/'exit_code').write_text(str(proc.returncode)+'\n')
    if proc.returncode:raise RuntimeError(f'failed {case}')
    with (case/'history.csv').open() as f:
        reader=csv.DictReader(f);history=[{k.strip().strip('"'):float(v) for k,v in r.items()} for r in reader]
    steps=round(p['end']/dt)
    if len(history)!=steps:raise ValueError('history step count')
    per_step=[]
    for k in range(1,steps+1):
        data=np.genfromtxt(case/f'restart_{k-1:05d}.csv',delimiter=',',names=True)
        ux=data['Velocity_x'];old=1+dt**2*k*(k-1);new=1+dt**2*k*(k+1)
        per_step.append({'step':k,'reported_time':history[k-1]['Cur_Time'],'mean_ux':float(ux.mean()),'spatial_spread':float(np.ptp(ux)),
                         'max_error_previous_time_prediction':float(np.max(np.abs(ux-old))),
                         'max_error_next_time_prediction':float(np.max(np.abs(ux-new))),
                         'all_residuals_met':all(history[k-1][key]<-10 for key in ['rms[P]','rms[U]','rms[V]','rms[W]'])})
    result={'dt':dt,'steps':per_step,'matches_previous_time':all(r['max_error_previous_time_prediction']<p['comparison_absolute_tolerance'] for r in per_step),'matches_next_time':all(r['max_error_next_time_prediction']<p['comparison_absolute_tolerance'] for r in per_step)}
    (case/'diagnostics.json').write_text(json.dumps(result,indent=2)+'\n')
    archive=out/(case.name+'.tar.gz')
    with tarfile.open(archive,'w:gz') as tar:
        for f in sorted(case.iterdir()):tar.add(f,arcname=f.name)
    rows.append({**result,'archive_sha256':hashlib.sha256(archive.read_bytes()).hexdigest()})
    (out/'summary.json').write_text(json.dumps({'image_id':identity,'cases':rows},indent=2)+'\n')
    print(dt,result['matches_previous_time'],result['matches_next_time'],flush=True)
