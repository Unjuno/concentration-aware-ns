"""Bind matrix query configuration to enclosed witnesses before native execution."""
import json,re
from fractions import Fraction
from tools.run_amr_mean_quality import ROOT,sha


def validate_spec(spec):
    for k in ('cell','face','tetPt'):
        if type(spec[k]) is not int or spec[k]<0:raise ValueError('nonnegative integer target required')
    if spec['step_powers']!=[14,16,18] or spec['query_count']!=19:raise ValueError('fixed query schedule differs')
    if not re.fullmatch('[0-9a-f]{64}',spec['release_sha256']):raise ValueError('release digest required')
    if not spec['release_url'].startswith('https://github.com/Unjuno/concentration-aware-ns/releases/download/'):
        raise ValueError('unexpected release location')
    loaded=[]
    for name in ('witness','neighborhood'):
        path=ROOT/spec[name+'_path']
        if not path.resolve().is_relative_to(ROOT.resolve()) or sha(path)!=spec[name+'_sha256']:
            raise ValueError('witness identity differs')
        loaded.append(json.loads(path.read_text()))
    w,b=loaded
    if w['status']!='ENCLOSED_LOCAL_IDEALIZED_AFFINE_PIECE_WITNESS' or b['status']!='UNIQUE_IDEALIZED_PIECE_ON_ENCLOSED_BALL':
        raise ValueError('enclosed witness and unique ball required')
    if any(w[k]!=spec[k] for k in ('case_id','cell','face','tetPt','point_indices','capture_manifest_sha256')):
        raise ValueError('target differs from witness')
    if b['witness_sha256']!=spec['witness_sha256'] or b['capture_manifest_sha256']!=spec['capture_manifest_sha256'] or b['cell']!=spec['cell']:
        raise ValueError('ball differs from witness')
    if b['radius']['lower_rational']!='1/4096':raise ValueError('fixed ball radius differs')
    return w,b


def verify_query_ball(queries,ball):
    radius=Fraction(ball['radius']['lower_rational'])
    bounds=[(Fraction(c['lower_rational']),Fraction(c['upper_rational'])) for c in ball['centre']]
    # Exact decoded binary floats; maximum coordinate distance covers every
    # enclosed centre independently, so no interval rounding is needed here.
    for q in queries:
        distance=sum(max(abs(Fraction.from_float(q[a])-lo),abs(Fraction.from_float(q[a])-hi))**2 for a,(lo,hi) in zip('xyz',bounds))
        if distance>=radius**2:raise ValueError('native query outside certified ball')
    return True


def verify_candidate_coverage(candidates,queries,ball):
    expected={(c['face'],c['tetPt']) for c in ball['candidate_labels']}
    if len(expected)!=len(ball['candidate_labels']):raise ValueError('duplicate enclosed candidate label')
    ids={q['query'] for q in queries}
    if {c['query'] for c in candidates}!=ids:raise ValueError('candidate query coverage differs')
    for q in ids:
        labels=[(c['face'],c['tetPt']) for c in candidates if c['query']==q]
        if len(labels)!=len(expected) or set(labels)!=expected:
            raise ValueError('native candidate set differs from enclosed ball')
    return True
