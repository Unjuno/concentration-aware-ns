#!/bin/sh
set -eu

project_root=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
source_file="$project_root/verification/AxisForceSign.lean"
expected_source_sha=fe989c3a279d7515b2584e82ada2632930a80299f98f502f68720ff45e2fb793
expected_image=sha256:0637e54d4b04b0fb3b1eae5829b7616bee43ddb4fa9019628a76219d3466e9de
actual_source_sha=$(shasum -a 256 "$source_file" | awk '{print $1}')
actual_image=$(docker image inspect concentration-aware-ns:checker --format '{{.Id}}')

if [ "$actual_source_sha" != "$expected_source_sha" ]; then
  echo "AxisForceSign.lean hash differs from the audited source" >&2
  exit 1
fi
if [ "$actual_image" != "$expected_image" ]; then
  echo "checker image ID differs from the audited image" >&2
  exit 1
fi

stamp=$(date -u +%Y%m%dT%H%M%SZ)
out=${1:-"$project_root/work/axis-force-nanoda-$stamp"}
case "$out" in
  /*) ;;
  *) out="$project_root/$out" ;;
esac
if [ -e "$out" ]; then
  echo "output path already exists: $out" >&2
  exit 1
fi
mkdir -p "$out"

docker run --rm --name cans-axis-nanoda --user 501:20 --network none \
  --cpus=2 --memory=8g --ulimit nofile=1048576:1048576 -e LEAN_NUM_THREADS=2 \
  --mount type=volume,src=cans-lean-verification,dst=/verify,readonly \
  --mount type=volume,src=cans-lean-verification,dst=/verify/independent-source/.lake,volume-subpath=independent-source/.lake \
  --mount "type=bind,src=$source_file,dst=/extension/AxisForceSign.lean,readonly" \
  --mount "type=bind,src=$out,dst=/out" \
  --entrypoint /verify/checker-bin/no_unix \
  -w /verify/independent-source concentration-aware-ns:checker /bin/bash -c '
    set -euo pipefail
    export PATH=/verify/toolchain/checker-wrappers:/verify/toolchain/bin:$PATH
    cat /extension/AxisForceSign.lean | lake env lean --stdin -o /out/AxisForceSign.olean > /out/lean.log 2>&1
    export LEAN_PATH="/out:$(lake env printenv LEAN_PATH)"
    lake env /verify/packages/lean4export/.lake/build/bin/lean4export AxisForceSign \
      -- ConcentrationAware.actual_ratio_negative_of_local_Z \
         ConcentrationAware.actual_ratio_has_strictly_negative_limit \
         ConcentrationAware.outgoing_root_Z_positive_iff_moment_threshold \
      > /out/axis-force.ndjson 2> /out/export.log
    python3 -c '\''import json; json.dump({
      "export_file_path":"/out/axis-force.ndjson",
      "permitted_axioms":["propext","Classical.choice","Quot.sound"],
      "unpermitted_axiom_hard_error":True,
      "nat_extension":True,
      "string_extension":True,
      "print_success_message":True
    },open("/out/nanoda-config.json","w"))'\''
    /verify/checker-sources/nanoda/target/release/nanoda_bin \
      /out/nanoda-config.json > /out/nanoda.log 2>&1
    cat /out/nanoda.log
  '

python3 - "$out" "$expected_source_sha" "$expected_image" <<'PY'
import hashlib
import json
import mmap
import pathlib
import re
import sys

out = pathlib.Path(sys.argv[1])
source_sha, image_id = sys.argv[2:]
export_path = out / "axis-force.ndjson"
required = (
    b"actual_ratio_negative_of_local_Z",
    b"actual_ratio_has_strictly_negative_limit",
    b"outgoing_root_Z_positive_iff_moment_threshold",
)
with export_path.open("rb") as stream:
    with mmap.mmap(stream.fileno(), 0, access=mmap.ACCESS_READ) as data:
        present = [name.decode() for name in required if data.find(name) >= 0]
if len(present) != len(required):
    raise SystemExit(f"export is missing selected theorem declarations: {present}")
log = (out / "nanoda.log").read_text()
match = re.search(r"Checked (\d+) declarations with no typechecker errors", log)
if not match:
    raise SystemExit("nanoda log has no successful typecheck summary")

def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return {"path": path.name, "bytes": path.stat().st_size, "sha256": h.hexdigest()}

summary = {
    "status": "PASS",
    "scope": "Independent nanoda typecheck of the selected actual-field viscous-acceleration ratio and local pressure-moment theorems, including their exported dependency closure.",
    "source_sha256": source_sha,
    "checker_image_id": image_id,
    "lean": "4.34.0-rc2",
    "lean4export": "3.1.0",
    "nanoda": "0.4.16",
    "nanoda_commit": "05055695879dfebb6628a67da88ceca6cd6b0421",
    "checked_declarations": int(match.group(1)),
    "typechecker_errors": 0,
    "pretty_printer_errors": ["Unable to print axioms"] if "pretty printer errors" in log else [],
    "permitted_axioms": ["propext", "Classical.choice", "Quot.sound"],
    "selected_declarations_present": present,
    "artifacts": [digest(out / name) for name in (
        "AxisForceSign.olean", "axis-force.ndjson", "nanoda-config.json",
        "lean.log", "export.log", "nanoda.log",
    )],
    "limitations": [
        "The exported dependency closure is large and is retained locally under work/ rather than committed.",
        "This checks Lean proof terms independently; it does not discharge the local Z>0 condition for FinalSlowBase.actualProfile.",
        "It is not a physical model or a proof of molecular or constitutive-viscosity behavior.",
    ],
}
(out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
print(json.dumps(summary, indent=2))
PY
