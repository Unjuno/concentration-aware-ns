"""Run one unchanged fine/temporal mean-quality recipe, then capture cellPoint read-only."""
import argparse,hashlib,json,shlex,shutil,subprocess,tarfile
from pathlib import Path
from tools.run_amr_mean_quality import ROOT,SOURCE_FILES,sha,run
from tools.run_high_gradient_openfoam import resolve_docker_cli,resolve_docker_context
from tools.audit_cell_point_contract import FILES,PIN


def capture(case_id,image,source,work,evidence):
    if case_id not in ("n32-dt0.001","n64-dt0.001","n32-dt0.0005"):raise ValueError("case outside frozen extension")
    if work.exists() or evidence.exists():raise FileExistsError('preserve prior experiment')
    frozen=json.loads((ROOT/'evidence/of13-amr-mean-quality-v1'/case_id/'manifest.json').read_text())
    if set(frozen['source_files_sha256'])!=set(SOURCE_FILES) or any(sha(ROOT/p)!=h for p,h in frozen['source_files_sha256'].items()):
        raise ValueError('original numerical recipe changed')
    upstream={p:sha(source/p) for p in FILES}
    for p in FILES:
        data=subprocess.check_output(['git','-C',str(source),'show',PIN+':'+p])
        if hashlib.sha256(data).hexdigest()!=upstream[p]:raise ValueError('upstream pin mismatch')
    work.mkdir(parents=True);evidence.mkdir(parents=True)
    base=run(case_id,image,source,work/'solver',evidence/'base')
    original_main=next(r for r in frozen['runs'] if r['label']=='main')
    current_main=next(r for r in base['runs'] if r['label']=='main')
    if any(original_main[key]!=current_main[key] for key in ('inputs_sha256','final_field_sha256')):
        raise ValueError('rerun differs from original input or final fields; preserve partial evidence')
    probe=work/'probe';shutil.copytree(ROOT/'runtime/of13-cell-point-probe',probe)
    case=work/'solver/main';out=evidence/'capture';out.mkdir()
    before={p:sha(case/'0.05'/p) for p in ('U','p')}
    cli,_=resolve_docker_cli();docker=[cli,'--context',resolve_docker_context(cli)]
    paths=' '.join(shlex.quote('/opt/openfoam13/'+p) for p in FILES)
    script='source /opt/openfoam13/etc/bashrc\ncd /probe\nwmake > /capture/build.log 2>&1 || exit $?\nsha256sum '+paths+' > /capture/installed-source-files.sha256 || exit $?\ncp /opt/openfoam13/COPYING /capture/OpenFOAM-COPYING || exit $?\ncd /case\n/probe/cansCellPointProbe > /capture/probe.log 2>&1\n'
    argv=[*docker,'run','--rm','--network','none','--platform','linux/arm64','--cpus','3','--memory','12g','--pids-limit','512','--entrypoint','/bin/bash','-v',str(probe)+':/probe','-v',str(case)+':/case:ro','-v',str(out)+':/capture',base['image']['Id'],'-lc',script]
    receipt={'status':'INCOMPLETE_CAPTURE','case_id':case_id,'original_input_and_final_fields_byte_identical':True,'base_manifest':'base/manifest.json','upstream_commit':PIN,'upstream_files_sha256':upstream,'argv':argv,'field_sha256_before':before}
    manifest=evidence/'capture-manifest.json';manifest.write_text(json.dumps(receipt,indent=2)+'\n')
    result=subprocess.run(argv,timeout=600);receipt['exit_code']=result.returncode
    if result.returncode:manifest.write_text(json.dumps(receipt,indent=2)+'\n');raise RuntimeError('capture failed; preserve logs')
    after={p:sha(case/'0.05'/p) for p in ('U','p')}
    if after!=before:raise ValueError('read-only probe changed final fields')
    receipt['field_sha256_after']=after;receipt['summary']=json.loads((out/'summary.json').read_text())
    installed={}
    for line in (out/'installed-source-files.sha256').read_text().splitlines():
        digest,path=line.split(maxsplit=1);installed[path.removeprefix('/opt/openfoam13/')]=digest
    receipt['installed_sources_match_pin']=installed==upstream
    if not receipt['installed_sources_match_pin']:raise ValueError('installed interpolation source differs from pin')
    meshes={}
    with tarfile.open(evidence/'mesh.tar.gz','w:gz') as archive:
        for p in sorted(case.rglob('*')):
            if p.is_file() and '/polyMesh/' in p.as_posix():
                name=p.relative_to(case).as_posix();meshes[name]=sha(p);archive.add(p,arcname=name,recursive=False)
    if not meshes:raise ValueError('no final mesh instances preserved')
    receipt.update(status='CAPTURE_COMPLETE_NOT_CONTINUUM_CERTIFICATION',mesh_members_sha256=meshes,mesh_archive_sha256=sha(evidence/'mesh.tar.gz'),capture_files_sha256={p.name:sha(p) for p in out.iterdir() if p.is_file()},probe_binary_sha256=sha(probe/'cansCellPointProbe'))
    manifest.write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps({'status':receipt['status'],'summary':receipt['summary']}),flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--image',required=True);p.add_argument('--source',type=Path,required=True)
    p.add_argument('--work',type=Path,required=True);p.add_argument('--evidence',type=Path,required=True)
    p.add_argument('--case',required=True);a=p.parse_args();capture(a.case,a.image,a.source.resolve(),a.work.resolve(),a.evidence.resolve())
