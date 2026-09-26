"""Replay raw boundary-time observations, independent of runner coordinate masks."""
import csv
import hashlib
import io
import json
import math
from pathlib import Path
import tarfile


def check(root=Path('evidence/su2-boundary-time-pilot-v1')):
    protocol=json.loads(Path('protocols/su2-boundary-time-pilot-v1.json').read_text())
    summary=json.loads((root/'summary.json').read_text())
    assert [c['variant'] for c in summary['cases']]==['original','shifted']
    rows=[]
    for case in summary['cases']:
        path=root/(case['variant']+'.tar.gz')
        assert hashlib.sha256(path.read_bytes()).hexdigest()==case['archive_sha256']
        with tarfile.open(path) as archive:
            def read(name):
                return archive.extractfile(name).read().decode()
            assert read('exit_code').strip()=='0'
            params=json.loads(read('parameters.json'))
            assert all(params[key]==value for key,value in protocol.items())
            assert params['image_id']==case['image_id']
            config=read('case.cfg')
            assert 'MARKER_CUSTOM= (x0, x1, y0, y1, z0, z1)' in config
            assert 'MARKER_PERIODIC=' not in config
            assert 'TIME_MARCHING= '+protocol['scheme'] in config
            history=[{k.strip().strip('"'):float(v) for k,v in row.items()} for row in csv.DictReader(io.StringIO(read('history.csv')))]
            steps=round(protocol['end']/protocol['dt']);assert len(history)==steps
            width=protocol['n']+1
            for k in range(1,steps+1):
                records=list(csv.DictReader(io.StringIO(read(f'restart_{k-1:05d}.csv'))))
                ids=[int(r['PointID']) for r in records]
                assert sorted(ids)==list(range(width**3))
                boundary=[r for r in records if any(v in [0,width-1] for v in [int(r['PointID'])%width,(int(r['PointID'])//width)%width,int(r['PointID'])//width**2])]
                assert len(boundary)==width**3-(width-2)**3
                ux=[float(r['Velocity_x']) for r in boundary];assert all(math.isfinite(x) for x in ux)
                errors={name:max(abs(x-(1+t*t)) for x in ux) for name,t in [('old',(k-1)*protocol['dt']),('target',k*protocol['dt'])]}
                predicted='old' if case['variant']=='original' else 'target'
                assert errors[predicted]<protocol['boundary_absolute_tolerance']
                assert errors['target' if predicted=='old' else 'old']>protocol['boundary_absolute_tolerance']
                residuals={key:history[k-1][key] for key in ['rms[P]','rms[U]','rms[V]','rms[W]']}
                assert all(math.isfinite(x) and x<protocol['log10_residual_threshold'] for x in residuals.values())
                assert abs(history[k-1]['Cur_Time']-(k-1)*protocol['dt'])<1e-12
                rows.append({'variant':case['variant'],'step':k,'boundary_count':len(boundary),'errors':errors,'reported_time':history[k-1]['Cur_Time'],'residuals':residuals})
    return {'success':True,'scope':'Archived two-step boundary-time observations only; no temporal-order, restart or general-fix claim.','checks':rows}


if __name__=='__main__':
    result=check()
    Path('evidence/tests/su2-boundary-time-pilot.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
