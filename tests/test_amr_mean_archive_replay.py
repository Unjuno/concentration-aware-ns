"""Synthetic archive integrity controls; these fixtures are not solver evidence."""
import hashlib
import io
import json
from pathlib import Path
import tarfile
import tempfile
import unittest
from unittest.mock import patch

from tools.replay_amr_mean_archive import replay
from tools.run_amr_mean_quality import generate_case, PAYLOAD_AUDIT, PROTOCOL


class AmrMeanArchiveReplayTests(unittest.TestCase):
    def fixture(self, root, mutation=None):
        spec = json.loads(PROTOCOL.read_text()); case = spec['cases'][0]
        input_dir = root/'inputs'
        inputs = generate_case(input_dir, case, spec)
        digest = lambda b: hashlib.sha256(b).hexdigest()
        members = {}
        runs = []
        for label in ('main', 'disabled-control'):
            for name in inputs:
                members[label+'/'+name] = (input_dir/name).read_bytes()
            members[label+'/log.foamRun'] = b'Time = 0.05\nEnd\n'
            members[label+'/log.loader.1'] = b'1: calling init: /instrumented/libincompressibleFluid.so\n'
            members[label+'/0.05/U'] = b'internalField nonuniform List<vector> 2 ((1 0 0)(0 1 0));'
            members[label+'/0.05/p'] = b'internalField nonuniform List<scalar> 2 (0 0.5);'
            runs.append({'label': label, 'inputs_sha256': inputs,
                         'log_sha256': digest(members[label+'/log.foamRun']),
                         'final_field_sha256': {f: digest(members[label+'/0.05/'+f]) for f in ('U', 'p')}})
        members['main/postProcessing/amrStages/0.05/postSolve_cells.csv'] = b'Ux,Uy,Uz,p\n1,0,0,0\n0,1,0,0.5\n'
        members['module/incompressibleFluid.C'] = b'// synthetic source fixture, never compiled\n'
        if mutation in ('ulp', 'large-value'):
            for run in runs:
                key = run['label']+'/0/U'; data = members[key]
                start = data.index(b'\n(\n(')+4; end = data.index(b' ', start)
                number = float(data[start:end])
                import numpy as np
                changed = np.nextafter(number, float('inf')) if mutation == 'ulp' else number+.001
                members[key] = data[:start]+format(changed, '.17g').encode()+data[end:]
                run['inputs_sha256'] = dict(inputs)
                run['inputs_sha256']['0/U'] = digest(members[key])
        if mutation == 'input': members['main/system/controlDict'] += b'\nendTime 0.1;\n'
        if mutation == 'loader': members['main/log.loader.1'] = b'trying file=/instrumented/libincompressibleFluid.so\n'
        if mutation == 'snapshot': members['main/postProcessing/amrStages/0.05/postSolve_cells.csv'] = b'Ux,Uy,Uz,p\n1,0,0,0\n0,1,0,0.4\n'
        payload = json.loads(PAYLOAD_AUDIT.read_text())
        (root/'package-stock-libraries.log').write_text(''.join(h+'  '+p+'\n' for p,h in payload['stock_library_sha256'].items()))
        manifest = {'case_id': case['id'], 'runs': runs, 'source_commit': 'synthetic-fixture',
                    'protocol_sha256': digest(PROTOCOL.read_bytes()),
                    'stock_library_payloads_verified': len(payload['stock_library_sha256']),
                    'instrumentation': {'original_module_file_sha256': spec['target']['module_source_sha256'],
                        'instrumented_module_file_sha256': {'incompressibleFluid.C': digest(members['module/incompressibleFluid.C'])}},
                    'archive': {'path': 'raw.tar.gz', 'sha256': None,
                                'members_sha256': {p: digest(b) for p,b in members.items()}}}
        with tarfile.open(root/'raw.tar.gz', 'w:gz') as tf:
            for name, data in members.items():
                entry = tarfile.TarInfo(name); entry.size = len(data)
                tf.addfile(entry, io.BytesIO(data))
        manifest['archive']['sha256'] = digest((root/'raw.tar.gz').read_bytes())
        (root/'manifest.json').write_text(json.dumps(manifest))

    def test_independent_input_positive_load_and_final_snapshot_integrity(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); self.fixture(root)
            with patch('tools.replay_amr_mean_archive.analyze', return_value={'fixture_only': True}):
                result = replay(root)
            self.assertEqual(result['status'], 'PASS_ARCHIVE_INPUT_FIELD_AND_ANALYSIS_REPLAY')
            self.assertEqual(result['final_snapshot_field_checks']['p']['maximum_absolute_difference'], 0)

    def test_optional_machine_scale_compatibility_never_promotes_strict_identity(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); self.fixture(root, 'ulp')
            with patch('tools.replay_amr_mean_archive.analyze', return_value={'fixture_only': True}):
                with self.assertRaisesRegex(ValueError, 'regenerated input hashes'):
                    replay(root)
                result = replay(root, allow_input_ulp_drift=True)
            self.assertEqual(result['independent_input_byte_identity'], 'FAIL')
            self.assertIn('STRICT_BYTE_IDENTITY_FAIL', result['status'])
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); self.fixture(root, 'large-value')
            with patch('tools.replay_amr_mean_archive.analyze', return_value={'fixture_only': True}):
                with self.assertRaisesRegex(ValueError, 'machine-scale compatibility'):
                    replay(root, allow_input_ulp_drift=True)

    def test_rehashed_mutations_cannot_pass_supplemental_checks(self):
        for mutation, message in (('input', 'preserved run manifest'), ('loader', 'positive loader'),
                                  ('snapshot', 'captured values')):
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as temp:
                root = Path(temp); self.fixture(root, mutation)
                with patch('tools.replay_amr_mean_archive.analyze', return_value={'fixture_only': True}):
                    with self.assertRaisesRegex(ValueError, message): replay(root)


if __name__ == '__main__':
    unittest.main()
