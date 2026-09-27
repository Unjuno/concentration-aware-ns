"""Build the startup probe from the recorded image without a running solver."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--root', default='work/of13-startup-probe-v1')
    args=parser.parse_args()
    root=Path(args.root).resolve()
    root.mkdir(parents=True,exist_ok=False)
    recorded=json.loads(Path('evidence/of13-startup-probe-v1/build-result.json').read_text())
    image=recorded['image_id']
    # Fail if the exact local image is absent; do not silently follow a mutable tag.
    subprocess.run(['docker','image','inspect',image],check=True,stdout=subprocess.DEVNULL)
    container=subprocess.check_output(['docker','create',image],text=True).strip()
    commands=[]
    try:
        copy=['docker','cp',container+':/opt/openfoam13/applications/solvers/foamRun',str(root/'installed-foamRun')]
        commands.append(copy);subprocess.run(copy,check=True)
    finally:
        subprocess.run(['docker','rm',container],check=True,stdout=subprocess.DEVNULL)
    prepare=[sys.executable,'runtime/of13-startup-probe/prepare.py',str(root/'installed-foamRun'),str(root/'app')]
    commands.append(prepare);subprocess.run(prepare,check=True)
    build=['docker','run','--rm','--network','none','--entrypoint','/bin/bash','-v',f'{root}:/probe',image,'-c','source /opt/openfoam13/etc/bashrc && cd /probe/app && wmake > /probe/build.log 2>&1']
    commands.append(build)
    (root/'build-commands.json').write_text(json.dumps(commands,indent=2)+'\n')
    with (root/'build-container.log').open('w') as log:
        result=subprocess.run(build,stdout=log,stderr=subprocess.STDOUT)
    binary=root/'startupProbe'
    review={'image_id':image,'exit_code':result.returncode,'binary_exists':binary.exists()}
    if binary.exists():
        review['executable_sha256']=hashlib.sha256(binary.read_bytes()).hexdigest()
        review['matches_original_executable']=review['executable_sha256']==recorded['executable_sha256']
    (root/'build-review.json').write_text(json.dumps(review,indent=2)+'\n')
    print(json.dumps(review,indent=2))
    if result.returncode:raise SystemExit(result.returncode)


if __name__=='__main__':main()
