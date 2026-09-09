"""Compare archived final mean energies to the continuum analytic integral."""
import json
from pathlib import Path
import tarfile
from tools.reference_energy import mean_energy
rows=[]
for group in ('of13-study-v1','physicsnemo-study-v1'):
    for archive in sorted((Path('evidence')/group).glob('*.tar.gz')):
        with tarfile.open(archive) as tar:
            d=json.load(tar.extractfile('diagnostics.json'))
            try:p=d['parameters']
            except KeyError:p=json.load(tar.extractfile('parameters.json'))
        ref=mean_energy(p['end'],p['sigma']);actual=d['computed']['mean_kinetic_energy']
        rows.append({'group':group,'case':archive.name,'reference_continuum_mean_energy':ref,'computed_sample_mean_energy':actual,'relative_error':abs(actual-ref)/ref})
print(json.dumps({'scope':'Sample mean versus exact continuum formula; numerical-field quadrature and solution errors are combined, not separately certified.','cases':rows},indent=2))
