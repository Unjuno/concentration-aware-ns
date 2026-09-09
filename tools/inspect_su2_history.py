"""Inspect completed history rows without implying an in-progress run is final."""
import argparse
import csv
import hashlib
import io
import json
from pathlib import Path


def inspect(path, threshold=-10.0):
    blob = Path(path).read_bytes()
    # A concurrent writer may have left an incomplete last row.
    complete = blob[:blob.rfind(b'\n') + 1]
    rows = [{k.strip().strip('"'): float(v) for k, v in row.items()}
            for row in csv.DictReader(io.StringIO(complete.decode()))]
    fields = ('rms[P]', 'rms[U]', 'rms[V]', 'rms[W]')
    failed = [{'time_iter': int(r['Time_Iter']), 'inner_iter': int(r['Inner_Iter']),
               'residuals': {f: r[f] for f in fields}}
              for r in rows if not all(r[f] < threshold for f in fields)]
    return {'scope': 'Completed newline-terminated history rows only; no run completion or final accuracy claim.',
            'history_prefix_sha256': hashlib.sha256(complete).hexdigest(),
            'history_rows': len(rows), 'threshold_log10_strict': threshold,
            'converged_rows': len(rows)-len(failed), 'unconverged_rows': failed}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('history')
    args = parser.parse_args()
    print(json.dumps(inspect(args.history), indent=2))
