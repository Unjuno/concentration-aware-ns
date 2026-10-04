import copy,csv,io,tarfile
from pathlib import Path
import pytest
from tools.run_su2_full_horizon_cfl_pair import verify_history


def original():
    with tarfile.open(Path('evidence/su2-study-v1/n32-dt0.001.tar.gz')) as archive:
        rows=list(csv.DictReader(io.TextIOWrapper(archive.extractfile('history.csv'))))
    return [{k.strip().strip('"'):v for k,v in r.items()} for r in rows]


def test_existing_full_horizon_clock_matches():
    assert verify_history(original())['steps']==50


@pytest.mark.parametrize('kind',['missing','duplicate','step','time','nonfinite'])
def test_bad_history_cannot_claim_matched_horizon(kind):
    rows=copy.deepcopy(original())
    if kind=='missing':rows.pop()
    elif kind=='duplicate':rows[1]['Time_Iter']=rows[0]['Time_Iter']
    elif kind=='step':rows[1]['Time_Step']='0.0005'
    elif kind=='time':rows[1]['Cur_Time']='0.002'
    else:rows[1]['Cur_Time']='nan'
    with pytest.raises(ValueError):verify_history(rows)
