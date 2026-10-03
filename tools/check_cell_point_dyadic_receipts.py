"""Standard-library scalar check of conservative published dyadic bounds.

Does not prove reference formulas, native geometry or the interval kernel.
"""
import argparse,json,hashlib
from pathlib import Path
from fractions import Fraction


def exact_point(record):
    lo=Fraction(record['lower_rational']);hi=Fraction(record['upper_rational'])
    if lo!=hi:raise ValueError('exact rational lower-bound point required')
    return lo


def check_bounds(old,new,witness):
    if new['lower_bound_quantization_bits']!=32 or old['case_id']!=new['case_id']:
        raise ValueError('quantization/case identity differs')
    step=Fraction(1,1<<32);result={}
    for kind in ('gradient','curl'):
        raw=exact_point(old[kind+'_error_lower']);absolute=exact_point(new[kind+'_error_lower'])
        relative=exact_point(new[kind+'_relative_reference_peak_error_lower'])
        peak=Fraction(witness['reference_'+kind+'_peak_upper']['upper_rational'])
        if raw<=0 or peak<=0:raise ValueError('positive source lower bound and reference upper required')
        if (absolute/step).denominator!=1 or (relative/step).denominator!=1:
            raise ValueError('non-dyadic published lower bound')
        if not absolute<=raw<absolute+step:raise ValueError('absolute bound is not conservative grid floor')
        # This independently uses the earlier, slightly wider reference peak
        # upper enclosure. It must still support the new normalized assertion.
        if not relative<=absolute/peak<relative+step:
            raise ValueError('relative bound unsupported by independent reference enclosure')
        result[kind]={'absolute_lower':str(absolute),'relative_lower':str(relative),'reference_peak_upper':str(peak),'absolute_floor_verified':True,'independent_normalization_verified':True}
    return result


def check(root):
    root=Path(root);results={}
    for key in ('n32','n64','n32half'):
        protocol=root/f'protocols/of13-cell-point-matrix-query-{key}-v1.json';spec=json.loads(protocol.read_text())
        wp=root/spec['witness_path']
        if hashlib.sha256(wp.read_bytes()).hexdigest()!=spec['witness_sha256']:
            raise ValueError('witness hash differs from protocol')
        old=json.loads((root/f'evidence/cell-point-uniform-ball-error-v1/{key}/analysis.json').read_text())
        new=json.loads((root/f'evidence/cell-point-uniform-ball-error-v2/{key}/analysis.json').read_text())
        for r in (old,new):
            if r['case_id']!=spec['case_id'] or r['witness_sha256']!=spec['witness_sha256'] or r['neighborhood_sha256']!=spec['neighborhood_sha256']:
                raise ValueError('bound identity differs from protocol')
        results[key]=check_bounds(old,new,json.loads(wp.read_text())['witness'])
    return {'status':'EXACT_RATIONAL_DYADIC_SCALAR_CHAIN_VERIFIED','results':results,'limits':['Checks scalar implications against recorded bounds; does not prove upstream reference formulas','Does not reconstruct geometry or prove correctness of the Arb kernel','No physical or original acceptance-gate claim']}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    if a.output.exists():raise FileExistsError('preserve previous verification')
    r=check(a.root);a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(r,indent=2)+'\n');print(r['status'])
