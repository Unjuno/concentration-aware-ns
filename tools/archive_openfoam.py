"""Archive completed study cases only; never infer success from an open process."""
import hashlib
import json
import re
import tarfile
from pathlib import Path


def archive():
    target=Path('evidence/of13-study-v1'); target.mkdir(exist_ok=True)
    rows=[]
    for case in sorted(Path('work/of13-study-v1').glob('n*')):
        if not (case/'diagnostics.json').exists():
            continue
        d=json.loads((case/'diagnostics.json').read_text())
        log=(case/'log.foamRun').read_text()
        files=[p for folder in ('0','system') for p in (case/folder).rglob('*') if p.is_file()]
        files += [p for p in (case/'constant').iterdir() if p.is_file()]
        files += [p for p in case.iterdir() if p.is_file()]
        time_dir=next(p for p in case.iterdir() if p.is_dir() and p.name[0].isdigit() and float(p.name)==d['parameters']['end'])
        files += [time_dir/name for name in ('U','p','C')]
        dest=target/(case.name+'.tar.gz')
        with tarfile.open(dest,'w:gz') as tar:
            for p in files:
                tar.add(p,arcname=str(p.relative_to(case)))
        rows.append({'case':case.name,'velocity_relative_l2':d['velocity_relative_l2'],
                     'gradient_peak_relative_error_cell_samples':d['gradient_peak_relative_error_cell_samples'],
                     'reference_only_fd_gradient_error':abs(d['reference_sampled_fd2']['max_gradient_fd2']-d['reference_gradient_peak_cell_samples'])/d['reference_gradient_peak_cell_samples'],
                     'time_steps':len(re.findall(r'^Time = ',log,re.M)),
                     'outer_converged_steps':len(re.findall('PIMPLE: Converged in',log)),
                     'archive_sha256':hashlib.sha256(dest.read_bytes()).hexdigest()})
    (target/'summary.json').write_text(json.dumps({'expected_cases':5,'completed_cases':len(rows),
      'quality':'UNCERTAIN','cases':rows},indent=2)+'\n')


if __name__=='__main__':
    archive()
