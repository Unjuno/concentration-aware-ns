"""Generate evidence-linked reports without promoting sample errors to bounds."""
import hashlib
import json
from pathlib import Path
from tools.acceptance_gate import evaluate


def main():
    comparison = json.loads(Path('evidence/physicsnemo-study-v1/comparison.json').read_text())
    thresholds = json.loads(Path('protocols/of13-study-v1.json').read_text())['relative_error_thresholds']
    reports = []
    for case in comparison['cases']:
        name = case['case']
        paths = {
            'reference_verified': 'evidence/physicsnemo/reference-autograd.json',
            'forcing_verified': 'evidence/physicsnemo/residual-check.json',
            'derivatives_verified': f'evidence/physicsnemo-study-v1/{name}-gradient.json',
            'space_time_study_verified': 'evidence/physicsnemo-study-v1/comparison.json',
            'thresholds_preregistered': 'protocols/physicsnemo-study-v1.json',
            'raw_artifacts_reviewed': f'evidence/physicsnemo-study-v1/{name}.tar.gz',
            'evaluation_time_verified': 'evidence/physicsnemo-study-v1/summary.json',
            'standard_acceptance_verified': 'reports/physicsnemo-study-v1.md',
        }
        flags = dict.fromkeys(paths, True)
        for key in ('space_time_study_verified', 'thresholds_preregistered', 'standard_acceptance_verified'):
            flags[key] = False
        report = {
            'schema_version': 2, 'case': name, 'standard_acceptance': 'UNCERTAIN',
            'evidence': flags,
            'artifacts': {key: {'path': path, 'sha256': hashlib.sha256(Path(path).read_bytes()).hexdigest()}
                          for key, path in paths.items()},
            'metrics': [{'name': metric, 'error_lower': 0.0, 'error_upper': None,
                         'tolerance': thresholds[metric]} for metric in ('max_gradient', 'max_vorticity')],
            'observed_samples': case,
            'scope': 'Continuous peak relative error has no certified nontrivial bound. Sample errors are observations only.',
            'threshold_scope': '5% is imported for comparison from the OpenFOAM protocol; PhysicsNeMo-specific preregistration is not established.',
            'unresolved': ['No continuous peak error enclosure',
                           'Fixed-budget single-seed sampling matrix does not establish optimizer or asymptotic convergence',
                           'PhysicsNeMo protocol does not explicitly preregister acceptance thresholds',
                           'No established full standard acceptance criterion for this trained network'],
            'amr': 'Not applicable to this fixed-architecture PINN experiment',
        }
        verdict = evaluate(report, Path('.'))
        output = Path(f'reports/physicsnemo-{name}-gate.json')
        output.write_text(json.dumps(report, indent=2) + '\n')
        reports.append({'case': name, 'report': str(output), 'verdict': verdict})
    Path('reports/physicsnemo-gate-verdicts.json').write_text(json.dumps(reports, indent=2) + '\n')


if __name__ == '__main__':
    main()
