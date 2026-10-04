"""Restore hash-pinned capture data and replay native position interpolation."""
import argparse,hashlib,json,shlex,shutil,subprocess,tarfile
from pathlib import Path,PurePosixPath
from tools.run_amr_mean_quality import ROOT,sha
from tools.analyze_amr_mean_quality import verify_archive
from tools.audit_cell_point_contract import FILES,PIN
from tools.run_high_gradient_openfoam import resolve_docker_cli,resolve_docker_context

PROTOCOL=ROOT/'protocols/of13-cell-point-query-v1.json'
SOURCES=(*FILES,'src/finiteVolume/interpolation/interpolation/interpolationCellPoint/cellPointWeight/cellPointWeight.H')


def unpack_verified(archive,destination,expected=None):
    """Copy only finite regular relative members; never delegate tar extraction."""
    destination=Path(destination);seen=set();total=0
    with tarfile.open(archive,'r:gz') as tf:
        for member in tf:
            p=PurePosixPath(member.name);total+=member.size
            if (not member.isfile() or member.issparse() or p.is_absolute() or '..' in p.parts
                    or member.name in seen or member.size<0 or total>8*1024**3
                    or (expected is not None and member.name not in expected)):
                raise ValueError('unsafe/unexpected archive member')
            data=tf.extractfile(member).read()
            if expected is not None and hashlib.sha256(data).hexdigest()!=expected[member.name]:
                raise ValueError('member digest mismatch')
            path=destination.joinpath(*p.parts)
            if path.exists():raise FileExistsError('preserve existing extracted member')
            path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data);seen.add(member.name)
    if expected is not None and seen!=set(expected):raise ValueError('missing archive member')


def prepare(bundle,work):
    spec=json.loads(PROTOCOL.read_text());work=Path(work)
    if work.exists():raise FileExistsError('preserve prior replay')
    if sha(bundle)!=spec['release_sha256']:raise ValueError('release bundle digest mismatch')
    work.mkdir(parents=True);unpack_verified(bundle,work/'bundle')
    data=work/'bundle/capture-evidence'
    if sha(data/'capture-manifest.json')!=spec['capture_manifest_sha256']:
        raise ValueError('capture manifest differs from witness source')
    receipt=json.loads((data/'capture-manifest.json').read_text())
    for name,digest in receipt['capture_files_sha256'].items():
        if sha(data/'capture'/name)!=digest:raise ValueError('capture file digest mismatch')
    base=json.loads((data/'base/manifest.json').read_text());verify_archive(data/'base/raw.tar.gz',base)
    unpack_verified(data/'base/raw.tar.gz',work/'raw',base['archive']['members_sha256'])
    case=work/'case';case.mkdir()
    # Only configuration and stored fields are restored; no solver libraries or evolution.
    for p in sorted((work/'raw/main').rglob('*')):
        rel=p.relative_to(work/'raw/main')
        if p.is_file() and rel.parts[0] in ('0','0.05','constant','system'):
            dest=case/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,dest)
    if sha(data/'mesh.tar.gz')!=receipt['mesh_archive_sha256']:raise ValueError('mesh archive digest mismatch')
    unpack_verified(data/'mesh.tar.gz',case,receipt['mesh_members_sha256'])
    fields={p:sha(case/'0.05'/p) for p in ('U','p')}
    if fields!=receipt['field_sha256_after']:raise ValueError('restored final fields differ')
    return data,case,fields


def replay(bundle,image,source,work,evidence):
    work=Path(work);evidence=Path(evidence);source=Path(source)
    if evidence.exists():raise FileExistsError('preserve prior evidence')
    upstream={p:hashlib.sha256(subprocess.check_output(['git','-C',str(source),'show',PIN+':'+p])).hexdigest() for p in SOURCES}
    data,case,before=prepare(bundle,work);evidence.mkdir(parents=True)
    probe=work/'probe';shutil.copytree(ROOT/'runtime/of13-cell-point-query-probe',probe)
    cli,_=resolve_docker_cli();docker=[cli,'--context',resolve_docker_context(cli)]
    image_data=json.loads(subprocess.check_output([*docker,'image','inspect',image]))[0]
    paths=' '.join(shlex.quote('/opt/openfoam13/'+p) for p in SOURCES)
    script=('source /opt/openfoam13/etc/bashrc\ncd /probe\nwmake > /capture/build.log 2>&1 || exit $?\n'
            +'sha256sum '+paths+' > /capture/installed-source-files.sha256 || exit $?\n'
            +'sha256sum /opt/openfoam13/platforms/linuxArm64GccDPInt32Opt/lib/libfiniteVolume.so /opt/openfoam13/platforms/linuxArm64GccDPInt32Opt/lib/libOpenFOAM.so > /capture/libraries.sha256 || exit $?\n'
            +'cp /opt/package-versions.txt /capture/package-versions.txt || exit $?\n'
            +'cd /case\n/probe/cansCellPointQueryProbe > /capture/probe.log 2>&1\n')
    argv=[*docker,'run','--rm','--network','none','--platform','linux/arm64','--cpus','3','--memory','12g','--pids-limit','512','--entrypoint','/bin/bash','-v',str(probe)+':/probe','-v',str(case)+':/case:ro','-v',str(evidence)+':/capture',image_data['Id'],'-lc',script]
    receipt={'status':'INCOMPLETE_NATIVE_QUERY_REPLAY','source_commit':subprocess.check_output(['git','-C',str(ROOT),'rev-parse','HEAD'],text=True).strip(),'protocol_sha256':sha(PROTOCOL),'bundle_sha256':sha(bundle),'capture_manifest_sha256':sha(data/'capture-manifest.json'),'upstream_commit':PIN,'upstream_files_sha256':upstream,'image':image_data,'argv':argv,'field_sha256_before':before}
    manifest=evidence/'manifest.json';manifest.write_text(json.dumps(receipt,indent=2)+'\n')
    result=subprocess.run(argv,timeout=600);receipt['exit_code']=result.returncode
    manifest.write_text(json.dumps(receipt,indent=2)+'\n')
    if result.returncode:raise RuntimeError('probe failed; preserve partial evidence')
    after={p:sha(case/'0.05'/p) for p in ('U','p')}
    if after!=before:raise ValueError('read-only replay changed fields')
    installed={}
    for line in (evidence/'installed-source-files.sha256').read_text().splitlines():
        digest,path=line.split(maxsplit=1);installed[path.removeprefix('/opt/openfoam13/')]=digest
    if installed!=upstream:raise ValueError('installed source differs from pin')
    stock={line.split(maxsplit=1)[1]:line.split(maxsplit=1)[0] for line in (data/'base/package-stock-libraries.log').read_text().splitlines()}
    libraries={line.split(maxsplit=1)[1]:line.split(maxsplit=1)[0] for line in (evidence/'libraries.sha256').read_text().splitlines()}
    if len(libraries)!=2 or any(stock.get(path)!=digest for path,digest in libraries.items()):
        raise ValueError('native interpolation libraries differ from original stock binaries')
    receipt['libraries_match_original_stock']=True
    receipt.update(status='NATIVE_QUERY_REPLAY_COMPLETE_NOT_CONTINUUM_CERTIFICATION',field_sha256_after=after,installed_sources_match_pin=True,probe_binary_sha256=sha(probe/'cansCellPointQueryProbe'),output_files_sha256={p.name:sha(p) for p in evidence.iterdir() if p.is_file() and p.name!='manifest.json'})
    manifest.write_text(json.dumps(receipt,indent=2)+'\n');print(receipt['status'],flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for key in ('bundle','source','work','evidence'):p.add_argument('--'+key,required=True,type=Path)
    p.add_argument('--image',required=True);a=p.parse_args()
    replay(a.bundle.resolve(),a.image,a.source.resolve(),a.work.resolve(),a.evidence.resolve())
