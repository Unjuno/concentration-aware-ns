"""Build a conservative real-evidence report; preserve known review gaps."""
import hashlib
import json
from pathlib import Path
from tools.acceptance_gate import evaluate

paths={
'reference_verified':'evidence/tests/reference-symbolic.json',
'forcing_verified':'evidence/tests/openfoam-force.json',
'derivatives_verified':'docs/analytic-self-audit.md',
'space_time_study_verified':'evidence/tests/openfoam-time-comparison.json',
'thresholds_preregistered':'protocols/of13-study-v1.json',
'raw_artifacts_reviewed':'evidence/of13-study-v1/n32-dt0.001.tar.gz',
'evaluation_time_verified':'evidence/of13-study-v1/summary.json',
'standard_acceptance_verified':'reports/openfoam-study-v1.md'}
flags=dict.fromkeys(paths,True)
flags['space_time_study_verified']=False
flags['standard_acceptance_verified']=False
bound=json.loads(Path('evidence/tests/peak-lower-bounds-complete.json').read_text())['n32-dt0.001']
summary=json.loads(Path('evidence/of13-study-v1/summary.json').read_text())
case=next(r for r in summary['cases'] if r['case']=='n32-dt0.001')
energies=json.loads(Path('evidence/tests/continuum-energy-comparison.json').read_text())
energy=next(r for r in energies['cases'] if r['group']=='of13-study-v1' and r['case']=='n32-dt0.001.tar.gz')
report={'schema_version':2,'standard_acceptance':'UNCERTAIN','evidence':flags,
'artifacts':{k:{'path':v,'sha256':hashlib.sha256(Path(v).read_bytes()).hexdigest()} for k,v in paths.items()},
'metrics':[{'name':'max_'+name,'error_lower':bound[name]['relative_underestimation_lower_bound'],'error_upper':None,'tolerance':.05} for name in ('gradient','vorticity')],
'scope':'Reported sampled FD2 peak versus continuum maximum. Floating-point evaluation of analytic lower bounds, not interval certification.',
'unresolved':['Asymptotic temporal convergence not established','Full standard acceptance review incomplete','Continuous peak upper bounds and full uncertainty budget unavailable'],
'observed_aggregate_thresholds':{'velocity_relative_l2':case['velocity_relative_l2'],'energy_relative_error':energy['relative_error'],'velocity_tolerance':.02,'energy_tolerance':.02}}
Path('reports/openfoam-n32-gate.json').write_text(json.dumps(report,indent=2)+'\n')
Path('reports/openfoam-n32-verdict.json').write_text(json.dumps(evaluate(report,Path('.')),indent=2)+'\n')
