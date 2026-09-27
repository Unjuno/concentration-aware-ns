"""Build isolated pressure diagnostics and compare one n=16 endpoint to baseline."""
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
    study = 'of13-pressure-reconstruction-pilot-v6'
    root = (Path('work') / study).resolve()
    root.mkdir(exist_ok=False)
    image = json.loads(Path('protocols/of13-pressure-reconstruction-v1.json').read_text())['image_id']
    subprocess.run(['docker', 'image', 'inspect', image], check=True, stdout=subprocess.DEVNULL, timeout=10)
    container = subprocess.check_output(['docker', 'create', image], text=True).strip()
    module = root / 'module-original'
    try:
        subprocess.run(['docker', 'cp', container + ':/opt/openfoam13/applications/modules/incompressibleFluid', str(module)], check=True)
    finally:
        subprocess.run(['docker', 'rm', container], check=True, stdout=subprocess.DEVNULL, timeout=10)
    orig_hash = sha(module / 'correctPressure.C')
    assert orig_hash == '1e6b6d38e1f2730368b5de45a4fc76017b06284748349149da41c90c6d84efb2'
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
    lib = root / 'diag/lib/libincompressibleFluid.so'
    assert lib.is_file()
    base = Path('work/of13-study-v1/n16-dt0.001')
    case = root / 'case'
    shutil.copytree(base, case, ignore=shutil.ignore_patterns('polyMesh', 'dynamicCode', 'log.*', 'diagnostics.json'))
    run_as_user = ("source /opt/openfoam13/etc/bashrc && "
                   "export LD_LIBRARY_PATH=/diag/lib:$LD_LIBRARY_PATH && cd /case && "
                   "blockMesh > log.blockMesh 2>&1 && foamRun > log.foamRun 2>&1 && "
                   "foamPostProcess -func writeCellCentres -latestTime > log.centres 2>&1")
    command = ['docker', 'run', '--rm', '--network', 'none', '--entrypoint', '/bin/bash', '-v',
               f'{case}:/case', '-v', f'{root}/diag:/diag:ro', image, '-c',
               f'useradd -o -u "$1" -m runner && su runner -s /bin/bash -c \'{run_as_user}\'',
               '--', str(os.getuid())]
    rc = run(command, case / 'log.container')
    (case / 'exit.json').write_text(json.dumps({'exit_code': rc}) + '\n')
    log = (case / 'log.foamRun').read_text() if (case / 'log.foamRun').exists() else ''
    assert rc == 0 and log.rstrip().endswith('End'), 'Pilot failed; preserve all output and inspect.'
    assert log.count('CANS_PRESSURE_RECONSTRUCTION time=') > 0
    endpoint = Path('0.05')
    comparison = {}
    for name in ('U', 'p', 'phi'):
        baseline = base / '0.05' / name
        observed = case / endpoint / name
        comparison[name] = {'byte_identical': baseline.read_bytes() == observed.read_bytes(),
                            'baseline_sha256': sha(baseline), 'diagnostic_sha256': sha(observed)}
    files = sorted(p for p in case.rglob('*') if p.is_file() and not any(x in ('polyMesh', 'dynamicCode') for x in p.relative_to(case).parts))
    archive = Path('evidence') / study
    archive.mkdir(parents=True, exist_ok=False)
    with tarfile.open(archive / 'n16-dt0.001.tar.gz', 'w:gz') as tar:
        for p in files:
            tar.add(p, arcname=str(p.relative_to(case)))
    result = {'image_id': image, 'original_source_sha256': orig_hash,
              'diagnostic_source_sha256': sha(src), 'diagnostic_library_sha256': sha(lib),
              'diagnostic_library_loaded_from': '/diag/lib/libincompressibleFluid.so',
              'exit_code': rc, 'steps': log.count('PIMPLE: Converged in'),
              'instrumentation_calls': log.count('CANS_PRESSURE_RECONSTRUCTION time='),
              'endpoint_fields': comparison,
              'noninterference_pass': all(v['byte_identical'] for v in comparison.values()),
              'scope': 'n=16 endpoint pilot only; build and source telemetry do not establish temporal-error causality.'}
    result['archive_sha256'] = sha(archive / 'n16-dt0.001.tar.gz')
    (archive / 'pilot-review.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
    if not result['noninterference_pass']:
        raise SystemExit('Instrumentation changed endpoint fields; stop before scaling up.')


if __name__ == '__main__':
    main()
