"""Fixed-step output-clock diagnostic; not a production timing patch."""
from pathlib import Path
p=Path('/opt/SU2/SU2_CFD/src/output/COutput.cpp')
s=p.read_text()
old='SetHistoryOutputValue("CUR_TIME",  GetHistoryFieldValue("CUR_TIME") + GetHistoryFieldValue("TIME_STEP"));'
new='SetHistoryOutputValue("CUR_TIME", static_cast<su2double>(curTimeIter) * GetHistoryFieldValue("TIME_STEP"));'
assert s.count(old)==1
p.write_text(s.replace(old,new))
