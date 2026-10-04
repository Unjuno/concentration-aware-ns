import copy,json
from pathlib import Path
import pytest
from flint import ctx
from tools.amr_point_gradient_bound import exact_float
from tools.bound_su2_continuous_response import checked_force_constants


def row():
    return json.loads(Path('evidence/su2-force-envelope-upper-v2/analysis.json').read_text())['cases'][0]


def test_recorded_constants_enclose_recomputed_values():
    with ctx.workprec(128):
        linear,quadratic=checked_force_constants(row(),exact_float(4.),exact_float(.01))
        assert linear>0 and quadratic>0


@pytest.mark.parametrize('key',['linear_force_bound_expression','quadratic_force_bound_expression'])
def test_zeroed_force_constant_is_rejected(key):
    value=copy.deepcopy(row());value[key]['upper_rational']='0'
    with ctx.workprec(128),pytest.raises(ValueError,match='does not enclose'):
        checked_force_constants(value,exact_float(4.),exact_float(.01))
