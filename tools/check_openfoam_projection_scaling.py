"""Spatial refinement of two explicit startup operators, not new solver runs."""
import hashlib,json
from pathlib import Path
import numpy as np
from tools.analyze_openfoam import vectors
rows=[]
for n in [16,32,64]:
 path=Path(f'work/of13-study-v1/n{n}-dt0.001/0/U');dx=2*np.pi/n
 u=vectors(path,n**3).reshape(n,n,n,3).transpose(2,1,0,3)
 symbol=np.sin(2*np.pi*np.fft.fftfreq(n))/dx;symbol[0]=symbol[n//2]=0
 q=np.stack(np.meshgrid(symbol,symbol,symbol,indexing='ij'),axis=-1)
 squared=np.sum(q*q,axis=-1);active=squared>0
 hat=np.fft.fftn(u,axes=(0,1,2));dot=np.sum(q*hat,axis=-1)
 correction_hat=np.zeros_like(hat);correction_hat[active]=q[active]*(dot[active]/squared[active])[...,None]
 correction=np.fft.ifftn(correction_hat,axes=(0,1,2)).real
 div=sum((np.roll(u[...,j],-1,axis=j)-np.roll(u[...,j],1,axis=j))/(2*dx) for j in range(3))
 theta=np.meshgrid(*([2*np.pi*np.fft.fftfreq(n)]*3),indexing='ij')
 lap_symbol=-sum(4*np.sin(t/2)**2/dx**2 for t in theta)
 pi_hat=np.zeros(div.shape,dtype=complex);nz=lap_symbol!=0
 pi_hat[nz]=np.fft.fftn(div)[nz]/lap_symbol[nz]
 pi=np.fft.ifftn(pi_hat).real
 grad=np.stack([(np.roll(pi,-1,axis=j)-np.roll(pi,1,axis=j))/(2*dx) for j in range(3)],axis=-1)
 corrected=u-correction
 d_after=sum((np.roll(corrected[...,j],-1,axis=j)-np.roll(corrected[...,j],1,axis=j))/(2*dx) for j in range(3))
 assert np.max(abs(d_after))<1e-12
 rows.append({'n':n,'input_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'minimum_L2_correction_relative':float(np.linalg.norm(correction)/np.linalg.norm(u)),'face_laplacian_model_cell_correction_relative':float(np.linalg.norm(grad)/np.linalg.norm(u)),'pressure_impulse_rms':float(np.sqrt(np.mean(pi*pi))),'discrete_divergence_rms':float(np.sqrt(np.mean(div*div)))})
orders={key:[float(np.log2(rows[i][key]/rows[i+1][key])) for i in range(2)] for key in ['minimum_L2_correction_relative','face_laplacian_model_cell_correction_relative','pressure_impulse_rms','discrete_divergence_rms']}
result={'cases':rows,'observed_spatial_orders':orders,'scope':'Algebraic operators applied to archived initial samples; no new solver execution and no proven asymptotic rate from three samples','interpretation':'Quantifies whether fixed-grid startup correction shrinks under spatial refinement; does not explain late-time temporal-order result'}
Path('evidence/tests/openfoam-projection-scaling.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
