"""Evidence-linked interval triage, not an independent scientific certification."""
import argparse
import hashlib
import json
import math
from pathlib import Path

REQUIRED=("reference_verified","forcing_verified","derivatives_verified",
          "space_time_study_verified","thresholds_preregistered",
          "raw_artifacts_reviewed","evaluation_time_verified",
          "standard_acceptance_verified")


def evaluate(report, artifact_root=None):
    result=dict(standard_acceptance='UNCERTAIN',local_quality='UNCERTAIN',hypothesis='UNCERTAIN')
    if not isinstance(report,dict) or report.get('schema_version')!=2 or artifact_root is None:return result
    evidence=report.get('evidence');artifacts=report.get('artifacts')
    if not isinstance(evidence,dict) or not isinstance(artifacts,dict):return result
    root=Path(artifact_root).resolve()
    for key in REQUIRED:
        if evidence.get(key) is not True:return result
        ref=artifacts.get(key)
        if not isinstance(ref,dict) or not isinstance(ref.get('path'),str) or not isinstance(ref.get('sha256'),str):return result
        path=Path(ref['path'])
        if path.is_absolute():return result
        path=(root/path).resolve()
        if not path.is_relative_to(root):return result
        try:
            if hashlib.sha256(path.read_bytes()).hexdigest()!=ref['sha256']:return result
        except OSError:return result
    standard=report.get('standard_acceptance')
    if standard in ('PASS','FAIL'):result['standard_acceptance']=standard
    metrics=report.get('metrics')
    if not isinstance(metrics,list) or not metrics:return result
    outcomes=[];names=set()
    for metric in metrics:
        if not isinstance(metric,dict):return result
        name=metric.get('name')
        if not isinstance(name,str) or not name or name in names:return result
        names.add(name)
        lo,hi,tol=[metric.get(k) for k in ('error_lower','error_upper','tolerance')]
        if any(type(v) not in (int,float) or not math.isfinite(v) or v<0 for v in (lo,tol)):return result
        # Missing upper bound is legitimate for a one-sided analytic estimate.
        if hi is not None and (type(hi) not in (int,float) or not math.isfinite(hi) or hi<lo):return result
        outcomes.append('FAIL' if lo>tol else 'PASS' if hi is not None and hi<=tol else 'UNCERTAIN')
    if not {'max_gradient','max_vorticity'}.issubset(names):return result
    result['local_quality']='FAIL' if 'FAIL' in outcomes else 'PASS' if all(v=='PASS' for v in outcomes) else 'UNCERTAIN'
    if standard=='PASS':
        result['hypothesis']={'FAIL':'REPRODUCED','PASS':'NOT_OBSERVED','UNCERTAIN':'UNCERTAIN'}[result['local_quality']]
    return result


def exit_code(result):
    if result['local_quality']=='FAIL' or result['standard_acceptance']=='FAIL':return 1
    if result['local_quality']=='PASS' and result['standard_acceptance']=='PASS':return 0
    return 2


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('report');parser.add_argument('--artifact-root');args=parser.parse_args()
    try:
        path=Path(args.report)
        result=evaluate(json.loads(path.read_text()),args.artifact_root or path.parent)
    except (OSError,ValueError):result=evaluate(None)
    print(json.dumps(result,indent=2));raise SystemExit(exit_code(result))
