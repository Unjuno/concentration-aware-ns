"""Compare only completed tighter-tolerance cases with the archived baseline."""
import hashlib
import json
import re
from pathlib import Path
import numpy as np
from tools.analyze_openfoam import vectors


def alignment(us):
    a, b = (us[0]-us[1]).ravel(), (us[1]-us[2]).ravel()
    na, nb = np.linalg.norm(a), np.linalg.norm(b)
    assert na > 0 and nb > 0
    return {'cosine':float(a@b/(na*nb)), 'norm_order':float(np.log2(na/nb)), 'best_fit_scale':float(a@b/(nb*nb)), 'first_order_defect':float(np.linalg.norm(a-2*b)/na), 'relative_differences':[float(na/np.linalg.norm(us[-1])), float(nb/np.linalg.norm(us[-1]))]}


def completed_times(log):
    """OpenFOAM 13 writes dimensional time as e.g. `Time = 0.05s`."""
    return [float(value) for value in re.findall(
        r'^Time = ([+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?)s?\s*$',
        log, re.M)]


def main():
    root = Path('work/of13-iteration-sensitivity-v1')
    baseline = Path('work/of13-study-v1')
    spec = json.loads(Path('protocols/of13-iteration-sensitivity-v1.json').read_text())
    original, tight, rows = [], [], []
    for dt in spec['dt']:
        name = f'n{spec["n"]}-dt{dt}'
        case, old = root/name, baseline/name
        assert json.loads((case/'exit.json').read_text())['exit_code'] == 0
        log = (case/'log.foamRun').read_text()
        assert log.rstrip().endswith('End')
        times = completed_times(log)
        expected = round(spec['end']/dt)
        assert len(times) == expected and times[-1] == spec['end']
        c, co = vectors(case/'0.05/C', spec['n']**3), vectors(old/'0.05/C', spec['n']**3)
        assert np.array_equal(c, co)
        u, v = vectors(case/'0.05/U', spec['n']**3), vectors(old/'0.05/U', spec['n']**3)
        assert np.isfinite(u).all() and np.isfinite(v).all()
        tight.append(u); original.append(v)
        paths = [case/'0.05/U', old/'0.05/U', case/'log.foamRun']
        rows.append({'case':name, 'same_dt_relative_field_shift':float(np.linalg.norm(u-v)/np.linalg.norm(v)), 'steps':expected, 'outer_converged_steps':log.count('PIMPLE: Converged in'), 'all_steps_outer_converged':log.count('PIMPLE: Converged in') == expected, 'input_sha256':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}})
    result = {'cases':rows, 'original':alignment(original), 'tighter_iteration':alignment(tight), 'quality':'UNCERTAIN', 'scope':'Iteration sensitivity and observed difference geometry, not proof of asymptotic convergence or a continuum error bound'}
    Path('evidence/of13-iteration-sensitivity-v1/comparison.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
