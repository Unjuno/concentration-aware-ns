"""Resolve manifest entries to verified archives, without changing theorem files."""
import json
from pathlib import Path
root=Path('work/lean-verification');source=root/'source';p=source/'lake-manifest.json'
original=p.read_bytes();backup=source/'lake-manifest.upstream.json'
if backup.exists():raise ValueError('Already configured; inspect before changing')
backup.write_bytes(original);manifest=json.loads(original)
for entry in manifest['packages']:
    name=entry['name']
    if not (root/'packages'/name/entry['configFile']).exists():raise ValueError(name)
    for key in ['url','rev','inputRev','subDir']:entry.pop(key,None)
    entry['type']='path';entry['dir']='../packages/'+name
p.write_text(json.dumps(manifest,indent=2)+'\n')

config=source/'lakefile.toml'
text=config.read_text();(source/'lakefile.upstream.toml').write_text(text)
text=text.replace('git = "https://github.com/leanprover-community/mathlib4.git"\nrev = "v4.34.0-rc2"', 'path = "../packages/mathlib"')
text=text.replace('git = "https://github.com/leanprover/comparator.git"\nrev = "v4.34.0-rc2"', 'path = "../packages/Comparator"')
config.write_text(text)
