"""Compare completed uniform study fields at the same final time and grid."""
import json
from pathlib import Path
import numpy as np
from tools.analyze_openfoam import vectors


def compare(root=Path('work/of13-study-v1')):
    names=['n64-dt0.001','n64-dt0.0005','n64-dt0.00025']
    ds=[json.loads((root/name/'diagnostics.json').read_text()) for name in names]
    for name,d in zip(names,ds):
        if d['parameters']['n']!=64 or d['parameters']['end']!=.05:
            raise ValueError('grid/time mismatch')
        if not (root/name/'log.foamRun').read_text().rstrip().endswith('End'):
            raise ValueError('incomplete run')
    us=[vectors(root/name/'0.05/U',64**3) for name in names]
    cs=[vectors(root/name/'0.05/C',64**3) for name in names]
    if any(not np.array_equal(cs[0],c) for c in cs[1:]):
        raise ValueError('cell correspondence mismatch')
    differences=[float(np.linalg.norm(us[i]-us[i+1])/np.linalg.norm(us[-1])) for i in range(2)]
    return {'cases':names,'relative_field_differences_normalized_by_finest':differences,
            'observed_difference_order':float(np.log2(differences[0]/differences[1])),
            'velocity_errors':[d['velocity_relative_l2'] for d in ds],
            'input_sha256':[d['sha256'] for d in ds],
            'interpretation':'Small temporal field differences at this spatial grid; not a bound on temporal error or proof of asymptotic convergence.'}


if __name__=='__main__':
    print(json.dumps(compare(),indent=2))
