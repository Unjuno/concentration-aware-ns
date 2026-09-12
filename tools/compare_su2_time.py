"""Compare archived endpoint velocity fields at fixed spatial resolution."""
import hashlib
import json
import math
from pathlib import Path
import tarfile
import numpy as np
from tools.compare_su2_spectral import vertex_grid


def compare():
    base=Path('evidence/su2-study-v1')
    summary=json.loads((base/'summary.json').read_text())
    entries={r['case']:r for r in summary['cases']}
    names=['n64-dt0.001','n64-dt0.0005','n64-dt0.00025']
    arrays=[]; records=[]; parameters=[]
    for name in names:
        entry=entries[name]; path=base/(name+'.tar.gz')
        digest=hashlib.sha256(path.read_bytes()).hexdigest()
        if digest!=entry['archive_sha256']: raise ValueError('hash mismatch')
        with tarfile.open(path) as archive:
            p=json.load(archive.extractfile('parameters.json'))
            steps=round(p['end']/p['dt'])
            if steps!=entry['steps'] or archive.extractfile('exit_code').read().strip()!=b'0':
                raise ValueError('incomplete run')
            data=np.genfromtxt(archive.extractfile(f'restart_{steps-1:05d}.csv'),delimiter=',',names=True)
        xyz=np.stack([data[k] for k in ('x','y','z')],axis=-1)
        u=np.stack([data['Velocity_'+k] for k in ('x','y','z')],axis=-1)
        xyz,u,mismatch=vertex_grid(xyz,u,p['n'])
        if mismatch!=0: raise ValueError('periodic mismatch')
        arrays.append(u); parameters.append(p)
        records.append(dict(case=name,archive_sha256=digest,converged_steps=entry['converged_steps'],steps=steps))
    for p in parameters[1:]:
        for key in ('n','end','sigma','nu'):
            if p[key]!=parameters[0][key]: raise ValueError('incompatible cases')
    if not all(parameters[i]['dt']==2*parameters[i+1]['dt'] for i in range(2)):
        raise ValueError('not a halving sequence')
    differences=[]
    for i in range(2):
        delta=arrays[i]-arrays[i+1]
        differences.append(dict(coarse=names[i],fine=names[i+1],rms_vector=float(np.sqrt(np.mean(np.sum(delta**2,axis=-1)))),max_vector=float(np.linalg.norm(delta,axis=-1).max()),relative_l2_to_finer=float(np.linalg.norm(delta)/np.linalg.norm(arrays[i+1]))))
    d0,d1=[r['rms_vector'] for r in differences]
    return dict(scope='Direct fixed-grid endpoint field differences; descriptive observed order only. Unconverged inner solves and absence of an asymptotic regime prevent a temporal error certificate.',cases=records,differences=differences,observed_order=math.log2(d0/d1) if d0>0 and d1>0 else None,temporal_error_certified=False)

if __name__=='__main__':
    result=compare()
    Path('evidence/tests/su2-time-comparison.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
