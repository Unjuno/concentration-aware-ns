"""Conditional continuous-PDE energy response, not a SU2 discretization estimate."""
import argparse,json
from pathlib import Path
from flint import arb,ctx
from tools.run_amr_mean_quality import ROOT,sha
from tools.amr_point_gradient_bound import exact_float
from tools.amr_arb_mean_certificate import endpoints
from tools.tighten_su2_force_envelope_bound import validate_prior


def audit(output,source_commit):
    if output.exists():raise FileExistsError('preserve previous response bound')
    original_path=ROOT/'evidence/su2-force-time-uniform-upper-v1/analysis.json'
    envelope_path=ROOT/'evidence/su2-force-envelope-upper-v2/analysis.json'
    original=json.loads(original_path.read_text());validate_prior(original)
    envelope=json.loads(envelope_path.read_text())
    if envelope['prior_receipt_sha256']!=sha(original_path):raise ValueError('prior receipt changed')
    prior={r['case']:r for r in original['cases']};rows=[];old=ctx.prec;ctx.prec=128
    try:
        if len(envelope['cases'])!=len(prior) or {r['case'] for r in envelope['cases']}!=set(prior):raise ValueError('case mismatch')
        for row in envelope['cases']:
            p=prior[row['case']]
            if row['archive_sha256']!=p['archive_sha256']:raise ValueError('archive mismatch')
            beta=1/exact_float(p['sigma'])**2;h=exact_float(p['dt']);T=exact_float(p['end'])
            K=2*arb(14).sqrt()*beta*(arb(-1)/2).exp()
            BL=arb(row['linear_force_bound_expression']['upper_rational'])
            BQ=arb(row['quadratic_force_bound_expression']['upper_rational'])
            F=(h.exp()-1)*BL+((2*h).exp()-1)*BQ
            E=F*((K*T).exp()-1)/K
            rows.append({'case':row['case'],'gradient_operator_upper_expression':endpoints(K),
                         'time_uniform_force_upper_expression':endpoints(F),
                         'normalized_L2_response_upper_expression':endpoints(E)})
    finally:ctx.prec=old
    result={'status':'CONDITIONAL_CONTINUOUS_PDE_RESPONSE_UPPER','source_commit':source_commit,
            'envelope_receipt_sha256':sha(envelope_path),'precision_bits':128,'cases':rows,
            'assumptions':['Smooth incompressible periodic strong solutions u and v on [0,T]',
                           'Same viscosity and identical initial velocity',
                           'v forced by analytic shifted force f(t-h), including its extension at negative times',
                           'Volume-normalized L2 norm and real arithmetic'],
            'limits':['Does not prove existence of v or represent the discrete SU2 source schedule',
                      'No inner residual, discretization, restart or floating error included',
                      'Absolute conditional upper bound, not endpoint-error attribution or acceptance verdict']}
    output.mkdir(parents=True);(output/'analysis.json').write_text(json.dumps(result,indent=2)+'\n');print(result['status'])


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);p.add_argument('--source-commit',required=True);a=p.parse_args();audit(a.output,a.source_commit)
