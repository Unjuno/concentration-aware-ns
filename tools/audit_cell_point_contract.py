"""Scoped pinned-source cellPoint trace and exact affine controls; no C++ run."""
import argparse
import itertools
import json
import subprocess
import tarfile
from pathlib import Path

import sympy as sp
from tools.analyze_amr_mean_quality import verify_archive
from tools.run_amr_mean_quality import ROOT, sha

PIN='18870c24d21c6b982e2cdec27b2f59738cca5f90'
BASE='src/finiteVolume/interpolation/interpolation/'
FILES=(BASE+'interpolationCellPoint/interpolationCellPoint.H',
       BASE+'interpolationCellPoint/interpolationCellPoint.C',
       BASE+'interpolationCellPoint/interpolationCellPointI.H',
       BASE+'interpolationCellPoint/cellPointWeight/cellPointWeight.C',
       BASE+'interpolationVolPointInterpolation/interpolationVolPointInterpolation.C',
       'src/OpenFOAM/meshes/polyMesh/polyMeshTetDecomposition/tetIndicesI.H',
       'src/OpenFOAM/meshes/polyMesh/polyMeshTetDecomposition/polyMeshTetDecomposition.C',
       'src/OpenFOAM/meshes/primitiveShapes/tetrahedron/tetrahedronI.H')


def affine_controls():
    x,y,z=sp.symbols('x y z');a,b,p,q,r=sp.symbols('a b p q r', real=True)
    face=p+(q-p)*x+(r-p)*y
    minus=face+(p-a)*z;plus=face+(b-p)*z
    endpoint=(sp.expand(minus.subs({x:0,y:0,z:-1})-a),
              sp.expand(plus.subs({x:0,y:0,z:1})-b))
    trace=sp.expand(minus.subs(z,0)-plus.subs(z,0))
    slope_sum=sp.expand(sp.diff(minus,z)+sp.diff(plus,z)-(b-a))
    assert endpoint==(0,0) and trace==0 and slope_sum==0
    checked=0
    for ua,ub,vertex in itertools.product(range(-2,3),repeat=3):
        assert 2*max(abs(vertex-ua),abs(ub-vertex))>=abs(ub-ua)
        checked+=1
    # A degenerate-tetrahedron uniform-weight fallback need not reproduce a centre.
    fallback=(a+p+q+r)/4
    noninterpolating=sp.expand(fallback-a)
    assert noninterpolating!=0
    return {'endpoint_residuals':[str(v) for v in endpoint],
            'shared_face_trace_residual':str(trace),'gradient_slope_sum_residual':str(slope_sum),
            'integer_chord_controls':checked,
            'degenerate_fallback_centre_error':str(noninterpolating),
            'scope':'Exact scalar two-tetrahedron affine identities, componentwise applicable to vector fields; not upstream C++ execution or actual mesh validation.'}


def audit(upstream,raw_map,output,source_commit):
    upstream=Path(upstream);output=Path(output);raw_map=json.loads(Path(raw_map).read_text())
    if output.exists():raise FileExistsError('preserve prior evidence')
    spec=json.loads((ROOT/'protocols/of13-amr-mean-quality-v1.json').read_text())
    if set(raw_map)!={c['id'] for c in spec['cases']} or len(source_commit)!=40:
        raise ValueError('complete archive map and source commit required')
    sources=[]
    for name in FILES:
        data=subprocess.check_output(['git','-C',str(upstream),'show',PIN+':'+name])
        if data!=(upstream/name).read_bytes():raise ValueError('upstream differs from pin')
        sources.append({'path':name,'sha256':sha(upstream/name),
                        'url':'https://github.com/OpenFOAM/OpenFOAM-13/blob/'+PIN+'/'+name})
    rows=[]
    for case in spec['cases']:
        key=case['id'];manifest=json.loads((ROOT/'evidence/of13-amr-mean-quality-v1'/key/'manifest.json').read_text())
        if manifest['source_commit']!='3566f89058071910a41bb68010eb258c7bbc3d74':
            raise ValueError('unexpected original CFD source')
        archive=Path(raw_map[key]);verify_archive(archive,manifest)
        with tarfile.open(archive,'r:gz') as tf:
            names=tf.getnames()
        mesh=[name for name in names if '/polyMesh/' in name]
        rows.append({'case_id':key,'archive_sha256':manifest['archive']['sha256'],
                     'archive_members':len(names),'polyMesh_members':mesh,
                     'actual_tetrahedral_geometry_verified':False})
    result={'status':'PINNED_SOURCE_AND_AFFINE_CONTROLS_VERIFIED_ACTUAL_MESH_UNVERIFIED',
            'numerical_source_commit':source_commit,'upstream_commit':PIN,'source_files':sources,
            'affine_controls':affine_controls(),'archives':rows,
            'required_actual_case_evidence':['final mesh points/faces/owner/neighbour and boundaries',
                'nondegenerate conforming tetrahedral decomposition with consistent shared-face triangles',
                'actual cellPoint centre interpolation and shared-face trace checks',
                'binary/source implementation identity and recorded scheme selection'],
            'limits':['cellPoint is a named interpolation, not the implicit solver continuum solution',
                      'source fallback behavior requires a nondegeneracy condition',
                      'no actual cellPoint C++ evaluation or new CFD run performed',
                      'original gates and conditional point witnesses unchanged']}
    output.mkdir(parents=True);(output/'analysis.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'sources':len(sources),'archives':len(rows)}))
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--upstream',required=True,type=Path);p.add_argument('--raw-map',required=True,type=Path)
    p.add_argument('--output',required=True,type=Path);p.add_argument('--source-commit',required=True)
    a=p.parse_args();audit(a.upstream,a.raw_map,a.output,a.source_commit)
