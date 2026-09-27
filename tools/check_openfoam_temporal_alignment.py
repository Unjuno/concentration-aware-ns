"""Archived temporal error-direction diagnostic; no solver accuracy certificate."""
import hashlib
import json
from pathlib import Path
import numpy as np
from tools.analyze_openfoam import vectors
from tools.reference import fields

root = Path('work/of13-study-v1')
names = ['n64-dt0.001', 'n64-dt0.0005', 'n64-dt0.00025']
paths = [root / name / '0.05/U' for name in names]
u = [vectors(p, 64**3) for p in paths]
c = [vectors(root / name / '0.05/C', 64**3) for name in names]
assert all(np.array_equal(c[0], cc) for cc in c[1:])
assert all(np.isfinite(a).all() for a in u)
a, b = (u[0]-u[1]).ravel(), (u[1]-u[2]).ravel()
aa, bb, ab = float(a@a), float(b@b), float(a@b)
assert aa > 0 and bb > 0
scale = ab/bb
orth = a-scale*b
reference = fields(c[0], time=.05)['u'].ravel()
reference_sq = float(reference@reference)
projections = []
for difference in [a, b]:
    coefficient = float(difference@reference/reference_sq)
    residual = difference-coefficient*reference
    projections.append({'reference_amplitude_coefficient': coefficient,
                        'non_amplitude_norm_fraction': float(np.linalg.norm(residual)/np.linalg.norm(difference))})
result = {
    'cases': names,
    'input_sha256': {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},
    'reference_amplitude_projections': projections,
    'difference_cosine': ab/np.sqrt(aa*bb),
    'best_fit_coarse_to_fine_difference_scale': scale,
    'norm_ratio': np.sqrt(aa/bb),
    'observed_norm_order': float(np.log2(np.sqrt(aa/bb))),
    'orthogonal_fraction_of_coarse_difference': float(np.linalg.norm(orth)/np.sqrt(aa)),
    'first_order_defect_relative_to_coarse_difference': float(np.linalg.norm(a-2*b)/np.sqrt(aa)),
    'component_norms': [[float(np.linalg.norm((u[i]-u[i+1])[:,k])) for k in range(3)] for i in range(2)],
    'interpretation': 'For a single leading first-order temporal error vector, coarse difference approaches twice the fine difference. These post-hoc diagnostics test that consistency, not a bound or attribution to solver, iteration or spatial error.',
    'acceptance': 'UNCERTAIN'
}
Path('evidence/tests/openfoam-temporal-alignment.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps(result, indent=2))
