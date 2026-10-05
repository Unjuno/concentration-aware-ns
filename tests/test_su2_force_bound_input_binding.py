import copy
import json
from pathlib import Path
import pytest
from tools.tighten_su2_force_envelope_bound import validate_prior


def original():
    return json.loads(Path('evidence/su2-force-time-uniform-upper-v1/analysis.json').read_text())


def test_original_input_chain_validates():
    validate_prior(original())


@pytest.mark.parametrize('kind', ['reference', 'sigma', 'missing', 'duplicate', 'archive'])
def test_corrupted_chain_is_rejected(kind):
    value=copy.deepcopy(original())
    if kind=='reference':value['reference_sha256']='0'*64
    elif kind=='sigma':value['cases'][0]['sigma']=1.
    elif kind=='missing':value['cases'].pop()
    elif kind=='duplicate':value['cases'][1]=copy.deepcopy(value['cases'][0])
    elif kind=='archive':value['cases'][0]['archive_sha256']='0'*64
    with pytest.raises(ValueError):validate_prior(value)
