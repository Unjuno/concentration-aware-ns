"""Select a captured tet witness, certify its idealized local affine derivative."""
import argparse,json,hashlib
from pathlib import Path
import numpy as np
from flint import ctx
from tools.analyze_of13_cell_point_capture import read_csv
from tools.cell_point_local_derivative import certificate
from tools.high_gradient_reference import fields


def audit(evidence,output,source_commit):
    evidence=Path(evidence);output=Path(output)
    if output.exists():raise FileExistsError('preserve prior witness')
    receipt=json.loads((evidence/'capture-manifest.json').read_text())
    if receipt['status']!='CAPTURE_COMPLETE_NOT_CONTINUUM_CERTIFICATION' or receipt['exit_code']!=0:
        raise ValueError('successful native capture required')
    for name,digest in receipt['capture_files_sha256'].items():
        if hashlib.sha256((evidence/'capture'/name).read_bytes()).hexdigest()!=digest:raise ValueError('capture digest mismatch')
    c,p,t=(read_csv(evidence/'capture'/(name+'.csv')) for name in ('cells','points','tets'))
    coords=np.stack([c[k] for k in ('cx','cy','cz')],axis=1);u=np.stack([c['U'+a] for a in 'xyz'],axis=1)
    points=np.stack([p[a] for a in 'xyz'],axis=1);pu=np.stack([p['U'+a] for a in 'xyz'],axis=1)
    cells=t['cell'].astype(int);indices=np.stack([t[k].astype(int) for k in ('p0','p1','p2')],axis=1)
    vertices=np.concatenate((coords[cells,None,:],points[indices]),axis=1)
    values=np.concatenate((u[cells,None,:],pu[indices]),axis=1)
    a=vertices[:,1:]-vertices[:,:1];d=values[:,1:]-values[:,:1]
    gradients=np.swapaxes(np.linalg.solve(a,d),1,2)
    errors=gradients-fields(vertices.mean(axis=1),N=3,time=.05)['grad_u']
    row=int(np.argmax(np.linalg.norm(errors,axis=(1,2))))
    old=ctx.prec;ctx.prec=96
    try:result=certificate(vertices[row],values[row])
    finally:ctx.prec=old
    record={'status':'ENCLOSED_LOCAL_IDEALIZED_AFFINE_PIECE_WITNESS','numerical_source_commit':source_commit,
            'capture_source_commit':'4999a4db38d0ac41a5f253a6665f6701d64f561c','precision_bits':96,
            'tet_csv_row':row,'cell':int(cells[row]),'face':int(t['face'][row]),'point_indices':indices[row].tolist(),
            'witness':result,'capture_manifest_sha256':hashlib.sha256((evidence/'capture-manifest.json').read_bytes()).hexdigest(),
            'limits':['Idealized real-arithmetic piece of the explicit barycentric overload; not floating point-query branch certification',
                      'Strict interior centroid of one nondegenerate tet; no global geometry/continuity or maximum search certificate',
                      'Curl computed directly from this derivative, not inferred from the older point-chord gradient bound',
                      'Original solver quality gates and physical interpretation unchanged']}
    output.mkdir(parents=True);(output/'analysis.json').write_text(json.dumps(record,indent=2,allow_nan=False)+'\n')
    print(json.dumps({'tet_row':row,'gradient_lower':result['gradient_relative_reference_peak_error_lower']['display_lower'],
                      'curl_lower':result['curl_relative_reference_peak_error_lower']['display_lower']}))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--evidence',required=True,type=Path)
    p.add_argument('--output',required=True,type=Path);p.add_argument('--source-commit',required=True)
    a=p.parse_args();audit(a.evidence,a.output,a.source_commit)
