"""Prepare, but do not enqueue, the preregistered startup intervention."""
import argparse,hashlib,json,re,shutil,tarfile
from pathlib import Path
import numpy as np
from tools.analyze_openfoam import vectors
parser=argparse.ArgumentParser();parser.add_argument('--protocol',default='protocols/of13-solenoidal-startup-control-v1.json');args=parser.parse_args()
spec_path=Path(args.protocol)
study=spec_path.stem
spec=json.loads(spec_path.read_text())
control=Path('evidence/of13-solenoidal-initial-control-v1.tar.gz')
review=json.loads(Path('evidence/tests/openfoam-solenoidal-initial-control.json').read_text())
with tarfile.open(control) as tar:raw=tar.extractfile('U').read()
assert hashlib.sha256(raw).hexdigest()==review['control_U_sha256']
root=Path('work')/study;root.mkdir(exist_ok=False)
rows=[]
for dt in spec['dt']:
 name=f'n64-dt{dt}';baseline=Path('work')/spec['baseline']/name;case=root/name;case.mkdir()
 inputs=[p for folder in ['0','system','constant'] for p in (baseline/folder).rglob('*') if p.is_file() and 'polyMesh' not in p.parts]
 for p in inputs:
  relative=p.relative_to(baseline);target=case/relative;target.parent.mkdir(parents=True,exist_ok=True)
  target.write_bytes(raw if str(relative)=='0/U' else p.read_bytes())
 assert not (case/'0/phi').exists()
 u=vectors(case/'0/U',64**3).reshape(64,64,64,3).transpose(2,1,0,3)
 div=sum((np.roll(u[...,j],-1,axis=j)-np.roll(u[...,j],1,axis=j))/(4*np.pi/64) for j in range(3))
 assert np.max(abs(div))<1e-12
 # Verify boundary dictionary is untouched, beyond numerical checks of internal field.
 old=(baseline/'0/U').read_text();new=(case/'0/U').read_text()
 assert old.split('boundaryField',1)[1]==new.split('boundaryField',1)[1]
 hashes={str(p.relative_to(case)):hashlib.sha256(p.read_bytes()).hexdigest() for p in case.rglob('*') if p.is_file()}
 differing=[str(p.relative_to(baseline)) for p in inputs if (case/p.relative_to(baseline)).read_bytes()!=p.read_bytes()]
 assert differing==['0/U']
 params=json.loads((baseline/'parameters.json').read_text());params['purpose']=spec['scope']
 (case/'parameters.json').write_text(json.dumps(params,indent=2)+'\n')
 row={'case':name,'baseline':str(baseline),'changed_input_files':differing,'input_hashes':hashes,'discrete_divergence_max':float(np.max(abs(div))),'solver_executed':False}
 (case/'input-review.json').write_text(json.dumps(row,indent=2)+'\n');rows.append(row)
result={'protocol_sha256':hashlib.sha256(spec_path.read_bytes()).hexdigest(),'cases':rows,'status':'prepared only; no Docker request issued','scope':spec['scope']}
(Path('evidence/tests')/('openfoam-solenoidal-case-preparation.json' if study=='of13-solenoidal-startup-control-v1' else study+'-preparation.json')).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':result['status'],'cases':[{'case':r['case'],'changed_input_files':r['changed_input_files'],'discrete_divergence_max':r['discrete_divergence_max']} for r in rows]},indent=2))
