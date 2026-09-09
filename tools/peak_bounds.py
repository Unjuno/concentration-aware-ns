"""One-sided analytic peak bounds for this MMS (not exact global extrema).

At x=(pi,pi,pi), Hessian(psi)=-exp(-t)/sigma^2 I. Thus
||grad u||_F=sqrt(28)exp(-t)/sigma^2 and ||curl u||=sqrt(56)exp(-t)/sigma^2.
The true global maxima are at least these values. A reported peak below a
threshold fraction of these lower bounds must underestimate the true maximum;
a peak above them does not establish accuracy. Floating-point evaluation only.
"""
import json
import math
from pathlib import Path


def bound_report(d):
    p=d['parameters']; c=math.exp(-p['end'])/p['sigma']**2
    output={}
    for metric,lower in [('gradient',math.sqrt(28)*c),('vorticity',math.sqrt(56)*c)]:
        observed=d['computed'][f'max_{metric}_fd2']
        output[metric]={'analytic_peak_lower_bound':lower,
                        'reported_fd2_peak':observed,
                        'relative_underestimation_lower_bound':max(0.,1-observed/lower)}
    return output


if __name__=='__main__':
    result={p.parent.name:bound_report(json.loads(p.read_text()))
            for p in sorted(Path('work/of13-study-v1').glob('*/diagnostics.json'))}
    print(json.dumps(result,indent=2))
