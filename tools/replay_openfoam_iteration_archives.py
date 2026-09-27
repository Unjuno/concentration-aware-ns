"""Reconstruct the iteration comparison from published archives in a fresh directory."""
import hashlib,json,os,shutil,subprocess,sys,tarfile,tempfile
from pathlib import Path
repo=Path.cwd();name='of13-iteration-sensitivity-v1'
spec=json.loads((repo/f'protocols/{name}.json').read_text())
summary=json.loads((repo/f'evidence/{name}/summary.json').read_text())
assert len(summary['cases'])==3
hashes={r['case']:r['archive_sha256'] for r in summary['cases']}
with tempfile.TemporaryDirectory(prefix='cans-iteration-replay-') as tmp:
 root=Path(tmp);(root/'protocols').mkdir();shutil.copyfile(repo/f'protocols/{name}.json',root/f'protocols/{name}.json')
 (root/f'evidence/{name}').mkdir(parents=True)
 archives=[]
 for dt in spec['dt']:
  case=f'n64-dt{dt}'
  for study in [name,'of13-study-v1']:
   path=repo/f'evidence/{study}/{case}.tar.gz';digest=hashlib.sha256(path.read_bytes()).hexdigest()
   if study==name:assert digest==hashes[case]
   with tarfile.open(path) as tar:
    required=['0.05/U','0.05/C','log.foamRun']+(['exit.json'] if study==name else [])
    for member in required:
     target=root/f'work/{study}/{case}'/member;target.parent.mkdir(parents=True,exist_ok=True)
     target.write_bytes(tar.extractfile(member).read())
   archives.append({'archive':str(path.relative_to(repo)),'sha256':digest})
 env=dict(os.environ);env['PYTHONPATH']=str(repo)
 run=subprocess.run([sys.executable,'-m','tools.compare_openfoam_iteration_sensitivity'],cwd=root,env=env,capture_output=True,text=True)
 if run.returncode:raise RuntimeError(run.stdout+run.stderr)
 generated=json.loads((root/f'evidence/{name}/comparison.json').read_text())
 published=json.loads((repo/f'evidence/{name}/comparison.json').read_text())
 assert generated==published, 'Reconstructed report differs from published report'
result={'success':True,'published_comparison_reproduced':True,'archives':archives,'scope':'Fresh-directory replay using archived fields and the published comparison routine; no solver run or independent numerical algorithm validation'}
(repo/f'evidence/{name}/archive-replay.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'success':True,'archives':len(archives)}))
