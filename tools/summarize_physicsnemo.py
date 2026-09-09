"""Summarize only archived completed PINN cases; do not read an active training log."""
import json
from pathlib import Path
import tarfile
rows=[]
root=Path('evidence/physicsnemo-study-v1')
for archive in sorted(root.glob('*.tar.gz')):
    with tarfile.open(archive) as tar:
        if tar.extractfile('exit_code').read().strip()!=b'0':raise ValueError('incomplete archive')
        d=json.load(tar.extractfile('diagnostics.json'))
    gradient=root/(archive.name.removesuffix('.tar.gz')+'-gradient.json')
    g=json.loads(gradient.read_text()) if gradient.exists() else {}
    rows.append({'case':archive.name.removesuffix('.tar.gz'),'velocity_relative_l2':d['velocity_relative_l2'],
      'gradient_peak_error_autograd_samples':g.get('gradient_peak_relative_error_samples'),
      'vorticity_peak_error_autograd_samples':g.get('vorticity_peak_relative_error_samples'),
      'max_validation_momentum_residual':max(v for r in d['independent_validation'] for k,v in r['max_absolute_residuals'].items() if k.startswith('momentum')),
      'max_validation_continuity_residual':max(r['max_absolute_residuals']['continuity'] for r in d['independent_validation'])})
print(json.dumps({'quality':'UNCERTAIN','scope':'Completed fixed-budget paired-seed runs only; residuals nondimensional, no universal tolerance implied.','cases':rows},indent=2))
