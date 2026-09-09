"""Fetch manifest-pinned dependency archives without creating Git repositories."""
import hashlib
import json
from pathlib import Path
import subprocess
import tarfile
root=Path('work/lean-verification');manifest=json.loads(Path('work/openai-inspection/lake-manifest.json').read_text())
packages=root/'packages';packages.mkdir(exist_ok=True);rows=[]
for package in manifest['packages']:
    name=package['name'];revision=package['rev'];url=package['url'].removesuffix('.git')
    if not url.startswith('https://github.com/'):raise ValueError(url)
    archive=root/(name+'.tar.gz');target=packages/name
    if target.exists():raise ValueError(f'Existing dependency; inspect before reuse: {target}')
    address='https://codeload.github.com/'+url.removeprefix('https://github.com/')+'/tar.gz/'+revision
    subprocess.run(['curl','-fL','--retry','3','--silent','--show-error',address,'-o',str(archive)],check=True)
    target.mkdir()
    with tarfile.open(archive) as tar:
        for member in tar.getmembers():
            parts=member.name.split('/',1)
            if len(parts)==2 and parts[1]:
                member.name=parts[1];tar.extract(member,target,filter='data')
    rows.append({'name':name,'revision':revision,'url':address,'sha256':hashlib.sha256(archive.read_bytes()).hexdigest()})
    (root/'dependency-archives.json').write_text(json.dumps(rows,indent=2)+'\n')
    print(name,revision,flush=True)
