"""Execute pinned PhysicsInformer on the exact transient 3D reference."""
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path('work/physicsnemo-source').resolve()))
import numpy as np
import torch
from sympy import Function, Symbol
from physicsnemo.sym.eq.pde import PDE
from physicsnemo.sym.eq.phy_informer import PhysicsInformer
from tools.reference import fields

from tools.physicsnemo_equations import TransientNS

torch.set_default_dtype(torch.float64)
rng=np.random.default_rng(481);points=rng.uniform(0,2*np.pi,(96,3));time=.037
coords=torch.tensor(points,requires_grad=True);t=torch.full((96,1),time,requires_grad=True)
d=coords-torch.pi
psi=torch.exp(-t+((torch.cos(d)-1)/.25).sum(dim=1,keepdim=True))
g=-psi*torch.sin(d)/.25
u=torch.linalg.cross(g,torch.tensor([1.,2.,3.]).expand_as(g))
values={'coordinates':coords,'p':coords.sum(dim=1,keepdim=True)*0}
for i,name in enumerate(('u','v','w')):
    values[name]=u[:,i:i+1]
    values[name+'__t']=torch.autograd.grad(u[:,i].sum(),t,create_graph=True,retain_graph=True)[0]
force=fields(points,time)['force']
for i,name in enumerate(('x','y','z')):values['f'+name]=torch.tensor(force[:,i:i+1])
model=TransientNS();informer=PhysicsInformer(required_outputs=list(model.equations),equations=model,grad_method='autodiff',device='cpu')
result=informer.forward(values)
errors={k:float(v.detach().abs().max()) for k,v in result.items()}
if max(errors.values())>1e-10:raise ValueError(errors)
print(json.dumps({'samples':96,'seed':481,'time':time,'dtype':'float64','maximum_absolute_residuals':errors,'required_inputs':informer.required_inputs,'scope':'Exact manufactured field; time derivatives supplied explicitly, spatial derivatives by PhysicsInformer. No neural training or approximation-quality verdict.'},indent=2))
