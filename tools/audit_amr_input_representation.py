"""Verify archived initial U against independent point and cube-mean references."""
import argparse,hashlib,json,re,subprocess,tarfile
from pathlib import Path

import numpy as np

from tools.amr_p0_spectrum import reference_coefficients
from tools.high_gradient_cell_average import exact_cell_average_velocity
from tools.analyze_amr_gauss_gradient import _read_csv,_vector
from tools.analyze_amr_mean_quality import verify_archive
from tools.run_amr_mean_quality import ROOT,SOURCE_FILES,sha


def diagnose(centers,values,n,frequency=3):
    centers=np.asarray(centers);values=np.asarray(values)
    if centers.shape!=(n**3,3) or values.shape!=centers.shape or not np.isfinite(values).all():
        raise ValueError('complete finite uniform initial field required')
    modes=np.array([(x,y,z) for x in (-frequency,frequency) for y in range(-4,5) for z in range(-4,5)])
    coefficients=reference_coefficients(modes,frequency,0.)
    point=np.empty_like(values,dtype=float);imaginary=0.
    for start in range(0,len(values),4096):
        result=np.exp(1j*(centers[start:start+4096]@modes.T))@coefficients
        point[start:start+4096]=result.real
        imaginary=max(imaginary,float(np.max(np.abs(result.imag))))
    mean=exact_cell_average_velocity(centers,2*np.pi/n,0.,frequency)
    point_error=float(np.linalg.norm(values-point)/np.linalg.norm(point))
    mean_error=float(np.linalg.norm(values-mean)/np.linalg.norm(mean))
    return {'relative_l2_vs_point_reference':point_error,'relative_l2_vs_exact_cube_mean':mean_error,
        'point_to_mean_relative_l2':float(np.linalg.norm(point-mean)/np.linalg.norm(mean)),
        'maximum_absolute_point_difference':float(np.max(np.abs(values-point))),
        'maximum_reference_imaginary_residual':imaginary,
        'point_matches_at_recipe_tolerance':point_error<=2e-12,
        'exact_mean_matches_at_recipe_tolerance':mean_error<=2e-12,
        'scope':'Initial values only; numerical recipe check, not a solver quality gate or attribution of final error.'}


def parse_vectors(text,count):
    text=re.sub(r'/\*.*?\*/|//[^\n]*','',text,flags=re.S)
    match=re.search(r'internalField\s+nonuniform\s+List<vector>\s+(\d+)\s*\((.*?)\)\s*;',text,re.S)
    if not match or int(match[1])!=count or re.search(r'format\s+binary',text):
        raise ValueError('matching nonuniform ASCII initial vectors required')
    data=np.fromstring(match[2].replace('(',' ').replace(')',' '),sep=' ')
    if data.size!=3*count or not np.isfinite(data).all():raise ValueError('invalid initial vectors')
    return data.reshape(count,3)


def audit(raw_map,upstream,output,source_commit):
    protocol=ROOT/'protocols/amr-input-representation-audit-v1.json';spec=json.loads(protocol.read_text())
    inputs_path=ROOT/spec['input_protocol'];inputs=json.loads(inputs_path.read_text())
    raw_map=json.loads(Path(raw_map).read_text());upstream=Path(upstream);output=Path(output)
    if output.exists():raise FileExistsError('refuse to replace prior input audit')
    if set(raw_map)!=set(spec['case_ids']):raise ValueError('complete archive map required')
    source_rows=[]
    for p in spec['upstream_files']:
        blob=subprocess.check_output(['git','-C',str(upstream),'show',spec['upstream_commit']+':'+p])
        if (upstream/p).read_bytes()!=blob:raise ValueError('local upstream file differs from pin')
        source_rows.append({'path':p,'sha256':hashlib.sha256(blob).hexdigest(),
            'url':'https://github.com/OpenFOAM/OpenFOAM-13/blob/'+spec['upstream_commit']+'/'+p})
    rows=[]
    for case_id in spec['case_ids']:
        case=next(c for c in inputs['cases'] if c['id']==case_id)
        manifest=json.loads((ROOT/spec['input_evidence']/case_id/'manifest.json').read_text())
        if (manifest['source_commit']!=spec['input_source_commit'] or manifest['case_id']!=case_id
                or manifest['protocol_sha256']!=sha(inputs_path)
                or set(manifest['source_files_sha256'])!=set(SOURCE_FILES)
                or any(sha(ROOT/p)!=h for p,h in manifest['source_files_sha256'].items())):
            raise ValueError('frozen input source identity failed')
        archive=Path(raw_map[case_id]);verify_archive(archive,manifest)
        table=_read_csv(archive,'main/postProcessing/amrStages/0.002/preMap_cells.csv')
        if len(table['cell'])!=case['n']**3 or not np.array_equal(table['cell'],np.arange(case['n']**3)):
            raise ValueError('uniform original cell labels/order unverified')
        with tarfile.open(archive,'r:gz') as tf:
            data=tf.extractfile('main/0/U').read();forcing=tf.extractfile('main/constant/fvModels').read()
        result=diagnose(_vector(table,('cx','cy','cz')),parse_vectors(data.decode(),case['n']**3),case['n'])
        if not result['point_matches_at_recipe_tolerance'] or result['exact_mean_matches_at_recipe_tolerance']:
            raise ValueError('archived initialization differs from source-derived point recipe')
        for anchor in (b'const vectorField& centers = mesh().C();',b'source[celli] -= volumes[celli]*forcing;'):
            if forcing.count(anchor)!=1:raise ValueError('forcing centre/volume source anchors changed')
        rows.append({'case_id':case_id,'archive_sha256':manifest['archive']['sha256'],
            'initial_U_sha256':hashlib.sha256(data).hexdigest(),'fvModels_sha256':hashlib.sha256(forcing).hexdigest(),
            'diagnostic':result,'forcing_representation':'Centre-evaluated analytic force multiplied by cell volume; not independently integrated exact force average.'})
    record={'status':'VERIFIED_POINT_INITIALIZATION_AND_CENTRE_FORCING_RECIPE','numerical_source_commit':source_commit,
        'protocol_sha256':sha(protocol),'input_protocol_sha256':sha(inputs_path),'cases':rows,'pinned_upstream_files':source_rows,
        'source_sha256':{p:sha(ROOT/p) for p in ('tools/audit_amr_input_representation.py','tools/amr_p0_spectrum.py','tools/high_gradient_cell_average.py','tools/openfoam_case.py','tools/openfoam_amr_case.py','tools/run_amr_mean_quality.py')},
        'contract_disposition':'Exact native-average H1 preservation is a benchmark analysis condition; no such upstream exact-reconstruction guarantee established by these inspected files/docs.',
        'limits':spec['limits']}
    output.mkdir(parents=True);(output/'analysis.json').write_text(json.dumps(record,indent=2,allow_nan=False)+'\n')
    print(json.dumps({'status':record['status'],'cases':len(rows)}));return record


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--raw-map',required=True,type=Path)
    p.add_argument('--upstream',required=True,type=Path);p.add_argument('--output',required=True,type=Path)
    p.add_argument('--source-commit',required=True);a=p.parse_args();audit(a.raw_map,a.upstream,a.output,a.source_commit)
