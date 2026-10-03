"""Check declared scalar C++ diagnostics; not native OpenFOAM equivalence."""
import argparse
import hashlib
import json
import math
from pathlib import Path


def check(paths):
    records = []
    for path in paths:
        data = Path(path).read_bytes()
        value = json.loads(data)
        if not all(isinstance(v, (int, float)) and math.isfinite(v) for v in value.values()):
            raise ValueError('nonfinite scalar diagnostic')
        low, high = value['carrier_low'], value['carrier_high']
        if low != .01 or high != math.nextafter(low, math.inf):
            raise ValueError('wrong adjacent input pair')
        if value['carrier_difference'] != high-low:
            raise ValueError('inconsistent input difference')
        delta = value['update_high']-value['update_low']
        if value['update_difference'] != delta or not 3e-6 < delta < 3.3e-6:
            raise ValueError('declared finite branch jump not reproduced')
        if value['finite_difference_gain'] != delta/(high-low):
            raise ValueError('inconsistent two-float quotient')
        records.append({'path': str(path), 'sha256': hashlib.sha256(data).hexdigest(),
                        'output_difference': delta})
    if not records:
        raise ValueError('missing scalar diagnostic')
    return {'status': 'SCALAR_TRANSCRIPTION_CONTROLS_PASS', 'records': records,
            'limits': ['Synthetic scalar transcription, not an OpenFOAM binary/cloud run',
                       'Two-float quotient is not a continuous derivative',
                       'No trajectory, molecular viscosity or phase-transition inference']}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, action='append', required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError('preserve previous transcription check')
    args.output.write_text(json.dumps(check(args.input), indent=2, allow_nan=False)+'\n')
