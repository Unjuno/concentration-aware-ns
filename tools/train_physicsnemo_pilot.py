"""Actual PINN training pilot; record failure/accuracy without acceptance claims."""
import json
import logging
from pathlib import Path
import time
import numpy as np
import torch
from tools.physicsnemo_equations import TransientNS
from physicsnemo.models.mlp.fully_connected import FullyConnected
from physicsnemo.sym.eq.phy_informer import PhysicsInformer
from tools.reference import fields
from tools.metrics import diagnostics

p=json.loads(Path('protocols/physicsnemo-pinn-pilot-v1.json').read_text())
root=Path('work/physicsnemo-pinn-pilot-v1');root.mkdir(exist_ok=False)
(root/'parameters.json').write_text(json.dumps(p,indent=2)+'\n')
torch.set_default_dtype(torch.float64);torch.set_num_threads(p['threads']);torch.manual_seed(p['seed'])
rng=np.random.default_rng(p['seed'])
net=FullyConnected(in_features=7,out_features=4,num_layers=p['layers'],layer_size=p['width'],activation_fn='tanh')
ns=TransientNS();inf=PhysicsInformer(required_outputs=list(ns.equations),equations=ns,grad_method='autodiff',device='cpu')
# The expected time-derivative warning repeats on introspection; the API contract
# and supplied derivatives are recorded in the independent residual audit.
logging.getLogger('physicsnemo.sym.eq.phy_informer').setLevel(logging.ERROR)

def output(x,t):
    psi=torch.exp(((torch.cos(x-torch.pi)-1)/p['sigma']**2).sum(dim=1,keepdim=True))
    g=-psi*torch.sin(x-torch.pi)/p['sigma']**2
    u0=torch.linalg.cross(g,torch.tensor([1.,2.,3.]).expand_as(g))
    raw=net(torch.cat((torch.sin(x),torch.cos(x),t/p['end']),dim=1))
    return u0+t*raw[:,:3],raw[:,3:4]

def residual(x,t,force):
    u,pressure=output(x,t);v={'coordinates':x,'p':pressure}
    for i,name in enumerate(('u','v','w')):
        v[name]=u[:,i:i+1]
        v[name+'__t']=torch.autograd.grad(u[:,i].sum(),t,create_graph=True,retain_graph=True)[0]
    for i,name in enumerate(('x','y','z')):v['f'+name]=torch.tensor(force[:,i:i+1])
    return inf.forward(v)

opt=torch.optim.Adam(net.parameters(),lr=p['learning_rate']);start=time.monotonic()
with (root/'training.jsonl').open('w') as log:
    for step in range(p['iterations']):
        xyz=(rng.integers(0,p['n'],(p['batch'],3))+.5)*2*np.pi/p['n']
        at=float(rng.integers(0,p['time_nodes']))*p['end']/(p['time_nodes']-1)
        x=torch.tensor(xyz,requires_grad=True);t=torch.full((p['batch'],1),at,requires_grad=True)
        rs=residual(x,t,fields(xyz,at)['force']);loss=sum((r*r).mean() for r in rs.values())
        if not torch.isfinite(loss):raise ValueError('nonfinite loss')
        opt.zero_grad();loss.backward();opt.step()
        if step%25==0 or step==p['iterations']-1:
            row={'iteration':step+1,'loss':float(loss.detach()),'elapsed_seconds':time.monotonic()-start}
            log.write(json.dumps(row)+'\n');log.flush();print(row,flush=True)
torch.save(net.state_dict(),root/'weights.pt')
n=p['evaluation_n'];axis=(np.arange(n)+.5)*2*np.pi/n
xyz=np.stack(np.meshgrid(axis,axis,axis,indexing='ij'),axis=-1).reshape(-1,3)
chunks=[]
with torch.no_grad():
    for i in range(0,len(xyz),256):
        x=torch.tensor(xyz[i:i+256]);t=torch.full((len(x),1),p['end']);chunks.append(output(x,t)[0].numpy())
u=np.concatenate(chunks);ref=fields(xyz,p['end']);diag=diagnostics(u.reshape(n,n,n,3))
result={'quality':'UNCERTAIN','velocity_relative_l2':float(np.linalg.norm(u-ref['u'])/np.linalg.norm(ref['u'])),
        'computed':diag,'reference_sampled_fd2':diagnostics(ref['u'].reshape(n,n,n,3)),
        'reference_gradient_peak_samples':float(np.linalg.norm(ref['grad_u'],axis=(-2,-1)).max()),
        'reference_vorticity_peak_samples':float(np.linalg.norm(ref['vorticity'],axis=-1).max()),
        'elapsed_seconds':time.monotonic()-start,'scope':p['scope']}
np.savez_compressed(root/'evaluation.npz',coordinates=xyz,velocity=u)
(root/'diagnostics.json').write_text(json.dumps(result,indent=2)+'\n')
(root/'exit_code').write_text('0\n');print('COMPLETE',result['velocity_relative_l2'],flush=True)
