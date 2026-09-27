"""Archive-only late-time initialization sensitivity, without MMS acceptance."""
import hashlib
import json
import tarfile
import tempfile
from pathlib import Path
import numpy as np
from tools.analyze_openfoam import vectors
from tools.compare_openfoam_iteration_sensitivity import alignment, completed_times


def main():
    study = 'of13-solenoidal-late-control-v1'
    protocol = Path('protocols') / (study + '.json')
    spec = json.loads(protocol.read_text())
    manifest = json.loads((Path('evidence/tests') / (study + '-preparation.json')).read_text())
    assert hashlib.sha256(protocol.read_bytes()).hexdigest() == manifest['protocol_sha256']
    manifests = {r['case']: r['input_hashes'] for r in manifest['cases']}
    control, baseline, rows = [], [], []
    paths = [Path('evidence') / s / (f'n{spec["n"]}-dt{dt}.tar.gz')
             for dt in spec['dt'] for s in (study, spec['baseline'])]
    missing = [str(p) for p in paths if not p.is_file()]
    if missing:
        raise SystemExit('INCOMPLETE: no result written; missing: ' + ', '.join(missing))
    common_centers = None
    for dt in spec['dt']:
        name = f'n{spec["n"]}-dt{dt}'
        data = []
        hashes = {}
        initial_bytes = []
        for source in (study, spec['baseline']):
            archive = Path('evidence') / source / (name + '.tar.gz')
            hashes[source] = hashlib.sha256(archive.read_bytes()).hexdigest()
            with tarfile.open(archive) as tar, tempfile.TemporaryDirectory() as folder:
                def read(member):
                    return tar.extractfile(member).read()
                def field(member):
                    path = Path(folder) / member
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_bytes(read(member))
                    return vectors(path, spec['n'] ** 3)
                assert json.loads(read('exit.json'))['exit_code'] == 0
                log = read('log.foamRun').decode()
                times = completed_times(log)
                count = round(spec['end'] / dt)
                assert log.rstrip().endswith('End') and len(times) == count
                assert np.allclose(times, np.arange(1, count + 1) * dt, atol=1e-12, rtol=0)
                assert log.count('PIMPLE: Converged in') == count
                for member, digest in manifests[name].items():
                    if source == study or member != '0/U':
                        assert hashlib.sha256(read(member)).hexdigest() == digest
                initial_bytes.append(read('0/U'))
                prefix = format(spec['end'], '.12g')
                u = field(prefix + '/U')
                centers = field(prefix + '/C')
                assert np.isfinite(u).all() and np.isfinite(centers).all()
                if common_centers is not None:
                    assert np.array_equal(common_centers, centers)
                common_centers = centers
                data.append(u)
        assert initial_bytes[0] != initial_bytes[1]
        control.append(data[0]); baseline.append(data[1])
        rows.append({'case': name, 'archive_sha256': hashes,
                     'relative_endpoint_shift': float(np.linalg.norm(data[0]-data[1])/np.linalg.norm(data[1])),
                     'steps_each': round(spec['end']/dt)})
    result = {'cases': rows, 'control': alignment(control), 'baseline': alignment(baseline),
              'protocol_sha256': manifest['protocol_sha256'], 'quality': 'UNCERTAIN',
              'scope': spec['scope']}
    (Path('evidence') / study / 'comparison.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
