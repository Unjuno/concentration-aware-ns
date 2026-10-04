"""Enclose a point-interpolating C1 gradient-error witness in each archived case."""
import argparse
import json
from pathlib import Path

import numpy as np
from flint import ctx
from tools.amr_point_gradient_bound import select_witness
from tools.analyze_amr_gauss_gradient import _read_csv, _vector
from tools.analyze_amr_mean_quality import verify_archive
from tools.run_amr_mean_quality import ROOT, SOURCE_FILES, sha


def audit(raw_map, output, source_commit):
    protocol=ROOT/'protocols/amr-point-gradient-bound-v1.json'
    spec=json.loads(protocol.read_text())
    input_protocol=ROOT/spec['input_protocol'];inputs=json.loads(input_protocol.read_text())
    raw_map=json.loads(Path(raw_map).read_text());output=Path(output)
    if output.exists():raise FileExistsError('refuse to replace prior evidence')
    if set(raw_map)!=set(spec['case_ids']) or len(source_commit)!=40:
        raise ValueError('complete frozen archive map and source commit required')
    old=ctx.prec;ctx.prec=spec['precision_bits'];rows=[]
    try:
        for case_id in spec['case_ids']:
            manifest=json.loads((ROOT/spec['input_evidence']/case_id/'manifest.json').read_text())
            if (manifest['source_commit']!=spec['input_source_commit'] or manifest['case_id']!=case_id
                or manifest['status']!='RUN_COMPLETE_MEASURED_MEAN_QUALITY_INPUTS'
                or manifest['tracked_status'].strip() or manifest['protocol_sha256']!=sha(input_protocol)
                or set(manifest['source_files_sha256'])!=set(SOURCE_FILES)
                or any(sha(ROOT/p)!=h for p,h in manifest['source_files_sha256'].items())):
                raise ValueError('frozen original source/run identity failed')
            archive=Path(raw_map[case_id]);verify_archive(archive,manifest)
            member='main/postProcessing/amrStages/0.05/postSolve_cells.csv'
            table=_read_csv(archive,member);centers=_vector(table,('cx','cy','cz'))
            values=_vector(table,('Ux','Uy','Uz'))
            if np.any(centers<0) or np.any(centers>2*np.pi):
                raise ValueError('points outside convex reference cube')
            result=select_witness(centers,values,spec['time_exact_decimal'],inputs['model']['frequency'])
            rows.append({'case_id':case_id,'archive_sha256':manifest['archive']['sha256'],
                         'member':member,'cells':len(centers),'witness':result})
            print(json.dumps({'case_id':case_id,'relative_lower':result['gradient_relative_peak_error_lower']['display_lower']}),flush=True)
    finally:ctx.prec=old
    sources=('tools/amr_point_gradient_bound.py','tools/audit_amr_point_gradient_bound.py',
             'tools/amr_arb_mean_certificate.py','tools/high_gradient_reference.py')
    record={'status':'ENCLOSED_CONDITIONAL_POINT_INTERPOLATION_GRADIENT_WITNESSES',
            'numerical_source_commit':source_commit,'precision_bits':spec['precision_bits'],
            'protocol_sha256':sha(protocol),'input_protocol_sha256':sha(input_protocol),
            'source_sha256':{p:sha(ROOT/p) for p in sources},'cases':rows,'limits':spec['limits'],
            'original_gate_verdict':'UNCHANGED_POINT_RECONSTRUCTION_CONTRACT_NOT_ESTABLISHED'}
    output.mkdir(parents=True);(output/'analysis.json').write_text(json.dumps(record,indent=2,allow_nan=False)+'\n')
    return record


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--raw-map',required=True,type=Path);p.add_argument('--output',required=True,type=Path)
    p.add_argument('--source-commit',required=True)
    a=p.parse_args();audit(a.raw_map,a.output,a.source_commit)
