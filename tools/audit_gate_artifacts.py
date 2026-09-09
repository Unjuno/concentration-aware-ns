"""Check every gate artifact link, including links behind false review flags."""
import hashlib
import json
from pathlib import Path


def audit(root):
    root = Path(root).resolve()
    results = []
    for report in sorted((root / 'reports').glob('*-gate.json')):
        data = json.loads(report.read_text())
        for name, ref in data.get('artifacts', {}).items():
            relative = Path(ref['path'])
            target = (root / relative).resolve()
            if relative.is_absolute() or not target.is_relative_to(root):
                status = 'INVALID_PATH'
            elif not target.is_file():
                status = 'MISSING'
            else:
                actual = hashlib.sha256(target.read_bytes()).hexdigest()
                status = 'MATCH' if actual == ref['sha256'] else 'MISMATCH'
            results.append({'report': str(report.relative_to(root)), 'artifact': name,
                            'path': ref['path'], 'status': status})
    return {'scope': 'Artifact byte identity only; does not validate scientific review flags or conclusions.',
            'links_checked': len(results), 'all_match': bool(results) and all(r['status'] == 'MATCH' for r in results),
            'links': results}


if __name__ == '__main__':
    result = audit('.')
    Path('evidence/tests/gate-artifact-audit.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'links'}, indent=2))
    raise SystemExit(0 if result['all_match'] else 1)
