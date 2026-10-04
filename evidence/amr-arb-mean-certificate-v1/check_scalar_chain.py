"""Validate only the rational scalar inequality chain, not the FFT enclosures."""
import json
from fractions import Fraction as Q
from pathlib import Path
import sys


def check(record):
    checked=[]
    for row in record['cases']:
        c=row['certificate'];endpoint=lambda name,side:Q(c[name][side+'_rational'])
        norm=endpoint('centered_p0_norm','lower');h=endpoint('hminus_upper','upper')
        lower=endpoint('gradient_absolute_lower','lower')
        l2=endpoint('gradient_relative_l2_lower','lower')
        peak=endpoint('gradient_relative_peak_error_lower','lower')
        curl=endpoint('solenoidal_curl_relative_peak_error_lower','lower')
        if not (norm>0 and h>0 and lower>0):raise ValueError('positive bounds required')
        if lower*lower*h>norm*norm:raise ValueError('absolute lower exceeds certified scalar chain')
        if l2*l2*endpoint('reference_gradient_mean_square','upper')>lower*lower:raise ValueError('L2 normalization fails')
        if peak*endpoint('reference_gradient_peak_upper','upper')>lower:raise ValueError('gradient peak normalization fails')
        if curl*endpoint('reference_curl_peak_upper','upper')>lower:raise ValueError('curl peak normalization fails')
        if (peak>Q(1,20))!=c['strictly_above_five_percent_peak_error']:raise ValueError('gradient threshold mismatch')
        if (curl>Q(1,20))!=c['solenoidal_curl_strictly_above_five_percent_peak_error']:raise ValueError('curl threshold mismatch')
        checked.append(row['case_id'])
    return {'status':'PASS_RATIONAL_SCALAR_CHAIN_ONLY','cases':checked,
            'limits':'Does not independently prove raw-input interpretation, DFT ball enclosures, alias inequality or reference peak theorem.'}


if __name__=='__main__':print(json.dumps(check(json.loads(Path(sys.argv[1]).read_text()))))
