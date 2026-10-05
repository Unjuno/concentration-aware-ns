"""Verify prepared full-horizon inputs; never launch a solver."""
import argparse,json,hashlib
from pathlib import Path


def verify(root,protocol):
    p=json.loads(Path(protocol).read_text());configs={};rows=[]
    for label,cfl in [('baseline',10),('control',100)]:
        case=Path(root)/label;cfg=(case/'case.cfg').read_bytes();mesh=(case/'mesh.su2').read_bytes()
        if hashlib.sha256(cfg).hexdigest()!=p[label+'_config_sha256']:raise ValueError('configuration identity mismatch')
        if hashlib.sha256(mesh).hexdigest()!=p['mesh_sha256']:raise ValueError('mesh identity mismatch')
        params=json.loads((case/'parameters.json').read_text())
        if any(params[k]!=v for k,v in [('n',32),('dt',.001),('end',.05),('sigma',.5),('nu',.01)]):raise ValueError('parameter mismatch')
        if params['image_id']!=p['image_id_required']:raise ValueError('original image metadata mismatch')
        token=f'CFL_NUMBER= {cfl}\n'.encode()
        if cfg.count(token)!=1:raise ValueError('CFL assignment missing or duplicated')
        configs[label]=cfg
        rows.append({'case':label,'CFL_NUMBER_from_actual_config':cfl,'expected_updates':50})
    if configs['control'].replace(b'CFL_NUMBER= 100\n',b'CFL_NUMBER= 10\n')!=configs['baseline']:raise ValueError('non-CFL configuration change')
    return {'status':'PREPARED_INPUTS_IDENTICAL_EXCEPT_CFL','cases':rows,
            'limits':['Input verification only; image availability and source equivalence are separate',
                      'No solver run, residual, final-time accuracy or acceptance result']}


if __name__=='__main__':
    a=argparse.ArgumentParser(description=__doc__);a.add_argument('--root',type=Path,required=True);a.add_argument('--protocol',type=Path,required=True);a.add_argument('--output',type=Path,required=True);v=a.parse_args()
    if v.output.exists():raise FileExistsError('preserve earlier verification')
    v.output.write_text(json.dumps(verify(v.root,v.protocol),indent=2)+'\n')
