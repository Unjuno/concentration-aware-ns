"""Reconstruct the recorded final pressure/velocity correction from its archive."""
import hashlib
import json
import tarfile
import tempfile
from pathlib import Path
import numpy as np
from tools.analyze_amr import values
from tools.analyze_openfoam import vectors


def main():
    archive = Path('evidence/of13-pressure-reconstruction-pilot-v6/n16-dt0.001.tar.gz')
    review = json.loads(Path('evidence/of13-pressure-reconstruction-pilot-v6/pilot-review.json').read_text())
    assert hashlib.sha256(archive.read_bytes()).hexdigest() == review['archive_sha256']
    n = 16**3
    with tarfile.open(archive) as tar, tempfile.TemporaryDirectory() as tmp:
        def vec(name):
            p = Path(tmp)/name
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(tar.extractfile(name).read())
            return vectors(p, n)

        def scalar(name):
            p = Path(tmp)/name
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(tar.extractfile(name).read())
            import re
            text = p.read_text()
            match = re.search(r'internalField\s+nonuniform\s+List<scalar>\s+(\d+)', text)
            assert match
            return values(p, int(match.group(1)))

        u = vec('0.05/cansUBeforeConstraints')
        h = vec('0.05/cansHbyA')
        correction = vec('0.05/cansPressureCorrection')
        after_constraints = vec('0.05/cansUAfterConstraints')
        output_u = vec('0.05/U')
        p_before = scalar('0.05/cansPressureBeforeRelax')
        p_after = scalar('0.05/cansPressureAfterRelax')
        output_p = scalar('0.05/p')
        phi_corrected = scalar('0.05/cansPhiCorrected')
        output_phi = scalar('0.05/phi')
        identity = u - (h-correction)
        norm_u = np.linalg.norm(u)
        result = {
            'archive_sha256': hashlib.sha256(archive.read_bytes()).hexdigest(),
            'velocity_update_identity_relative_l2': float(np.linalg.norm(identity)/norm_u),
            'velocity_update_identity_max_abs': float(np.max(np.abs(identity))),
            'velocity_scale_max_abs': float(np.max(np.abs(u))),
            'post_constraint_velocity_relative_change': float(np.linalg.norm(after_constraints-u)/norm_u),
            'endpoint_U_vs_recorded_after_constraints_relative_l2': float(np.linalg.norm(output_u-after_constraints)/norm_u),
            'pressure_relaxation_relative_change': float(np.linalg.norm(p_after-p_before)/np.linalg.norm(p_before)),
            'endpoint_p_vs_recorded_after_relax_relative_l2': float(np.linalg.norm(output_p-p_after)/np.linalg.norm(output_p)),
            'corrected_face_flux_vs_endpoint_phi_relative_l2': float(np.linalg.norm(output_phi-phi_corrected)/np.linalg.norm(output_phi)),
            'scope': 'Final write-time correction call in n=16 pilot only. Does not reconstruct earlier trajectory or attribute n=64 temporal order.'
        }
    Path('evidence/of13-pressure-reconstruction-pilot-v6/algebra-review.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
