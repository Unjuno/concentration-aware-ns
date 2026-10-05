"""Conservative continuous-domain bound for the executed SU2 MMS force only."""
import argparse,json,hashlib,tarfile
from pathlib import Path
from flint import arb,ctx
from tools.amr_point_gradient_bound import exact_float
from tools.amr_arb_mean_certificate import endpoints
from tools.run_amr_mean_quality import ROOT,sha


def audit(output,source_commit):
    if output.exists():raise FileExistsError('preserve prior bound')
    base=ROOT/'evidence/su2-study-v1'
    summary=json.loads((base/'summary.json').read_text())
    rows=[];old=ctx.prec;ctx.prec=128
    try:
        for case in summary['cases']:
            if not case['case'].startswith('n64-dt'):continue
            archive=base/(case['case']+'.tar.gz')
            if sha(archive)!=case['archive_sha256']:raise ValueError('archive hash mismatch')
            with tarfile.open(archive) as stream:params=json.load(stream.extractfile('parameters.json'))
            sigma,nu,h,t=(exact_float(params[k]) for k in ('sigma','nu','dt','end'))
            if not (sigma>0 and nu>0 and h>0 and t>=h):raise ValueError('positive aligned interval required')
            beta=1/(sigma*sigma);root3=arb(3).sqrt();root42=arb(42).sqrt()
            # At t=0, |psi|<=1, |q_i|,|r_i|,|s_i|<=beta, |a|=sqrt(14).
            linear=root42*(beta+nu*(3*beta**3+5*beta**2+beta))
            quadratic=14*root3*beta*(3*beta**2+root3*beta)
            bound=(h.exp()-1)*(-t).exp()*linear+((2*h).exp()-1)*(-2*t).exp()*quadratic
            coefficient=(h-t).exp()*linear+2*(2*h-2*t).exp()*quadratic
            if not (bound>0 and coefficient>0):raise ValueError('positive enclosure required')
            rows.append({'case':case['case'],'archive_sha256':case['archive_sha256'],
                         'sigma':params['sigma'],'nu':params['nu'],'dt':params['dt'],'end':params['end'],
                         'linear_force_bound_expression':endpoints(linear),
                         'quadratic_force_bound_expression':endpoints(quadratic),
                         'force_displacement_bound_expression':endpoints(bound),
                         'linear_in_dt_coefficient_expression':endpoints(coefficient)})
    finally:ctx.prec=old
    result={'status':'CONSERVATIVE_CONTINUOUS_MMS_FORCE_UPPER_BOUND','source_commit':source_commit,
            'reference_sha256':sha(ROOT/'tools/reference.py'),'precision_bits':128,'cases':rows,
            'inequality':'sup_x |f(x,t-h)-f(x,t)| <= (exp(h)-1)*exp(-t)*L_bound+(exp(2h)-1)*exp(-2t)*Q_bound <= h*C(h,t)',
            'limits':['Use upper endpoints of bound expressions; lower endpoints are not lower bounds on actual supremum',
                      'Real analytic periodic exponential-envelope MMS with decoded archived parameters',
                      'Conservative triangle bounds, not tight extrema, relative errors or solver endpoint errors',
                      'No bound for floating evaluator rounding, discrete solve or callback implementation']}
    output.mkdir(parents=True);(output/'analysis.json').write_text(json.dumps(result,indent=2)+'\n')
    print(result['status'])


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,required=True);parser.add_argument('--source-commit',required=True);args=parser.parse_args();audit(args.output,args.source_commit)
