import json,tarfile,hashlib,sys
from pathlib import Path
from tools.analyze_amr_mean_quality import verify_archive
from tools.run_amr_mean_quality import ROOT,SOURCE_FILES,sha
p=Path(sys.argv[1]);case=sys.argv[2];out=Path(sys.argv[3]);assert not out.exists()
c=json.load(open(p/'capture-manifest.json'));b=json.load(open(p/'base/manifest.json'));old=json.load(open(ROOT/'evidence/of13-amr-mean-quality-v1'/case/'manifest.json'))
assert b['source_commit']=='4e60b23065811d488fe6890ad59af698a81c35b8'
assert c['case_id']==b['case_id']==case and c['status']=='CAPTURE_COMPLETE_NOT_CONTINUUM_CERTIFICATION' and c['exit_code']==0
assert set(b['source_files_sha256'])==set(SOURCE_FILES) and b['source_files_sha256']==old['source_files_sha256']
assert all(sha(ROOT/q)==h for q,h in b['source_files_sha256'].items())
r=next(r for r in b['runs'] if r['label']=='main');o=next(r for r in old['runs'] if r['label']=='main')
assert r['inputs_sha256']==o['inputs_sha256'] and r['final_field_sha256']==o['final_field_sha256']==c['field_sha256_before']==c['field_sha256_after']
assert r['container_state']['Running'] is False and r['container_state']['ExitCode']==0
verify_archive(p/'base/raw.tar.gz',b)
expected=c['mesh_members_sha256'];assert sha(p/'mesh.tar.gz')==c['mesh_archive_sha256'];seen=set()
with tarfile.open(p/'mesh.tar.gz') as t:
 for m in t:
  assert m.isfile() and not m.issparse() and m.name in expected and m.name not in seen
  assert hashlib.sha256(t.extractfile(m).read()).hexdigest()==expected[m.name];seen.add(m.name)
assert seen==set(expected)
for q,h in c['capture_files_sha256'].items():assert sha(p/'capture'/q)==h
installed={}
for line in (p/'capture/installed-source-files.sha256').read_text().splitlines():
 digest,name=line.split(maxsplit=1);installed[name.removeprefix('/opt/openfoam13/')]=digest
reference=json.load(open(ROOT/'evidence/of13-cell-point-capture-v1-n16/capture-manifest.json'))
assert installed==c['upstream_files_sha256']==reference['upstream_files_sha256'] and c['upstream_commit']==reference['upstream_commit'] and c['installed_sources_match_pin']
assert sha(p.parent.parent/'work/cell-point-v1/probe/cansCellPointProbe')==c['probe_binary_sha256']
result={'status':'ARCHIVES_INPUTS_FINAL_FIELDS_AND_CAPTURE_IDENTITIES_VERIFIED','case_id':case,'runtime_source_commit':b['source_commit'],'raw_archive_sha256':b['archive']['sha256'],'raw_members':len(b['archive']['members_sha256']),'mesh_archive_sha256':c['mesh_archive_sha256'],'mesh_members':len(expected),'capture_manifest_sha256':sha(p/'capture-manifest.json'),'original_input_and_final_fields_byte_identical':True,'probe_fields_unchanged':True,'source_files_verified':len(SOURCE_FILES),'installed_interpolation_sources_verified':len(installed),'probe_binary_hash_matches_downloaded_artifact':True,'probe_binary_sha256':c['probe_binary_sha256'],'verification_script_sha256':sha(__file__),'limits':['Archive integrity and floating topology are separate from continuous quality/native branch obligations']}
out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)
