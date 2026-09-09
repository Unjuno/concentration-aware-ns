"""Signed algebraic diagnostic decomposition, not causal error attribution."""
import hashlib
import json
import math
from pathlib import Path
import tarfile

rows = []
for group in ('of13-study-v1', 'su2-study-v1'):
    for path in sorted(Path('evidence', group).glob('*.tar.gz')):
        with tarfile.open(path) as tar:
            data = json.load(tar.extractfile('diagnostics.json'))
        p = data['parameters']; factor = math.exp(-p['end'])/p['sigma']**2
        metrics = {}
        for name, constant in [('gradient', math.sqrt(28)), ('vorticity', math.sqrt(56))]:
            exact = constant * factor
            ref = data['reference_sampled_fd2']['max_'+name+'_fd2']
            computed = data['computed']['max_'+name+'_fd2']
            bias = (exact-ref)/exact
            difference = (ref-computed)/exact
            total = (exact-computed)/exact
            assert abs(bias+difference-total) < 1e-14
            metrics[name] = {'global_reference_peak': exact, 'reference_fd2_peak': ref,
                             'computed_fd2_peak': computed,
                             'reference_sampling_and_fd2_signed_deficit': bias,
                             'difference_of_fd2_peaks_normalized_by_global_reference': difference,
                             'total_signed_deficit': total}
        rows.append({'group': group, 'case': path.name, 'archive_sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'metrics': metrics})
Path('evidence/tests/peak-diagnostic-decomposition.json').write_text(json.dumps({
    'scope': 'Exact algebraic decomposition of peak scalar discrepancies. Maxima may occur at different points; terms are not independent causal error components or field norm errors.',
    'cases': rows}, indent=2)+'\n')
