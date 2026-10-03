"""Audit actual and exact-native-mean smooth reconstructions of archived AMR."""
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np

from tools.amr_p0_spectrum import voxel_fft
from tools.amr_voxel_mean_reconstruction import reconstruct, recovered_voxel_averages, cube_averages, errors
from tools.high_gradient_cell_average import exact_cell_average_velocity
from tools.amr_projection_decomposition import exact_mms_mean_square_velocity
from tools.analyze_amr_gauss_gradient import _read_csv, _vector
from tools.analyze_amr_mean_quality import verify_archive
from tools.compare_amr_resolution_volume_integrated import _cell_widths_and_validate
from tools.run_amr_mean_quality import ROOT, SOURCE_FILES, sha


def measure(centers,volumes,values,n,time):
    widths=_cell_widths_and_validate(centers,volumes,n)
    transform,voxel=voxel_fft(centers,volumes,values,n)
    axis,coefficients,metadata=reconstruct(transform)
    recovered,imaginary=recovered_voxel_averages(axis,coefficients)
    input_values=np.fft.ifftn(transform,axes=(0,1,2))*transform.shape[0]**3
    difference=float(np.max(np.abs(recovered-input_values.real)))
    scale=max(float(np.max(np.abs(values))),1e-300)
    if max(difference,imaginary)>2e-11*scale:
        raise ValueError('finest voxel means are not preserved')
    chosen=[]
    for width in np.unique(widths):
        candidates=np.flatnonzero(widths==width)
        chosen.extend(candidates[np.linspace(0,len(candidates)-1,min(4,len(candidates)),dtype=int)].tolist())
    means=cube_averages(axis,coefficients,centers[chosen],widths[chosen])
    native_difference=float(np.max(np.abs(means-values[chosen])))
    if native_difference>2e-11*scale:
        raise ValueError('independent native cube mean integral failed')
    result=errors(axis,coefficients,3,time)
    if abs(result['reference']['velocity_mean_square']/exact_mms_mean_square_velocity(time,3)-1)>2e-13:
        raise ValueError('reference velocity norm differs from independent rational Parseval formula')
    result.update({'reconstruction':metadata,'coefficient_bytes_sha256':hashlib.sha256(coefficients.tobytes()).hexdigest(),
        'voxelization':voxel,'maximum_voxel_mean_difference':difference,
        'maximum_voxel_round_trip_imaginary':imaginary,'selected_native_cell_indices':chosen,
        'maximum_selected_native_mean_integral_difference':native_difference})
    return result


def audit(raw_map,output,source_commit):
    protocol=ROOT/'protocols/amr-voxel-mean-reconstruction-v1.json';spec=json.loads(protocol.read_text())
    input_protocol=ROOT/spec['input_protocol'];inputs=json.loads(input_protocol.read_text())
    raw_map=json.loads(Path(raw_map).read_text());output=Path(output)
    if output.exists():raise FileExistsError('refuse to overwrite prior operator evidence')
    if set(raw_map)!=set(spec['case_ids']) or len(source_commit)!=40:
        raise ValueError('complete case map and frozen numerical source required')
    rows=[];identities=[]
    for case_id in spec['case_ids']:
        path=ROOT/spec['input_evidence']/case_id;manifest=json.loads((path/'manifest.json').read_text())
        case=next(c for c in inputs['cases'] if c['id']==case_id)
        if (manifest['status']!='RUN_COMPLETE_MEASURED_MEAN_QUALITY_INPUTS'
                or manifest['source_commit']!=spec['input_source_commit']
                or manifest['case_id']!=case_id or manifest['tracked_status'].strip()
                or manifest['protocol_sha256']!=sha(input_protocol)
                or set(manifest['source_files_sha256'])!=set(SOURCE_FILES)
                or any(sha(ROOT/p)!=h for p,h in manifest['source_files_sha256'].items())):
            raise ValueError('frozen source/run identity failed')
        archive=Path(raw_map[case_id]);verify_archive(archive,manifest)
        stages=[]
        for stage in spec['stages']:
            time=inputs['measurements']['state_times'][stage]
            table=_read_csv(archive,f'main/postProcessing/amrStages/{time:g}/{stage}_cells.csv')
            centers=_vector(table,('cx','cy','cz'));volumes=table['V'];values=_vector(table,('Ux','Uy','Uz'))
            actual=measure(centers,volumes,values,case['n'],time)
            exact_means=exact_cell_average_velocity(centers,_cell_widths_and_validate(centers,volumes,case['n']),time,3)
            control=measure(centers,volumes,exact_means,case['n'],time)
            stages.append({'stage':stage,'time':time,'cells':len(volumes),'actual':actual,'exact_native_mean_control':control})
            print(json.dumps({'case_id':case_id,'stage':stage,'actual_relative_l2':actual['relative_l2'],'control_relative_l2':control['relative_l2']}),flush=True)
        identity=stages[0]['actual']['coefficient_bytes_sha256']==stages[1]['actual']['coefficient_bytes_sha256']
        if not identity:raise ValueError('same-time parent repartition changed the reconstructed polynomial')
        identities.append({'case_id':case_id,'preMap_mapped_full_coefficient_identity':identity})
        rows.append({'case_id':case_id,'archive_sha256':manifest['archive']['sha256'],'stages':stages})
    sources=('tools/amr_voxel_mean_reconstruction.py','tools/audit_amr_voxel_mean_reconstruction.py',
        'tools/amr_p0_spectrum.py','tools/high_gradient_cell_average.py','tools/amr_projection_decomposition.py',
        'tools/analyze_amr_mean_quality.py','tools/analyze_amr_gauss_gradient.py','tools/compare_amr_resolution_volume_integrated.py')
    result={'status':'MEASURED_MEAN_PRESERVING_RECONSTRUCTION_AND_REFERENCE_OPERATOR_CONTROL',
        'numerical_source_commit':source_commit,'protocol_sha256':sha(protocol),'input_protocol_sha256':sha(input_protocol),
        'source_sha256':{p:sha(ROOT/p) for p in sources},'cases':rows,'same_time_map_identities':identities,
        'quality_verdict':'NO_ORIGINAL_SOLVER_GATE_VERDICT_FROM_THIS_OPERATOR_AUDIT','limits':spec['limits']}
    output.mkdir(parents=True);(output/'analysis.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps({'status':result['status'],'states':sum(len(c['stages']) for c in rows)}))
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--raw-map',required=True,type=Path)
    parser.add_argument('--output',required=True,type=Path);parser.add_argument('--source-commit',required=True)
    args=parser.parse_args();audit(args.raw_map,args.output,args.source_commit)
