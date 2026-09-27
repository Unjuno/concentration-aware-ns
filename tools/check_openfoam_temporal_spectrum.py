"""Post-hoc Fourier localization of archived temporal differences, not a gate."""
import hashlib,json,tarfile,tempfile
from pathlib import Path
import numpy as np
from tools.analyze_openfoam import vectors


def main():
 n=64
 validated=json.loads(Path('evidence/of13-solenoidal-late-control-v2/comparison.json').read_text())
 axis=(np.arange(n)+.5)*2*np.pi/n
 z,y,x=np.meshgrid(axis,axis,axis,indexing='ij');expected=np.stack((x,y,z),axis=-1).reshape(-1,3)
 k=np.fft.fftfreq(n)*n
 kz,ky,kx=np.meshgrid(k,k,k,indexing='ij');radius=np.sqrt(kx*kx+ky*ky+kz*kz)
 qaxis=np.sin(2*np.pi*k/n)/(2*np.pi/n)
 qaxis[(k==0)|(abs(k)==n/2)]=0
 qz,qy,qx=np.meshgrid(qaxis,qaxis,qaxis,indexing='ij')
 q=np.stack((qx,qy,qz),axis=-1);q2=np.sum(q*q,axis=-1)
 active=q2>0
 assert np.count_nonzero(~active)==8
 masks=[('0<=k<=4',radius<=4),('4<k<=8',(radius>4)&(radius<=8)),('8<k<=16',(radius>8)&(radius<=16)),('16<k<=32',(radius>16)&(radius<=32)),('k>32',radius>32)]
 assert np.all(sum(m.astype(int) for _,m in masks)==1)
 rows=[]
 for study in ('of13-iteration-sensitivity-v1','of13-solenoidal-late-control-v2'):
  us=[];hashes={}
  for row in validated['cases']:
   p=Path('evidence')/study/(row['case']+'.tar.gz');digest=hashlib.sha256(p.read_bytes()).hexdigest()
   assert digest==row['archive_sha256'][study];hashes[str(p)]=digest
   with tarfile.open(p) as tar,tempfile.TemporaryDirectory() as folder:
    for member in ('0.05/U','0.05/C'):
     out=Path(folder)/member;out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(tar.extractfile(member).read())
    c=vectors(Path(folder)/'0.05/C',n**3);assert np.allclose(c,expected,atol=1e-12,rtol=0)
    us.append(vectors(Path(folder)/'0.05/U',n**3).reshape(n,n,n,3))
  differences=[us[0]-us[1],us[1]-us[2]]
  transforms=[np.fft.fftn(d,axes=(0,1,2),norm='ortho') for d in differences]
  energy=[np.sum(abs(f)**2,axis=-1) for f in transforms]
  totals=[float(e.sum()) for e in energy]
  parseval=[abs(t-float(np.sum(d*d)))/t for t,d in zip(totals,differences)]
  assert max(parseval)<1e-12
  defect=np.sum(abs(transforms[0]-2*transforms[1])**2,axis=-1)
  components=[]
  for f,d in zip(transforms+[transforms[0]-2*transforms[1]],differences+[differences[0]-2*differences[1]]):
   dot=np.sum(q*f,axis=-1)
   real_div=sum((np.roll(d[...,j],-1,axis=a)-np.roll(d[...,j],1,axis=a))/(4*np.pi/n) for j,a in enumerate((2,1,0)))
   div_fft=np.fft.fftn(real_div,norm='ortho')
   stencil_defect=float(np.linalg.norm(div_fft-1j*dot)/np.linalg.norm(div_fft))
   assert stencil_defect<1e-12
   factor=np.divide(dot,q2,out=np.zeros_like(dot),where=active)
   longitudinal=q*factor[...,None]
   transverse=np.where(active[...,None],f-longitudinal,0)
   kernel=np.where(active[...,None],0,f)
   total=float(np.sum(abs(f)**2))
   energies=[float(np.sum(abs(v)**2)) for v in (longitudinal,transverse,kernel)]
   assert abs(sum(energies)-total)/total<1e-12
   residual=float(np.linalg.norm(np.sum(q*transverse,axis=-1)))
   assert residual/(np.sqrt(total)*np.max(np.sqrt(q2)))<1e-12
   components.append({'real_stencil_symbol_relative_defect':stencil_defect,'energy_fractions':dict(zip(('longitudinal','transverse_nonzero_symbol','zero_symbol_kernel'),[e/total for e in energies])),'energies':energies})
  component_orders={name:float(.5*np.log2(components[0]['energies'][i]/components[1]['energies'][i])) for i,name in enumerate(('longitudinal','transverse_nonzero_symbol','zero_symbol_kernel')) if min(components[0]['energies'][i],components[1]['energies'][i])>0}
  bands=[]
  for label,mask in masks:
   a,b=[float(e[mask].sum()) for e in energy]
   bands.append({'band':label,'difference_energy_fractions':[a/totals[0],b/totals[1]],'norm_order':float(.5*np.log2(a/b)) if a>0 and b>0 else None,'first_order_defect_energy_fraction':float(defect[mask].sum()/defect.sum())})
  rows.append({'study':study,'archives':hashes,'parseval_relative_defects':parseval,'bands':bands,'centered_divergence_decomposition':{'coarse_difference':components[0],'fine_difference':components[1],'first_order_defect':components[2],'component_norm_orders':component_orders,'symbol':'q_j=sin(k_j*dx)/dx; zero and Nyquist entries set exactly zero; eight zero-symbol modes kept separate'}})
 result={'studies':rows,'scope':'Post-hoc radial integer-wave-number bands on verified uniform 2pi-periodic mesh. Bands partition all modes; energy fractions concern temporal differences, not total solution energy. No continuum error bound or causal diagnosis.','quality':'UNCERTAIN'}
 Path('evidence/tests/openfoam-temporal-spectrum.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result,indent=2))


if __name__=='__main__':main()
