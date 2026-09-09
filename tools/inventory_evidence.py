"""Inventory readable published archives; this does not verify scientific claims."""
import hashlib
import json
from pathlib import Path
import tarfile


def inventory(root=Path('evidence')):
    rows=[]
    for path in sorted(root.rglob('*.tar.gz')):
        with tarfile.open(path,'r:gz') as tar:
            members=tar.getmembers();names=[m.name for m in members]
            if len(names)!=len(set(names)):raise ValueError(f'duplicate archive names: {path}')
            diagnostic=None
            if 'diagnostics.json' in names:
                diagnostic=json.load(tar.extractfile('diagnostics.json'))
            exit_text=tar.extractfile('exit_code').read().decode().strip() if 'exit_code' in names else None
            if exit_text is None and 'exit.json' in names:
                exit_text=json.load(tar.extractfile('exit.json')).get('exit_code')
        rows.append({'archive':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                     'bytes':path.stat().st_size,'members':len(members),'has_diagnostics':diagnostic is not None,
                     'recorded_exit_code':exit_text,'reported_quality':diagnostic.get('quality') if isinstance(diagnostic,dict) else None})
    return {'scope':'Archive readability and identity inventory only; absent exit codes remain absent. No scientific acceptance or proof verification.',
            'archive_count':len(rows),'archives':rows}


if __name__=='__main__':print(json.dumps(inventory(),indent=2))
