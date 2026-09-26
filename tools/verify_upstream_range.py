"""Replay the bounded new-range/old-dependency Lean compatibility check."""
import hashlib
import json
from pathlib import Path
import subprocess


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    root=Path(__file__).resolve().parents[1]
    manifest=json.loads((root/'evidence/upstream-refresh/range-check.json').read_text())
    work=root/'work/upstream-refresh'
    work.mkdir(parents=True,exist_ok=True)
    source=work/'NaturalAxisRange.lean'
    if not source.exists():
        response=subprocess.run(['gh','api',
            'repos/openai/NavierStokesAndEuler/contents/NavierStokes/NaturalAxisRange.lean?ref='+manifest['source_commit'],
            '-H','Accept: application/vnd.github.raw+json'],capture_output=True,check=True,timeout=60)
        source.write_bytes(response.stdout)
    if digest(source)!=manifest['source_sha256']:
        raise ValueError('Source hash differs from the reviewed module')
    check=work/'RangeCheck.lean'
    check.write_bytes(source.read_bytes()+manifest['check_suffix'].encode())
    if digest(check)!=manifest['check_sha256']:
        raise ValueError('Generated check hash mismatch')
    command=['docker','run','--rm','--name','cans-range-check','--user','501:20',
        '--network','none','--cpus=2','--memory=4g',
        '--mount','type=volume,src=cans-lean-verification,dst=/verify,readonly',
        '--mount',f'type=bind,src={work},dst=/extension,readonly',
        '-w','/verify/independent-source','--entrypoint','/bin/bash',
        'concentration-aware-ns:checker','-c',
        'export PATH=/verify/toolchain/bin:$PATH; lake env lean /extension/RangeCheck.lean']
    run=subprocess.run(command,capture_output=True,text=True)
    log=run.stdout+run.stderr
    output=root/'evidence/upstream-refresh/range-replay.log'
    output.write_text(log)
    expected="'NavierStokes.NaturalAxisRange.ofSmall' depends on axioms: [propext, Classical.choice, Quot.sound]"
    unchanged=digest(source)==manifest['source_sha256'] and digest(check)==manifest['check_sha256']
    success=run.returncode==0 and expected in log and 'sorryAx' not in log and unchanged
    result={'success':success,'exit_code':run.returncode,'scope':manifest['scope'],
        'source_commit':manifest['source_commit'],'dependency_commit':manifest['dependency_commit'],
        'source_sha256':manifest['source_sha256'],'check_sha256':manifest['check_sha256'],
        'source_and_check_unchanged':unchanged,'log_sha256':digest(output),
        'command':command,'runner_sha256':digest(Path(__file__))}
    (root/'evidence/upstream-refresh/range-replay.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'success':success,'exit_code':run.returncode}))
    return 0 if success else 1


if __name__=='__main__':
    raise SystemExit(main())
