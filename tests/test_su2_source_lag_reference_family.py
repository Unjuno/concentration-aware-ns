"""Ensure resolution metadata cannot select a different manufactured field."""
import hashlib
import io
import json
import tarfile
from tools.audit_su2_localized_source_lag import audit


def make_case(base, n=64, sigma=.5):
    base.mkdir()
    path = base/'n64-dt0.001.tar.gz'
    data = json.dumps({'n': n, 'sigma': sigma, 'nu': .01, 'dt': .001, 'end': .05}).encode()
    with tarfile.open(path, 'w:gz') as archive:
        member = tarfile.TarInfo('parameters.json')
        member.size = len(data)
        archive.addfile(member, io.BytesIO(data))
    (base/'summary.json').write_text(json.dumps({'cases': [
        {'case': 'n64-dt0.001', 'archive_sha256': hashlib.sha256(path.read_bytes()).hexdigest()}]}))
    return audit(base)['cases'][0]


def test_resolution_does_not_change_continuum_force(tmp_path):
    first = make_case(tmp_path/'first', n=32)
    second = make_case(tmp_path/'second', n=64)
    for key in ('max_force_difference', 'rms_force_difference', 'max_relative_force_difference'):
        assert first[key] == second[key]


def test_archive_sigma_selects_the_executed_family(tmp_path):
    narrow = make_case(tmp_path/'narrow', sigma=.5)
    wide = make_case(tmp_path/'wide', sigma=1.)
    assert narrow['rms_force_difference'] > wide['rms_force_difference']
    assert narrow['max_force_difference'] > wide['max_force_difference']
