"""Replay twelve archived AMR states using analytic P0 Fourier integrals."""
import argparse
import hashlib
import json
import math
from pathlib import Path

import numpy as np

from tools.amr_p0_spectrum import voxel_fft, fft_coefficients, direct_cube_coefficients, spectrum
from tools.amr_projection_decomposition import exact_mms_mean_square_velocity
from tools.analyze_amr_gauss_gradient import _read_csv, _vector
from tools.analyze_amr_mean_quality import verify_archive
from tools.compare_amr_resolution_volume_integrated import _cell_widths_and_validate
from tools.run_amr_mean_quality import ROOT, SOURCE_FILES, sha

PROTOCOL = ROOT/'protocols/amr-p0-spectrum-v1.json'


def audit(raw_map, output):
    spec = json.loads(PROTOCOL.read_text())
    input_protocol = ROOT/spec['input_protocol']
    inputs = json.loads(input_protocol.read_text()); model = inputs['model']
    raw_map = json.loads(Path(raw_map).read_text()); output = Path(output)
    if set(raw_map) != set(spec['case_ids']):
        raise ValueError('exact complete case-to-archive map required')
    if output.exists():
        raise FileExistsError('refuse to overwrite an earlier spectrum audit')
    if model['frequency'] != 3 or spec['cutoff_cube'] != 7:
        raise ValueError('unexpected frozen spectrum/reference parameters')
    output.mkdir(parents=True)
    rows=[]; identities=[]
    for case_id in spec['case_ids']:
        evidence = ROOT/spec['input_evidence']/case_id
        manifest=json.loads((evidence/'manifest.json').read_text())
        prior_path=evidence/'analysis.json'; prior=json.loads(prior_path.read_text())
        case=next(c for c in inputs['cases'] if c['id']==case_id)
        if (manifest['status']!='RUN_COMPLETE_MEASURED_MEAN_QUALITY_INPUTS'
                or manifest['case_id']!=case_id or manifest['tracked_status'].strip()
                or manifest['source_commit']!=spec['input_source_commit']
                or manifest['protocol_sha256']!=sha(input_protocol)
                or set(manifest['source_files_sha256'])!=set(SOURCE_FILES)
                or any(sha(ROOT/p)!=h for p,h in manifest['source_files_sha256'].items())
                or prior['source_commit']!=manifest['source_commit'] or prior['case']!=case
                or prior['archive_sha256']!=manifest['archive']['sha256']
                or prior['protocol_sha256']!=manifest['protocol_sha256']):
            raise ValueError('archive/run/reference identity incomplete or changed')
        archive=Path(raw_map[case_id]);verify_archive(archive,manifest)
        records=[];first_coefficients=None;first_norm=None
        for stage in spec['stages']:
            time=inputs['measurements']['state_times'][stage]
            table=_read_csv(archive,f'main/postProcessing/amrStages/{time:g}/{stage}_cells.csv')
            centers=_vector(table,('cx','cy','cz'));velocity=_vector(table,('Ux','Uy','Uz'));volumes=table['V']
            widths=_cell_widths_and_validate(centers,volumes,case['n'])
            transform,norm=voxel_fft(centers,volumes,velocity,case['n'])
            summary,modes,coefficients,reference=spectrum(transform,norm['voxel_mean_square'],model['frequency'],time,spec['cutoff_cube'])
            continuum_norm=exact_mms_mean_square_velocity(time,model['frequency'])
            if abs(summary['reference_mean_square']/continuum_norm-1)>2e-13:
                raise ValueError('binomial reference norm fails independently derived Parseval mean')
            selected=np.array([(0,0,0),(3,0,0),(3,1,4),(-3,-4,2),(7,0,0),(0,7,-7)])
            direct=direct_cube_coefficients(centers,widths,volumes,velocity,selected)
            fft_selected=fft_coefficients(transform,selected)
            mode_difference=float(np.max(np.abs(direct-fft_selected)))
            if mode_difference > 2e-12*math.sqrt(continuum_norm):
                raise ValueError('FFT coefficient differs from direct analytic cube integration')
            prior_stage=next(s for s in prior['stages'] if s['stage']==stage)
            spatial=prior_stage['velocity_p0_total_relative_l2']
            difference=summary['p0_global_error_relative_l2']-spatial
            if abs(difference)>2e-11:
                raise ValueError('global spectral error differs from independent archived spatial error')
            filename=case_id+'-'+stage+'-band.npz'
            np.savez_compressed(output/filename,modes=modes,velocity_coefficients=coefficients,reference_coefficients=reference)
            records.append({'stage':stage,'time':time,'cells':len(volumes),'voxelization':norm,
                'direct_integral_selected_modes':selected.tolist(),'maximum_direct_fft_coefficient_difference':mode_difference,
                'archived_spatial_p0_error_relative_l2':spatial,'spectral_spatial_relative_l2_difference':difference,
                'band_artifact':filename,'band_artifact_sha256':sha(output/filename),'spectrum':summary})
            if stage=='preMap':
                first_coefficients=coefficients.copy();first_norm=norm['voxel_mean_square']
            elif stage=='mapped':
                coefficient_difference=float(np.max(np.abs(coefficients-first_coefficients)))
                norm_difference=norm['voxel_mean_square']-first_norm
                if coefficient_difference>2e-13*math.sqrt(continuum_norm) or abs(norm_difference)>2e-13*continuum_norm:
                    raise ValueError('same-time map does not preserve the diagnosed P0 velocity spectrum')
                identities.append({'case_id':case_id,'pre_map_to_mapped_coefficient_max_difference':coefficient_difference,
                    'p0_norm_difference':norm_difference,'exact_band_array_identity':bool(np.array_equal(coefficients,first_coefficients))})
            del transform,table,centers,velocity,volumes,widths
        rows.append({'case_id':case_id,'archive_sha256':manifest['archive']['sha256'],
                     'prior_spatial_analysis_sha256':sha(prior_path),'stages':records})
    result={'status':'PASS_DECLARED_P0_SPECTRUM_FORMULAS_AND_ARCHIVED_CONTROLS','protocol_sha256':sha(PROTOCOL),
        'input_source_commit':spec['input_source_commit'],'cases':rows,'same_time_map_identities':identities,
        'source_sha256':{p:sha(ROOT/p) for p in ('tools/amr_p0_spectrum.py','tools/audit_amr_p0_spectrum.py',
            'tools/amr_projection_decomposition.py','tools/analyze_amr_mean_quality.py',
            'tools/analyze_amr_gauss_gradient.py','tools/compare_amr_resolution_volume_integrated.py')},
        'quality_verdict':'NO_NEW_QUALITY_THRESHOLD_OR_ORIGINAL_GATE_COMPLETION',
        'limits':spec['limits']}
    (output/'analysis.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps({'status':result['status'],'cases':len(rows),'stages':sum(len(r['stages']) for r in rows)}))
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--raw-map',required=True,type=Path)
    parser.add_argument('--output',required=True,type=Path)
    args=parser.parse_args();audit(args.raw_map,args.output)
