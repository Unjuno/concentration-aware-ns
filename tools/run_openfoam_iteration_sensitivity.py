"""Run frozen tighter-iteration controls from byte-matched original inputs."""
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
from tools.analyze_openfoam import analyze


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    spec_path = Path('protocols/of13-iteration-sensitivity-v1.json')
    spec = json.loads(spec_path.read_text())
    root = Path('work/of13-iteration-sensitivity-v1').resolve()
    out = Path('evidence/of13-iteration-sensitivity-v1')
    root.mkdir(exist_ok=False)
    out.mkdir(exist_ok=False)
    image_id = subprocess.check_output(['docker', 'image', 'inspect', spec['image'], '--format', '{{.Id}}'], text=True).strip()
    results = []
    for dt in spec['dt']:
        name = f'n{spec["n"]}-dt{dt}'
        source = Path('work/of13-study-v1') / name
        case = root / name
        case.mkdir()
        baseline = Path('evidence/of13-study-v1') / (name+'.tar.gz')
        inputs = [p for folder in ('0', 'system') for p in (source/folder).rglob('*') if p.is_file()]
        inputs += [p for p in (source/'constant').iterdir() if p.is_file()]
        inputs += [source/'parameters.json']
        hashes = {}
        with tarfile.open(baseline) as archive:
            for p in inputs:
                relative = p.relative_to(source)
                assert p.read_bytes() == archive.extractfile(str(relative)).read()
                target = case/relative
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(p, target)
                hashes[str(relative)] = sha(p)
        fv = case/'system/fvSolution'
        text = fv.read_text()
        for old, new, expected in [('tolerance 1e-10;', 'tolerance 1e-12;', 2), ('tolerance 1e-8;', 'tolerance 1e-10;', 2), ('nOuterCorrectors 12;', 'nOuterCorrectors 40;', 1)]:
            assert text.count(old) == expected
            text = text.replace(old, new)
        fv.write_text(text)
        (case/'control-provenance.json').write_text(json.dumps({'protocol_sha256':sha(spec_path), 'baseline_archive_sha256':sha(baseline), 'baseline_input_hashes':hashes, 'modified_fvSolution_sha256':sha(fv), 'image_id':image_id}, indent=2)+'\n')
        command = ['docker', 'run', '--rm', '--network', 'none', '--name', f'cans-iter-{name}', '--entrypoint', '/bin/bash', '-v', f'{case}:/case', spec['image'], '-c', 'useradd -o -u "$1" -m runner && su runner -s /bin/bash -c "source /opt/openfoam13/etc/bashrc && cd /case && blockMesh > log.blockMesh 2>&1 && foamRun > log.foamRun 2>&1 && foamPostProcess -func writeCellCentres -latestTime > log.centres 2>&1"', '--', str(os.getuid())]
        (case/'command.json').write_text(json.dumps(command, indent=2)+'\n')
        print('START '+name, flush=True)
        with (case/'log.container').open('w') as log:
            run = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT)
        (case/'exit.json').write_text(json.dumps({'exit_code':run.returncode})+'\n')
        log = (case/'log.foamRun').read_text() if (case/'log.foamRun').exists() else ''
        if run.returncode == 0 and log.rstrip().endswith('End'):
            (case/'diagnostics.json').write_text(json.dumps(analyze(case), indent=2, allow_nan=False)+'\n')
        destination = out/(name+'.tar.gz')
        with tarfile.open(destination, 'w:gz') as archive:
            for p in sorted(case.rglob('*')):
                if p.is_file() and not any(part in ('dynamicCode', 'polyMesh') for part in p.relative_to(case).parts):
                    archive.add(p, arcname=str(p.relative_to(case)))
        row = {'case':name, 'exit_code':run.returncode, 'log_ends_with_End':log.rstrip().endswith('End'), 'time_steps':len(re.findall(r'^Time = ', log, re.M)), 'outer_converged_steps':log.count('PIMPLE: Converged in'), 'archive_sha256':sha(destination)}
        results.append(row)
        (out/'summary.json').write_text(json.dumps({'expected_cases':3, 'cases':results, 'quality':'UNCERTAIN'}, indent=2)+'\n')
        print('END '+json.dumps(row), flush=True)
        if run.returncode or not row['log_ends_with_End']:
            raise RuntimeError('Failed run preserved; inspect before continuing')


if __name__ == '__main__':
    main()
