"""Run prebuilt constructor-only probe against copied baseline inputs."""
import json,os,shutil,subprocess,tarfile,hashlib
from pathlib import Path
root=Path('work/of13-startup-probe-v1').resolve()
out=Path('evidence/of13-startup-probe-v1');out.mkdir(exist_ok=False)
spec=json.loads(Path('protocols/of13-startup-probe-v1.json').read_text())
rows=[]
for n in spec['grids']:
 case=root/f'n{n}';case.mkdir(exist_ok=False)
 source=Path(f'work/of13-study-v1/n{n}-dt0.001')
 for folder in ['0','system']:
  shutil.copytree(source/folder,case/folder)
 (case/'constant').mkdir()
 for p in (source/'constant').iterdir():
  if p.is_file():shutil.copyfile(p,case/'constant'/p.name)
 assert not (case/'0/phi').exists()
 command=['docker','run','--rm','--network','none','--entrypoint','/bin/bash','-v',f'{root}:/probe',spec['image'],'-c','useradd -o -u "$1" -m runner && su runner -s /bin/bash -c "source /opt/openfoam13/etc/bashrc && cd /probe/n'+str(n)+' && blockMesh > log.blockMesh 2>&1 && /probe/startupProbe > log.probe 2>&1"','--',str(os.getuid())]
 (case/'command.json').write_text(json.dumps(command)+'\n')
 with (case/'log.container').open('w') as log:run=subprocess.run(command,stdout=log,stderr=subprocess.STDOUT)
 (case/'exit.json').write_text(json.dumps({'exit_code':run.returncode})+'\n')
 archive=out/f'n{n}.tar.gz'
 with tarfile.open(archive,'w:gz') as tar:
  for p in sorted(case.rglob('*')):
   if p.is_file():tar.add(p,arcname=str(p.relative_to(case)))
 assert run.returncode==0
 assert 'STARTUP_PROBE_COMPLETE_NO_TIME_ADVANCE' in (case/'log.probe').read_text()
 rows.append({'n':n,'exit_code':run.returncode,'archive_sha256':hashlib.sha256(archive.read_bytes()).hexdigest()})
 (out/'runs.json').write_text(json.dumps(rows,indent=2)+'\n')
 print(rows[-1],flush=True)
