"""Hostile integrity tests use fabricated evidence; no package or binary runs."""
import contextlib
import io
import json
from pathlib import Path
import sys
import tarfile
import tempfile
import unittest
from unittest.mock import patch

from test_interface_operator_analysis import cartesian_snapshots
from tools.build_interface_operator_cases import build_cases
from tools import replay_interface_operator_archive as replay


class OperatorArchiveIntegrity(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory(); self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name); self.raw = self.root/'raw'; self.raw.mkdir()
        self.evidence = self.root/'evidence'; self.evidence.mkdir()
        self.head = 'a'*40
        utility_names = ['interfaceOperatorProbe.C','run_cases.sh','package-source-paths.txt','Make/files','Make/options']
        names = [replay.ANALYZER,replay.GENERATOR,replay.DEPENDENCY,'tools/run_interface_operator_probe.py',
                 'protocols/of13-interface-operator-v1.json',replay.AUDIT]
        protocol_current = json.loads((replay.REPOSITORY/'protocols/of13-interface-operator-v1.json').read_text())
        recipe = protocol_current['target']['runtime_recipe']; names.append(recipe)
        if recipe.startswith('runtime/of13-interface-operator/'):
            utility_names.append(recipe.removeprefix('runtime/of13-interface-operator/'))
        names += ['runtime/of13-interface-operator/'+name for name in utility_names]
        self.blobs = {name:(replay.REPOSITORY/name).read_bytes() for name in names}
        protocol_name = 'protocols/of13-interface-operator-v1.json'
        protocol = json.loads(self.blobs[protocol_name]); sources = {name:replay.digest(data)
            for name,data in self.blobs.items() if name != replay.AUDIT and name != replay.DEPENDENCY}
        for name in utility_names:
            path = self.raw/'app'/name; path.parent.mkdir(parents=True,exist_ok=True)
            path.write_bytes(self.blobs['runtime/of13-interface-operator/'+name])
        (self.raw/'protocol-frozen.json').write_bytes(self.blobs[protocol_name])
        metadata = build_cases(self.raw/'cases'); case_records = {}
        for row in metadata:
            case_name = f"nx{row['inputs']['nx']}"; case = self.raw/'cases'/case_name
            case_records[case_name] = {'inputs_sha256':row['inputs_sha256'], 'files_sha256':row['files_sha256'],
                'metadata_sha256':replay.digest((case/'case_metadata.json').read_bytes())}
            for mode in ('arithmetic','harmonic','constant'):
                before,after,_,_ = cartesian_snapshots(row,mode)
                directory = case/'probe'/mode; directory.mkdir(parents=True)
                for stage,snapshot in (('before',before),('after',after)):
                    if snapshot is not None: (directory/f'{stage}.json').write_text(json.dumps(snapshot))
            (case/'log.interfaceOperatorProbe').write_text('INTERFACE_OPERATOR_PROBE_COMPLETE\n')
        audit = json.loads(self.blobs[replay.AUDIT]); libraries = audit['linked_library_payloads']
        (self.raw/'package-source-sha256.log').write_text(''.join(
            row['package_source_sha256']+'  /opt/openfoam13/'+row['path']+'\n' for row in audit['files']))
        (self.raw/'linked-library-sha256.log').write_text(''.join(
            row['sha256']+'  /'+row['path'].removeprefix('./')+'\n' for row in libraries))
        (self.raw/'linked-libraries.log').write_text(''.join('/'+row['path'].removeprefix('./')+'\n' for row in libraries))
        binary = b'Synthetic unexecuted binary fixture'; binary_hash = replay.digest(binary)
        (self.raw/'interfaceOperatorProbe').write_bytes(binary)
        (self.raw/'binary-sha256.txt').write_text(binary_hash+'  /probe/interfaceOperatorProbe\n')
        for name in ('runtime-environment.log','package-inventory.log','build.log'):
            (self.raw/name).write_text('Synthetic provenance fixture; no execution.\n')
        image = {'Id':'sha256:'+'b'*64,'Os':'linux','Architecture':'arm64'}
        state = {'Status':'exited','Running':False,'ExitCode':0}; cid = 'c'*64
        (self.raw/'COMPLETED').write_text('RUN_CASES_COMPLETE\n'); (self.raw/'container-id').write_text(cid)
        command = ['docker','run','--pull=never','--network','none','--cpus','2','--memory','2g',
                   '--pids-limit','512','--platform','linux/arm64','--entrypoint','/bin/bash',image['Id'],'/probe/app/run_cases.sh']
        (self.raw/'container-command.json').write_text(json.dumps(command))
        logs = self.raw/'command-logs'; logs.mkdir()
        (logs/'image.json').write_text(json.dumps([image]))
        (logs/'container.json').write_text(json.dumps([{'Id':cid,'Image':image['Id'],'State':state}]))
        self.manifest = {'schema':'of13-interface-operator-run/v1','git_head':self.head,'status':'RUN_COMPLETE_OPERATOR_ONLY','disposition':'COMPLETE',
            'tracked_status':'','docker_run_exit_code':0,'container_state':state,'image_inspect':image,
            'resolved_image_id':image['Id'],'container_image_id':image['Id'],'container_id':cid,
            'source_files_sha256':sources,'protocol':{'path':protocol_name,'sha256':replay.digest(self.blobs[protocol_name]),'content':protocol},
            'utility_binary_sha256':binary_hash,'case_input_hashes':case_records,
            'commands':[{'label':'container-run','return_code':0,'argv':command},
                {'label':'container-inspect','stdout_file':'command-logs/container.json'},
                {'label':'image-inspect','stdout_file':'command-logs/image.json'}],
            'runtime_logs_sha256':{name:replay.digest((self.raw/name).read_bytes()) for name in (
                'runtime-environment.log','package-inventory.log','linked-libraries.log','binary-sha256.txt',
                'build.log','package-source-sha256.log','linked-library-sha256.log')}}
        self.repack()

    def repack(self, hostile=None, symlink=False):
        files = sorted(path for path in self.raw.rglob('*') if path.is_file())
        hashes = {path.relative_to(self.raw).as_posix():replay.digest(path.read_bytes()) for path in files}
        archive = self.evidence/'raw.tar.gz'
        with tarfile.open(archive,'w:gz') as stream:
            for path in files: stream.add(path,arcname=path.relative_to(self.raw).as_posix(),recursive=False)
            if hostile is not None:
                info = tarfile.TarInfo(hostile); info.size = 1
                if symlink:
                    info.type = tarfile.SYMTYPE; info.linkname = '../outside'; info.size = 0
                    stream.addfile(info)
                else:
                    stream.addfile(info,io.BytesIO(b'x'))
                hashes[hostile] = replay.digest(b'x')
        self.manifest['work_files_sha256'] = hashes
        self.manifest['archive'] = {'sha256':replay.digest(archive.read_bytes()),'regular_file_count':len(hashes)}
        self.save_manifest()

    def save_manifest(self):
        (self.evidence/'run-manifest.json').write_text(json.dumps(self.manifest))

    def checked_replay(self, commit=None):
        with patch.object(replay,'git_blob',side_effect=lambda head,name:self.blobs[name]):
            return replay.replay(self.evidence,commit)

    def test_complete_synthetic_archive_replays_all_fifteen_snapshots(self):
        recipe = self.manifest['protocol']['content']['target']['runtime_recipe']
        self.assertIn(recipe,self.manifest['source_files_sha256'])
        if recipe.startswith('runtime/of13-interface-operator/'):
            archived = 'app/'+recipe.removeprefix('runtime/of13-interface-operator/')
            with tarfile.open(self.evidence/'raw.tar.gz') as archive:
                self.assertEqual(archive.extractfile(archived).read(),self.blobs[recipe])
        result = self.checked_replay(self.head)
        self.assertEqual(result['integrity'],'VERIFIED_ARCHIVE_AND_FROZEN_INPUTS')
        self.assertEqual(result['operator_quality'],'PASS')
        self.assertEqual([row['nx'] for row in result['cases']],[16,32,64])
        self.assertEqual(result['native_diagnostic'],{'16':'OBSERVED','32':'OBSERVED','64':'OBSERVED'})
        self.assertEqual(len(result['package_provenance']['source_comparisons']),25)
        self.assertEqual(len(result['package_provenance']['linked_library_comparisons']),3)

    def test_archive_sha_and_work_file_hash_mismatches_are_rejected(self):
        self.manifest['archive']['sha256'] = '0'*64; self.save_manifest()
        with self.assertRaisesRegex(ValueError,'archive SHA256'): self.checked_replay()
        self.repack(); self.manifest['work_files_sha256']['cases/nx16/0/shear'] = '0'*64; self.save_manifest()
        with self.assertRaisesRegex(ValueError,'work file SHA256'): self.checked_replay()

    def test_traversal_member_never_leaves_temporary_extraction(self):
        self.repack('../escape')
        with self.assertRaisesRegex(ValueError,'unsafe'): self.checked_replay()
        self.assertFalse((self.root/'escape').exists())

    def test_nonregular_and_duplicate_members_are_rejected(self):
        self.repack('hostile-link',symlink=True)
        with self.assertRaisesRegex(ValueError,'nonregular'): self.checked_replay()
        self.repack('COMPLETED')
        with self.assertRaisesRegex(ValueError,'member map'): self.checked_replay()

    def test_missing_generated_input_is_rejected_even_with_self_consistent_tar(self):
        (self.raw/'cases/nx32/0/U').unlink(); self.repack()
        with self.assertRaises(FileNotFoundError): self.checked_replay()

    def test_wrong_frozen_source_and_explicit_commit_are_rejected(self):
        with self.assertRaisesRegex(ValueError,'source commit'): self.checked_replay('d'*40)
        self.manifest['source_files_sha256'][replay.GENERATOR] = '0'*64; self.save_manifest()
        with self.assertRaisesRegex(ValueError,'Git source blob'): self.checked_replay()

    def test_last_snapshot_is_validated_and_native_diagnostic_stays_separate(self):
        path = self.raw/'cases/nx64/probe/constant/before.json'
        snapshot = json.loads(path.read_text()); snapshot['cells']['nativeResidual'] = [0.]*256
        path.write_text(json.dumps(snapshot)); self.repack()
        result = self.checked_replay(); self.assertEqual(result['operator_quality'],'PASS')
        self.assertEqual(result['native_diagnostic']['64'],'NOT_OBSERVED')
        snapshot['fieldDimensions'] = [0]*7; path.write_text(json.dumps(snapshot)); self.repack()
        with self.assertRaisesRegex(ValueError,'fieldDimensions'): self.checked_replay()

    def test_source_checksum_tamper_and_existing_output_are_preserved(self):
        path = self.raw/'package-source-sha256.log'
        path.write_text('0'*64+path.read_text()[64:]); self.repack()
        self.manifest['runtime_logs_sha256'][path.name] = replay.digest(path.read_bytes()); self.save_manifest()
        with self.assertRaisesRegex(ValueError,'differs from named audit'): self.checked_replay()
        output = self.root/'keep.json'; output.write_text('preserve existing output')
        with patch.object(sys,'argv',['replay','--evidence-root',str(self.evidence),'--output',str(output)]), contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit): replay.main()
        self.assertEqual(output.read_text(),'preserve existing output')


if __name__ == '__main__':
    unittest.main()
