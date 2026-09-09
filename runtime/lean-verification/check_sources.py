"""Verify original Lean source bytes against their pinned downloaded archives."""
import hashlib
import json
from pathlib import Path
import tarfile
root=Path('work/lean-verification')
items=[('project',Path('work/downloads/navier-stokes-euler.tar.gz'),root/'source')]
items += [(r['name'],root/(r['name']+'.tar.gz'),root/'packages'/r['name']) for r in json.loads((root/'dependency-archives.json').read_text())]
rows=[]
for name,archive,target in items:
    count=0;digests=[]
    with tarfile.open(archive) as tar:
        for member in tar:
            if member.isfile() and member.name.endswith('.lean'):
                path=member.name.split('/',1)[1];raw=tar.extractfile(member).read()
                if (target/path).read_bytes()!=raw:raise ValueError(f'Changed Lean source: {name}/{path}')
                digests.append(path+':'+hashlib.sha256(raw).hexdigest());count+=1
    rows.append({'package':name,'unchanged_lean_files':count,'source_list_sha256':hashlib.sha256('\n'.join(sorted(digests)).encode()).hexdigest()})
print(json.dumps({'scope':'Source byte identity only; not type checking or proof verification.','packages':rows},indent=2))
