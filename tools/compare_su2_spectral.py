"""Alternative derivative diagnostic of completed, archived SU2 vertex fields."""
import hashlib
import json
import math
from pathlib import Path
import platform
import tarfile

import numpy as np

from tools.reference import fields
from tools.spectral_derivative import gradient


def vertex_grid(xyz, velocity, n):
    """Check the full endpoint-inclusive lattice before removing duplicates."""
    xyz = np.asarray(xyz)
    velocity = np.asarray(velocity)
    if xyz.shape != ((n+1)**3, 3) or velocity.shape != xyz.shape:
        raise ValueError('incomplete endpoint-inclusive grid')
    if not np.isfinite(xyz).all() or not np.isfinite(velocity).all():
        raise ValueError('nonfinite grid or velocity')
    order = np.lexsort((xyz[:, 2], xyz[:, 1], xyz[:, 0]))
    axis = np.arange(n+1)*2*np.pi/n
    expected = np.stack(np.meshgrid(axis, axis, axis, indexing='ij'), axis=-1)
    if not np.allclose(xyz[order], expected.reshape(-1, 3), atol=1e-12, rtol=0):
        raise ValueError('coordinates do not match the complete vertex lattice')
    full = velocity[order].reshape(n+1, n+1, n+1, 3)
    grid = full[:n, :n, :n]
    periodic = np.arange(n+1) % n
    mismatch = float(np.max(np.abs(full-grid[np.ix_(periodic, periodic, periodic)])))
    return expected[:n, :n, :n], grid, mismatch


def curl(g):
    return np.stack((g[..., 2, 1]-g[..., 1, 2],
                     g[..., 0, 2]-g[..., 2, 0],
                     g[..., 1, 0]-g[..., 0, 1]), axis=-1)


def compare():
    summary = json.loads(Path('evidence/su2-study-v1/summary.json').read_text())
    rows = []
    for entry in summary['cases']:
        path = Path('evidence/su2-study-v1')/(entry['case']+'.tar.gz')
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest != entry['archive_sha256']:
            raise ValueError('archive hash mismatch')
        with tarfile.open(path) as archive:
            p = json.load(archive.extractfile('parameters.json'))
            if archive.extractfile('exit_code').read().strip() != b'0':
                raise ValueError('unsuccessful solver termination')
            if b'Exit Success (SU2_CFD)' not in archive.extractfile('solver.log').read():
                raise ValueError('missing solver success marker')
            steps = round(p['end']/p['dt'])
            if steps != entry['steps']:
                raise ValueError('step count mismatch')
            data = np.genfromtxt(archive.extractfile(f'restart_{steps-1:05d}.csv'),
                                 delimiter=',', names=True)
        xyz = np.stack([data[k] for k in ('x', 'y', 'z')], axis=-1)
        u = np.stack([data['Velocity_'+k] for k in ('x', 'y', 'z')], axis=-1)
        xyz, u, mismatch = vertex_grid(xyz, u, p['n'])
        t = steps*p['dt']
        ref = fields(xyz, t, p['sigma'], p['nu'])
        computed_g = gradient(u)
        reference_g = gradient(ref['u'])
        computed_w, reference_w = curl(computed_g), curl(reference_g)
        metrics = {}
        for name, actual, control, exact, axes, coefficient in (
            ('gradient', computed_g, reference_g, ref['grad_u'], (-2, -1), math.sqrt(28)),
            ('vorticity', computed_w, reference_w, ref['vorticity'], -1, math.sqrt(56)),
        ):
            peak = coefficient*math.exp(-t)/p['sigma']**2
            actual_peak = float(np.linalg.norm(actual, axis=axes).max())
            metrics[name] = {
                'computed_relative_l2_at_samples': float(np.linalg.norm(actual-exact)/np.linalg.norm(exact)),
                'reference_spectral_relative_l2_at_samples': float(np.linalg.norm(control-exact)/np.linalg.norm(exact)),
                'computed_spectral_peak_samples': actual_peak,
                'reference_spectral_peak_samples': float(np.linalg.norm(control, axis=axes).max()),
                'exact_global_reference_peak': peak,
                'computed_peak_signed_deficit': (peak-actual_peak)/peak,
            }
        rows.append({'case': entry['case'], 'archive_sha256': digest,
                     'n': p['n'], 'dt': p['dt'], 'updated_solution_time': t,
                     'periodic_duplicate_max_mismatch': mismatch,
                     'computed_max_abs_spectral_divergence': float(np.abs(np.trace(computed_g, axis1=-2, axis2=-1)).max()),
                     'reference_max_abs_spectral_divergence': float(np.abs(np.trace(reference_g, axis1=-2, axis2=-1)).max()),
                     'metrics': metrics})
    return {
        'scope': 'Real periodic trigonometric reconstruction differentiated at verified vertex samples, with the real Nyquist convention. No intersample peak certification or scientific verdict upgrade. Exact-reference control measures this diagnostic on the reference only.',
        'environment': {'python': platform.python_version(), 'numpy': np.__version__},
        'source_sha256': {name: hashlib.sha256(Path(name).read_bytes()).hexdigest() for name in ('tools/compare_su2_spectral.py', 'tools/spectral_derivative.py', 'tools/reference.py')},
        'expected_cases': summary['expected_cases'], 'completed_cases': len(rows), 'cases': rows,
    }


if __name__ == '__main__':
    result = compare()
    Path('evidence/tests/su2-spectral-gradient.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))
