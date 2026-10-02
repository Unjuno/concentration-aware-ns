#!/bin/sh
# Compile and audit the selected-field fixed-time spatial Hessian transfer.
set -eu

project_root=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
out=${1:-"$project_root/evidence/spatial-hessian-transfer"}
case "$out" in
  /*) ;;
  *) out="$project_root/$out" ;;
esac
if [ -e "$out" ]; then
  echo "output path already exists: $out" >&2
  exit 1
fi
mkdir -p "$out"

expected_image=sha256:0637e54d4b04b0fb3b1eae5829b7616bee43ddb4fa9019628a76219d3466e9de
actual_image=$(docker image inspect concentration-aware-ns:checker --format '{{.Id}}')
if [ "$actual_image" != "$expected_image" ]; then
  echo "unexpected checker image: $actual_image" >&2
  exit 1
fi

docker run --rm --name cans-spatial-hessian-transfer-check \
  --user 501:20 --network none --cpus=2 --memory=6g \
  --mount type=volume,src=cans-lean-verification,dst=/verify,readonly \
  --mount type=volume,src=cans-lean-verification,dst=/verify/independent-source/.lake,volume-subpath=independent-source/.lake \
  --mount "type=bind,src=$project_root/verification,dst=/extension,readonly" \
  --mount "type=bind,src=$out,dst=/out" \
  -w /verify/independent-source --entrypoint /bin/bash concentration-aware-ns:checker \
  -c 'set -eu
    export PATH=/verify/toolchain/bin:$PATH
    export LEAN_NUM_THREADS=2
    test "$(cut -d " " -f1 /verify/source.sha256)" = e44f67a2bc3c133c14856d73b697f77344b030e3fae2f798254b64dcefbbb772
    test "$(python3 -c "import json; print(next(p['rev'] for p in json.load(open('lake-manifest.json'))['packages'] if p['name'] == 'mathlib'))")" = 85e3a25e006c35636f0e53b0e9296caca2685bc0
    lake env lean /extension/SupportHoleAssembly.lean \
      -o .lake/build/lib/lean/SupportHoleAssembly.olean
    lake env lean /extension/SpatialJetRestriction.lean \
      -o .lake/build/lib/lean/SpatialJetRestriction.olean
    { cat /extension/SpatialHessianTransfer.lean
      printf "\n#print axioms ConcentrationAware.selected_cusp_ball_actual_spatial_hessian_rate\n"
      printf "#print axioms ConcentrationAware.spatial_jet_norm_le_spacetime_jet_norm_at\n"
    } > /out/SpatialHessianTransferAudit.lean
    lake env lean /out/SpatialHessianTransferAudit.lean \
      -o /out/SpatialHessianTransferAudit.olean > /out/lean.log 2>&1
    cat /out/lean.log'

python3 - "$project_root" "$out" <<'PY'
import hashlib
import json
import pathlib
import re
import subprocess
import sys

root, out = map(pathlib.Path, sys.argv[1:])
files = {
    "SupportHoleAssembly.lean": root / "verification/SupportHoleAssembly.lean",
    "SpatialJetRestriction.lean": root / "verification/SpatialJetRestriction.lean",
    "SpatialHessianTransfer.lean": root / "verification/SpatialHessianTransfer.lean",
}
log = out / "lean.log"
text = log.read_text()
normalized = re.sub(r"\s+", " ", text)
declarations = (
    "ConcentrationAware.selected_cusp_ball_actual_spatial_hessian_rate",
    "ConcentrationAware.spatial_jet_norm_le_spacetime_jet_norm_at",
)
axioms = "depends on axioms: [propext, Classical.choice, Quot.sound]"
printed = re.findall(r"'([^']+)' depends on axioms:", normalized)
if "error:" in text or "sorryAx" in text or tuple(printed) != declarations:
    raise SystemExit("Lean compile or declaration audit did not pass")
if normalized.count(axioms) != len(declarations):
    raise SystemExit("unexpected axiom set")

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

image = subprocess.check_output(
    ["docker", "image", "inspect", "concentration-aware-ns:checker", "--format", "{{.Id}}"],
    text=True,
).strip()
result = {
    "status": "PASS",
    "scope": "Composes the local ContDiffAt spatial-jet restriction with the selected-field cusp-ball full-spacetime Hessian bound, yielding a fixed-time spatial Hessian bound C*q^(-40) throughout the same shrinking ball on an existential terminal interval.",
    "upstream_repository": "https://github.com/openai/NavierStokesAndEuler",
    "upstream_commit": "f9e8bc5b38b6e212696e8a30e3e91517af887bbd",
    "mathlib_commit": "85e3a25e006c35636f0e53b0e9296caca2685bc0",
    "lean": "4.34.0-rc2",
    "checker_image_id": image,
    "source_sha256": {name: sha(path) for name, path in files.items()},
    "lean_log_sha256": sha(log),
    "declarations": list(declarations),
    "permitted_axioms": ["propext", "Classical.choice", "Quot.sound"],
    "limitations": [
        "The radius coefficient, Hessian constant, and terminal interval remain existential and parameter-dependent.",
        "The classical nonlinear packet comparison and executable finite-stage extraction are not formalized by this theorem.",
        "The result does not establish fixed-size packet misalignment, molecular ordering, phase transition, particle-position certainty, or a constitutive-viscosity law.",
    ],
}
(out / "manifest.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
PY
