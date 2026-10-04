"""Enclose a fixed-radius neighborhood of a hash-bound matrix witness."""
import argparse,json
from pathlib import Path
import numpy as np
from flint import arb,ctx
from tools.run_amr_mean_quality import sha
from tools.cell_point_capture_chunks import chunks,TET_HEADER
from tools.cell_point_local_neighborhood import unique_neighborhood
from tools.amr_point_gradient_bound import exact_float


def selected_nodes(path,header,label,axes,wanted,count,chunk_size):
    result={};offset=0
    for batch in chunks(path,header,chunk_size):
        size=len(batch[label])
        if not np.array_equal(batch[label],np.arange(offset,offset+size)):
            raise ValueError('unordered native labels')
        for i in wanted.intersection(range(offset,offset+size)):
            result[i]=[float(batch[a][i-offset]) for a in axes]
        offset+=size
    if offset!=count or set(result)!=wanted:raise ValueError('incomplete native nodes')
    return result


def audit(capture,witness,output,source_commit,chunk_size=10000):
    capture=Path(capture);witness=Path(witness);output=Path(output)
    if output.exists():raise FileExistsError('preserve prior certificate')
    previous=json.loads(witness.read_text());receipt=json.loads((capture/'capture-manifest.json').read_text())
    if sha(capture/'capture-manifest.json')!=previous['capture_manifest_sha256']:
        raise ValueError('wrong capture manifest')
    if previous['status']!='ENCLOSED_LOCAL_IDEALIZED_AFFINE_PIECE_WITNESS':
        raise ValueError('enclosed derivative witness required')
    for n,d in receipt['capture_files_sha256'].items():
        if sha(capture/'capture'/n)!=d:raise ValueError('candidate digest mismatch')
    summary=receipt['summary'];cell=previous['cell'];selected=[];offset=0;target=-1
    for batch in chunks(capture/'capture/tets.csv',TET_HEADER,chunk_size):
        for key,limit in [('cell',summary['cells']),('p0',summary['points']),('p1',summary['points']),('p2',summary['points'])]:
            a=batch[key]
            if np.any(a!=np.floor(a)) or np.any(a<0) or np.any(a>=limit):raise ValueError('invalid node addressing')
        for i in np.flatnonzero(batch['cell']==cell):
            r={k:float(v[i]) for k,v in batch.items()};row=offset+int(i)
            if row==previous['tet_csv_row']:target=len(selected)
            selected.append((row,r))
        offset+=len(batch['cell'])
    if offset!=summary['tets'] or target<0:raise ValueError('incomplete candidate stream')
    ids={int(r['p'+str(j)]) for _,r in selected for j in range(3)}
    c=selected_nodes(capture/'capture/cells.csv',('cell','V','cx','cy','cz','Ux','Uy','Uz','Ix','Iy','Iz'),'cell',('cx','cy','cz'),{cell},summary['cells'],chunk_size)[cell]
    points=selected_nodes(capture/'capture/points.csv',('point','x','y','z','Ux','Uy','Uz'),'point',tuple('xyz'),ids,summary['points'],chunk_size)
    vertices=[[c]+[points[int(r['p'+str(j)])] for j in range(3)] for _,r in selected]
    r=selected[target][1]
    if vertices[target]!=previous['witness']['vertices'] or int(r['face'])!=previous['face'] or int(r['tetPt'])!=previous['tetPt']:
        raise ValueError('target witness differs')
    old=ctx.prec;ctx.prec=128
    try:
        centre=[sum((exact_float(v[j]) for v in vertices[target]),arb(0))/4 for j in range(3)]
        result=unique_neighborhood(vertices,target,centre,arb(1)/4096)
    finally:ctx.prec=old
    result.update(case_id=previous['case_id'],numerical_source_commit=source_commit,witness_sha256=sha(witness),capture_manifest_sha256=previous['capture_manifest_sha256'],precision_bits=128,screened_tets=offset,cell=cell,candidate_labels=[{'tet_csv_row':i,'face':int(r['face']),'tetPt':int(r['tetPt'])} for i,r in selected],limits=['Fixed exploratory radius 1/4096; failure preserved without adaptive retries','Complete candidates of one cell; no global partition or floating position-query certification','Decoded-node real arithmetic; no original gate or physical claim'])
    output.mkdir(parents=True);(output/'analysis.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps({'case_id':previous['case_id'],'status':result['status'],'candidates':len(selected)}),flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for k in ('capture','witness','output'):p.add_argument('--'+k,type=Path,required=True)
    p.add_argument('--source-commit',required=True);p.add_argument('--chunk-size',type=int,default=10000)
    a=p.parse_args();audit(a.capture,a.witness,a.output,a.source_commit,a.chunk_size)
