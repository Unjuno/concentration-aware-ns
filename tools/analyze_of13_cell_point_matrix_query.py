"""Verify matrix native samples against frozen pieces and enclosed balls."""
import argparse,json
from pathlib import Path
from tools.run_amr_mean_quality import sha
from tools.analyze_of13_cell_point_query import rows,measure
from tools.cell_point_matrix_query_spec import validate_spec,verify_query_ball,verify_candidate_coverage


def analyze(evidence,protocol):
    evidence=Path(evidence);receipt=json.loads((evidence/'manifest.json').read_text());spec=json.loads(protocol.read_text())
    if (receipt['status']!='NATIVE_QUERY_REPLAY_COMPLETE_NOT_CONTINUUM_CERTIFICATION' or receipt['exit_code']!=0
            or receipt['protocol_sha256']!=sha(protocol) or receipt['bundle_sha256']!=spec['release_sha256']
            or receipt['capture_manifest_sha256']!=spec['capture_manifest_sha256']
            or receipt['field_sha256_before']!=receipt['field_sha256_after']
            or not receipt['installed_sources_match_pin'] or not receipt['libraries_match_original_stock']):
        raise ValueError('native replay integrity incomplete')
    for p,digest in receipt['output_files_sha256'].items():
        if sha(evidence/p)!=digest:raise ValueError('query output digest mismatch')
    log=(evidence/'probe.log').read_text()
    if 'Tetrahedron search failed' in log or 'CELL_POINT_QUERY_REPLAY_COMPLETE queries=19' not in log:
        raise ValueError('native search fallback or incomplete replay')
    previous,ball=validate_spec(spec)
    witness=previous['witness']
    verify_query_ball(rows(evidence/'queries.csv'),ball)
    verify_candidate_coverage(rows(evidence/'candidates.csv'),rows(evidence/'queries.csv'),ball)
    measured=measure(*(rows(evidence/(n+'.csv')) for n in ('nodes','queries','candidates')),witness,spec)
    result={'status':'FINITE_NATIVE_POSITION_REPLAY_VERIFIED','runtime_source_commit':receipt['source_commit'],'manifest_sha256':sha(evidence/'manifest.json'),'measurements':measured,'limits':spec['limits']}
    (evidence/'analysis.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n');print(json.dumps(result),flush=True)
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--evidence',required=True,type=Path);p.add_argument('--protocol',required=True,type=Path);a=p.parse_args();analyze(a.evidence,a.protocol)
