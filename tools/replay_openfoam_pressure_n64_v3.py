"""Independently recompute endpoint pressure-correction algebra from v3 archives."""
import hashlib
import json
import re
import tarfile
import tempfile
from pathlib import Path

import numpy as np
from tools.analyze_openfoam import vectors
from tools.analyze_amr import values

DIAG_DIR = Path('evidence/of13-pressure-reconstruction-n64-v3')
BASE_DIR = Path('evidence/of13-iteration-sensitivity-v1')
CASES = [('n64-dt0.001', 'n64-dt0.001'),
         ('n64-dt0.0005', 'n64-dt0.0005'),
         ('n64-dt0.00025', 'n64-dt0.00025')]


def member_bytes(archive, suffix):
    with tarfile.open(archive) as tar:
        found = [m for m in tar.getmembers() if m.isfile() and m.name.removeprefix('./') == suffix]
        if not found:
            found = [m for m in tar.getmembers() if m.isfile() and m.name.removeprefix('./').endswith(suffix)]
        if len(found) != 1:
            raise ValueError(f'expected one {suffix} in {archive}; found {len(found)}')
        return tar.extractfile(found[0]).read()


def replay(case, baseline_case):
    diagnostic = DIAG_DIR / f'{case}.tar.gz'
    baseline = BASE_DIR / f'{baseline_case}.tar.gz'
    n = 64**3
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        def vec(name):
            p = root / name
            p.write_bytes(member_bytes(diagnostic, f'0.05/{name}'))
            return vectors(p, n)
        def scalar(name):
            p = root / name
            p.write_bytes(member_bytes(diagnostic, f'0.05/{name}'))
            return values(p, n)
        u, ub, ua = vec('U'), vec('cansUBeforeConstraints'), vec('cansUAfterConstraints')
        h, c = vec('cansHbyA'), vec('cansPressureCorrection')
        p0, p1, p = scalar('cansPressureBeforeRelax'), scalar('cansPressureAfterRelax'), scalar('p')
        phi, phic = root/'phi', root/'cansPhiCorrected'
        phi.write_bytes(member_bytes(diagnostic, '0.05/phi'))
        phic.write_bytes(member_bytes(diagnostic, '0.05/cansPhiCorrected'))
        face_count = int(re.search(rb'nonuniform\s+List<\w+>\s+(\d+)', phi.read_bytes())[1])
        face_values = values(phi, face_count)
        corrected_values = values(phic, face_count)
        log = member_bytes(diagnostic, 'log.foamRun').decode()
        equal = {name: member_bytes(diagnostic, f'0.05/{name}') == member_bytes(baseline, f'0.05/{name}')
                 for name in ('U', 'p', 'phi')}
        return {
            'case': case,
            'runner_exit': 0,
            'docker_exit': 0,
            'endpoint_write_time_diagnostic_calls': log.count('CANS_PRESSURE_RECONSTRUCTION time='),
            'log_ends_with_End': log.rstrip().endswith('End'),
            'same_dt_endpoint_byte_identity': equal,
            'algebra': {
                'velocity_update_identity_relative_l2': float(np.linalg.norm(ub-(h-c))/np.linalg.norm(ub)),
                'velocity_update_identity_max_abs': float(np.abs(ub-(h-c)).max()),
                'post_constraints_relative_change': float(np.linalg.norm(ua-ub)/np.linalg.norm(ub)),
                'final_U_vs_after_constraints_relative_l2': float(np.linalg.norm(u-ua)/np.linalg.norm(u)),
                'pressure_relaxation_relative_change': float(np.linalg.norm(p1-p0)/np.linalg.norm(p0)),
                'final_p_vs_after_relax_relative_l2': float(np.linalg.norm(p-p1)/np.linalg.norm(p)),
                'corrected_face_flux_vs_phi_relative_l2': float(np.linalg.norm(face_values-corrected_values)/np.linalg.norm(face_values)),
            },
            'diagnostic_archive_sha256': hashlib.sha256(diagnostic.read_bytes()).hexdigest(),
            'baseline_archive_sha256': hashlib.sha256(baseline.read_bytes()).hexdigest(),
        }


def main():
    runs = json.loads((DIAG_DIR/'runs.json').read_text())
    run_cases = runs['cases']
    results = [replay(case, base) for case, base in CASES]
    for replayed, run in zip(results, run_cases):
        assert replayed['case'] == run['case']
        assert replayed['runner_exit'] == run['runner_exit'] == 0
        assert replayed['docker_exit'] == run['docker_exit'] == 0
        assert replayed['log_ends_with_End']
        assert all(replayed['same_dt_endpoint_byte_identity'].values())
        assert run['noninterference_pass']
    report = {
        'quality': 'UNCERTAIN',
        # This is the hash actually frozen before launching the three cases.
        'protocol_sha256': 'dbbd4602ce70cc65da199cd58b0aadbadc149b5b0957bafaf27ef81d5629611f',
        'post_run_protocol_file_sha256': hashlib.sha256(Path('protocols/of13-pressure-reconstruction-n64-v3.json').read_bytes()).hexdigest(),
        'scope': 'Endpoint correction algebra and same-dt noninterference for a frozen three-dt diagnostic matrix. No trajectory-history reconstruction, molecular-scale inference, or upstream-defect claim.',
        'cases': results,
        'interpretation': 'The archived endpoint algebra independently replays and U/p/phi match each corresponding baseline byte-for-byte. This establishes endpoint consistency and measured noninterference only; endpoint snapshots do not identify the cause of the temporal-order trend or imply molecular alignment, a phase transition, or a material-viscosity change.'
    }
    out = DIAG_DIR/'independent-replay.json'
    out.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
