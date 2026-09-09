"""Extract a fresh challenge/source tree; do not compile solutions here."""
import hashlib
import json
from pathlib import Path
import tarfile

archive = Path('work/downloads/navier-stokes-euler.tar.gz')
expected = 'e44f67a2bc3c133c14856d73b697f77344b030e3fae2f798254b64dcefbbb772'
assert hashlib.sha256(archive.read_bytes()).hexdigest() == expected
root = Path('work/lean-verification/independent-source')
root.mkdir(exist_ok=False)
with tarfile.open(archive) as tar:
    for member in tar:
        parts = Path(member.name).parts
        if len(parts) < 2:
            continue
        member.name = str(Path(*parts[1:]))
        tar.extract(member, root, filter='data')
manifest_path = root / 'lake-manifest.json'
manifest = json.loads(manifest_path.read_text())
for entry in manifest['packages']:
    for key in ('url', 'rev', 'inputRev', 'subDir'):
        entry.pop(key, None)
    entry.update(type='path', dir='../packages/' + entry['name'])
manifest_path.write_text(json.dumps(manifest, indent=2) + '\n')
config = root / 'lakefile.toml'
text = config.read_text()
for repo, name in [('leanprover-community/mathlib4', 'mathlib'), ('leanprover/comparator', 'Comparator')]:
    original = f'git = "https://github.com/{repo}.git"\nrev = "v4.34.0-rc2"'
    assert text.count(original) == 1
    text = text.replace(original, f'path = "../packages/{name}"')
config.write_text(text)
files = {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
         for p in sorted((root/'ComparatorChallenges').glob('*')) if p.is_file()}
Path('evidence/lean-verification/fresh-challenge-source.json').write_text(json.dumps({
    'archive_sha256': expected, 'challenge_files': files,
    'scope': 'Fresh archive extraction, only Lake path configuration changed. No solution compiled here yet. Shared dependency artifacts remain an explicit trust input.'}, indent=2) + '\n')
