#!/bin/sh
set -eu

project_root=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
source_file="$project_root/verification/SelectedScheduleTailPressure.lean"
expected_source_sha=d047cb638d428c72f8b68ee32d2f821842f7246efb0ecf388203574a4aa05910
expected_image=sha256:0637e54d4b04b0fb3b1eae5829b7616bee43ddb4fa9019628a76219d3466e9de
actual_source_sha=$(shasum -a 256 "$source_file" | awk '{print $1}')
actual_image=$(docker image inspect concentration-aware-ns:checker --format '{{.Id}}')

if [ "$actual_source_sha" != "$expected_source_sha" ]; then
  echo "SelectedScheduleTailPressure.lean hash differs from the audited source" >&2
  exit 1
fi
if [ "$actual_image" != "$expected_image" ]; then
  echo "checker image ID differs from the audited image" >&2
  exit 1
fi

stamp=$(date -u +%Y%m%dT%H%M%SZ)
out=${1:-"$project_root/work/selected-schedule-tail-nanoda-$stamp"}
case "$out" in
  /*) ;;
  *) out="$project_root/$out" ;;
esac
if [ -e "$out" ]; then
  echo "output path already exists: $out" >&2
  exit 1
fi
mkdir -p "$out"

docker run --rm --name cans-selected-tail-nanoda --user 501:20 --network none \
  --cpus=2 --memory=8g --ulimit nofile=1048576:1048576 -e LEAN_NUM_THREADS=2 \
  --mount type=volume,src=cans-lean-verification,dst=/verify,readonly \
  --mount type=volume,src=cans-lean-verification,dst=/verify/independent-source/.lake,volume-subpath=independent-source/.lake \
  --mount "type=bind,src=$source_file,dst=/extension/SelectedScheduleTailPressure.lean,readonly" \
  --mount "type=bind,src=$out,dst=/out" \
  --entrypoint /verify/checker-bin/no_unix \
  -w /verify/independent-source concentration-aware-ns:checker /bin/bash -c '
    set -euo pipefail
    export PATH=/verify/toolchain/checker-wrappers:/verify/toolchain/bin:$PATH
    cat /extension/SelectedScheduleTailPressure.lean | lake env lean --stdin -o /out/SelectedScheduleTailPressure.olean > /out/lean.log 2>&1
    export LEAN_PATH="/out:$(lake env printenv LEAN_PATH)"
    lake env /verify/packages/lean4export/.lake/build/bin/lean4export SelectedScheduleTailPressure \
      -- ConcentrationAwareSelectedScheduleTail.tail_relative_coefficient_small \
         ConcentrationAwareSelectedScheduleTail.tail_pressure_lower_bound_small \
         ConcentrationAwareSelectedScheduleTail.exists_rate_capped_prepared_profile \
         ConcentrationAwareSelectedScheduleTail.exists_rate_capped_profile_data \
         ConcentrationAwareSelectedScheduleTail.rate_capped_profile_data_tail_pressure_small \
         ConcentrationAwareSelectedScheduleTail.rate_capped_profile_data_tail_mass_upper_bound \
      > /out/selected-tail.ndjson 2> /out/export.log
    python3 -c '\''import json; json.dump({
      "export_file_path":"/out/selected-tail.ndjson",
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
export_path = out / "selected-tail.ndjson"
required = (
    b"tail_relative_coefficient_small",
    b"tail_pressure_lower_bound_small",
    b"exists_rate_capped_prepared_profile",
    b"exists_rate_capped_profile_data",
    b"rate_capped_profile_data_tail_pressure_small",
    b"rate_capped_profile_data_tail_mass_upper_bound",
)
with export_path.open("rb") as stream:
    with mmap.mmap(stream.fileno(), 0, access=mmap.ACCESS_READ) as data:
        missing = [name.decode() for name in required if data.find(name) < 0]
if missing:
    raise SystemExit(f"export is missing selected theorem declarations: {missing}")
log = (out / "nanoda.log").read_text()
match = re.search(r"Checked (\d+) declarations with no typechecker errors", log)
if not match:
    raise SystemExit("nanoda log has no successful typecheck summary")
lean_log = (out / "lean.log").read_text()
if "error:" in lean_log or "sorryAx" in lean_log:
    raise SystemExit("Lean compile or axiom output contains a forbidden marker")

def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return {"path": path.name, "bytes": path.stat().st_size, "sha256": h.hexdigest()}

summary = {
    "status": "PASS",
    "scope": "Independent nanoda typecheck of the selected-schedule tail coefficient and pressure bounds, plus the existential rate-capped prepared/full ProfileData construction.",
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
    "selected_declarations_present": [name.decode() for name in required],
    "artifacts": [digest(out / name) for name in (
        "SelectedScheduleTailPressure.olean", "selected-tail.ndjson", "nanoda-config.json",
        "lean.log", "export.log", "nanoda.log",
    )],
    "limitations": [
        "The rate-capped result is existential and does not transfer to FinalSlowBase.actualProfile.",
        "Independent term checking is not a validation of the pinned upstream construction's mathematical truth or its application to physical fluids.",
        "The result supplies one conditional pressure-tail bound, not a full pressure-sign conclusion or physical/molecular consequence.",
    ],
}
(out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
print(json.dumps(summary, indent=2))
PY
