import json,tarfile,hashlib
from pathlib import Path


def main():
    out=Path('evidence/of13-amr-v1');out.mkdir(exist_ok=True);rows=[]
    for case in sorted(Path('work/of13-amr-v1').glob('cap*')):
        if not (case/'diagnostics.json').exists():continue
        d=json.loads((case/'diagnostics.json').read_text());dest=out/(case.name+'.tar.gz')
        if not dest.exists():
            with tarfile.open(dest,'w:gz') as tar:
                for p in case.iterdir():
                    if p.name!='dynamicCode':tar.add(p,arcname=p.name)
        else:
            with tarfile.open(dest,'r:gz') as tar:
                if tar.extractfile('diagnostics.json').read()!=(case/'diagnostics.json').read_bytes():raise ValueError('Version changed evidence explicitly')
        d['archive_sha256']=hashlib.sha256(dest.read_bytes()).hexdigest();rows.append(d)
    (out/'summary.json').write_text(json.dumps({'expected_cases':3,'completed_cases':len(rows),'quality':'UNCERTAIN','cases':rows},indent=2)+'\n')


if __name__=='__main__':main()
