"""Positive/negative filesystem controls; not a complete sandbox escape audit."""
import argparse
import json
import subprocess
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('--best-effort', action='store_true')
args = parser.parse_args()
root = Path('work/lean-verification').resolve()
scratch = root / 'sandbox-smoke'
scratch.mkdir(exist_ok=True)
(scratch / 'allowed.txt').write_text('allowed-control\n')
(scratch / 'denied.txt').write_text('denied-control\n')
base = ['docker', 'run', '--rm', '--user', '501:20', '--network', 'none',
        '--entrypoint', '/verify/checker-bin/landrun', '-v', f'{root}:/verify:ro',
        'concentration-aware-ns:su2', '--rox', '/usr', '--rox', '/lib',
        '--ro', '/verify/sandbox-smoke/allowed.txt']
if args.best_effort:
    base.append('--best-effort')
results = []
for name in ('allowed', 'denied'):
    run = subprocess.run(base + ['/usr/bin/cat', f'/verify/sandbox-smoke/{name}.txt'],
                         capture_output=True, text=True)
    results.append({'case': name, 'exit_code': run.returncode, 'stdout': run.stdout, 'stderr': run.stderr})
passed = results[0]['exit_code'] == 0 and results[0]['stdout'] == 'allowed-control\n' and results[1]['exit_code'] != 0 and results[1]['stdout'] == ''
report = {'scope': 'Read permission positive/negative control only; no AF_UNIX or sandbox escape assurance.',
          'passed': passed, 'command_base': base, 'results': results}
Path('evidence/lean-verification/landrun-filesystem-' + ('best-effort' if args.best_effort else 'smoke') + '.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
raise SystemExit(0 if passed else 1)
