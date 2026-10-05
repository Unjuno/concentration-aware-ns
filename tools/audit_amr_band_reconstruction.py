"""Replay a named smooth projection of twelve archived AMR P0 spectra."""
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np

from tools.amr_band_reconstruction import diagnostics
from tools.amr_p0_spectrum import reference_coefficients

ROOT = Path(__file__).resolve().parents[1]


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def audit(output, source_commit):
    protocol = ROOT/'protocols/amr-band-reconstruction-v1.json'
    spec = json.loads(protocol.read_text())
    prior_path = ROOT/spec['input_analysis']; prior = json.loads(prior_path.read_text())
    output = Path(output)
    if output.exists():
        raise FileExistsError('refuse to replace prior reconstruction evidence')
    if (prior['status'] != 'PASS_DECLARED_P0_SPECTRUM_FORMULAS_AND_ARCHIVED_CONTROLS'
            or len(prior['cases']) != 4 or len(source_commit) != 40
            or spec['cutoff_cube'] != 7):
        raise ValueError('complete frozen spectral evidence required')
    rows=[]; identities=[]
    for case in prior['cases']:
        stages=[]
        for record in case['stages']:
            path=prior_path.parent/record['band_artifact']
            if sha(path) != record['band_artifact_sha256']:
                raise ValueError('changed archived coefficients')
            with np.load(path,allow_pickle=False) as data:
                modes=data['modes'];actual=data['velocity_coefficients'];reference=data['reference_coefficients']
            axis=np.arange(-7,8)
            expected=np.stack(np.meshgrid(axis,axis,axis,indexing='ij'),axis=-1).reshape(-1,3)
            if not np.array_equal(modes,expected) or not np.array_equal(reference,reference_coefficients(modes,3,record['time'])):
                raise ValueError('frozen mode set/reference mismatch')
            grids=[diagnostics(modes,actual,reference,m) for m in spec['sample_grids']]
            stages.append({'stage':record['stage'],'time':record['time'],
                'input_coefficients_sha256':sha(path),'grids':grids,
                'discarded_p0_velocity_mass':record['spectrum']['outside_cube_mean_square'],
                'discarded_p0_velocity_norm_relative_to_reference':record['spectrum']['outside_cube_norm_relative_to_reference'],
                'band_velocity_error_relative_l2':record['spectrum']['inside_cube_error_relative_l2']})
        if len(stages)!=3:
            raise ValueError('complete stage matrix required')
        before,after=stages[:2]
        identity=before['grids']==after['grids']
        if not identity:
            raise ValueError('parent repartition changes the named polynomial diagnostics')
        identities.append({'case_id':case['case_id'],'preMap_mapped_diagnostics_exact_identity':identity})
        rows.append({'case_id':case['case_id'],'stages':stages})
    result={'status':'MEASURED_NAMED_BAND_RECONSTRUCTION_ONLY','source_commit':source_commit,
        'protocol_sha256':sha(protocol),'input_analysis_sha256':sha(prior_path),
        'sources_sha256':{p:sha(ROOT/p) for p in ('tools/amr_band_reconstruction.py','tools/audit_amr_band_reconstruction.py','tools/amr_p0_spectrum.py')},
        'cases':rows,'same_time_map_identities':identities,'limits':spec['limits'],
        'quality_verdict':'NO_NEW_THRESHOLD_OR_ORIGINAL_FULL_FIELD_GATE_COMPLETION'}
    output.mkdir(parents=True)
    (output/'analysis.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps({'status':result['status'],'states':sum(len(c['stages']) for c in rows),'sample_grids':spec['sample_grids']}))
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',required=True,type=Path)
    parser.add_argument('--source-commit',required=True)
    args=parser.parse_args();audit(args.output,args.source_commit)
