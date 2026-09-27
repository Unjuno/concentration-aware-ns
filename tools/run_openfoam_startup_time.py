"""Short frozen startup trace from the completed tight-tolerance inputs."""
import hashlib,json,os,re,shutil,subprocess,tarfile
from pathlib import Path
spec_path=Path('protocols/of13-startup-time-v1.json')
spec=json.loads(spec_path.read_text())
root=Path('work/of13-startup-time-v1').resolve();root.mkdir(exist_ok=False)
out=Path('evidence/of13-startup-time-v1');out.mkdir(exist_ok=False)
rows=[]
for dt in spec['dt']:
 name=f'n64-dt{dt}';case=root/name;case.mkdir()
 source=Path('work/of13-iteration-sensitivity-v1')/name
 for folder in ['0','system']:shutil.copytree(source/folder,case/folder)
 (case/'constant').mkdir()
 for p in (source/'constant').iterdir():
  if p.is_file():shutil.copyfile(p,case/'constant'/p.name)
 assert not (case/'0/phi').exists()
 control=case/'system/controlDict';text=control.read_text()
 for key,value in [('endTime',spec['end']),('writeInterval',dt)]:
  text,count=re.subn(r'\b'+key+r'\s+[^;]+;',f'{key} {value};',text);assert count==1
 control.write_text(text)
 params=json.loads((source/'parameters.json').read_text());params['end']=spec['end']
 (case/'parameters.json').write_text(json.dumps(params,indent=2)+'\n')
 (case/'provenance.json').write_text(json.dumps({'protocol_sha256':hashlib.sha256(spec_path.read_bytes()).hexdigest(),'source':str(source),'image_id':spec['image_id'],'initial_U_sha256':hashlib.sha256((case/'0/U').read_bytes()).hexdigest(),'fvSolution_sha256':hashlib.sha256((case/'system/fvSolution').read_bytes()).hexdigest()},indent=2)+'\n')
 command=['docker','run','--rm','--network','none','--entrypoint','/bin/bash','-v',f'{case}:/case',spec['image_id'],'-c','useradd -o -u "$1" -m runner && su runner -s /bin/bash -c "source /opt/openfoam13/etc/bashrc && cd /case && blockMesh > log.blockMesh 2>&1 && foamRun > log.foamRun 2>&1 && foamPostProcess -func writeCellCentres -latestTime > log.centres 2>&1"','--',str(os.getuid())]
 (case/'command.json').write_text(json.dumps(command)+'\n')
 print('START '+name,flush=True)
 with (case/'log.container').open('w') as log:run=subprocess.run(command,stdout=log,stderr=subprocess.STDOUT)
 (case/'exit.json').write_text(json.dumps({'exit_code':run.returncode})+'\n')
 archive=out/(name+'.tar.gz')
 with tarfile.open(archive,'w:gz') as tar:
  for p in sorted(case.rglob('*')):
   if p.is_file() and not any(part in ['polyMesh','dynamicCode'] for part in p.relative_to(case).parts):tar.add(p,arcname=str(p.relative_to(case)))
 log=(case/'log.foamRun').read_text()
 row={'case':name,'exit_code':run.returncode,'steps':len(re.findall(r'^Time = ',log,re.M)),'converged_steps':log.count('PIMPLE: Converged in'),'complete_log':log.rstrip().endswith('End'),'archive_sha256':hashlib.sha256(archive.read_bytes()).hexdigest()}
 rows.append(row);(out/'runs.json').write_text(json.dumps(rows,indent=2)+'\n');print(row,flush=True)
 assert run.returncode==0 and row['complete_log']
 assert row['steps']==row['converged_steps']==round(spec['end']/dt)
