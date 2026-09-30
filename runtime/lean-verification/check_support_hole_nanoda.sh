#!/bin/sh
set -eu

project_root=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
source_file="$project_root/verification/SupportHoleAssembly.lean"
expected_source_sha=a31432420d0783c94e4be3bd65fec7b0b3a516a422cec64dce4bd97f407618f7
expected_image=sha256:0637e54d4b04b0fb3b1eae5829b7616bee43ddb4fa9019628a76219d3466e9de
actual_source_sha=$(shasum -a 256 "$source_file" | awk '{print $1}')
actual_image=$(docker image inspect concentration-aware-ns:checker --format '{{.Id}}')

if [ "$actual_source_sha" != "$expected_source_sha" ]; then
  echo "SupportHoleAssembly.lean hash differs from the audited source" >&2
  exit 1
fi
if [ "$actual_image" != "$expected_image" ]; then
  echo "checker image ID differs from the audited image" >&2
  exit 1
fi

stamp=$(date -u +%Y%m%dT%H%M%SZ)
out=${1:-"$project_root/work/support-hole-nanoda-$stamp"}
case "$out" in
  /*) ;;
  *) out="$project_root/$out" ;;
esac
if [ -e "$out" ]; then
  echo "output path already exists: $out" >&2
  exit 1
fi
mkdir -p "$out"

docker run --rm --name cans-support-hole-nanoda --user 501:20 --network none \
  --cpus=2 --memory=8g --ulimit nofile=1048576:1048576 -e LEAN_NUM_THREADS=2 \
  --mount type=volume,src=cans-lean-verification,dst=/verify,readonly \
  --mount type=volume,src=cans-lean-verification,dst=/verify/independent-source/.lake,volume-subpath=independent-source/.lake \
  --mount "type=bind,src=$source_file,dst=/extension/SupportHoleAssembly.lean,readonly" \
  --mount "type=bind,src=$out,dst=/out" \
  --entrypoint /verify/checker-bin/no_unix \
  -w /verify/independent-source concentration-aware-ns:checker /bin/bash -c '
    set -euo pipefail
    export PATH=/verify/toolchain/checker-wrappers:/verify/toolchain/bin:$PATH
    cat /extension/SupportHoleAssembly.lean > /tmp/SupportHoleAssemblyWithAudit.lean
    printf "\\n#print axioms ConcentrationAware.coordinateEta_margin_of_euclidean_ball\\n" >> /tmp/SupportHoleAssemblyWithAudit.lean
    printf "#print axioms ConcentrationAware.transverse_radius_le_of_euclidean_ball\\n" >> /tmp/SupportHoleAssemblyWithAudit.lean
    printf "#print axioms ConcentrationAware.axial_deviation_le_of_euclidean_ball\\n" >> /tmp/SupportHoleAssemblyWithAudit.lean
    printf "#print axioms ConcentrationAware.cusp_ball_point_in_physical_exterior\\n" >> /tmp/SupportHoleAssemblyWithAudit.lean
    printf "#print axioms ConcentrationAware.selected_velocity_germ_of_cusp_ball_point\\n" >> /tmp/SupportHoleAssemblyWithAudit.lean
    printf "#print axioms ConcentrationAware.selected_axis_center_small_eventually\\n" >> /tmp/SupportHoleAssemblyWithAudit.lean
    printf "#print axioms ConcentrationAware.selected_velocity_germ_on_cusp_tube\\n" >> /tmp/SupportHoleAssemblyWithAudit.lean
    printf "#print axioms ConcentrationAware.exists_admissible_cusp_radius\\n" >> /tmp/SupportHoleAssemblyWithAudit.lean
    printf "#print axioms ConcentrationAware.cusp_ball_eventually_in_endpoint_neighborhood\\n" >> /tmp/SupportHoleAssemblyWithAudit.lean
    printf "#print axioms ConcentrationAware.selected_cusp_ball_actual_hessian_rate\\n" >> /tmp/SupportHoleAssemblyWithAudit.lean
    lake env lean --stdin -o /out/SupportHoleAssembly.olean < /tmp/SupportHoleAssemblyWithAudit.lean > /out/lean.log 2>&1
    export LEAN_PATH="/out:$(lake env printenv LEAN_PATH)"
    lake env /verify/packages/lean4export/.lake/build/bin/lean4export SupportHoleAssembly \
      -- ConcentrationAware.coordinateEta_margin_of_euclidean_ball \
         ConcentrationAware.transverse_radius_le_of_euclidean_ball \
         ConcentrationAware.axial_deviation_le_of_euclidean_ball \
         ConcentrationAware.cusp_ball_point_in_physical_exterior \
         ConcentrationAware.selected_velocity_germ_of_cusp_ball_point \
         ConcentrationAware.selected_axis_center_small_eventually \
         ConcentrationAware.selected_velocity_germ_on_cusp_tube \
         ConcentrationAware.exists_admissible_cusp_radius \
         ConcentrationAware.cusp_ball_eventually_in_endpoint_neighborhood \
         ConcentrationAware.selected_cusp_ball_actual_hessian_rate \
      > /out/support-hole.ndjson 2> /out/export.log
    python3 -c '\''import json; json.dump({
      "export_file_path":"/out/support-hole.ndjson",
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
export_path = out / "support-hole.ndjson"
required = (
    b"coordinateEta_margin_of_euclidean_ball",
    b"transverse_radius_le_of_euclidean_ball",
    b"axial_deviation_le_of_euclidean_ball",
    b"cusp_ball_point_in_physical_exterior",
    b"selected_velocity_germ_of_cusp_ball_point",
    b"selected_axis_center_small_eventually",
    b"selected_velocity_germ_on_cusp_tube",
    b"exists_admissible_cusp_radius",
    b"cusp_ball_eventually_in_endpoint_neighborhood",
    b"selected_cusp_ball_actual_hessian_rate",
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
normalized = re.sub(r"\s+", " ", lean_log)
expected_axioms = "depends on axioms: [propext, Classical.choice, Quot.sound]"
printed = re.findall(r"'([^']+)' depends on axioms:", normalized)
if "error:" in lean_log or "sorryAx" in lean_log:
    raise SystemExit("Lean compile or axiom output contains a forbidden marker")
expected_printed = tuple(name.decode() for name in required)
if tuple(printed) != expected_printed or normalized.count(expected_axioms) != len(required):
    raise SystemExit("Lean axiom audit does not match the expected theorem set")

def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return {"path": path.name, "bytes": path.stat().st_size, "sha256": h.hexdigest()}

summary = {
    "status": "PASS",
    "scope": "Independent nanoda typecheck of the selected cusp-ball and full-spacetime Hessian-transfer theorem closure, with the pinned Lean axiom audit.",
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
        "SupportHoleAssembly.olean", "support-hole.ndjson", "nanoda-config.json",
        "lean.log", "export.log", "nanoda.log",
    )],
    "limitations": [
        "This independently checks the exported Lean proof terms; it does not validate the mathematical truth of the pinned upstream source construction.",
        "The theorem has existential, parameter-dependent terminal intervals and shrinking radii; it is not a fixed-size packet theorem or a singular-endpoint result.",
        "The spatial restriction of the local jet and the classical nonlinear packet estimate are not jointly formalized.",
        "It does not establish particle alignment, molecular determinism, phase transition, or a constitutive-viscosity change.",
    ],
}
(out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
print(json.dumps(summary, indent=2))
PY
