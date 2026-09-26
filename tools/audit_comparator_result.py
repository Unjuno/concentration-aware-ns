"""Audit a completed recorded Comparator run; never substitutes for executing it."""
import argparse
import hashlib
import json
from pathlib import Path
import re


def audit(result, inputs, log_bytes):
    text = log_bytes.decode('utf-8')
    config = inputs['configuration']
    names = config['theorem_names']
    permitted = set(config['permitted_axioms'])
    reports = {}
    for name, axioms in re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]", text):
        reports.setdefault(name, []).append({x.strip() for x in axioms.split(',') if x.strip()})
    checks = {
        'exit_zero': result.get('exit_code') == 0,
        'log_hash_matches': hashlib.sha256(log_bytes).hexdigest() == result.get('log_sha256'),
        'source_pin_matches': result.get('upstream_commit') == inputs.get('source_commit')
                              and bool(inputs.get('source_commit')),
        'nanoda_enabled': config.get('enable_nanoda') is True,
        'targets_nonempty_unique': bool(names) and len(names) == len(set(names)),
        'target_axioms_present_and_permitted': all(
            name in reports and all(ax <= permitted for ax in reports[name]) for name in names),
        'nanoda_accepted': 'nanoda kernel accepts the solution' in text.splitlines(),
        'lean_accepted': 'Lean default kernel accepts the solution' in text.splitlines(),
        'final_success': bool(text.strip()) and text.strip().splitlines()[-1] == 'Your solution is okay!',
    }
    return {'success': all(checks.values()), 'checks': checks,
            'targets': names, 'scope': 'Recorded log and configuration consistency only; not a new kernel run or source semantics audit.'}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--result', required=True)
    p.add_argument('--inputs', required=True)
    p.add_argument('--output', required=True)
    args = p.parse_args()
    result = json.loads(Path(args.result).read_text())
    inputs = json.loads(Path(args.inputs).read_text())
    report = audit(result, inputs, Path(result['log']).read_bytes())
    report['result_sha256'] = hashlib.sha256(Path(args.result).read_bytes()).hexdigest()
    report['inputs_sha256'] = hashlib.sha256(Path(args.inputs).read_bytes()).hexdigest()
    Path(args.output).write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))
    return 0 if report['success'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
