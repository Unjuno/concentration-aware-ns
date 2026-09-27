"""Initial sampled velocity divergence under uniform arithmetic face fluxes."""
import hashlib
import json
from pathlib import Path
import numpy as np
from tools.analyze_openfoam import vectors
from tools.reference import fields

rows = []
for n in [16, 32, 64]:
    root = Path(f'work/of13-study-v1/n{n}-dt0.001')
    path = root/'0/U'
    u = vectors(path, n**3).reshape(n,n,n,3).transpose(2,1,0,3)
    dx = 2*np.pi/n
    # Unit-area-normalized face flux, evaluated with arithmetic interpolation.
    face_div = np.zeros((n,n,n))
    central_div = np.zeros_like(face_div)
    for axis in range(3):
        component = u[...,axis]
        plus = (component+np.roll(component,-1,axis=axis))/2
        minus = np.roll(plus,1,axis=axis)
        face_div += (plus-minus)/dx
        central_div += (np.roll(component,-1,axis=axis)-np.roll(component,1,axis=axis))/(2*dx)
    assert np.allclose(face_div,central_div,atol=2e-14,rtol=0)
    centers = vectors(root/'0.05/C',n**3)
    axis_values=(np.arange(n)+.5)*dx
    zz,yy,xx=np.meshgrid(axis_values,axis_values,axis_values,indexing='ij')
    initial_points=np.stack([xx,yy,zz],axis=-1).reshape(-1,3)
    assert np.allclose(centers,initial_points,atol=1e-12,rtol=0)
    analytic = fields(initial_points,0)['u']
    assert np.allclose(u.transpose(2,1,0,3).reshape(-1,3),analytic,atol=1e-14,rtol=1e-14)
    rows.append({'n':n,'initial_U_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                 'divergence_max':float(abs(face_div).max()),
                 'divergence_rms':float(np.sqrt(np.mean(face_div**2))),
                 'mean_divergence':float(np.mean(face_div)),
                 'flux_and_centered_difference_match':True})
result={'cases':rows,'scope':'Arithmetic face-flux diagnostic on the recorded uniform periodic initial velocity; actual OpenFOAM phi initialization/correction is not traced here',
        'interpretation':'Continuum solenoidality does not make these sampled arithmetic face fluxes discretely divergence-free. Startup projection is a candidate to investigate, not an established explanation of temporal order.',
        'upstream_defect_established':False}
Path('evidence/tests/openfoam-initial-flux.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
