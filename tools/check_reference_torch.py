"""Independent autograd check of the reference; not a PhysicsNeMo execution."""
import json
import numpy as np
import torch
from tools.reference import fields

torch.set_default_dtype(torch.float64)
rng=np.random.default_rng(127)
points=rng.uniform(0,2*np.pi,(96,3));times=rng.uniform(0,.1,(96,1))
c=torch.tensor(np.concatenate((points,times),axis=1),requires_grad=True)
psi=torch.exp(-c[:,3]+((torch.cos(c[:,:3]-torch.pi)-1)/.25).sum(dim=1))
gradpsi=torch.autograd.grad(psi.sum(),c,create_graph=True)[0][:,:3]
u=torch.linalg.cross(gradpsi,torch.tensor([1.,2.,3.]).expand_as(gradpsi))
grad=torch.stack([torch.autograd.grad(u[:,i].sum(),c,create_graph=True)[0] for i in range(3)],dim=1)
lap=torch.stack([sum(torch.autograd.grad(grad[:,i,j].sum(),c,retain_graph=True)[0][:,j] for j in range(3)) for i in range(3)],dim=1)
f=grad[:,:,3]+torch.einsum('bij,bj->bi',grad[:,:,:3],u)-.01*lap
ref=[fields(points[i:i+1],float(times[i,0])) for i in range(len(points))]
errors={}
for name,actual in [('u',u),('grad_u',grad[:,:,:3]),('force',f)]:
 expected=np.concatenate([r[name] for r in ref])
 errors[name]=float(np.abs(actual.detach().numpy()-expected).max())
if max(errors.values())>1e-10:raise ValueError(errors)
print(json.dumps({'torch':torch.__version__,'dtype':'float64','device':'cpu','seed':127,'samples':96,'maximum_absolute_errors':errors,'scope':'PyTorch autograd of analytic potential; not PhysicsNeMo evaluation or neural solution.'},indent=2))
