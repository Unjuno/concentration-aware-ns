"""Recompute endpoint algebra from the preserved, exit-uncertain n64 diagnostic."""
import hashlib
import json
import re
import tarfile
import tempfile
from pathlib import Path

import numpy as np
from tools.analyze_openfoam import vectors
from tools.analyze_amr import values

DIAGNOSTIC = Path('evidence/of13-pressure-reconstruction-n64-v1/n64-dt0.001-unverified-exit.tar.gz')
BASELINE = Path('evidence/of13-iteration-sensitivity-v1/n64-dt0.001.tar.gz')


def member_bytes(archive, suffix):
    with tarfile.open(archive) as tar:
        found = [m for m in tar.getmembers() if m.isfile() and m.name.removeprefix('./') == suffix]
        if not found:
            found = [m for m in tar.getmembers() if m.isfile() and m.name.removeprefix('./').endswith(suffix)]
        if len(found) != 1:
            raise ValueError(f'expected one {suffix} in {archive}; found {len(found)}')
        return tar.extractfile(found[0]).read()


def main():
    n = 64**3
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        def vec(name):
            p = root / name
            p.write_bytes(member_bytes(DIAGNOSTIC, f'0.05/{name}'))
            return vectors(p, n)
        def scalar(name):
            p = root / name
            p.write_bytes(member_bytes(DIAGNOSTIC, f'0.05/{name}'))
            return values(p, n)
        u, ub, ua = vec('U'), vec('cansUBeforeConstraints'), vec('cansUAfterConstraints')
        h, c = vec('cansHbyA'), vec('cansPressureCorrection')
        p0, p1, p = scalar('cansPressureBeforeRelax'), scalar('cansPressureAfterRelax'), scalar('p')
        phi, phic = root/'phi', root/'cansPhiCorrected'
        phi.write_bytes(member_bytes(DIAGNOSTIC, '0.05/phi'))
        phic.write_bytes(member_bytes(DIAGNOSTIC, '0.05/cansPhiCorrected'))
        face_count = int(re.search(rb'nonuniform\s+List<\w+>\s+(\d+)', phi.read_bytes())[1])
        face_values = values(phi, face_count); corrected_values = values(phic, face_count)
        baseline_equal = {}
        for name in ('U', 'p', 'phi'):
            baseline_equal[name] = member_bytes(DIAGNOSTIC, f'0.05/{name}') == member_bytes(BASELINE, f'0.05/{name}')
        log = member_bytes(DIAGNOSTIC, 'log.foamRun').decode()
        result = {
            'quality': 'UNCERTAIN',
            'case': 'n64-dt0.001; runner/container exit unavailable',
            'observed': {'foamRun_log_ends_with_End': log.rstrip().endswith('End'),
                         'converged_steps': log.count('PIMPLE: Converged in'),
                         'write_time_diagnostic_calls': log.count('CANS_PRESSURE_RECONSTRUCTION time=')},
            'algebra': {
                'velocity_update_identity_relative_l2': float(np.linalg.norm(ub-(h-c))/np.linalg.norm(ub)),
                'velocity_update_identity_max_abs': float(np.abs(ub-(h-c)).max()),
                'post_constraints_relative_change': float(np.linalg.norm(ua-ub)/np.linalg.norm(ub)),
                'final_U_vs_after_constraints_relative_l2': float(np.linalg.norm(u-ua)/np.linalg.norm(u)),
                'pressure_relaxation_relative_change': float(np.linalg.norm(p1-p0)/np.linalg.norm(p0)),
                'final_p_vs_after_relax_relative_l2': float(np.linalg.norm(p-p1)/np.linalg.norm(p)),
                'corrected_face_flux_vs_phi_relative_l2': float(np.linalg.norm(face_values-corrected_values)/np.linalg.norm(face_values))},
            'same_dt_noninterference': {f'{k}_byte_identical_to_baseline': v for k, v in baseline_equal.items()},
            'diagnostic_archive_sha256': hashlib.sha256(DIAGNOSTIC.read_bytes()).hexdigest(),
            'baseline_archive_sha256': hashlib.sha256(BASELINE.read_bytes()).hexdigest(),
            'interpretation': 'Endpoint algebra and same-dt noninterference only; unknown process exit, no earlier correction history, and incomplete dt triple.'}
    out = Path('evidence/of13-pressure-reconstruction-n64-v1/dt0.001-forensic-review.json')
    out.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
