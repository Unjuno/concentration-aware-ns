"""Execute preregistered MAX_TIME clock control; retain failed predictions."""
import csv
import hashlib
import io
import json
from pathlib import Path
import re
import subprocess
import tarfile
from decimal import Decimal


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_csv(path):
    return [{k.strip().strip('"'): Decimal(v.strip()) for k, v in row.items()}
            for row in csv.DictReader(io.StringIO(path.read_text()))]


def main():
    protocol_path = Path('protocols/su2-max-time-clock-control-v1.json')
    protocol = json.loads(protocol_path.read_text())
    root = Path('work/su2-max-time-clock-control-v1')
    out = Path('evidence/su2-max-time-clock-control-v1')
    root.mkdir(exist_ok=False)
    out.mkdir(exist_ok=False)
    results = []
    for label, image in zip(['original', 'output-control'], protocol['images']):
        identity = subprocess.check_output(['docker', 'image', 'inspect', image, '--format', '{{.Id}}'], text=True).strip()
        for mode in protocol['modes']:
            case = root / f'{label}-{mode}'
            case.mkdir()
            baseline = Path('evidence/su2-restart-time-pilot-v1') / f'original-{mode}.tar.gz'
            with tarfile.open(baseline) as archive:
                inputs = ['case.cfg', 'mesh.su2'] + (['restart_00000.csv', 'restart_00001.csv'] if mode == 'resumed' else [])
                for name in inputs:
                    (case / name).write_bytes(archive.extractfile(name).read())
            config = (case / 'case.cfg').read_text()
            for key, value in [('MAX_TIME', protocol['max_time']), ('TIME_ITER', protocol['time_iter'])]:
                config, count = re.subn(rf'^{key}=.*$', f'{key}= {value}', config, flags=re.M)
                assert count == 1
            (case / 'case.cfg').write_text(config)
            params = {'protocol_sha256': sha(protocol_path), 'image': image, 'image_id': identity, 'baseline_sha256': sha(baseline), 'mode': mode}
            (case / 'parameters.json').write_text(json.dumps(params, indent=2)+'\n')
            command = ['docker', 'run', '--rm', '--network', 'none', '--cpus=2', '--memory=4g', '--user', '501:20', '-e', 'OMP_NUM_THREADS=2', '-v', f'{case.resolve()}:/case', image, 'SU2_CFD', 'case.cfg']
            (case / 'command.json').write_text(json.dumps(command)+'\n')
            with (case / 'solver.log').open('w') as log:
                run = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT)
            (case / 'exit_code').write_text(str(run.returncode)+'\n')
            destination = out / f'{case.name}.tar.gz'
            with tarfile.open(destination, 'w:gz') as archive:
                for path in sorted(case.iterdir()):
                    archive.add(path, arcname=path.name)
            history_path = case / ('history.csv' if mode == 'continuous' else 'history_00002.csv')
            history = read_csv(history_path) if history_path.exists() else []
            indices = [int(row['Time_Iter']) for row in history]
            expected_last = 5 if label == 'original' and mode == 'resumed' else 4
            log = (case / 'solver.log').read_text()
            checks = {'exit_zero': run.returncode == 0, 'predicted_indices': indices == list(range(0 if mode == 'continuous' else 2, expected_last+1)), 'max_time_stop': 'Maximum time reached (MAX_TIME' in log, 'iteration_cap_not_reached': 'Maximum number of time iterations reached (TIME_ITER' not in log, 'residuals_met': bool(history) and all(row[k].is_finite() and row[k] < -10 for row in history for k in ['rms[P]', 'rms[U]', 'rms[V]', 'rms[W]'])}
            results.append({'case': case.name, 'archive_sha256': sha(destination), 'indices': indices, 'times': [str(row['Cur_Time']) for row in history], 'checks': checks})
            (out / 'summary.json').write_text(json.dumps({'scope': protocol['scope'], 'cases': results}, indent=2)+'\n')
            print(results[-1], flush=True)
    comparisons = []
    for mode in protocol['modes']:
        differences = []
        for index in range(0 if mode == 'continuous' else 2, 5):
            name = f'restart_{index:05d}.csv'
            a = read_csv(root / f'original-{mode}' / name)
            b = read_csv(root / f'output-control-{mode}' / name)
            assert len(a) == len(b) == 125
            assert [r['PointID'] for r in a] == [r['PointID'] for r in b] == list(range(125))
            for left, right in zip(a, b):
                for key in ['Pressure', 'Velocity_x', 'Velocity_y', 'Velocity_z']:
                    assert left[key].is_finite() and right[key].is_finite()
                    differences.append(abs(left[key]-right[key]))
        maximum = max(differences)
        comparisons.append({'mode': mode, 'maximum_difference': str(maximum), 'pass': maximum < Decimal('1e-7')})
    summary = {'scope': protocol['scope'], 'cases': results, 'field_comparisons': comparisons, 'prediction_reproduced': all(all(r['checks'].values()) for r in results) and all(c['pass'] for c in comparisons), 'general_fix_validated': False}
    (out / 'summary.json').write_text(json.dumps(summary, indent=2)+'\n')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
