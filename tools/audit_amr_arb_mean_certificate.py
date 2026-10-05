"""Certify final-state nominal-mean H1 obstructions using Arb balls."""
import argparse,json,time
from pathlib import Path

import numpy as np
from flint import ctx

from tools.amr_arb_mean_certificate import certificate
from tools.analyze_amr_gauss_gradient import _read_csv,_vector
from tools.analyze_amr_mean_quality import verify_archive
from tools.compare_amr_resolution_volume_integrated import _cell_widths_and_validate
from tools.run_amr_mean_quality import ROOT,SOURCE_FILES,sha


def audit(raw_map,output,source_commit):
    protocol=ROOT/'protocols/amr-arb-mean-certificate-v1.json';spec=json.loads(protocol.read_text())
    input_protocol=ROOT/spec['input_protocol'];inputs=json.loads(input_protocol.read_text())
    raw_map=json.loads(Path(raw_map).read_text());output=Path(output)
    if output.exists():raise FileExistsError('refuse to replace a prior certificate')
    if set(raw_map)!=set(spec['case_ids']) or len(source_commit)!=40:
        raise ValueError('complete frozen archive map required')
    old=ctx.prec;ctx.prec=spec['precision_bits'];rows=[]
    try:
        for case_id in spec['case_ids']:
            begin=time.monotonic();case=next(c for c in inputs['cases'] if c['id']==case_id)
            manifest=json.loads((ROOT/spec['input_evidence']/case_id/'manifest.json').read_text())
            if (manifest['source_commit']!=spec['input_source_commit'] or manifest['case_id']!=case_id
                    or manifest['status']!='RUN_COMPLETE_MEASURED_MEAN_QUALITY_INPUTS'
                    or manifest['tracked_status'].strip() or manifest['protocol_sha256']!=sha(input_protocol)
                    or set(manifest['source_files_sha256'])!=set(SOURCE_FILES)
                    or any(sha(ROOT/p)!=h for p,h in manifest['source_files_sha256'].items())):
                raise ValueError('frozen run/source identity failed')
            archive=Path(raw_map[case_id]);verify_archive(archive,manifest)
            member='main/postProcessing/amrStages/0.05/postSolve_cells.csv';table=_read_csv(archive,member)
            centers=_vector(table,('cx','cy','cz'));volumes=table['V'];values=_vector(table,('Ux','Uy','Uz'))
            widths=_cell_widths_and_validate(centers,volumes,case['n'])
            def progress(stage):print(json.dumps({'case_id':case_id,'phase':stage}),flush=True)
            result=certificate(centers,widths,values,case['n'],spec['time_exact_decimal'],3,progress)
            rows.append({'case_id':case_id,'archive_sha256':manifest['archive']['sha256'],
                         'member':member,'cells':len(volumes),'certificate':result})
            print(json.dumps({'case_id':case_id,'elapsed_seconds':time.monotonic()-begin,
                              'peak_lower':result['gradient_relative_peak_error_lower']['display_lower']}),flush=True)
    finally:ctx.prec=old
    sources=('tools/amr_arb_mean_certificate.py','tools/audit_amr_arb_mean_certificate.py',
        'tools/analyze_amr_mean_quality.py','tools/analyze_amr_gauss_gradient.py','tools/compare_amr_resolution_volume_integrated.py')
    record={'status':'ARITHMETIC_ENCLOSURES_FOR_DECLARED_NOMINAL_NATIVE_MEAN_CONSTRAINTS',
        'numerical_source_commit':source_commit,'precision_bits':spec['precision_bits'],
        'protocol_sha256':sha(protocol),'input_protocol_sha256':sha(input_protocol),
        'source_sha256':{p:sha(ROOT/p) for p in sources},'cases':rows,
        'original_gate_verdict':'UNCHANGED_SCOPE_AND_INPUT_INTERPRETATION_REMAIN_REQUIRED','limits':spec['limits']}
    output.mkdir(parents=True);(output/'analysis.json').write_text(json.dumps(record,indent=2,allow_nan=False)+'\n')
    print(json.dumps({'status':record['status'],'cases':len(rows)}));return record


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--raw-map',required=True,type=Path)
    p.add_argument('--output',required=True,type=Path);p.add_argument('--source-commit',required=True)
    a=p.parse_args();audit(a.raw_map,a.output,a.source_commit)
