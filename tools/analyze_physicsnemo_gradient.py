"""Separate neural derivative error from FD2 postprocessing at identical samples."""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
import torch
from tools.physicsnemo_equations import TransientNS  # sets pinned source import path
from physicsnemo.models.mlp.fully_connected import FullyConnected
from tools.reference import fields

parser=argparse.ArgumentParser();parser.add_argument('case');args=parser.parse_args();root=Path(args.case)
if (root/'exit_code').read_text().strip()!='0':raise ValueError('incomplete run')
p=json.loads((root/'parameters.json').read_text());d=json.loads((root/'diagnostics.json').read_text())
torch.set_default_dtype(torch.float64);torch.set_num_threads(2)
net=FullyConnected(in_features=7,out_features=4,num_layers=p['layers'],layer_size=p['width'],activation_fn='tanh')
net.load_state_dict(torch.load(root/'weights.pt',map_location='cpu',weights_only=True));net.eval()
with np.load(root/'evaluation.npz') as a:xyz=a['coordinates'];saved=a['velocity']
max_g=max_w=max_error_g=max_error_w=prediction_difference=0.
for start in range(0,len(xyz),512):
    points=xyz[start:start+512];x=torch.tensor(points,requires_grad=True);t=torch.full((len(x),1),p['end'])
    psi=torch.exp(((torch.cos(x-torch.pi)-1)/p['sigma']**2).sum(dim=1,keepdim=True))
    g=-psi*torch.sin(x-torch.pi)/p['sigma']**2
    u0=torch.linalg.cross(g,torch.tensor([1.,2.,3.]).expand_as(g))
    raw=net(torch.cat((torch.sin(x),torch.cos(x),t/p['end']),dim=1));u=u0+t*raw[:,:3]
    prediction_difference=max(prediction_difference,float(np.abs(u.detach().numpy()-saved[start:start+len(x)]).max()))
    jac=torch.stack([torch.autograd.grad(u[:,i].sum(),x,retain_graph=True)[0] for i in range(3)],dim=1).numpy()
    w=np.stack((jac[:,2,1]-jac[:,1,2],jac[:,0,2]-jac[:,2,0],jac[:,1,0]-jac[:,0,1]),axis=1)
    ref=fields(points,p['end']);max_g=max(max_g,float(np.linalg.norm(jac,axis=(-2,-1)).max()));max_w=max(max_w,float(np.linalg.norm(w,axis=1).max()))
    max_error_g=max(max_error_g,float(np.linalg.norm(jac-ref['grad_u'],axis=(-2,-1)).max()))
    max_error_w=max(max_error_w,float(np.linalg.norm(w-ref['vorticity'],axis=1).max()))
if prediction_difference>1e-12:raise ValueError('checkpoint/evaluation mismatch')
r={'scope':'Analytic derivative of trained network at saved evaluation points, not continuous extrema.',
   'checkpoint_sha256':hashlib.sha256((root/'weights.pt').read_bytes()).hexdigest(),
   'evaluation_sha256':hashlib.sha256((root/'evaluation.npz').read_bytes()).hexdigest(),
   'prediction_difference':prediction_difference,'max_gradient_autograd_samples':max_g,'max_vorticity_autograd_samples':max_w,
   'max_gradient_fd2':d['computed']['max_gradient_fd2'],'max_vorticity_fd2':d['computed']['max_vorticity_fd2'],
   'gradient_peak_relative_error_samples':abs(max_g-d['reference_gradient_peak_samples'])/d['reference_gradient_peak_samples'],
   'vorticity_peak_relative_error_samples':abs(max_w-d['reference_vorticity_peak_samples'])/d['reference_vorticity_peak_samples'],
   'maximum_gradient_field_error_samples':max_error_g,'maximum_vorticity_field_error_samples':max_error_w,'quality':'UNCERTAIN'}
print(json.dumps(r,indent=2))
