"""Run the preregistered localized SU2 sweep sequentially and preserve evidence."""
import json
from pathlib import Path
import subprocess
import tarfile
import hashlib
from tools.su2_case import generate
from tools.analyze_su2 import analyze

p=json.loads(Path('protocols/su2-study-v1.json').read_text());root=Path('work/su2-study-v1');root.mkdir(exist_ok=False)
out=Path('evidence/su2-study-v1');out.mkdir(exist_ok=False)
image=p['image'];identity=subprocess.check_output(['docker','image','inspect',image,'--format','{{.Id}}'],text=True).strip()
cases=list(dict.fromkeys([(n,p['spatial_dt']) for n in p['spatial_n']]+[(p['temporal_n'],dt) for dt in p['temporal_dt']]))
rows=[]
for n,dt in cases:
    case=root/f'n{n}-dt{dt}';generate(case,n=n,dt=dt,end=p['end'],inner=p['inner_cap'])
    (case/'parameters.json').write_text(json.dumps({**p,'n':n,'dt':dt,'image_id':identity},indent=2)+'\n')
    cfg=case/'case.cfg';cfg.write_text(cfg.read_text().replace('OUTPUT_WRT_FREQ= 1',f'OUTPUT_WRT_FREQ= {round(p["end"]/dt)}').replace('(RESTART_ASCII, PARAVIEW_ASCII)','(RESTART_ASCII)'))
    cmd=['docker','run','--rm','--name',f'cans-su2-n{n}-dt{dt}','--user','501:20','-e','OMP_NUM_THREADS=2','-v',f'{case.resolve()}:/case',image,'SU2_CFD','case.cfg']
    (case/'command.json').write_text(json.dumps(cmd)+'\n');print('START',case.name,flush=True)
    with (case/'solver.log').open('w') as log:r=subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT)
    (case/'exit_code').write_text(str(r.returncode)+'\n')
    if r.returncode:raise RuntimeError(case)
    d=analyze(case);(case/'diagnostics.json').write_text(json.dumps(d,indent=2)+'\n')
    archive=out/(case.name+'.tar.gz')
    with tarfile.open(archive,'w:gz') as tar:
        for f in sorted(case.iterdir()):tar.add(f,arcname=f.name)
    rows.append({'case':case.name,'velocity_relative_l2':d['velocity_relative_l2'],'converged_steps':d['converged_steps'],'steps':d['steps'],'archive_sha256':hashlib.sha256(archive.read_bytes()).hexdigest()})
    (out/'summary.json').write_text(json.dumps({'expected_cases':len(cases),'completed_cases':len(rows),'quality':'UNCERTAIN','cases':rows},indent=2)+'\n')
    print('END',case.name,d['velocity_relative_l2'],flush=True)
