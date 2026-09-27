"""Independently replay archived clock intervention using decimal CSV values."""
import csv
from decimal import Decimal
import hashlib
import io
import json
from pathlib import Path
import tarfile


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def table(archive, name):
    data = archive.extractfile(name).read().decode()
    result = []
    for row in csv.DictReader(io.StringIO(data)):
        parsed = {key.strip().strip('"'): Decimal(value.strip()) for key, value in row.items()}
        if not all(value.is_finite() for value in parsed.values()):
            raise ValueError('Nonfinite CSV entry')
        result.append(parsed)
    return result


def check():
    root = Path('evidence/su2-output-clock-control-v1')
    protocol = json.loads(Path('protocols/su2-output-clock-control-v1.json').read_text())
    summary = json.loads((root / 'summary.json').read_text())
    assert [case['mode'] for case in summary['cases']] == ['continuous', 'resumed']
    records = []
    for claimed in summary['cases']:
        mode = claimed['mode']
        path = root / f'{mode}.tar.gz'
        baseline = Path('evidence/su2-restart-time-pilot-v1') / f'original-{mode}.tar.gz'
        assert digest(path) == claimed['archive_sha256']
        with tarfile.open(path) as actual, tarfile.open(baseline) as original:
            params = json.load(actual.extractfile('parameters.json'))
            assert params['baseline_sha256'] == digest(baseline)
            assert params['image_id'] == summary['image_id']
            assert params['mode'] == mode
            assert all(params[key] == value for key, value in protocol.items())
            assert actual.extractfile('exit_code').read().strip() == b'0'
            inputs = ['case.cfg', 'mesh.su2']
            if mode == 'resumed':
                inputs += ['restart_00000.csv', 'restart_00001.csv']
            for name in inputs:
                assert actual.extractfile(name).read() == original.extractfile(name).read()
            indices = list(range(4)) if mode == 'continuous' else [2, 3]
            history_name = 'history.csv' if mode == 'continuous' else 'history_00002.csv'
            history = table(actual, history_name)
            old_history = table(original, history_name)
            assert [row['Time_Iter'] for row in history] == indices
            assert [row['Time_Iter'] for row in old_history] == indices
            differences = []
            for index, row, old_row in zip(indices, history, old_history):
                expected = Decimal(index) / 10
                assert row['Cur_Time'] == expected
                assert row['Time_Step'] == Decimal('.1')
                assert old_row['Cur_Time'] == expected - (Decimal('.1') if mode == 'resumed' else 0)
                assert all(row[key] < -10 for key in ('rms[P]', 'rms[U]', 'rms[V]', 'rms[W]'))
                name = f'restart_{index:05d}.csv'
                left, right = table(actual, name), table(original, name)
                assert len(left) == len(right) == 125
                assert [r['PointID'] for r in left] == [Decimal(i) for i in range(125)]
                assert [r['PointID'] for r in right] == [Decimal(i) for i in range(125)]
                for a, b in zip(left, right):
                    assert all(a[k] == b[k] for k in ('x', 'y', 'z'))
                    differences.extend(abs(a[k] - b[k]) for k in ('Pressure', 'Velocity_x', 'Velocity_y', 'Velocity_z'))
            maximum = max(differences)
            assert maximum < Decimal(str(protocol['comparison_absolute_tolerance']))
            assert maximum == Decimal(str(claimed['same_mode_field_max_difference']))
            assert [row['Cur_Time'] for row in history] == [Decimal(str(v)) for v in claimed['times']]
            records.append({'mode': mode, 'archive_sha256': digest(path), 'baseline_sha256': digest(baseline), 'input_bytes_identical': inputs, 'field_values_compared': len(differences), 'maximum_difference': str(maximum), 'times': [str(row['Cur_Time']) for row in history]})
    return {'success': True, 'scope': protocol['scope'], 'method': 'Decimal CSV replay, independent of runner NumPy arrays; finite entries, full node IDs, coordinates, imported inputs, residuals and old/new clocks checked', 'cases': records, 'general_fix_validated': False}


if __name__ == '__main__':
    result = check()
    destination = Path('evidence/su2-output-clock-control-v1/independent-review.json')
    destination.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
