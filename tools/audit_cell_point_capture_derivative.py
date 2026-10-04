"""Screen native affine pieces in bounded batches, enclose one local witness."""
import argparse,json
from pathlib import Path
import numpy as np
from flint import ctx
from tools.run_amr_mean_quality import ROOT,sha,SOURCE_FILES
from tools.cell_point_capture_chunks import chunks,nodes,TET_HEADER
from tools.cell_point_local_derivative import certificate
from tools.high_gradient_reference import fields


def audit(capture,output,source_commit,chunk_size=10000):
    capture=Path(capture);output=Path(output)
    if output.exists():raise FileExistsError('preserve prior witness')
    receipt=json.loads((capture/'capture-manifest.json').read_text());base=json.loads((capture/'base/manifest.json').read_text())
    case=base['case_id']
    if case not in ('n16-dt0.001','n32-dt0.001','n64-dt0.001','n32-dt0.0005'):raise ValueError('case outside original matrix')
    original=json.loads((ROOT/'evidence/of13-amr-mean-quality-v1'/case/'manifest.json').read_text())
    current=next(r for r in base['runs'] if r['label']=='main');old=next(r for r in original['runs'] if r['label']=='main')
    if (receipt['status']!='CAPTURE_COMPLETE_NOT_CONTINUUM_CERTIFICATION' or receipt['exit_code']!=0
            or receipt['field_sha256_before']!=receipt['field_sha256_after']
            or current['inputs_sha256']!=old['inputs_sha256']
            or current['final_field_sha256']!=old['final_field_sha256']
            or current['final_field_sha256']!=receipt['field_sha256_after']):raise ValueError('native capture/input/final field integrity incomplete')
    if (set(base['source_files_sha256'])!=set(SOURCE_FILES) or base['source_files_sha256']!=original['source_files_sha256']
            or any(sha(ROOT/p)!=h for p,h in base['source_files_sha256'].items())):raise ValueError('original recipe differs')
    for n,h in receipt['capture_files_sha256'].items():
        if sha(capture/'capture'/n)!=h:raise ValueError('captured CSV/source digest mismatch')
    reference_sources=json.loads((ROOT/'evidence/of13-cell-point-capture-v1-n16/capture-manifest.json').read_text())
    if (receipt['upstream_commit']!=reference_sources['upstream_commit'] or receipt['upstream_files_sha256']!=reference_sources['upstream_files_sha256']
            or not receipt['installed_sources_match_pin']):raise ValueError('native interpolation pin differs')
    summary=receipt['summary'];directory=capture/'capture'
    coords,u=nodes(directory/'cells.csv','cells',summary['cells'],chunk_size)
    points,pu=nodes(directory/'points.csv','points',summary['points'],chunk_size)
    offset=0;best=None;maximum=-1.
    for batch in chunks(directory/'tets.csv',TET_HEADER,chunk_size):
        size=len(batch['cell'])
        for key in ('cell','face','tetPt','p0','p1','p2'):
            if np.any(batch[key]!=np.floor(batch[key])) or np.any(batch[key]<0):raise ValueError('invalid native integer addressing')
        cells=batch['cell'].astype(np.int64);indices=np.stack([batch['p'+str(j)].astype(np.int64) for j in range(3)],axis=1)
        if np.any(cells>=len(coords)) or np.any(indices>=len(points)):raise ValueError('out-of-range node addressing')
        if np.any(np.abs(batch['det'])<summary['small']):raise ValueError('native degenerate candidate')
        vertices=np.concatenate((coords[cells,None,:],points[indices]),axis=1)
        values=np.concatenate((u[cells,None,:],pu[indices]),axis=1)
        try:g=np.swapaxes(np.linalg.solve(vertices[:,1:]-vertices[:,:1],values[:,1:]-values[:,:1]),1,2)
        except np.linalg.LinAlgError:raise ValueError('singular candidate in floating screen') from None
        error=np.linalg.norm(g-fields(vertices.mean(axis=1),N=3,time=.05)['grad_u'],axis=(1,2))
        if not np.isfinite(error).all():raise ValueError('nonfinite floating screen')
        row=int(np.argmax(error))
        if error[row]>maximum:
            maximum=float(error[row]);best={'tet_csv_row':offset+row,'cell':int(cells[row]),'face':int(batch['face'][row]),'tetPt':int(batch['tetPt'][row]),'point_indices':indices[row].tolist(),'vertices':vertices[row].copy(),'values':values[row].copy()}
        offset+=size
    if offset!=summary['tets'] or best is None:raise ValueError('incomplete tetrahedron stream')
    old_precision=ctx.prec;ctx.prec=96
    try:result=certificate(best.pop('vertices'),best.pop('values'))
    finally:ctx.prec=old_precision
    record={'status':'ENCLOSED_LOCAL_IDEALIZED_AFFINE_PIECE_WITNESS','case_id':case,'numerical_source_commit':source_commit,'capture_source_commit':base['source_commit'],'precision_bits':96,'screened_tets':offset,'chunk_size':chunk_size,**best,'witness':result,'capture_manifest_sha256':sha(capture/'capture-manifest.json'),'limits':['Floating batched screen selects one witness, not a global maximum certificate','Exact decoded-node real-affine piece; native position branch/global continuity remain separate','Original gates and physical interpretation unchanged']}
    output.mkdir(parents=True);(output/'analysis.json').write_text(json.dumps(record,indent=2,allow_nan=False)+'\n')
    print(json.dumps({'case_id':case,'row':best['tet_csv_row'],'screened_tets':offset,'gradient_lower':result['gradient_relative_reference_peak_error_lower']['display_lower'],'curl_lower':result['curl_relative_reference_peak_error_lower']['display_lower']}),flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--capture',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--source-commit',required=True);p.add_argument('--chunk-size',type=int,default=10000)
    a=p.parse_args();audit(a.capture,a.output,a.source_commit,a.chunk_size)
