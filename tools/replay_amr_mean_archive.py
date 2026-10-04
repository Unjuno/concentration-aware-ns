"""Supplement the frozen AMR analysis with independent archived input/field checks."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import tarfile
import tempfile

import numpy as np

from tools.analyze_amr_mean_quality import analyze
from tools.analyze_amr_gauss_gradient import _read_csv, _vector
from tools.analyze_amr_stage_snapshots import _parse_field
from tools.run_amr_mean_quality import generate_case, PAYLOAD_AUDIT, PROTOCOL, sha


def replay(evidence, allow_input_ulp_drift=False):
    evidence = Path(evidence)
    result = analyze(evidence)
    manifest = json.loads((evidence/'manifest.json').read_text())
    spec = json.loads(PROTOCOL.read_text())
    case = next(c for c in spec['cases'] if c['id'] == manifest['case_id'])
    archive = evidence/manifest['archive']['path']
    def raw(name):
        with tarfile.open(archive, 'r:gz') as tf:
            return tf.extractfile(name).read()
    def digest(data):
        return hashlib.sha256(data).hexdigest()
    with tempfile.TemporaryDirectory(prefix='cans-amr-input-replay-') as temp:
        inputs = generate_case(Path(temp)/'case', case, spec)
    input_checks = {}
    all_inputs_byte_identical = True
    for run in manifest['runs']:
        label = run['label']
        if set(inputs) != set(run['inputs_sha256']):
            raise ValueError('archived and independently generated input file maps differ')
        input_differences = []
        for path, expected in inputs.items():
            archived = raw(label+'/'+path)
            if digest(archived) != run['inputs_sha256'][path]:
                raise ValueError('archived input differs from preserved run manifest')
            if digest(archived) != expected:
                if not allow_input_ulp_drift or path != '0/U':
                    raise ValueError('independently regenerated input hashes differ; preserve platform/input discrepancy')
                # This optional compatibility check NEVER promotes byte identity.
                with tempfile.TemporaryDirectory(prefix='cans-amr-input-numeric-') as temp:
                    regenerated_dir = Path(temp)/'case'
                    generate_case(regenerated_dir, case, spec)
                    regenerated = (regenerated_dir/path).read_bytes()
                pattern = r'(internalField\s+nonuniform\s+List<vector>\s+\d+\s*\()(.*?)(\)\s*;)'
                structure = lambda data: re.sub(pattern, r'\1<VALUES>\3', data.decode(), flags=re.S)
                if structure(archived) != structure(regenerated):
                    raise ValueError('initial vector field nonvalue structure differs')
                av, bv = _parse_field(archived, 'vector', 3), _parse_field(regenerated, 'vector', 3)
                if av.shape != bv.shape:
                    raise ValueError('initial vector field shape differs')
                maximum = float(np.max(np.abs(av-bv)))
                # Fixed machine-scale compatibility limit; no solver quality threshold changes.
                tolerance = 32*np.finfo(float).eps*max(float(np.max(np.abs(bv))), 1e-300)
                if maximum > tolerance:
                    raise ValueError('initial vector field numerical difference exceeds machine-scale compatibility limit')
                all_inputs_byte_identical = False
                input_differences.append({'path': path, 'archived_sha256': digest(archived),
                    'regenerated_sha256': expected, 'maximum_absolute_difference': maximum,
                    'machine_scale_tolerance': tolerance, 'byte_identity': 'FAIL',
                    'numerical_compatibility': 'PASS'})
        if digest(raw(label+'/log.foamRun')) != run['log_sha256']:
            raise ValueError('solver log differs from run manifest')
        for field, expected in run['final_field_sha256'].items():
            if digest(raw(label+'/0.05/'+field)) != expected:
                raise ValueError('archived final field differs from control/hash record')
        loader_names = [name for name in manifest['archive']['members_sha256']
                        if name.startswith(label+'/log.loader.')]
        loader = ''.join(raw(name).decode() for name in loader_names)
        if not re.search(r'calling init:\s*/instrumented/libincompressibleFluid\.so(?:\s|$)', loader):
            raise ValueError('missing positive loader initialization for instrumented module')
        input_checks[label] = {'independently_regenerated_input_files': len(inputs),
                              'initial_input_differences': input_differences,
                              'archived_log_final_fields_and_positive_module_load': 'PASS'}
    payload = json.loads(PAYLOAD_AUDIT.read_text())
    if sha(PAYLOAD_AUDIT) != spec['target']['stock_payload_audit_sha256']:
        raise ValueError('stock payload audit hash differs from protocol')
    stock = {}
    for line in (evidence/'package-stock-libraries.log').read_text().splitlines():
        match = re.fullmatch(r'([0-9a-f]{64})\s+(/opt/openfoam13/.+)', line)
        if not match or match[2] in stock:
            raise ValueError('malformed stock library payload log')
        stock[match[2]] = match[1]
    if stock != payload['stock_library_sha256'] or manifest['stock_library_payloads_verified'] != len(stock):
        raise ValueError('stock library payload verification differs from official deb audit')
    provenance = manifest['instrumentation']
    if provenance['original_module_file_sha256'] != spec['target']['module_source_sha256']:
        raise ValueError('instrumented module original source differs from frozen protocol')
    for name, expected in provenance['instrumented_module_file_sha256'].items():
        if digest(raw('module/'+name)) != expected:
            raise ValueError('archived instrumented source differs from compiled input record')
    snapshot = _read_csv(archive, 'main/postProcessing/amrStages/0.05/postSolve_cells.csv')
    checks = {}
    for field, kind, width, values in (
        ('U', 'vector', 3, _vector(snapshot, ('Ux', 'Uy', 'Uz'))),
        ('p', 'scalar', 1, snapshot['p'])):
        stored = _parse_field(raw('main/0.05/'+field), kind, width)
        if stored.shape != values.shape:
            raise ValueError('final field and postSolve snapshot have different shapes')
        difference = float(np.max(np.abs(stored-values)))
        scale = max(1.0, float(np.max(np.abs(values))))
        if difference > 5e-13*scale:
            raise ValueError('postSolve captured values differ from written final fields')
        checks[field] = {'maximum_absolute_difference': difference,
                         'comparison_tolerance': 5e-13*scale}
    return {'status': ('PASS_ARCHIVE_INPUT_FIELD_AND_ANALYSIS_REPLAY' if all_inputs_byte_identical
                      else 'PASS_NUMERICAL_INPUT_COMPATIBILITY_REPLAY_WITH_STRICT_BYTE_IDENTITY_FAIL'),
            'independent_input_byte_identity': 'PASS' if all_inputs_byte_identical else 'FAIL',
            'allow_input_ulp_drift': allow_input_ulp_drift,
            'case_id': case['id'], 'source_commit': manifest['source_commit'],
            'protocol_sha256': manifest['protocol_sha256'], 'archive_sha256': manifest['archive']['sha256'],
            'input_checks': input_checks, 'stock_library_payloads_verified': len(stock),
            'final_snapshot_field_checks': checks, 'analysis': result,
            'scope': 'Frozen mean analysis plus independently regenerated inputs, archived logs/final fields, positive module load and stock payload checks. No new CFD, compiled-module binary replay, whole-runtime source/compiler equivalence or continuous peak/spectrum claim.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--evidence-root', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--allow-input-ulp-drift', action='store_true',
                        help='Supplemental numeric compatibility only; strict byte identity remains FAIL')
    args = parser.parse_args()
    result = replay(args.evidence_root, allow_input_ulp_drift=args.allow_input_ulp_drift)
    args.output.write_text(json.dumps(result, indent=2, allow_nan=False)+'\n')
    print(json.dumps({k: result[k] for k in ('status', 'case_id', 'source_commit')}))


if __name__ == '__main__':
    main()
