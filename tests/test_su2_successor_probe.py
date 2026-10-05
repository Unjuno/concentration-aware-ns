import pytest
from tools.run_su2_full_horizon_cfl_pair import verify_successor_probe


def valid():
    return {'binary_sha256':'a'*64,'patched_source_sha256':'b'*64,
            'package_versions_sha256':'c'*64,'compiler_version':'example compiler identity\n'}


def test_all_actual_probe_fields_must_match():
    verify_successor_probe(valid(),valid())


@pytest.mark.parametrize('kind',['empty','missing','extra','binary','compiler','invalid_digest'])
def test_incomplete_or_changed_actual_probe_is_rejected(kind):
    receipt=valid();measured=valid()
    if kind=='empty':measured={}
    elif kind=='missing':measured.pop('patched_source_sha256')
    elif kind=='extra':measured['irrelevant']='value'
    elif kind=='binary':measured['binary_sha256']='d'*64
    elif kind=='compiler':measured['compiler_version']='different compiler'
    else:receipt['binary_sha256']=measured['binary_sha256']='z'*64
    with pytest.raises(ValueError):verify_successor_probe(receipt,measured)
