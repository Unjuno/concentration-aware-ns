"""Read finite native CSV data in bounded row batches."""
import csv,itertools
import numpy as np


def chunks(path,expected_header,chunk_size=10000):
    if type(chunk_size) is not int or chunk_size<=0:raise ValueError('positive integer chunk size required')
    with open(path) as stream:
        reader=csv.reader(stream)
        if next(reader,None)!=list(expected_header):raise ValueError('unexpected CSV header')
        while rows:=list(itertools.islice(reader,chunk_size)):
            try:array=np.array(rows,dtype=float)
            except (ValueError,TypeError):raise ValueError('complete numeric CSV rows required') from None
            if array.shape!=(len(rows),len(expected_header)) or not np.isfinite(array).all():
                raise ValueError('complete finite CSV rows required')
            yield {key:array[:,j] for j,key in enumerate(expected_header)}


def nodes(path,kind,count,chunk_size=10000):
    if kind=='cells':header=('cell','V','cx','cy','cz','Ux','Uy','Uz','Ix','Iy','Iz');label='cell';coords=('cx','cy','cz')
    elif kind=='points':header=('point','x','y','z','Ux','Uy','Uz');label='point';coords=tuple('xyz')
    else:raise ValueError('unknown native node kind')
    if type(count) is not int or count<=0:raise ValueError('positive native node count required')
    position=np.empty((count,3));values=np.empty((count,3));offset=0
    for batch in chunks(path,header,chunk_size):
        size=len(batch[label])
        if offset+size>count or not np.array_equal(batch[label],np.arange(offset,offset+size)):
            raise ValueError('incomplete or unordered native node labels')
        if kind=='cells' and np.any(batch['V']<=0):raise ValueError('positive cell volumes required')
        position[offset:offset+size]=np.stack([batch[a] for a in coords],axis=1)
        values[offset:offset+size]=np.stack([batch['U'+a] for a in 'xyz'],axis=1);offset+=size
    if offset!=count:raise ValueError('missing native nodes')
    return position,values

TET_HEADER=('cell','face','tetPt','p0','p1','p2','det','volume','w0','w1','w2','w3')
