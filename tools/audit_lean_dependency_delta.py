"""Intersect old-pin local imports with recorded upstream changes; no build claim."""
import json
import re
from pathlib import Path

root=Path('work/lean-verification/independent-source')
def imports(text):
    return re.findall(r'^import\s+(NavierStokes(?:\.\w+)+)',text,re.M)
direct=imports(Path('verification/AxisForceSign.lean').read_text())
todo=direct[:]
seen=set()
missing=[]
while todo:
    name=todo.pop()
    if name in seen:
        continue
    seen.add(name)
    path=root/(name.replace('.','/')+'.lean')
    if not path.exists():
        missing.append(name)
        continue
    todo.extend(imports(path.read_text()))
record=json.loads(Path('evidence/upstream-refresh/openai-2026-09-26.json').read_text())
changes={f['filename']:f for f in record['files']}
impacted=[changes[n.replace('.','/')+'.lean'] for n in sorted(seen)
          if n.replace('.','/')+'.lean' in changes]
result={'base':record['base'],'head':record['head'],
        'scope':'Textual NavierStokes import closure at old pin intersected with recorded GitHub comparison. Not compilation or semantic compatibility; new dependency closure and external modules are not audited.',
        'direct_imports':direct,'old_pin_module_count':len(seen),
        'missing_local_modules':missing,'changed_dependency_count':len(impacted),
        'changed_dependencies':impacted}
Path('evidence/upstream-refresh/extension-dependency-impact.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ('changed_dependencies','direct_imports')},indent=2))
raise SystemExit(1 if missing else 0)
