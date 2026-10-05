"""Validate finite native position queries; secants are diagnostics, not proofs."""
import argparse,csv,json,math
from pathlib import Path
import numpy as np
from tools.run_amr_mean_quality import ROOT,sha
from tools.run_of13_cell_point_query import PROTOCOL


def rows(path):
    with Path(path).open() as stream:out=[{k:float(v) for k,v in r.items()} for r in csv.DictReader(stream)]
    if not out or any(not math.isfinite(v) for r in out for v in r.values()):
        raise ValueError('empty/nonfinite query data')
    return out


def measure(nodes,queries,candidates,witness,spec):
    """Require addressing, query coverage and values before evaluating secants."""
    vertices=np.array([[r[a] for a in 'xyz'] for r in nodes]);values=np.array([[r['U'+a] for a in 'xyz'] for r in nodes])
    if (len(nodes)!=4 or [r['node'] for r in nodes]!=list(range(4))
            or [r['label'] for r in nodes]!=[spec['cell'],*spec['point_indices']]
            or not np.array_equal(vertices,witness['vertices']) or not np.array_equal(values,witness['nodal_values'])):
        raise ValueError('restored nodal witness differs')
    expected=[(-1,0,0)]+[(a,2.**-p,s) for p in spec['step_powers'] for a in range(3) for s in (-1,1)]
    if len(queries)!=spec['query_count'] or len(queries)!=len(expected):raise ValueError('query coverage incomplete')
    centre=vertices.mean(axis=0);minimum=1.;max_manual=0.;max_explicit=0.
    ordinal_sets=[]
    for i,(r,(axis,h,sign)) in enumerate(zip(queries,expected)):
        if [r[k] for k in ('query','axis','h','sign')]!=[i,axis,h,sign]:raise ValueError('wrong/reordered query')
        pos=centre.copy()
        if axis>=0:pos[axis]+=sign*h
        if np.max(np.abs(pos-np.array([r[a] for a in 'xyz'])))>2e-15:raise ValueError('wrong query coordinate')
        if [r['p'+str(j)] for j in range(3)]!=spec['point_indices']:raise ValueError('native selected different vertex addressing')
        if (r['first_face'],r['first_tetPt'])!=(spec['face'],spec['tetPt']):raise ValueError('native first-accepted candidate differs')
        cc=[c for c in candidates if c['query']==i]
        if not cc or [c['ordinal'] for c in cc]!=list(range(len(cc))):raise ValueError('missing/reordered candidate scan')
        ordinal_sets.append([(c['face'],c['tetPt'],c['p0'],c['p1'],c['p2']) for c in cc])
        if any(c['accepted'] not in (0,1) or c['tol']!=np.finfo(float).eps or c['cellV']<=0 for c in cc):raise ValueError('invalid native predicate metadata')
        accepted=[c for c in cc if c['accepted']==1]
        if not accepted or (accepted[0]['face'],accepted[0]['tetPt'])!=(spec['face'],spec['tetPt']):raise ValueError('native recorded scan contradicts selected piece')
        first=accepted[0]
        if [first['p'+str(j)] for j in range(3)]!=spec['point_indices']:raise ValueError('first accepted addressing differs')
        for c in cc:
            w=[c['w'+str(j)] for j in range(4)];tol=c['tol']
            pred=abs(c['det']/c['cellV'])>tol and all(w[j]+tol>0 for j in range(3)) and sum(w[:3])<1+tol
            if bool(c['accepted'])!=pred:raise ValueError('recorded native predicate inconsistent')
        weights=np.array([r['w'+str(j)] for j in range(4)])
        if np.max(np.abs(weights-np.array([first['w'+str(j)] for j in range(4)])))>2e-14:raise ValueError('selected weights differ from native scan')
        if abs(weights.sum()-1)>2e-14 or weights.min()<=0:raise ValueError('query not strict interior')
        if abs(r['det'])<=np.finfo(float).eps:raise ValueError('degenerate target')
        if np.max(np.abs(weights@vertices-np.array([r[a] for a in 'xyz'])))>2e-14:raise ValueError('barycentric coordinate inconsistency')
        minimum=min(minimum,float(weights.min()))
        actual=np.array([r['U'+a] for a in 'xyz']);explicit=np.array([r['E'+a] for a in 'xyz'])
        max_manual=max(max_manual,float(np.max(np.abs(actual-weights@values))))
        max_explicit=max(max_explicit,float(np.max(np.abs(actual-explicit))))
    if any(s!=ordinal_sets[0] for s in ordinal_sets):raise ValueError('candidate list changed between queries')
    if max_manual>2e-14 or max_explicit>2e-14:raise ValueError('native position and weighted/explicit values differ')
    g=np.linalg.solve(vertices[1:]-vertices[0],values[1:]-values[0]).T
    differences=[]
    for power in spec['step_powers']:
        columns=[]
        for axis in range(3):
            neg=next(r for r in queries if r['axis']==axis and r['h']==2.**-power and r['sign']==-1)
            pos=next(r for r in queries if r['axis']==axis and r['h']==2.**-power and r['sign']==1)
            columns.append(np.array([pos['U'+a]-neg['U'+a] for a in 'xyz'])/(2*2.**-power))
        derivative=np.array(columns).T;error=float(np.max(np.abs(derivative-g)))
        if error>1e-8:raise ValueError('floating secant differs from affine map')
        differences.append({'h':2.**-power,'maximum_absolute_component_discrepancy':error})
    return {'queries':len(queries),'candidates_per_query':len(ordinal_sets[0]),'selected_face':spec['face'],'selected_tetPt':spec['tetPt'],
            'minimum_native_barycentric_weight':minimum,'maximum_weighted_value_component_discrepancy':max_manual,
            'maximum_explicit_overload_component_discrepancy':max_explicit,'floating_secant_diagnostics':differences}


def analyze(evidence):
    evidence=Path(evidence);receipt=json.loads((evidence/'manifest.json').read_text());spec=json.loads(PROTOCOL.read_text())
    if (receipt['status']!='NATIVE_QUERY_REPLAY_COMPLETE_NOT_CONTINUUM_CERTIFICATION' or receipt['exit_code']!=0
            or receipt['protocol_sha256']!=sha(PROTOCOL) or receipt['bundle_sha256']!=spec['release_sha256']
            or receipt['capture_manifest_sha256']!=spec['capture_manifest_sha256']
            or receipt['field_sha256_before']!=receipt['field_sha256_after']
            or not receipt['installed_sources_match_pin'] or not receipt['libraries_match_original_stock']):
        raise ValueError('native replay integrity incomplete')
    for p,digest in receipt['output_files_sha256'].items():
        if sha(evidence/p)!=digest:raise ValueError('query output digest mismatch')
    log=(evidence/'probe.log').read_text()
    if 'Tetrahedron search failed' in log or 'CELL_POINT_QUERY_REPLAY_COMPLETE queries=19' not in log:
        raise ValueError('native search fallback or incomplete replay')
    witness=json.loads((ROOT/'evidence/cell-point-local-derivative-v1/analysis.json').read_text())['witness']
    measured=measure(*(rows(evidence/(n+'.csv')) for n in ('nodes','queries','candidates')),witness,spec)
    result={'status':'FINITE_NATIVE_POSITION_REPLAY_VERIFIED','runtime_source_commit':receipt['source_commit'],'manifest_sha256':sha(evidence/'manifest.json'),'measurements':measured,'limits':spec['limits']}
    (evidence/'analysis.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n');print(json.dumps(result),flush=True)
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--evidence',required=True,type=Path);a=p.parse_args();analyze(a.evidence)
