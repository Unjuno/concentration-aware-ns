"""Build conservative evidence-linked SU2 reports without upgrading sample peaks."""
import hashlib
import json
from pathlib import Path
from tools.acceptance_gate import evaluate


def build():
    summary=json.loads(Path('evidence/su2-study-v1/summary.json').read_text())
    spectral=json.loads(Path('evidence/tests/su2-spectral-gradient.json').read_text())
    by_name={row['case']:row for row in spectral['cases']}
    protocol=json.loads(Path('protocols/su2-study-v1.json').read_text())
    for case in summary['cases']:
        name=case['case']
        paths={
            'reference_verified':'evidence/tests/reference-symbolic.json',
            'forcing_verified':'evidence/tests/su2-force-helper.json',
            'derivatives_verified':'evidence/tests/su2-spectral-gradient.json',
            'space_time_study_verified':'evidence/tests/su2-time-comparison.json',
            'thresholds_preregistered':'protocols/su2-study-v1.json',
            'raw_artifacts_reviewed':'evidence/su2-study-v1/archive-review.json',
            'evaluation_time_verified':'evidence/su2-study-v1/diagnostic-replay.json',
            'standard_acceptance_verified':'evidence/su2-study-v1/summary.json',
        }
        flags=dict.fromkeys(paths,True)
        # Successful postprocessing is not a continuum derivative error bound.
        flags['derivatives_verified']=False
        flags['space_time_study_verified']=False
        flags['standard_acceptance_verified']=False
        report={
            'schema_version':2,'standard_acceptance':'UNCERTAIN','evidence':flags,
            'artifacts':{k:{'path':v,'sha256':hashlib.sha256(Path(v).read_bytes()).hexdigest()} for k,v in paths.items()},
            'metrics':[{'name':'max_'+key,'error_lower':0.0,'error_upper':None,'tolerance':protocol['relative_error_thresholds']['max_'+key]} for key in ('gradient','vorticity')],
            'scope':'No certified continuum peak-error interval. [0, unbounded] records missing bounds, not zero measured error. Gate flags preserve unresolved review requirements.',
            'observations':{'case':name,'archive_sha256':case['archive_sha256'],'velocity_relative_l2':case['velocity_relative_l2'],'velocity_tolerance':protocol['relative_error_thresholds']['velocity_l2'],'converged_steps':case['converged_steps'],'steps':case['steps'],'all_steps_meet_residual_threshold':case['converged_steps']==case['steps'],'sample_spectral_metrics':by_name[name]['metrics']},
            'unresolved':['Continuum numerical-field peak bounds and uncertainty budget absent','Time comparison does not isolate inner-iteration error','Full standard acceptance review including energy not encoded here'],
        }
        Path(f'reports/su2-{name}-gate.json').write_text(json.dumps(report,indent=2)+'\n')
        Path(f'reports/su2-{name}-verdict.json').write_text(json.dumps(evaluate(report,Path('.')),indent=2)+'\n')

if __name__=='__main__':
    build()
