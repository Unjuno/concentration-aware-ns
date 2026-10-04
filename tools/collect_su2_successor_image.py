"""Collect actual successor identity before runs; no build or PDE execution."""
import argparse,json,hashlib,subprocess
from pathlib import Path
from tools.run_su2_full_horizon_cfl_pair import verify_successor_probe


def collect(image_id,output):
    if output.exists():raise FileExistsError('preserve previous image audit')
    if not image_id.startswith('sha256:') or len(image_id)!=71 or any(c not in '0123456789abcdef' for c in image_id[7:]):
        raise ValueError('explicit immutable image digest required')
    frozen=json.loads(Path('protocols/su2-n32-full-horizon-cfl-successor-v2.json').read_text())
    for path,digest in frozen['build_inputs_sha256'].items():
        if hashlib.sha256(Path(path).read_bytes()).hexdigest()!=digest:raise ValueError('recipe changed')
    output.mkdir()
    command=['docker','image','inspect',image_id,'--format','{{json .}}']
    result=subprocess.run(command,capture_output=True,text=True,timeout=10)
    (output/'inspect.stdout').write_text(result.stdout);(output/'inspect.stderr').write_text(result.stderr)
    if result.returncode:raise RuntimeError('image unavailable; no receipt emitted')
    image=json.loads(result.stdout)
    if image['Id']!=image_id or image.get('Os')!='linux' or image.get('Architecture')!='arm64':raise ValueError('image/platform mismatch')
    code="import json,hashlib,subprocess; from pathlib import Path; paths={'binary_sha256':'/opt/su2-install/bin/SU2_CFD','patched_source_sha256':'/opt/SU2/Common/src/toolboxes/MMS/CUserDefinedSolution.cpp','package_versions_sha256':'/opt/package-versions.txt'}; r={k:hashlib.sha256(Path(v).read_bytes()).hexdigest() for k,v in paths.items()}; r['compiler_version']=subprocess.check_output(['g++','--version'],text=True); print(json.dumps(r))"
    result=subprocess.run(['docker','run','--rm','--cpus','1','--entrypoint','python3',image_id,'-c',code],capture_output=True,text=True,timeout=30)
    (output/'probe.stdout').write_text(result.stdout);(output/'probe.stderr').write_text(result.stderr)
    if result.returncode:raise RuntimeError('probe failed; no receipt emitted')
    measured=json.loads(result.stdout);verify_successor_probe(measured,measured)
    receipt={**measured,'image_id':image_id,'source_commit':frozen['source_commit'],'architecture':frozen['architecture'],
             'build_inputs_sha256':frozen['build_inputs_sha256'],'scope':'Actual image files/compiler identities; recipe/source provenance is not independently proved by these hashes'}
    (output/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    return receipt


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--image-id',required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();collect(a.image_id,a.output)
