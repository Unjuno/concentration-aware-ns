"""Recheck published native samples and reproduce analytic ball enclosures."""
import argparse,json,shutil
from pathlib import Path
from tools.run_amr_mean_quality import ROOT,sha
from tools.analyze_of13_cell_point_matrix_query import analyze
from tools.audit_cell_point_uniform_ball_error import audit


def native_identity(evidence,protocol):
    spec=json.loads(Path(protocol).read_text());r=json.loads((evidence/'manifest.json').read_text())
    prior=json.loads((ROOT/'evidence/of13-cell-point-query-v1-n16/manifest.json').read_text())
    if r['upstream_commit']!=prior['upstream_commit'] or r['upstream_files_sha256']!=prior['upstream_files_sha256']:
        raise ValueError('published source identity differs from independent pin')
    lines=(evidence/'installed-source-files.sha256').read_text().splitlines()
    installed={line.split()[1].removeprefix('/opt/openfoam13/'):line.split()[0] for line in lines}
    if len(lines)!=len(installed) or installed!=r['upstream_files_sha256']:
        raise ValueError('published installed source identity differs')
    validation=json.loads((evidence/'independent-validation.json').read_text())
    if r['source_commit']!=validation['runtime_source_commit']:
        raise ValueError('runtime identity differs from independent receipt')
    if r['bundle_sha256']!=spec['release_sha256']:
        raise ValueError('published release identity differs')
    return r


def verify(output,verification_source_commit):
    output=Path(output)
    if output.exists():raise FileExistsError('preserve previous verification')
    output.mkdir(parents=True);results={}
    for key in ('n32','n64','n32half'):
        protocol=ROOT/f'protocols/of13-cell-point-matrix-query-{key}-v1.json'
        original=ROOT/'evidence/cell-point-matrix-native-query-v1'/key
        native_identity(original,protocol)
        dest=output/key/'native';shutil.copytree(original,dest)
        previous=json.loads((original/'analysis.json').read_text())
        current=analyze(dest,protocol)
        baseline=ROOT/'evidence/cell-point-uniform-ball-error-v2'/key/'analysis.json'
        old=json.loads(baseline.read_text());analytic=output/key/'analytic'
        audit(protocol,analytic,old['numerical_source_commit'])
        identical=(analytic/'analysis.json').read_bytes()==baseline.read_bytes()
        if not identical:raise ValueError('analytic published enclosure differs')
        results[key]={'native_status':current['status'],'native_analysis_equal':current==previous,'previous_measurements':previous['measurements'],'current_measurements':current['measurements'],'analytic_json_byte_identical':identical,'published_native_manifest_sha256':sha(original/'manifest.json'),'published_analytic_sha256':sha(baseline)}
    record={'status':'PUBLISHED_MATRIX_SAMPLES_AND_ANALYTIC_ENCLOSURES_VERIFIED','verification_source_commit':verification_source_commit,'results':results,'limits':['Finite native samples only; stock binaries are hashed receipts, not re-executed here','Recompute on installed host dependencies; no global search/continuity or physical claim','Small numeric diagnostic differences are preserved; analytic JSON equality required']}
    (output/'verification.json').write_text(json.dumps(record,indent=2,allow_nan=False)+'\n')
    print(record['status'],flush=True)
    return record


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);p.add_argument('--source-commit',required=True);a=p.parse_args();verify(a.output,a.source_commit)
