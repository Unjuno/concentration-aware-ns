"""Check the helper literally extracted from the SU2 patch; excludes solver assembly."""
import hashlib
import json
from pathlib import Path
import subprocess
import numpy as np
from tools.reference import fields

patch=Path('runtime/su2/mms.patch')
added='\n'.join(line[1:] for line in patch.read_text().splitlines() if line.startswith('+') and not line.startswith('+++'))
helper=added[added.index('namespace {'):added.index('CUserDefinedSolution::CUserDefinedSolution')]
root=Path('work/su2-force-check');root.mkdir(exist_ok=True)
code='#include <cmath>\n#include <iostream>\n#include <iomanip>\nusing su2double=double;\n'+helper+'\nint main(){ double x[3],t,u[3],f[3];while(std::cin>>x[0]>>x[1]>>x[2]>>t){localized(x,t,.01,u,f);std::cout<<std::setprecision(17);for(auto v:u)std::cout<<v<<" ";for(auto v:f)std::cout<<v<<" ";std::cout<<"\\n";}}\n'
(root/'check.cpp').write_text(code)
subprocess.run(['c++','-std=c++17','-O2',str(root/'check.cpp'),'-o',str(root/'check')],check=True)
rng=np.random.default_rng(984);points=rng.uniform(0,2*np.pi,(64,3));t=.037
proc=subprocess.run([str(root/'check')],input='\n'.join(' '.join(map(repr,[*map(float,x),t])) for x in points)+'\n',capture_output=True,text=True,check=True)
actual=np.fromstring(proc.stdout,sep=' ').reshape(64,6);ref=fields(points,t,sigma=.5,nu=.01)
errors={name:float(np.max(np.abs(actual[:,sl]-ref[name]))) for name,sl in [('u',slice(0,3)),('force',slice(3,6))]}
if max(errors.values())>1e-11:raise ValueError(errors)
print(json.dumps({'points':64,'seed':984,'time':t,'maximum_absolute_errors':errors,'patch_sha256':hashlib.sha256(patch.read_bytes()).hexdigest(),'scope':'Compiled patch helper using double; not full SU2 integration, source sign, or nondimensionalization verification.'},indent=2))
