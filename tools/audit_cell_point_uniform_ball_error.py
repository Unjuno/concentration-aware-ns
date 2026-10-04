"""Enclose uniform derivative-error lower bounds on previously certified balls."""
import argparse,json
from pathlib import Path
from flint import arb,ctx,fmpq
from fractions import Fraction
from tools.run_amr_mean_quality import sha
from tools.cell_point_matrix_query_spec import validate_spec
from tools.cell_point_local_derivative import affine_gradient,reference_gradient
from tools.amr_arb_mean_certificate import endpoints,reference_bounds


def norm_lower(components):
    # Componentwise infima may occur at different points: their sum remains
    # a conservative lower bound, without treating interval products as squares.
    total=arb(0)
    for v in components:
        lo=arb(0) if v.contains(0) else abs(v).lower()
        total+=lo*lo
    return total.sqrt().lower()


def dyadic_lower(value,bits=32):
    """Round an enclosed lower endpoint toward minus infinity, exactly."""
    if type(bits) is not int or bits<1:raise ValueError('positive integer grid bits required')
    q=Fraction(endpoints(value.lower())['lower_rational'])
    scale=1<<bits;n=(q.numerator*scale)//q.denominator
    return arb(fmpq(n,scale))


def audit(protocol,output,source_commit):
    protocol=Path(protocol);output=Path(output)
    if output.exists():raise FileExistsError('preserve prior enclosure')
    spec=json.loads(protocol.read_text());w,b=validate_spec(spec)
    old=ctx.prec;ctx.prec=128
    try:
        g,c,_=affine_gradient(w['witness']['vertices'],w['witness']['nodal_values'])
        for x,stored in zip(c,b['centre']):
            if endpoints(x)['lower_rational']!=stored['lower_rational'] or endpoints(x)['upper_rational']!=stored['upper_rational']:
                raise ValueError('ball centre differs from affine centroid')
        radius=arb(1)/4096
        box=[x+arb(0,radius) for x in c]
        error=g-reference_gradient(box)
        grad=dyadic_lower(norm_lower([error[i,j] for i in range(3) for j in range(3)]))
        curl=dyadic_lower(norm_lower([error[2,1]-error[1,2],error[0,2]-error[2,0],error[1,0]-error[0,1]]))
        _,peak,cp=reference_bounds('0.05',3)
        result={'status':'ENCLOSED_UNIFORM_IDEALIZED_BALL_ERROR_LOWER_BOUND','case_id':spec['case_id'],'numerical_source_commit':source_commit,'protocol_sha256':sha(protocol),'witness_sha256':spec['witness_sha256'],'neighborhood_sha256':spec['neighborhood_sha256'],'precision_bits':128,'lower_bound_quantization_bits':32,'radius':endpoints(radius),'reference_box':[endpoints(x) for x in box],'gradient_error_lower':endpoints(grad),'curl_error_lower':endpoints(curl),'gradient_relative_reference_peak_error_lower':endpoints(dyadic_lower(grad/peak.upper())),'curl_relative_reference_peak_error_lower':endpoints(dyadic_lower(curl/cp.upper())),'limits':['Componentwise interval infima on a containing box, not sharp minima','Exact downward dyadic rounding at 32 bits; old unquantized records retained','Certified idealized ball only; native floating search and global continuity remain separate','No CFD evolution, original acceptance upgrade or physical claim']}
    finally:ctx.prec=old
    output.mkdir(parents=True);(output/'analysis.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n');print(json.dumps(result),flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--protocol',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--source-commit',required=True);a=p.parse_args();audit(a.protocol,a.output,a.source_commit)
