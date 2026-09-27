"""Leading small-dt startup projection model; not the complete PIMPLE equation."""
import hashlib,json
from pathlib import Path
import numpy as np
from tools.analyze_openfoam import vectors
from tools.analyze_amr import values
n=64;dx=2*np.pi/n
initial_path=Path('work/of13-study-v1/n64-dt0.001/0/U')
u=vectors(initial_path,n**3).reshape(n,n,n,3).transpose(2,1,0,3)
div=sum((np.roll(u[...,j],-1,axis=j)-np.roll(u[...,j],1,axis=j))/(2*dx) for j in range(3))
frequency=2*np.pi*np.fft.fftfreq(n)
k=np.meshgrid(frequency,frequency,frequency,indexing='ij')
eigen=-sum(4*np.sin(x/2)**2/dx**2 for x in k)
rhs=np.fft.fftn(div-div.mean());hat=np.zeros_like(rhs)
nonzero=eigen!=0;hat[nonzero]=rhs[nonzero]/eigen[nonzero]
pi=np.fft.ifftn(hat).real
lap=sum((np.roll(pi,-1,axis=j)-2*pi+np.roll(pi,1,axis=j))/dx**2 for j in range(3))
residual=float(np.max(abs(lap-(div-div.mean()))));assert residual<1e-12
gradient_pi=np.stack([(np.roll(pi,-1,axis=j)-np.roll(pi,1,axis=j))/(2*dx) for j in range(3)],axis=-1)
velocity_correction=-gradient_pi
corrected_u=u+velocity_correction
cell_div_after=sum((np.roll(corrected_u[...,j],-1,axis=j)-np.roll(corrected_u[...,j],1,axis=j))/(2*dx) for j in range(3))
sines=[np.sin(x/2)**2 for x in k]
weights=sum(sines)
residual_multiplier=np.zeros_like(weights)
residual_multiplier[nonzero]=sum(x*x for x in sines)[nonzero]/weights[nonzero]
predicted_div=np.fft.ifftn(np.fft.fftn(div)*residual_multiplier).real
symbol_residual=float(np.max(abs(cell_div_after-predicted_div)))
assert symbol_residual<1e-12
assert np.min(residual_multiplier)>=0 and np.max(residual_multiplier)<=1+1e-14
operator_review={'cell_divergence_after_model_max':float(np.max(abs(cell_div_after))),
                 'cell_divergence_before_max':float(np.max(abs(div))),
                 'residual_divergence_symbol_max_error':symbol_residual,
                 'face_flux_model_divergence_max':residual,
                 'symbol':'sum_j sin(theta_j/2)^4 / sum_j sin(theta_j/2)^2 for nonzero modes',
                 'scope':'Leading model only; cell gradient/divergence composition differs from face-flux Laplacian'}
rows=[]
for dt in [.001,.0005]:
 path=Path(f'work/of13-startup-time-v1/n64-dt{dt}/{dt}/p')
 p=values(path,n**3).reshape(n,n,n).transpose(2,1,0)
 observed=dt*(p-p.mean());difference=observed-pi
 velocity_path=path.with_name('U')
 got=vectors(velocity_path,n**3).reshape(n,n,n,3).transpose(2,1,0,3)
 # Subtract known smooth exponential evolution, retaining the numerical error.
 observed_velocity_error=got-np.exp(-dt)*u
 velocity_remainder=observed_velocity_error-velocity_correction
 velocity_review={'endpoint_U_sha256':hashlib.sha256(velocity_path.read_bytes()).hexdigest(),
                  'relative_remainder_to_predicted_correction':float(np.linalg.norm(velocity_remainder)/np.linalg.norm(velocity_correction)),
                  'error_correction_cosine':float(np.sum(observed_velocity_error*velocity_correction)/(np.linalg.norm(observed_velocity_error)*np.linalg.norm(velocity_correction))),
                  'predicted_relative_initial_velocity_change':float(np.linalg.norm(velocity_correction)/np.linalg.norm(u))}
 rows.append({'velocity_model':velocity_review,'dt':dt,'pressure_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'relative_centered_pressure_impulse_error':float(np.linalg.norm(difference)/np.linalg.norm(pi)),'observed_impulse_range':float(np.ptp(observed)),'model_impulse_range':float(np.ptp(pi)),'cosine':float(np.sum(observed*pi)/(np.linalg.norm(observed)*np.linalg.norm(pi)))})
result={'operator_review':operator_review,'initial_U_sha256':hashlib.sha256(initial_path.read_bytes()).hexdigest(),'poisson_max_absolute_residual':residual,'cases':rows,'model':'Uniform periodic nearest-neighbor Laplacian(pi)=central_div(U0), mean(pi)=0; leading approximation rAU~dt and HbyA~U0 predicts dt*p~pi','scope':'Frozen-grid leading startup balance only. Ignores finite-dt transport/source and pressure-correction details; comparison is post-hoc, not a causal intervention or complete solver derivation.'}
Path('evidence/of13-startup-time-v1/poisson-model.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
