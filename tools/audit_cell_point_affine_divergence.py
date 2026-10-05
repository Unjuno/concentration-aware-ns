"""Enclose affine interpolation divergence, separate from discrete mass balance."""
import argparse,json
from pathlib import Path
from flint import arb,ctx
from tools.run_amr_mean_quality import ROOT,sha
from tools.cell_point_local_derivative import affine_gradient
from tools.audit_cell_point_uniform_ball_error import dyadic_lower
from tools.amr_arb_mean_certificate import endpoints,reference_bounds


def certificate(vertices,values):
    g,_,_=affine_gradient(vertices,values);trace=sum((g[i,i] for i in range(3)),arb(0))
    absolute=arb(0) if trace.contains(0) else abs(trace).lower()
    floor=dyadic_lower(absolute);distance=dyadic_lower(absolute/arb(3).sqrt().upper())
    _,peak,_=reference_bounds('0.05',3)
    return {'status':'NONZERO_IDEALIZED_AFFINE_DIVERGENCE' if not trace.contains(0) else 'NONZERO_DIVERGENCE_NOT_CERTIFIED',
            'signed_divergence':endpoints(trace),'absolute_divergence_lower':endpoints(floor),
            'distance_to_trace_free_gradient_lower':endpoints(distance),
            'gradient_error_relative_reference_peak_lower_from_trace':endpoints(dyadic_lower(distance/peak.upper())),
            'lower_bound_quantization_bits':32}


def audit(output,source_commit):
    output=Path(output)
    if output.exists():raise FileExistsError('preserve previous divergence audit')
    old=ctx.prec;ctx.prec=128
    try:
        records={}
        for case in ('n16-dt0.001','n32-dt0.001','n64-dt0.001','n32-dt0.0005'):
            path=ROOT/'evidence/cell-point-derivative-batches-v1'/case/'analysis.json';w=json.loads(path.read_text())
            if w['status']!='ENCLOSED_LOCAL_IDEALIZED_AFFINE_PIECE_WITNESS' or w['case_id']!=case:
                raise ValueError('wrong enclosed witness')
            records[case]={**certificate(w['witness']['vertices'],w['witness']['nodal_values']),
                           'witness_sha256':sha(path),'capture_manifest_sha256':w['capture_manifest_sha256']}
    finally:ctx.prec=old
    result={'status':'ENCLOSED_IDEALIZED_AFFINE_DIVERGENCE_AUDIT','numeric_source_commit':source_commit,'precision_bits':128,'cases':records,
            'limits':['Constant divergence of decoded-node real-affine pieces only','Any trace-free gradient differs by at least abs(trace)/sqrt(3); no reconstruction correction executed','No discrete face-flux mass-balance failure, global pressure or physical claim']}
    output.mkdir(parents=True);(output/'analysis.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n');print(json.dumps(result),flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);p.add_argument('--source-commit',required=True);a=p.parse_args();audit(a.output,a.source_commit)
