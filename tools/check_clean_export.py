"""Replay a fixed tracked commit in a fresh venv without borrowing work/ files.

This checks Python postprocessing, not solver builds, training or Lean replay.
The destination must not exist; incomplete attempts remain available for audit.
"""
import argparse
import hashlib
import json
import platform
from pathlib import Path
import subprocess
import sys
import tarfile


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--revision', default='HEAD')
    parser.add_argument('--destination', required=True)
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[1]
    commit = subprocess.check_output(
        ['git', 'rev-parse', '--verify', args.revision+'^{commit}'], cwd=repo, text=True).strip()
    destination = Path(args.destination).resolve()
    destination.mkdir(parents=True, exist_ok=False)
    archive = destination/'tracked.tar'
    with archive.open('wb') as stream:
        subprocess.run(['git', 'archive', commit], cwd=repo, stdout=stream, check=True)
    checkout = destination/'source'
    checkout.mkdir()
    with tarfile.open(archive) as stream:
        stream.extractall(checkout, filter='data')
    # Compare scientific reports and deterministic test evidence, not timing logs.
    observed = sorted(path for folder in ['reports', 'evidence/tests']
                      for path in (checkout/folder).rglob('*') if path.is_file())
    baseline = {str(path.relative_to(checkout)): digest(path) for path in observed}
    result = {
        'commit': commit,
        'scope': 'Tracked-only fixed-commit export, fresh venv, same host/interpreter. '
                 'No solver build, training, Lean execution or verdict upgrade.',
        'runner_sha256': digest(Path(__file__)),
        'archive_sha256': digest(archive),
        'python': sys.version,
        'platform': platform.platform(),
        'checks': [],
        'success': False,
    }
    record = destination/'result.json'

    def save():
        record.write_text(json.dumps(result, indent=2)+'\n')

    def run(name, command):
        logfile = destination/(name+'.log')
        with logfile.open('w') as stream:
            proc = subprocess.run(command, cwd=checkout, stdout=stream, stderr=subprocess.STDOUT)
        result['checks'].append({'name': name, 'command': command, 'exit_code': proc.returncode,
                                 'log': logfile.name, 'log_sha256': digest(logfile)})
        save()
        print(f'{name}: exit {proc.returncode}', flush=True)
        return proc.returncode == 0

    save()
    env = destination/'venv'
    if not run('venv', [sys.executable, '-m', 'venv', str(env)]):
        return 1
    python = str(env/'bin/python')
    commands = [('install', [python, '-m', 'pip', 'install', '-r', 'requirements-verification.txt'])]
    commands += [(name, [python, '-m', module]) for name, module in [
        ('report-replay', 'tools.replay_published_reports'),
        ('su2-standard', 'tools.review_su2_standard'),
        ('axis-force', 'tools.check_axis_force'),
        ('axis-dissipation', 'tools.check_axis_dissipation'),
        ('axis-deformation', 'tools.check_axis_deformation'),
        ('axis-packet', 'tools.check_axis_packet_bound'),
    ]]
    for name, command in commands:
        if not run(name, command):
            return 1
    freeze = subprocess.run([python, '-m', 'pip', 'freeze'], cwd=checkout,
                            text=True, capture_output=True, check=True)
    result['packages'] = freeze.stdout.splitlines()
    current = {str(path.relative_to(checkout)): digest(path)
               for folder in ['reports', 'evidence/tests']
               for path in (checkout/folder).rglob('*') if path.is_file()}
    result['compared_files'] = len(baseline)
    result['changed_files'] = [name for name in sorted(baseline.keys() | current.keys())
                               if baseline.get(name) != current.get(name)]
    replay = json.loads((checkout/'evidence/report-replay/summary.json').read_text())
    result['replay_steps'] = len(replay['steps'])
    result['replay_success'] = replay['success']
    result['success'] = replay['success'] and not result['changed_files']
    save()
    print(json.dumps({key: result[key] for key in
                      ['success', 'compared_files', 'changed_files', 'replay_steps']}, indent=2))
    return 0 if result['success'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
