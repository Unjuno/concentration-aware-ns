"""Hash-check captured candidates and enclose a unique local affine region."""
import argparse,json
from pathlib import Path
from flint import arb,ctx
from tools.run_amr_mean_quality import ROOT,sha
from tools.analyze_of13_cell_point_query import rows
from tools.cell_point_local_neighborhood import unique_neighborhood
from tools.amr_point_gradient_bound import exact_float


def audit(capture,output,source_commit):
    capture=Path(capture);output=Path(output)
    if output.exists():raise FileExistsError('preserve prior certificate')
    previous=json.loads((ROOT/'evidence/cell-point-local-derivative-v1/analysis.json').read_text())
    if sha(capture/'capture-manifest.json')!=previous['capture_manifest_sha256']:raise ValueError('wrong capture manifest')
    receipt=json.loads((capture/'capture-manifest.json').read_text())
    for n,d in receipt['capture_files_sha256'].items():
        if sha(capture/'capture'/n)!=d:raise ValueError('captured candidate digest mismatch')
    cells,points,tets=(rows(capture/'capture'/(n+'.csv')) for n in ('cells','points','tets'))
    cell=previous['cell'];c=cells[cell]
    if c['cell']!=cell or any(p['point']!=i for i,p in enumerate(points)):raise ValueError('invalid captured addressing')
    selected=[(i,r) for i,r in enumerate(tets) if r['cell']==cell]
    candidate_vertices=[];labels=[];target=-1
    for k,(i,r) in enumerate(selected):
        ids=[int(r['p'+str(j)]) for j in range(3)]
        v=[[c['c'+a] for a in 'xyz']]+[[points[p][a] for a in 'xyz'] for p in ids]
        candidate_vertices.append(v);labels.append({'tet_csv_row':i,'face':int(r['face']),'tetPt':int(r['tetPt']),'point_indices':ids})
        if i==previous['tet_csv_row']:
            if v!=previous['witness']['vertices']:raise ValueError('target nodes differ')
            target=k
    old=ctx.prec;ctx.prec=128
    try:
        centre=[sum((exact_float(v[j]) for v in previous['witness']['vertices']),arb(0))/4 for j in range(3)]
        result=unique_neighborhood(candidate_vertices,target,centre,arb(1)/128)
    finally:ctx.prec=old
    if result['status']!='UNIQUE_IDEALIZED_PIECE_ON_ENCLOSED_BALL':raise ValueError('local ball uniqueness unproved')
    result.update(numerical_source_commit=source_commit,precision_bits=128,cell=cell,capture_manifest_sha256=previous['capture_manifest_sha256'],candidate_labels=labels,
                  limits=['Finite complete candidate list recorded for one captured cell, not global mesh partition/continuity',
                          'Exact decoded-node idealization; floating search predicate and rounding are separate runtime obligations',
                          'No exact cell-average assumption, new evolution, original gate upgrade or physical claim'])
    output.mkdir(parents=True);(output/'analysis.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps({'status':result['status'],'candidates':len(selected),'radius':result['radius']}),flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--capture',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--source-commit',required=True)
    a=p.parse_args();audit(a.capture,a.output,a.source_commit)
