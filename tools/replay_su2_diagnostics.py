"""Recompute completed SU2 diagnostics from archived raw files with current code."""
import hashlib
import json
from pathlib import Path
import tarfile
import tempfile
import platform
import numpy as np
from tools.analyze_su2 import analyze


def replay():
    summary=json.loads(Path('evidence/su2-study-v1/summary.json').read_text())
    results=[]
    for entry in summary['cases']:
        path=Path('evidence/su2-study-v1')/(entry['case']+'.tar.gz')
        digest=hashlib.sha256(path.read_bytes()).hexdigest()
        if digest!=entry['archive_sha256']:raise ValueError('Archive hash mismatch')
        with tarfile.open(path) as archive, tempfile.TemporaryDirectory() as tmp:
            expected=json.load(archive.extractfile('diagnostics.json'))
            names=set(expected['sha256'])|{'parameters.json','exit_code'}
            for name in names:
                if Path(name).name!=name:raise ValueError('Unexpected nested path')
                member=archive.getmember(name)
                if not member.isfile():raise ValueError('Expected regular file')
                (Path(tmp)/name).write_bytes(archive.extractfile(member).read())
            actual=analyze(tmp)
            if actual!=expected:
                changed=[k for k in set(actual)|set(expected) if actual.get(k)!=expected.get(k)]
                raise ValueError(f'Diagnostic mismatch in {entry["case"]}: {changed}')
        results.append({'case':entry['case'],'archive_sha256':digest,
                        'recomputed_diagnostics_exact_match':True})
    return {'scope':'Current diagnostic implementation replayed from archived raw fields, history and parameters. Exact JSON-value equality in this environment; not an independent solver or derivative implementation.',
            'environment':{'python':platform.python_version(),'numpy':np.__version__,'platform':platform.platform()},
            'source_sha256':{name:hashlib.sha256(Path(name).read_bytes()).hexdigest() for name in ('tools/analyze_su2.py','tools/reference.py','tools/metrics.py')},
            'expected_cases':summary['expected_cases'],'replayed_cases':len(results),'cases':results}


if __name__=='__main__':
    result=replay()
    Path('evidence/su2-study-v1/diagnostic-replay.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
