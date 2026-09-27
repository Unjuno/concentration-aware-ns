"""Measure the changed initial-value problem from complete archived runs only."""
import hashlib
import json
import tarfile
import tempfile
from pathlib import Path

import numpy as np

from tools.analyze_amr import values
from tools.analyze_openfoam import vectors
from tools.compare_openfoam_iteration_sensitivity import completed_times


def main():
    protocol = Path('protocols/of13-solenoidal-startup-control-v1.json')
    spec = json.loads(protocol.read_text())
    manifest = json.loads(Path('evidence/tests/openfoam-solenoidal-case-preparation.json').read_text())
    assert hashlib.sha256(protocol.read_bytes()).hexdigest() == manifest['protocol_sha256']
    root = Path('evidence/of13-solenoidal-startup-control-v1')
    names = [f'n{spec["n"]}-dt{dt}' for dt in spec['dt']]
    archives = [root / (name + '.tar.gz') for name in names]
    missing = [str(p) for p in archives if not p.is_file()]
    if missing:
        raise SystemExit('INCOMPLETE: no result written; missing archives: ' + ', '.join(missing))
    inputs = {row['case']: row['input_hashes'] for row in manifest['cases']}
    rows = []
    for name, archive, dt in zip(names, archives, spec['dt']):
        with tarfile.open(archive) as tar, tempfile.TemporaryDirectory() as folder:
            def read(member):
                return tar.extractfile(member).read()

            def materialize(member):
                path = Path(folder) / member
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(read(member))
                return path

            for member, digest in inputs[name].items():
                assert hashlib.sha256(read(member)).hexdigest() == digest
            assert json.loads(read('exit.json'))['exit_code'] == 0
            log = read('log.foamRun').decode()
            times = completed_times(log)
            expected = np.arange(1, round(spec['end'] / dt) + 1) * dt
            assert log.rstrip().endswith('End')
            assert len(times) == len(expected)
            assert np.allclose(times, expected, atol=1e-14, rtol=0)
            assert log.count('PIMPLE: Converged in') == len(times)
            count = spec['n'] ** 3
            initial = vectors(materialize('0/U'), count)
            assert np.isfinite(initial).all()
            denominator = np.linalg.norm(initial)
            assert denominator > 0
            steps = []
            for time in times:
                prefix = format(time, '.12g')
                u = vectors(materialize(prefix + '/U'), count)
                p = values(materialize(prefix + '/p'), count)
                assert np.isfinite(u).all() and np.isfinite(p).all()
                steps.append({
                    'time': time,
                    'relative_velocity_increment_from_own_initial': float(np.linalg.norm(u - initial) / denominator),
                    'pressure_range': float(np.ptp(p)),
                    'centered_pressure_impulse_rms': float(dt * np.sqrt(np.mean((p - p.mean()) ** 2))),
                })
            baseline_archive = Path('evidence') / spec['baseline'] / (name + '.tar.gz')
            with tarfile.open(baseline_archive) as baseline:
                assert json.load(baseline.extractfile('exit.json'))['exit_code'] == 0
                baseline_log = baseline.extractfile('log.foamRun').read().decode()
                assert baseline_log.rstrip().endswith('End')
                assert completed_times(baseline_log) == times
                baseline_path = Path(folder) / 'baseline-first-p'
                baseline_path.write_bytes(baseline.extractfile(format(times[0], '.12g') + '/p').read())
                bp = values(baseline_path, count)
                assert np.isfinite(bp).all()
                impulse = float(dt * np.sqrt(np.mean((bp - bp.mean()) ** 2)))
                assert impulse > 0
            rows.append({'case': name, 'archive_sha256': hashlib.sha256(archive.read_bytes()).hexdigest(),
                         'baseline_archive_sha256': hashlib.sha256(baseline_archive.read_bytes()).hexdigest(),
                         'baseline_first_pressure_impulse_rms': impulse,
                         'first_pressure_impulse_control_over_baseline': steps[0]['centered_pressure_impulse_rms'] / impulse,
                         'steps': steps})
    result = {'cases': rows, 'quality': 'UNCERTAIN', 'scope': spec['scope'],
              'protocol_sha256': manifest['protocol_sha256'],
              'interpretation': 'Measurements only; no original-MMS accuracy score or automatic causal verdict. RMS uses equal-volume cells of the uniform mesh.'}
    (root / 'step-diagnostics.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
