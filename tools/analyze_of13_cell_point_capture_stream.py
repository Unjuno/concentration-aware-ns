"""Check all native capture rows with batched CSVs and disk-backed triangle keys."""
import argparse,json,sqlite3,tempfile
from pathlib import Path
import numpy as np
from tools.cell_point_capture_chunks import chunks,TET_HEADER
from tools.run_amr_mean_quality import sha

CELL_HEADER=('cell','V','cx','cy','cz','Ux','Uy','Uz','Ix','Iy','Iz')
POINT_HEADER=('point','x','y','z','Ux','Uy','Uz')
FACE_HEADER=('face','owner','neighbour','base','cx','cy','cz','Ox','Oy','Oz','Nx','Ny','Nz')


def integer(values):
    if np.any(values!=np.floor(values)) or np.any(values<0) or np.any(values>=2**53):raise ValueError('nonnegative exact integer addressing required')
    return values.astype(np.int64)


def ordered(batch,key,offset,count):
    labels=integer(batch[key]);size=len(labels)
    if offset+size>count or not np.array_equal(labels,np.arange(offset,offset+size)):raise ValueError('ordered complete native labels required')
    return size


def measure(directory,summary,scratch,chunk_size=10000):
    directory=Path(directory);scratch=Path(scratch)
    nc,npnt,nf,nt=(summary[k] for k in ('cells','points','internal_faces','tets'))
    if any(type(n) is not int or n<=0 for n in (nc,npnt,nf,nt)):raise ValueError('positive native counts required')
    volumes=np.empty(nc);owner=np.empty(nf,dtype=np.int64);neighbour=owner.copy()
    offset=0;centre_error=0.
    for b in chunks(directory/'cells.csv',CELL_HEADER,chunk_size):
        size=ordered(b,'cell',offset,nc)
        if np.any(b['V']<=0):raise ValueError('positive cell volumes required')
        volumes[offset:offset+size]=b['V'];centre_error=max(centre_error,float(np.sqrt(sum((b['I'+a]-b['U'+a])**2 for a in 'xyz')).max()));offset+=size
    if offset!=nc:raise ValueError('missing cells')
    offset=0
    for b in chunks(directory/'points.csv',POINT_HEADER,chunk_size):offset+=ordered(b,'point',offset,npnt)
    if offset!=npnt:raise ValueError('missing points')
    offset=0;trace_error=0.
    for b in chunks(directory/'faces.csv',FACE_HEADER,chunk_size):
        size=ordered(b,'face',offset,nf);o,n,base=(integer(b[k]) for k in ('owner','neighbour','base'))
        if np.any(o>=nc) or np.any(n>=nc) or np.any(o==n):raise ValueError('invalid face adjacency')
        owner[offset:offset+size]=o;neighbour[offset:offset+size]=n
        trace_error=max(trace_error,float(np.sqrt(sum((b['O'+a]-b['N'+a])**2 for a in 'xyz')).max()));offset+=size
    if offset!=nf:raise ValueError('missing faces')
    if not np.isclose(centre_error,summary['maximum_centre_interpolation_error'],atol=1e-15,rtol=1e-9):raise ValueError('centre summary mismatch')
    if not np.isclose(trace_error,summary['maximum_internal_face_trace_difference'],atol=1e-15,rtol=1e-9):raise ValueError('face summary mismatch')
    total_volume=np.zeros(nc);offset=0;safe=True;valid_sides=True
    scratch.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cell-point-triangles-',dir=scratch) as tmp:
        connection=sqlite3.connect(str(Path(tmp)/'triangles.sqlite'))
        try:
            connection.execute('PRAGMA cache_size=-8192')
            connection.execute('CREATE TABLE tri(face INTEGER,p0 INTEGER,p1 INTEGER,p2 INTEGER,oc INTEGER,nc INTEGER,PRIMARY KEY(face,p0,p1,p2)) WITHOUT ROWID')
            statement='INSERT INTO tri VALUES (?,?,?,?,?,?) ON CONFLICT(face,p0,p1,p2) DO UPDATE SET oc=oc+excluded.oc,nc=nc+excluded.nc'
            for b in chunks(directory/'tets.csv',TET_HEADER,chunk_size):
                tc,tf,tp,p0,p1,p2=(integer(b[k]) for k in ('cell','face','tetPt','p0','p1','p2'))
                if np.any(tc>=nc) or any(np.any(p>=npnt) for p in (p0,p1,p2)):raise ValueError('invalid tet node addressing')
                safe=safe and bool(np.all(np.abs(b['det'])>=summary['small']))
                total_volume+=np.bincount(tc,weights=np.abs(b['volume']),minlength=nc)
                internal=tf<nf;faces=tf[internal];cells=tc[internal];triangles=np.sort(np.stack((p0[internal],p1[internal],p2[internal]),axis=1),axis=1)
                o=cells==owner[faces];n=cells==neighbour[faces];valid_sides=valid_sides and bool(np.all(o|n))
                records=((int(f),int(p[0]),int(p[1]),int(p[2]),int(own),int(nei)) for f,p,own,nei in zip(faces,triangles,o,n))
                connection.executemany(statement,records);connection.commit();offset+=len(tc)
            if offset!=nt:raise ValueError('missing or excess tets')
            bad=connection.execute('SELECT COUNT(*) FROM tri WHERE oc!=1 OR nc!=1').fetchone()[0]
            covered=connection.execute('SELECT COUNT(DISTINCT face) FROM tri').fetchone()[0]
            keys=connection.execute('SELECT COUNT(*) FROM tri').fetchone()[0]
        finally:connection.close()
    return {'status':'MEASURED_CAPTURE_IDENTITIES_NOT_CONTINUUM_CERTIFICATION','cells':nc,'points':npnt,'tets':nt,'internal_faces':nf,
            'maximum_centre_error':centre_error,'maximum_face_trace_difference':trace_error,
            'shared_internal_face_triangles_match_owner_neighbour':bool(valid_sides and bad==0 and covered==nf),
            'maximum_cell_tet_volume_relative_mismatch':float(np.max(np.abs(total_volume-volumes)/volumes)),
            'all_recorded_tet_determinants_above_native_small':safe,
            'native_degenerate_and_invalid_base_counts_zero':summary['near_degenerate_tets']==summary['invalid_face_base_indices']==0,
            'disk_backed_internal_triangle_keys':keys,'csv_chunk_size':chunk_size,
            'limits':['Floating volume sums and sampled face traces, not outward-enclosed geometry/continuity proof',
                      'Cell volumes and internal-face owner/neighbour arrays remain resident; triangle keys use temporary SQLite storage',
                      'Batch summation may differ in last floating bits from the old all-at-once diagnostic',
                      'Original quality gates and point-witness/native branch obligations unchanged']}


def analyze(evidence,output,scratch,chunk_size=10000):
    evidence=Path(evidence);output=Path(output)
    if output.exists():raise FileExistsError('preserve prior analysis')
    r=json.loads((evidence/'capture-manifest.json').read_text())
    if r['status']!='CAPTURE_COMPLETE_NOT_CONTINUUM_CERTIFICATION' or r['exit_code']!=0:raise ValueError('complete native capture required')
    for name,digest in r['capture_files_sha256'].items():
        if sha(evidence/'capture'/name)!=digest:raise ValueError('capture digest mismatch')
    result=measure(evidence/'capture',r['summary'],scratch,chunk_size)
    output.parent.mkdir(parents=True,exist_ok=True);output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for name in ('evidence','output','scratch'):p.add_argument('--'+name,type=Path,required=True)
    p.add_argument('--chunk-size',type=int,default=10000);a=p.parse_args();analyze(a.evidence,a.output,a.scratch,a.chunk_size)
