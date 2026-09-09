"""Execute frozen sampling matrix; archive each completed independent training run."""
import json
import hashlib
from pathlib import Path
import subprocess
import sys
import tarfile
p=json.loads(Path('protocols/physicsnemo-study-v1.json').read_text())
root=Path('work/physicsnemo-study-v1');root.mkdir(exist_ok=False)
out=Path('evidence/physicsnemo-study-v1');out.mkdir(exist_ok=False);rows=[]
for n,nt in p['cases']:
    name=f'n{n}-nt{nt}';case=root/name;cfg=root/(name+'.json')
    cfg.write_text(json.dumps({**p['base'],'n':n,'time_nodes':nt},indent=2)+'\n')
    cmd=[sys.executable,'-m','tools.train_physicsnemo_pilot','--protocol',str(cfg),'--output',str(case)]
    print('START',name,flush=True)
    with (root/(name+'.log')).open('w') as log:r=subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT)
    if r.returncode:raise RuntimeError(f'{name}: exit {r.returncode}; log retained')
    (case/'console.log').write_bytes((root/(name+'.log')).read_bytes());(case/'command.json').write_text(json.dumps(cmd)+'\n')
    d=json.loads((case/'diagnostics.json').read_text())
    archive=out/(name+'.tar.gz')
    with tarfile.open(archive,'w:gz') as tar:
        for f in sorted(case.iterdir()):tar.add(f,arcname=f.name)
    rows.append({'case':name,'velocity_relative_l2':d['velocity_relative_l2'],'archive_sha256':hashlib.sha256(archive.read_bytes()).hexdigest()})
    (out/'summary.json').write_text(json.dumps({'expected_cases':5,'completed_cases':len(rows),'quality':'UNCERTAIN','cases':rows},indent=2)+'\n')
    print('END',name,d['velocity_relative_l2'],flush=True)
