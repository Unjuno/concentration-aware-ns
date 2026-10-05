"""Envelope-aware real-domain force bound; no solver error claim."""
import argparse,json,tarfile
from pathlib import Path
from flint import arb,ctx
from tools.amr_point_gradient_bound import exact_float
from tools.amr_arb_mean_certificate import endpoints
from tools.run_amr_mean_quality import ROOT,sha



def validate_prior(original):
    if original.get('status') != 'CONSERVATIVE_CONTINUOUS_MMS_FORCE_UPPER_BOUND':
        raise ValueError('wrong prior bound family')
    if original.get('reference_sha256') != sha(ROOT/'tools/reference.py'):
        raise ValueError('reference source identity mismatch')
    base=ROOT/'evidence/su2-study-v1'
    summary=json.loads((base/'summary.json').read_text())
    expected={r['case']:r for r in summary['cases'] if r['case'].startswith('n64-dt')}
    rows=original['cases']
    if len(rows)!=len(expected) or {r['case'] for r in rows}!=set(expected):
        raise ValueError('missing or duplicate temporal case')
    for row in rows:
        path=base/(row['case']+'.tar.gz')
        if row['archive_sha256']!=expected[row['case']]['archive_sha256'] or sha(path)!=row['archive_sha256']:
            raise ValueError('archive identity mismatch')
        with tarfile.open(path) as stream:params=json.load(stream.extractfile('parameters.json'))
        if any(row[k]!=params[k] for k in ('sigma','nu','dt','end')):
            raise ValueError('archived parameter mismatch')


def audit(output,source_commit):
    if output.exists():raise FileExistsError('preserve prior envelope bound')
    prior=ROOT/'evidence/su2-force-time-uniform-upper-v1/analysis.json'
    original=json.loads(prior.read_text());validate_prior(original);rows=[];old=ctx.prec;ctx.prec=128
    try:
        def maximum(a,c):return (a*((a/c).log()-1)).exp()
        half=arb(1)/2;threehalf=arb(3)/2
        for row in original['cases']:
            beta=1/exact_float(row['sigma'])**2;nu=exact_float(row['nu'])
            h=exact_float(row['dt']);t=exact_float(row['end'])
            u=(14*beta/arb(1).exp()).sqrt()
            lap=arb(14).sqrt()*(2*beta).sqrt()*(2*beta*maximum(threehalf,1)+(5*beta+1)*maximum(half,1))
            linear=u+nu*lap
            quadratic=14*(2*beta).sqrt()*(2*beta*maximum(threehalf,2)+arb(3).sqrt()*beta*maximum(half,2))
            bound=(h.exp()-1)*(-t).exp()*linear+((2*h).exp()-1)*(-2*t).exp()*quadratic
            previous_linear=arb(42).sqrt()*(beta+nu*(3*beta**3+5*beta**2+beta))
            previous_quadratic=14*arb(3).sqrt()*beta*(3*beta**2+arb(3).sqrt()*beta)
            previous=(h.exp()-1)*(-t).exp()*previous_linear+((2*h).exp()-1)*(-2*t).exp()*previous_quadratic
            if not (bound>0 and bound<previous):raise ValueError('strict improvement not certified')
            rows.append({'case':row['case'],'archive_sha256':row['archive_sha256'],
                         'linear_force_bound_expression':endpoints(linear),
                         'quadratic_force_bound_expression':endpoints(quadratic),
                         'force_displacement_bound_expression':endpoints(bound)})
    finally:ctx.prec=old
    result={'status':'ENVELOPE_AWARE_CONTINUOUS_FORCE_UPPER_BOUND','source_commit':source_commit,
            'prior_receipt_sha256':sha(prior),'input_binding':'Reference source and all archived parameters/digests revalidated; previous coarse bound freshly recomputed','precision_bits':128,'cases':rows,
            'scalar_maximum_identity':'sup_{S>=0} S^a*exp(-c*S)=(a/(c*e))^a for a,c>0',
            'limits':['Real-domain absolute upper bound; use rational upper endpoint',
                      'Prior receipt carries archived parameter identities; no new native execution',
                      'No PDE endpoint error, acceptance or floating rounding bound']}
    output.mkdir(parents=True);(output/'analysis.json').write_text(json.dumps(result,indent=2)+'\n');print(result['status'])


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);p.add_argument('--source-commit',required=True);a=p.parse_args();audit(a.output,a.source_commit)
