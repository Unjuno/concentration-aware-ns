"""Observed frozen aggregate checks, separate from continuum certification."""
import hashlib
import json
from pathlib import Path
import tarfile
from tools.reference_energy import mean_energy, periodic_vertex_mean_energy

protocol=json.loads(Path('protocols/su2-study-v1.json').read_text())
summary=json.loads(Path('evidence/su2-study-v1/summary.json').read_text())
rows=[]
for case in summary['cases']:
    path=Path('evidence/su2-study-v1')/(case['case']+'.tar.gz')
    digest=hashlib.sha256(path.read_bytes()).hexdigest()
    if digest!=case['archive_sha256']:raise ValueError('archive hash mismatch')
    with tarfile.open(path) as archive:
        d=json.load(archive.extractfile('diagnostics.json'))
    exact=mean_energy(d['updated_solution_time'],d['parameters']['sigma'])
    exact_vertices=periodic_vertex_mean_energy(d['parameters']['n'],d['updated_solution_time'],d['parameters']['sigma'])
    energy=abs(d['computed']['mean_kinetic_energy']-exact)/exact
    vertex_energy=abs(d['computed']['mean_kinetic_energy']-exact_vertices)/exact_vertices
    checks={'velocity':d['velocity_relative_l2']<=protocol['relative_error_thresholds']['velocity_l2'],
            'energy':energy<=protocol['relative_error_thresholds']['energy'],
            'all_steps_residual':d['converged_steps']==d['steps']}
    rows.append({'case':case['case'],'archive_sha256':digest,'velocity_relative_l2':d['velocity_relative_l2'],'continuum_reference_energy':exact,'sample_energy_relative_error':energy,'analytic_vertex_reference_energy':exact_vertices,'sample_energy_relative_error_vs_vertex_reference':vertex_energy,'vertex_quadrature_bias_relative_to_continuum':(exact_vertices-exact)/exact,'observed_checks':checks,'observed_conjunction':'PASS' if all(checks.values()) else 'FAIL'})
result={'scope':'Observed velocity, sample-energy versus analytic continuum integral, and all-step residual checks. An additional exact finite-grid reference separates analytic-solution quadrature bias from solver-field energy discrepancy; it does not certify continuous numerical-field energy or peak errors. The conjunction remains an audit convention, not a newly preregistered gate.','cases':rows}
Path('evidence/tests/su2-standard-review.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
