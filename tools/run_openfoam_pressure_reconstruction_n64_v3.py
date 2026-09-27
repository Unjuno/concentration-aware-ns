"""Run the frozen n=64 pressure diagnostic triple in the pinned OpenFOAM image."""
import hashlib
import json
import os
import shutil
import subprocess
import tarfile
from pathlib import Path


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def run(cmd, log):
    with Path(log).open('w') as out:
        return subprocess.run(cmd, stdout=out, stderr=subprocess.STDOUT).returncode


def main():
    study = 'of13-pressure-reconstruction-n64-v3'
    root = (Path('work') / study).resolve()
    root.mkdir(parents=True, exist_ok=True)
    spec = json.loads(Path('protocols/of13-pressure-reconstruction-n64-v3.json').read_text())
    image = spec['image_id']
    subprocess.run(['docker', 'image', 'inspect', image], check=True, stdout=subprocess.DEVNULL, timeout=60)
    module = root / 'module-original'
    lib = root / 'diag/lib/libincompressibleFluid.so'
    if not module.exists():
        container = subprocess.check_output(['docker', 'create', image], text=True).strip()
        try:
            subprocess.run(['docker', 'cp', container + ':/opt/openfoam13/applications/modules/incompressibleFluid', str(module)], check=True)
        finally:
            subprocess.run(['docker', 'rm', container], check=True, stdout=subprocess.DEVNULL, timeout=10)
    orig_hash = sha(module / 'correctPressure.C')
    assert orig_hash == spec['source_sha256']
    modified = root / 'module-diagnostic'
    if not lib.exists():
        modified = root / 'module-diagnostic'
        shutil.copytree(module, modified, ignore=shutil.ignore_patterns('linux*'))
        src = modified / 'correctPressure.C'
        text = src.read_text().replace('#include "incompressibleFluid.H"', '#include "incompressibleFluid.H"\n#include <type_traits>')
        anchor = '    volScalarField& p(p_);'
        assert text.count(anchor) == 1
        text = text.replace(anchor, '''    const bool cansWrite = mesh.time().writeTime();
        const auto cansSnapshot = [&](const word& name, const auto& field)
        {
            if (cansWrite)
            {
                typename std::decay<decltype(field)>::type snapshot
                (
                    IOobject(name, mesh.time().name(), mesh, IOobject::NO_READ, IOobject::NO_WRITE, false),
                    field
                );
                snapshot.write();
            }
        };
    '''.replace('+', '') + anchor)
        anchor = '    p.relax();'
        assert text.count(anchor) == 1
        text = text.replace(anchor, '''    cansSnapshot("cansPressureBeforeRelax", p);
        cansSnapshot("cansPhiHbyA", phiHbyA);
        cansSnapshot("cansPhiCorrected", phi);
    '''.replace('+', '') + anchor + '''
        cansSnapshot("cansPressureAfterRelax", p);
        cansSnapshot("cansHbyA", HbyA);
        cansSnapshot("cansRAU", rAU);
        cansSnapshot("cansRAtU", rAtU());
        if (cansWrite)
        {
            const volVectorField cansGradient(fvc::grad(p));
            const volVectorField cansCorrection(rAtU()*cansGradient);
            cansSnapshot("cansGradP", cansGradient);
            cansSnapshot("cansPressureCorrection", cansCorrection);
            Info<< "CANS_PRESSURE_RECONSTRUCTION time=" << mesh.time().name()
                << " consistent=" << pimple.consistent() << endl;
        }
    '''.replace('+', ''))
        anchor = '    U = HbyA - rAtU*fvc::grad(p);'
        assert text.count(anchor) == 1
        text = text.replace(anchor, anchor + '\n    cansSnapshot("cansUBeforeConstraints", U);')
        anchor = '    fvConstraints().constrain(U);'
        assert text.count(anchor) == 1
        text = text.replace(anchor, anchor + '\n    cansSnapshot("cansUAfterConstraints", U);')
        src.write_text(text)
        make_files = modified / 'Make/files'
        make_files.write_text(make_files.read_text().replace('$(FOAM_LIBBIN)', '/recon/diag/lib'))
        build = ['docker', 'run', '--rm', '--network', 'none', '--entrypoint', '/bin/bash',
                 '-v', f'{root}:/recon', image, '-lc',
                 'source /opt/openfoam13/etc/bashrc && cd /recon/module-diagnostic && wmake libso > /recon/build.log 2>&1']
        rc = run(build, root / 'build-container.log')
        if rc:
            raise RuntimeError('Diagnostic library build failed; preserved under ' + str(root))
        assert lib.is_file()
    else:
        assert sha(lib) == '93dff1fc99558a6f9073d819ea91af72783cf3e38e1e172f3817e06f0c2a76a8'
        src = modified / 'correctPressure.C'
    archive = Path('evidence') / study
    archive.mkdir(parents=True, exist_ok=True)
    rows = []
    for case_name in spec['cases']:
        base = Path('work') / spec['baseline'] / case_name
        case = root / case_name
        if case.exists():
            raise RuntimeError(f'{case} already exists; preserve it and use a fresh protocol version to retry')
        shutil.copytree(base, case, ignore=shutil.ignore_patterns('polyMesh', 'dynamicCode', 'log.*', 'diagnostics.json'))
        run_as_user = ("source /opt/openfoam13/etc/bashrc && export LD_LIBRARY_PATH=/diag/lib:$LD_LIBRARY_PATH && "
                       "cd /case && blockMesh > log.blockMesh 2>&1 && foamRun > log.foamRun 2>&1 && "
                       "foamPostProcess -func writeCellCentres -latestTime > log.centres 2>&1")
        command = ['docker', 'run', '--network', 'none', '--entrypoint', '/bin/bash', '--cidfile',
                   str(case / 'container-id'), '-v', f'{case}:/case', '-v', f'{root}/diag:/diag:ro', image, '-c',
                   'useradd -o -u "$1" -m runner && su runner -s /bin/bash -c \' ' + run_as_user + '\'', '--', str(os.getuid())]
        (case / 'command-used.json').write_text(json.dumps(command, indent=2) + '\n')
        rc = run(command, case / 'log.container')
        cid = (case / 'container-id').read_text().strip()
        state = json.loads(subprocess.check_output(['docker', 'inspect', cid], text=True, timeout=60))[0]['State']
        (case / 'exit.json').write_text(json.dumps({'runner_exit': rc, 'docker_exit': state['ExitCode'], 'state': state}, indent=2) + '\n')
        log = (case / 'log.foamRun').read_text() if (case / 'log.foamRun').exists() else ''
        assert rc == 0 and state['Status'] == 'exited' and state['ExitCode'] == 0 and log.rstrip().endswith('End'), 'Preserve incomplete case and stop.'
        comparison = {}
        for name in ('U', 'p', 'phi'):
            baseline = base / '0.05' / name; observed = case / '0.05' / name
            comparison[name] = {'byte_identical': baseline.read_bytes() == observed.read_bytes(),
                                'baseline_sha256': sha(baseline), 'diagnostic_sha256': sha(observed)}
        row = {'case': case_name, 'runner_exit': rc, 'docker_exit': state['ExitCode'],
               'steps': log.count('PIMPLE: Converged in'),
               'endpoint_instrumentation_calls': log.count('CANS_PRESSURE_RECONSTRUCTION time='),
               'endpoint_fields': comparison, 'noninterference_pass': all(v['byte_identical'] for v in comparison.values())}
        rows.append(row)
        with tarfile.open(archive / f'{case_name}.tar.gz', 'w:gz') as tar:
            for item in sorted(case.rglob('*')):
                if item.is_file() and not any(x in ('polyMesh', 'dynamicCode') for x in item.relative_to(case).parts):
                    tar.add(item, arcname=str(item.relative_to(case)))
        print(json.dumps(row), flush=True)
        assert row['noninterference_pass'], 'Instrumentation changed endpoint fields; stop.'
        (archive / 'runs.json').write_text(json.dumps({'cases': rows, 'quality': 'UNCERTAIN'}, indent=2) + '\n')
    result = {'image_id': image, 'original_source_sha256': orig_hash,
              'diagnostic_source_sha256': sha(src), 'diagnostic_library_sha256': sha(lib),
              'cases': rows, 'quality': 'UNCERTAIN', 'scope': spec['scope']}
    (archive / 'build-review.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
