"""Unpack only verified source/toolchain archives into the isolated work area."""
import argparse
import hashlib
from pathlib import Path
import tarfile
p=argparse.ArgumentParser();p.add_argument('kind',choices=['source','toolchain']);args=p.parse_args()
options={'source':('navier-stokes-euler.tar.gz','e44f67a2bc3c133c14856d73b697f77344b030e3fae2f798254b64dcefbbb772'),
         'toolchain':('lean-linux-aarch64.tar.zst','64b41db6c158163e53a40ff950cdc978f3892cb11128a4ee050e4de8e8721894')}
name,expected=options[args.kind];archive=Path('work/downloads')/name
if hashlib.sha256(archive.read_bytes()).hexdigest()!=expected:raise ValueError('archive digest mismatch')
target=Path('work/lean-verification')/args.kind;target.mkdir(exist_ok=False)
with tarfile.open(archive) as tar:
    for member in tar.getmembers():
        parts=member.name.split('/',1)
        if len(parts)==2 and parts[1]:
            member.name=parts[1];tar.extract(member,target,filter='data')
print(target)
