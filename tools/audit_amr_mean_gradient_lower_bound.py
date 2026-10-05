"""Archive audit of reconstruction-independent gradient lower-bound formulas."""
import argparse
import json
from pathlib import Path

import numpy as np

from tools.amr_mean_gradient_lower_bound import bound
from tools.amr_p0_spectrum import voxel_fft, reference_coefficients
from tools.amr_band_reconstruction import derivative_coefficients,sampled_peak_bounds
from tools.high_gradient_cell_average import exact_cell_average_velocity
from tools.analyze_amr_gauss_gradient import _read_csv,_vector
from tools.analyze_amr_mean_quality import verify_archive
from tools.compare_amr_resolution_volume_integrated import _cell_widths_and_validate
from tools.run_amr_mean_quality import ROOT,SOURCE_FILES,sha


def reference_norms(time):
    modes=np.array([(x,y,z) for x in (-3,3) for y in range(-4,5) for z in range(-4,5)])
    coefficients=reference_coefficients(modes,3,time)
    gradient=derivative_coefficients(modes,coefficients,'gradient')
    curl=derivative_coefficients(modes,coefficients,'curl')
    return {'gradient_mean_square':float(np.sum(np.abs(gradient)**2)),
        'curl_mean_square':float(np.sum(np.abs(curl)**2)),
        'gradient_peak':sampled_peak_bounds(modes,gradient,64),
        'curl_peak':sampled_peak_bounds(modes,curl,64)}


def audit(raw_map,output,source_commit):
    protocol=ROOT/'protocols/amr-mean-gradient-lower-bound-v1.json';spec=json.loads(protocol.read_text())
    input_protocol=ROOT/spec['input_protocol'];inputs=json.loads(input_protocol.read_text())
    raw_map=json.loads(Path(raw_map).read_text());output=Path(output)
    if output.exists():raise FileExistsError('refuse to replace earlier bound evidence')
    if set(raw_map)!=set(spec['case_ids']) or len(source_commit)!=40:
        raise ValueError('complete archive map and frozen numerical source required')
    rows=[];refs={}
    for case_id in spec['case_ids']:
        path=ROOT/spec['input_evidence']/case_id;manifest=json.loads((path/'manifest.json').read_text())
        case=next(c for c in inputs['cases'] if c['id']==case_id)
        if (manifest['status']!='RUN_COMPLETE_MEASURED_MEAN_QUALITY_INPUTS'
                or manifest['source_commit']!=spec['input_source_commit'] or manifest['case_id']!=case_id
                or manifest['tracked_status'].strip() or manifest['protocol_sha256']!=sha(input_protocol)
                or set(manifest['source_files_sha256'])!=set(SOURCE_FILES)
                or any(sha(ROOT/p)!=h for p,h in manifest['source_files_sha256'].items())):
            raise ValueError('frozen run/source identity failed')
        archive=Path(raw_map[case_id]);verify_archive(archive,manifest);stages=[]
        for stage in spec['stages']:
            time=inputs['measurements']['state_times'][stage]
            table=_read_csv(archive,f'main/postProcessing/amrStages/{time:g}/{stage}_cells.csv')
            centers=_vector(table,('cx','cy','cz'));volumes=table['V'];values=_vector(table,('Ux','Uy','Uz'))
            exact=exact_cell_average_velocity(centers,_cell_widths_and_validate(centers,volumes,case['n']),time,3)
            transform,norm=voxel_fft(centers,volumes,values-exact,case['n'])
            if time not in refs:refs[time]=reference_norms(time)
            reference=refs[time];bands=[]
            for cutoff in spec['cutoff_cubes']:
                q=bound(transform,norm['voxel_mean_square'],cutoff)
                q['gradient_relative_l2_lower']=q['gradient_mean_norm_lower']/np.sqrt(reference['gradient_mean_square'])
                q['gradient_relative_peak_error_lower']=q['gradient_mean_norm_lower']/reference['gradient_peak']['analytic_peak_upper']
                q['solenoidal_curl_relative_l2_lower']=q['gradient_mean_norm_lower']/np.sqrt(reference['curl_mean_square'])
                q['solenoidal_curl_relative_peak_error_lower']=q['gradient_mean_norm_lower']/reference['curl_peak']['analytic_peak_upper']
                bands.append(q)
            if any(bands[i+1]['upper_hminus_mean_square']>bands[i]['upper_hminus_mean_square']*(1+2e-12) for i in range(len(bands)-1)):
                raise ValueError('larger Fourier band does not tighten the H-1 upper bound')
            stages.append({'stage':stage,'time':time,'cells':len(volumes),'native_mean_error_voxelization':norm,
                           'reference':reference,'bounds':bands})
            print(json.dumps({'case_id':case_id,'stage':stage,'gradient_l2_lower':[q['gradient_relative_l2_lower'] for q in bands],'gradient_peak_lower':bands[-1]['gradient_relative_peak_error_lower']}),flush=True)
        rows.append({'case_id':case_id,'archive_sha256':manifest['archive']['sha256'],'stages':stages})
    sources=('tools/amr_mean_gradient_lower_bound.py','tools/audit_amr_mean_gradient_lower_bound.py',
        'tools/amr_p0_spectrum.py','tools/amr_band_reconstruction.py','tools/high_gradient_cell_average.py',
        'tools/analyze_amr_mean_quality.py','tools/analyze_amr_gauss_gradient.py','tools/compare_amr_resolution_volume_integrated.py')
    result={'status':'MEASURED_CONDITIONAL_H1_NATIVE_MEAN_CONSTRAINT_LOWER_BOUNDS',
        'numerical_source_commit':source_commit,'protocol_sha256':sha(protocol),'input_protocol_sha256':sha(input_protocol),
        'source_sha256':{p:sha(ROOT/p) for p in sources},'cases':rows,
        'quality_verdict':'NO_ROUNDING_CERTIFICATE_OR_ORIGINAL_SOLVER_GATE_COMPLETION','limits':spec['limits']}
    output.mkdir(parents=True);(output/'analysis.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps({'status':result['status'],'states':sum(len(c['stages']) for c in rows)}));return result


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--raw-map',required=True,type=Path)
    parser.add_argument('--output',required=True,type=Path);parser.add_argument('--source-commit',required=True)
    args=parser.parse_args();audit(args.raw_map,args.output,args.source_commit)
