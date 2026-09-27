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
  bands=[]
  for label,mask in masks:
   a,b=[float(e[mask].sum()) for e in energy]
   bands.append({'band':label,'difference_energy_fractions':[a/totals[0],b/totals[1]],'norm_order':float(.5*np.log2(a/b)) if a>0 and b>0 else None,'first_order_defect_energy_fraction':float(defect[mask].sum()/defect.sum())})
  rows.append({'study':study,'archives':hashes,'parseval_relative_defects':parseval,'bands':bands})
 result={'studies':rows,'scope':'Post-hoc radial integer-wave-number bands on verified uniform 2pi-periodic mesh. Bands partition all modes; energy fractions concern temporal differences, not total solution energy. No continuum error bound or causal diagnosis.','quality':'UNCERTAIN'}
 Path('evidence/tests/openfoam-temporal-spectrum.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result,indent=2))


if __name__=='__main__':main()
