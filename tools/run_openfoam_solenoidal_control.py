"""Execute prepared intervention after input validation and bounded Docker preflight."""
import argparse,hashlib,json,os,re,subprocess,tarfile
from pathlib import Path


def main():
 parser=argparse.ArgumentParser();parser.add_argument('--check-inputs-only',action='store_true');parser.add_argument('--protocol',default='protocols/of13-solenoidal-startup-control-v1.json');args=parser.parse_args()
 protocol=Path(args.protocol);spec=json.loads(protocol.read_text());study=protocol.stem
 prepared=json.loads((Path('evidence/tests')/('openfoam-solenoidal-case-preparation.json' if study=='of13-solenoidal-startup-control-v1' else study+'-preparation.json')).read_text())
 assert hashlib.sha256(protocol.read_bytes()).hexdigest()==prepared['protocol_sha256']
 root=(Path('work')/study).resolve()
 for row in prepared['cases']:
  case=root/row['case']
  for name,digest in row['input_hashes'].items():assert hashlib.sha256((case/name).read_bytes()).hexdigest()==digest
  assert not (case/'0/phi').exists()
  assert not (case/'command.json').exists(), 'Existing execution must be inspected, never overwritten'
 print('All three prepared solver input manifests match',flush=True)
 if args.check_inputs_only:return
 # Do not enqueue another run when Docker cannot answer a bounded read.
 subprocess.run(['docker','image','inspect',spec['image_id']],check=True,stdout=subprocess.DEVNULL,timeout=10)
 out=Path('evidence')/study;out.mkdir(exist_ok=False)
 results=[]
 for row in prepared['cases']:
  case=root/row['case']
  command=['docker','run','--rm','--network','none','--entrypoint','/bin/bash','-v',f'{case}:/case',spec['image_id'],'-c','useradd -o -u "$1" -m runner && su runner -s /bin/bash -c "source /opt/openfoam13/etc/bashrc && cd /case && blockMesh > log.blockMesh 2>&1 && foamRun > log.foamRun 2>&1 && foamPostProcess -func writeCellCentres -latestTime > log.centres 2>&1"','--',str(os.getuid())]
  if spec.get('retain_container',False):
   command[command.index('--rm'):command.index('--rm')+1]=['--cidfile',str(case/'container-id')]
  (case/'command.json').write_text(json.dumps(command)+'\n')
  print('START '+case.name,flush=True)
  with (case/'log.container').open('w') as log:run=subprocess.run(command,stdout=log,stderr=subprocess.STDOUT)
  (case/'exit.json').write_text(json.dumps({'exit_code':run.returncode})+'\n')
  log=(case/'log.foamRun').read_text() if (case/'log.foamRun').exists() else ''
  archive=out/(case.name+'.tar.gz')
  with tarfile.open(archive,'w:gz') as tar:
   for p in sorted(case.rglob('*')):
    if p.is_file() and not any(part in ['polyMesh','dynamicCode'] for part in p.relative_to(case).parts):tar.add(p,arcname=str(p.relative_to(case)))
  result={'case':case.name,'exit_code':run.returncode,'complete_log':log.rstrip().endswith('End'),'steps':len(re.findall(r'^Time = ',log,re.M)),'converged_steps':log.count('PIMPLE: Converged in'),'archive_sha256':hashlib.sha256(archive.read_bytes()).hexdigest()}
  results.append(result);(out/'runs.json').write_text(json.dumps(results,indent=2)+'\n');print(result,flush=True)
  if run.returncode or not result['complete_log']:raise RuntimeError('Failed execution preserved; inspect before proceeding')


if __name__=='__main__':main()
