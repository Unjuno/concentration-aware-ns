"""Archived uniform OpenFOAM fields through an alternative derivative diagnostic."""
import hashlib,json,math,tarfile,tempfile
from pathlib import Path
import numpy as np
from tools.analyze_openfoam import vectors
from tools.reference import fields
from tools.spectral_derivative import gradient

rows=[]
for archive in sorted(Path('evidence/of13-study-v1').glob('*.tar.gz')):
    with tarfile.open(archive) as tar, tempfile.TemporaryDirectory() as tmp:
        p=json.load(tar.extractfile('parameters.json'));n=p['n'];t=p['end']
        for field in ('U','C'):
            name=next(m.name for m in tar.getmembers() if len(m.name.split('/'))==2 and m.name.endswith('/'+field) and float(m.name.split('/')[0])==t)
            Path(tmp,field).write_bytes(tar.extractfile(name).read())
        centers=vectors(Path(tmp,'C'),n**3);u=vectors(Path(tmp,'U'),n**3)
    axis=(np.arange(n)+.5)*2*np.pi/n
    z,y,x=np.meshgrid(axis,axis,axis,indexing='ij')
    np.testing.assert_allclose(centers,np.stack((x,y,z),axis=-1).reshape(-1,3),atol=1e-12,rtol=0)
    ref=fields(centers,t,p['sigma'],p['nu'])
    grid=lambda v:v.reshape(n,n,n,3).transpose(2,1,0,3)
    actual=gradient(grid(u));control=gradient(grid(ref['u']))
    exact=ref['grad_u'].reshape(n,n,n,3,3).transpose(2,1,0,3,4)
    def curl(g):
        return np.stack((g[...,2,1]-g[...,1,2],g[...,0,2]-g[...,2,0],g[...,1,0]-g[...,0,1]),axis=-1)
    actual_w=curl(actual);control_w=curl(control);exact_w=grid(ref['vorticity'])
    P=math.sqrt(28)*math.exp(-t)/p['sigma']**2
    rows.append({'case':archive.name,'archive_sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),
                 'computed_gradient_peak':float(np.linalg.norm(actual,axis=(-2,-1)).max()),
                 'reference_spectral_gradient_peak':float(np.linalg.norm(control,axis=(-2,-1)).max()),
                 'exact_global_gradient_peak':P,
                 'computed_vorticity_relative_l2_at_samples':float(np.linalg.norm(actual_w-exact_w)/np.linalg.norm(exact_w)),
                 'reference_spectral_vorticity_relative_l2_at_samples':float(np.linalg.norm(control_w-exact_w)/np.linalg.norm(exact_w)),
                 'computed_vorticity_peak':float(np.linalg.norm(actual_w,axis=-1).max()),
                 'reference_spectral_vorticity_peak':float(np.linalg.norm(control_w,axis=-1).max()),
                 'computed_max_abs_divergence':float(np.abs(np.trace(actual,axis1=-2,axis2=-1)).max()),
                 'reference_max_abs_divergence':float(np.abs(np.trace(control,axis1=-2,axis2=-1)).max()),
                 'computed_gradient_relative_l2_at_samples':float(np.linalg.norm(actual-exact)/np.linalg.norm(exact)),
                 'reference_spectral_gradient_relative_l2_at_samples':float(np.linalg.norm(control-exact)/np.linalg.norm(exact))})
Path('evidence/tests/openfoam-spectral-gradient.json').write_text(json.dumps({'scope':'Real trigonometric interpolant derivative at verified uniform cell centers; no intersample accuracy or convergence certification.','cases':rows},indent=2)+'\n')
print(json.dumps(rows,indent=2))
