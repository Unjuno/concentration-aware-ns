from copy import deepcopy
import numpy as np
from tools.analyze_of13_cell_point_capture import validate


def fixture():
    cells={'cell':np.arange(2),'V':np.full(2,1/6)}
    for a in 'xyz':cells['U'+a]=np.zeros(2);cells['I'+a]=np.zeros(2)
    points={'point':np.arange(3)}
    tets={'cell':np.arange(2),'face':np.zeros(2),'tetPt':np.ones(2),
          'p0':np.zeros(2),'p1':np.array([1,2]),'p2':np.array([2,1]),
          'det':np.ones(2),'volume':np.full(2,1/6)}
    faces={'face':np.array([0]),'owner':np.array([0]),'neighbour':np.array([1]),'base':np.array([0])}
    for a in 'xyz':faces['O'+a]=np.zeros(1);faces['N'+a]=np.zeros(1)
    summary={'cells':2,'points':3,'internal_faces':1,'tets':2,'small':1e-15,
             'near_degenerate_tets':0,'invalid_face_base_indices':0,
             'maximum_centre_interpolation_error':0,'maximum_internal_face_trace_difference':0}
    return dict(cells=cells,points=points,tets=tets,faces=faces,summary=summary)


def test_reversed_shared_triangle_and_exact_volumes():
    r=validate(**fixture())
    assert r['shared_internal_face_triangles_match_owner_neighbour']
    assert r['maximum_cell_tet_volume_relative_mismatch']==0


def test_wrong_shared_vertex_is_not_hidden_by_zero_face_samples():
    data=fixture();data['tets']['p2'][1]=2
    assert not validate(**data)['shared_internal_face_triangles_match_owner_neighbour']


def test_degenerate_geometry_and_volume_deficit_are_recorded():
    data=fixture();data['tets']['det'][0]=0;data['tets']['volume'][0]=0
    r=validate(**data)
    assert not r['all_recorded_tet_determinants_above_native_small']
    assert r['maximum_cell_tet_volume_relative_mismatch']==1
