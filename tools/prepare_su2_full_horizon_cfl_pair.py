"""Reconstruct the paired inputs from a hash-verified original archive."""
import argparse,json,hashlib,tarfile
from pathlib import Path
from tools.verify_su2_cfl_pair_inputs import verify


def prepare(output,protocol):
    if output.exists():raise FileExistsError('preserve previous prepared inputs')
    p=json.loads(protocol.read_text());archive=Path('evidence/su2-study-v1')/(p['case']+'.tar.gz')
    if hashlib.sha256(archive.read_bytes()).hexdigest()!=p['baseline_archive_sha256']:raise ValueError('original archive changed')
    with tarfile.open(archive) as stream:
        cfg=stream.extractfile('case.cfg').read();mesh=stream.extractfile('mesh.su2').read();params=stream.extractfile('parameters.json').read()
    if cfg.count(b'CFL_NUMBER= 10\n')!=1:raise ValueError('unexpected original CFL')
    output.mkdir()
    for label,cfl in [('baseline',10),('control',100)]:
        case=output/label;case.mkdir();(case/'case.cfg').write_bytes(cfg.replace(b'CFL_NUMBER= 10\n',f'CFL_NUMBER= {cfl}\n'.encode()));(case/'mesh.su2').write_bytes(mesh);(case/'parameters.json').write_bytes(params)
    return verify(output,protocol)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);p.add_argument('--protocol',type=Path,required=True);a=p.parse_args();print(json.dumps(prepare(a.output,a.protocol),indent=2))
