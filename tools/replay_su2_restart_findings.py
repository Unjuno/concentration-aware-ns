"""Reproduce a specific scientific FAIL without accepting arbitrary process failures."""
import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys


def reproduced(result, code, protocol):
    if code != 1 or result.get('success') is not False or result.get('field_comparison_pass') is not True:
        return False
    expected={(v,m) for v in ['original','shifted'] for m in ['continuous','resumed']}
    history=result.get('history',[])
    if len(history)!=4 or {(r.get('variant'),r.get('mode')) for r in history}!=expected:
        return False
    R=protocol['restart_iter'];dt=protocol['dt'];steps=round(protocol['end']/dt)
    for row in history:
        resumed=row['mode']=='resumed'
        target=[k*dt for k in range(R if resumed else 0,steps)]
        observed=[(k-R+1)*dt if resumed else k*dt for k in range(R if resumed else 0,steps)]
        for key,values in [('times',observed),('expected_continuous_times',target)]:
            actual=row.get(key,[])
            if len(actual)!=len(values) or any(not math.isfinite(x) or abs(x-y)>1e-12 for x,y in zip(actual,values)):
                return False
        if row.get('history_time_matches') is not (not resumed):
            return False
    comparisons=result.get('comparisons',[])
    targets={(v,k) for v in ['original','shifted'] for k in range(R,steps)}
    if len(comparisons)!=len(targets) or {(r.get('variant'),r.get('saved_index')) for r in comparisons}!=targets:
        return False
    for row in comparisons:
        errors=row.get('max_differences',{})
        if set(errors)!={'Pressure','Velocity_x','Velocity_y','Velocity_z'}:
            return False
        if any(not math.isfinite(v) or not 0<=v<protocol['comparison_absolute_tolerance'] for v in errors.values()):
            return False
    return True


def main():
    records=[]
    for name in ['v1','r3']:
        path=Path(f'protocols/su2-restart-time-pilot-{name}.json')
        protocol=json.loads(path.read_text())
        command=[sys.executable,'-m','tools.check_su2_restart_time_pilot','--protocol',str(path)]
        run=subprocess.run(command,capture_output=True,text=True)
        try: result=json.loads(run.stdout)
        except json.JSONDecodeError: raise RuntimeError(f'{name}: checker did not emit a complete result: {run.stderr}')
        if not reproduced(result,run.returncode,protocol):
            raise RuntimeError(f'{name}: expected finding not reproduced')
        evidence=Path('evidence')/path.stem/'replay-review.json'
        if json.loads(evidence.read_text())!=result:raise RuntimeError('stdout/file mismatch')
        records.append({'protocol':str(path),'checker_exit_code':run.returncode,'finding_reproduced':True,'scientific_time_continuity_pass':False,'field_comparison_pass':True,'result_sha256':hashlib.sha256(evidence.read_bytes()).hexdigest()})
    output={'success':True,'scope':'Specific archived restart mismatch reproduced; time continuity remains FAIL. No new solver run or accuracy certification.','records':records}
    Path('evidence/tests/su2-restart-findings-replay.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps(output,indent=2))


if __name__=='__main__':main()
