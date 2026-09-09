"""Numerical attempt to falsify the analytic peak bound; not a proof."""
import json
import math
from pathlib import Path
import numpy as np
from tools.reference import fields

rng = np.random.default_rng(1909)
records = []
for sigma in (.05, .1, .25, .5, 1., 3.):
    # Cover both the torus and a sigma-scaled neighborhood of the peak.
    points = np.concatenate((rng.uniform(0,2*np.pi,(10000,3)),
                             (np.pi + sigma*rng.normal(size=(10000,3))) % (2*np.pi),
                             np.full((1,3),np.pi)))
    for time in (0., .05, 2.):
        ref = fields(points,time,sigma)
        grad = np.linalg.norm(ref['grad_u'],axis=(-2,-1))
        omega = np.linalg.norm(ref['vorticity'],axis=-1)
        factor = math.exp(-time)/sigma**2
        ratios = grad/(math.sqrt(28)*factor), omega/(math.sqrt(56)*factor)
        assert all(float(r.max()) <= 1+5e-13 for r in ratios)
        assert all(abs(float(r[-1])-1) <= 5e-13 for r in ratios)
        records.append({'sigma':sigma,'time':time,'points':len(points),
                        'largest_gradient_ratio':float(ratios[0].max()),
                        'largest_vorticity_ratio':float(ratios[1].max()),
                        'center_gradient_ratio':float(ratios[0][-1]),
                        'center_vorticity_ratio':float(ratios[1][-1])})
Path('evidence/tests/global-peak-formula-check.json').write_text(json.dumps({
    'seed':1909,'scope':'Finite-sample implementation consistency and counterexample search, including exact center; does not prove the global inequality.',
    'passed':True,'cases':records},indent=2)+'\n')
print('18 width/time combinations passed; no sampled violation found.')
