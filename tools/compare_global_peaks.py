"""Compare saved diagnostic peaks with analytic global MMS maxima."""
import hashlib
import json
import math
from pathlib import Path
import tarfile


def compare(observed, time, sigma):
    factor = math.exp(-time) / sigma**2
    return {name: {'reported_peak': observed[name], 'analytic_global_peak': exact,
                   'relative_discrepancy': abs(observed[name] / exact - 1)}
            for name, exact in [('gradient', math.sqrt(28)*factor), ('vorticity', math.sqrt(56)*factor)]}


def main():
    cases = []
    for group in ('of13-study-v1', 'su2-study-v1'):
        for path in sorted(Path('evidence', group).glob('*.tar.gz')):
            with tarfile.open(path) as tar:
                data = json.load(tar.extractfile('diagnostics.json'))
            params = data['parameters']
            cases.append({'group': group, 'case': path.name, 'method': 'sampled FD2',
                          'artifact': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                          'metrics': compare({n: data['computed']['max_'+n+'_fd2'] for n in ('gradient','vorticity')}, params['end'], params['sigma'])})
    params = json.loads(Path('protocols/physicsnemo-study-v1.json').read_text())['base']
    for path in sorted(Path('evidence/physicsnemo-study-v1').glob('*-gradient.json')):
        data = json.loads(path.read_text())
        cases.append({'group': 'physicsnemo-study-v1', 'case': path.name, 'method': 'autograd at saved samples',
                      'artifact': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                      'metrics': compare({n: data['max_'+n+'_autograd_samples'] for n in ('gradient','vorticity')}, params['end'], params['sigma'])})
    proof = Path('docs/reference-global-peaks.md')
    result = {'scope': 'Reported diagnostic peak versus exact global reference peak. Ordinary floating point, not interval certification or predicted-field supremum error.',
              'derivation': str(proof), 'derivation_sha256': hashlib.sha256(proof.read_bytes()).hexdigest(), 'cases': cases}
    Path('evidence/tests/global-peak-comparison.json').write_text(json.dumps(result, indent=2)+'\n')
    print('\n'.join(f"{c['group']}/{c['case']}: gradient={c['metrics']['gradient']['relative_discrepancy']:.6%}, vorticity={c['metrics']['vorticity']['relative_discrepancy']:.6%}" for c in cases))


if __name__ == '__main__':
    main()
