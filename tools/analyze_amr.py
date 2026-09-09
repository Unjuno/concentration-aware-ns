"""Nonuniform AMR diagnostics. No uniform FFT or cell-count equality assumption."""
import argparse,json,re
from pathlib import Path
import numpy as np
from tools.reference import fields
from tools.analyze_openfoam import vectors


def values(path,count,width=1):
    text=Path(path).read_text()
    m=re.search(r'internalField\s+nonuniform\s+List<\w+>\s+(\d+)\s*\((.*?)\)\s*;',text,re.S)
    if not m:
        uniform=re.search(r'internalField\s+uniform\s+(.*?)\s*;',text,re.S)
        if not uniform: raise ValueError('missing internal field')
        a=np.fromstring(uniform[1].replace('(',' ').replace(')',' '),sep=' ')
        if a.size!=width or not np.isfinite(a).all(): raise ValueError('invalid uniform field')
        return np.full(count,a[0]) if width==1 else np.tile(a,(count,1))
    if int(m[1])!=count: raise ValueError('nonuniform field count mismatch')
    a=np.fromstring(m[2].replace('(',' ').replace(')',' '),sep=' ')
    if a.size!=count*width or not np.isfinite(a).all(): raise ValueError('invalid field')
    return a.reshape(count,width).squeeze(axis=1) if width==1 else a.reshape(count,width)


def analyze(case):
    case=Path(case); params=json.loads((case/'parameters.json').read_text()); t=params['end']
    folder=next(p for p in case.iterdir() if p.is_dir() and re.fullmatch('[0-9.eE+-]+',p.name) and float(p.name)==t)
    if not (case/'log.foamRun').read_text().rstrip().endswith('End'): raise ValueError('incomplete run')
    text=(folder/'C').read_text(); count=int(re.search(r'List<vector>\s+(\d+)',text)[1])
    c=vectors(folder/'C',count); u=vectors(folder/'U',count); v=values(folder/'Vc',count)
    if np.any(v<=0) or not np.isclose(v.sum(),(2*np.pi)**3,rtol=1e-10): raise ValueError('invalid volume sum')
    g=values(folder/'grad(U)',count,9).reshape(-1,3,3)
    if (folder/'cellLevel').exists():
        levels=values(folder/'cellLevel',count); level_source='written cellLevel field'
    elif count==params['n']**3 and 'Refined from ' not in (case/'log.foamRun').read_text() and count>=params['amr']['maxCells']:
        levels=np.zeros(count); level_source='initial blockMesh count and no refinement events; budget disallows refinement'
    else:
        raise ValueError('cellLevel unavailable without a verified no-refinement history')
    ref=fields(c,t,sigma=params['sigma'],nu=params['nu'])
    error=float(np.sqrt(np.sum(v*np.sum((u-ref['u'])**2,axis=1))/np.sum(v*np.sum(ref['u']**2,axis=1))))
    norm=float(np.linalg.norm(g,axis=(1,2)).max())
    counts={str(int(level)):int(np.sum(levels==level)) for level in np.unique(levels)}
    return {'parameters':params,'cells':count,'level_counts':counts,'level_source':level_source,
            'cell_budget_reached_or_exceeded':bool(count>=params['amr']['maxCells']),
            'max_level_reached':bool(levels.max()>=params['amr']['maxRefinement']),
            'blocked_candidate_count':'UNOBSERVED', 'velocity_relative_volume_l2':error,
            'max_gradient_gauss':norm,'reference_max_gradient_cell_samples':float(np.linalg.norm(ref['grad_u'],axis=(1,2)).max()),
            'spectrum':'UNAVAILABLE: nonuniform mesh; no validated reconstruction',
            'quality':'UNCERTAIN','note':'AMR pilot; source sensor, interpolation and gradient reconstruction are distinct confounders.'}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('case');a=p.parse_args();print(json.dumps(analyze(a.case),indent=2))
