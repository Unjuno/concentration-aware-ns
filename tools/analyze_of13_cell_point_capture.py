"""Check captured cellPoint identities/topology without claiming continuum bounds."""
import argparse,csv,json,hashlib
from pathlib import Path
import numpy as np


def read_csv(path):
    with Path(path).open() as stream:
        reader=csv.reader(stream);header=next(reader);rows=list(reader)
    array=np.array(rows,dtype=float)
    if array.ndim!=2 or array.shape[1]!=len(header) or not np.isfinite(array).all():
        raise ValueError('complete finite CSV required')
    return {key:array[:,j] for j,key in enumerate(header)}


def validate(cells,points,tets,faces,summary):
    for table,key in ((cells,'cell'),(points,'point'),(faces,'face')):
        if not np.array_equal(table[key],np.arange(len(table[key]))):raise ValueError('ordered complete labels required')
    for table,keys in ((tets,('cell','face','tetPt','p0','p1','p2')),(faces,('owner','neighbour','base'))):
        for key in keys:
            if not np.array_equal(table[key],np.floor(table[key])):raise ValueError('integer addressing required')
    count=len(cells['cell']);npoints=len(points['point']);nfaces=len(faces['face'])
    if (summary['cells']!=count or summary['points']!=npoints or summary['internal_faces']!=nfaces
        or summary['tets']!=len(tets['cell'])):raise ValueError('capture summary counts differ')
    tc=tets['cell'].astype(int);tf=tets['face'].astype(int)
    if np.any(tc<0) or np.any(tc>=count):raise ValueError('bad cell addressing')
    for key in ('p0','p1','p2'):
        if np.any(tets[key]<0) or np.any(tets[key]>=npoints):raise ValueError('bad point addressing')
    if np.any(faces['owner']<0) or np.any(faces['owner']>=count) or np.any(faces['neighbour']<0) or np.any(faces['neighbour']>=count):raise ValueError('bad face addressing')
    centre=np.sqrt(sum((cells['I'+a]-cells['U'+a])**2 for a in 'xyz'))
    trace=np.sqrt(sum((faces['O'+a]-faces['N'+a])**2 for a in 'xyz'))
    if not np.allclose(centre.max(),summary['maximum_centre_interpolation_error'],atol=1e-15,rtol=1e-9):raise ValueError('centre summary mismatch')
    if not np.allclose(trace.max(),summary['maximum_internal_face_trace_difference'],atol=1e-15,rtol=1e-9):raise ValueError('face summary mismatch')
    counts={}
    for row in range(len(tc)):
        f=int(tf[row])
        if f<nfaces:
            key=(f,*sorted(int(tets[k][row]) for k in ('p0','p1','p2')))
            counts.setdefault(key,[]).append(int(tc[row]))
    matched=all(sorted(side)==sorted([int(faces['owner'][key[0]]),int(faces['neighbour'][key[0]])]) for key,side in counts.items())
    represented={key[0] for key in counts}
    matched=matched and represented==set(range(nfaces))
    volume=np.bincount(tc,weights=np.abs(tets['volume']),minlength=count)
    volume_error=float(np.max(np.abs(volume-cells['V'])/cells['V']))
    det_safe=bool(np.all(np.abs(tets['det'])>=summary['small']))
    return {'status':'MEASURED_CAPTURE_IDENTITIES_NOT_CONTINUUM_CERTIFICATION',
            'cells':count,'points':npoints,'tets':len(tc),'internal_faces':nfaces,
            'maximum_centre_error':float(centre.max()),'maximum_face_trace_difference':float(trace.max()),
            'shared_internal_face_triangles_match_owner_neighbour':bool(matched),
            'maximum_cell_tet_volume_relative_mismatch':volume_error,
            'all_recorded_tet_determinants_above_native_small':det_safe,
            'native_degenerate_and_invalid_base_counts_zero':summary['near_degenerate_tets']==summary['invalid_face_base_indices']==0,
            'limits':['CSV and topology checks, floating volume sum; no outward-enclosed geometric partition proof',
                      'face samples do not by themselves certify global continuity',
                      'no solver quality threshold or point-witness transfer is upgraded']}


def analyze(evidence,output):
    evidence=Path(evidence);output=Path(output)
    if output.exists():raise FileExistsError('preserve prior analysis')
    receipt=json.loads((evidence/'capture-manifest.json').read_text())
    if receipt['status']!='CAPTURE_COMPLETE_NOT_CONTINUUM_CERTIFICATION' or receipt['exit_code']!=0:
        raise ValueError('successful capture required')
    directory=evidence/'capture'
    for name,digest in receipt['capture_files_sha256'].items():
        if hashlib.sha256((directory/name).read_bytes()).hexdigest()!=digest:raise ValueError('capture digest mismatch')
    data={name:read_csv(directory/(name+'.csv')) for name in ('cells','points','tets','faces')}
    result=validate(**data,summary=receipt['summary']);output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--evidence',required=True,type=Path);p.add_argument('--output',required=True,type=Path)
    a=p.parse_args();analyze(a.evidence,a.output)
