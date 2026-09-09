from pathlib import Path
p=Path('/opt/SU2/Common/src/toolboxes/MMS/CUserDefinedSolution.cpp')
s=p.read_text()
a=s.index('namespace {');b=s.index('CUserDefinedSolution::CUserDefinedSolution()',a)
p.write_text(s[:a]+Path('/tmp/helper.cpp').read_text()+s[b:])
