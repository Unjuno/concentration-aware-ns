"""Minimal uniform-grid L2 correction for an initialization-only control."""
import hashlib,json,re
from pathlib import Path
import numpy as np
from tools.analyze_openfoam import vectors
n=64;dx=2*np.pi/n
source=Path('work/of13-study-v1/n64-dt0.001/0/U')
u=vectors(source,n**3).reshape(n,n,n,3).transpose(2,1,0,3)
symbol=np.sin(2*np.pi*np.fft.fftfreq(n))/dx
symbol[0]=0;symbol[n//2]=0  # centered differences annihilate both modes exactly
q=np.stack(np.meshgrid(symbol,symbol,symbol,indexing='ij'),axis=-1)
denominator=np.sum(q*q,axis=-1);active=denominator>0
hat=np.fft.fftn(u,axes=(0,1,2));dot=np.sum(q*hat,axis=-1)
correction_hat=np.zeros_like(hat)
correction_hat[active]=q[active]* (dot[active]/denominator[active])[...,None]
corrected=np.fft.ifftn(hat-correction_hat,axes=(0,1,2)).real
correction=u-corrected
# Divergence and orthogonality checked in real space independently of FFT symbols.
def divergence(v):
 return sum((np.roll(v[...,j],-1,axis=j)-np.roll(v[...,j],1,axis=j))/(2*dx) for j in range(3))
residual=float(np.max(abs(divergence(corrected))))
assert residual<1e-12
orthogonality=float(abs(np.sum(corrected*correction))/(np.linalg.norm(corrected)*np.linalg.norm(correction)))
assert orthogonality<1e-11
output=Path('work/of13-solenoidal-initial-control-v1');output.mkdir(exist_ok=False)
text=source.read_text();flat=corrected.transpose(2,1,0,3).reshape(-1,3)
body='\n'.join('('+' '.join(f'{v:.17g}' for v in row)+')' for row in flat)
text,count=re.subn(r'(internalField\s+nonuniform\s+List<vector>\s+\d+\s*\()(.*?)(\)\s*;)',lambda m:m[1]+'\n'+body+'\n'+m[3],text,count=1,flags=re.S);assert count==1
(output/'U').write_text(text)
roundtrip=vectors(output/'U',n**3).reshape(n,n,n,3).transpose(2,1,0,3)
assert np.array_equal(roundtrip,corrected)
result={'source_U_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'control_U_sha256':hashlib.sha256((output/'U').read_bytes()).hexdigest(),'relative_initial_field_change':float(np.linalg.norm(correction)/np.linalg.norm(u)),'initial_divergence_max':float(np.max(abs(divergence(u)))),'control_divergence_max':residual,'normalized_orthogonality_defect':orthogonality,'zero_symbol_modes_preserved':int(np.sum(~active)),'scope':'Orthogonal projection onto centered discrete divergence kernel on uniform periodic grid; changed initial condition is a causal diagnostic, not the original MMS acceptance case','solver_executed':False}
Path('evidence/tests/openfoam-solenoidal-initial-control.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
