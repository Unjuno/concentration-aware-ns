#!/bin/sh
# Compile the support-hole extension against the pinned OpenAI/Lean cache.
set -eu

project_root=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
out=${1:-"$project_root/evidence/openai-lean-2026-09-30-spatial-ball"}
case "$out" in
  /*) ;;
  *) out="$project_root/$out" ;;
esac
if [ -e "$out" ]; then
  echo "output path already exists: $out" >&2
  exit 1
fi
mkdir -p "$out"

docker run --rm --name cans-supporthole-assembly-check \
  --user 501:20 --network none --cpus=2 --memory=4g \
  --mount type=volume,src=cans-lean-verification,dst=/verify,readonly \
  --mount type=volume,src=cans-lean-verification,dst=/verify/independent-source/.lake,volume-subpath=independent-source/.lake \
  --mount "type=bind,src=$project_root/verification,dst=/extension,readonly" \
  --mount "type=bind,src=$out,dst=/out" \
  -w /verify/independent-source --entrypoint /bin/bash concentration-aware-ns:checker \
  -c 'set -eu
    export PATH=/verify/toolchain/bin:$PATH
    export LEAN_NUM_THREADS=2
    cat /extension/SupportHoleAssembly.lean > /tmp/SupportHoleAssemblyWithAudit.lean
    printf "\n#print axioms ConcentrationAware.coordinateEta_margin_of_euclidean_ball\n" >> /tmp/SupportHoleAssemblyWithAudit.lean
    printf "#print axioms ConcentrationAware.transverse_radius_le_of_euclidean_ball\n" >> /tmp/SupportHoleAssemblyWithAudit.lean
    printf "#print axioms ConcentrationAware.axial_deviation_le_of_euclidean_ball\n" >> /tmp/SupportHoleAssemblyWithAudit.lean
    printf "#print axioms ConcentrationAware.cusp_ball_point_in_physical_exterior\n" >> /tmp/SupportHoleAssemblyWithAudit.lean
    printf "#print axioms ConcentrationAware.selected_velocity_germ_of_cusp_ball_point\n" >> /tmp/SupportHoleAssemblyWithAudit.lean
    printf "#print axioms ConcentrationAware.selected_axis_center_small_eventually\n" >> /tmp/SupportHoleAssemblyWithAudit.lean
    printf "#print axioms ConcentrationAware.selected_velocity_germ_on_cusp_tube\n" >> /tmp/SupportHoleAssemblyWithAudit.lean
    printf "#print axioms ConcentrationAware.exists_admissible_cusp_radius\n" >> /tmp/SupportHoleAssemblyWithAudit.lean
    printf "#print axioms ConcentrationAware.cusp_ball_eventually_in_endpoint_neighborhood\n" >> /tmp/SupportHoleAssemblyWithAudit.lean
    printf "#print axioms ConcentrationAware.selected_cusp_ball_actual_hessian_rate\n" >> /tmp/SupportHoleAssemblyWithAudit.lean
    lake env lean /tmp/SupportHoleAssemblyWithAudit.lean > /out/lean.log 2>&1
    cat /out/lean.log'

python3 - "$project_root" "$out" <<'PY'
import hashlib
import json
import pathlib
import re
import subprocess
import sys

root, out = map(pathlib.Path, sys.argv[1:])
source = root / "verification/SupportHoleAssembly.lean"
log = out / "lean.log"

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

image = subprocess.check_output(
    ["docker", "image", "inspect", "concentration-aware-ns:checker", "--format", "{{.Id}}"],
    text=True,
).strip()
text = log.read_text()
declarations = (
    "ConcentrationAware.coordinateEta_margin_of_euclidean_ball",
    "ConcentrationAware.transverse_radius_le_of_euclidean_ball",
    "ConcentrationAware.axial_deviation_le_of_euclidean_ball",
    "ConcentrationAware.cusp_ball_point_in_physical_exterior",
    "ConcentrationAware.selected_velocity_germ_of_cusp_ball_point",
    "ConcentrationAware.selected_axis_center_small_eventually",
    "ConcentrationAware.selected_velocity_germ_on_cusp_tube",
    "ConcentrationAware.exists_admissible_cusp_radius",
    "ConcentrationAware.cusp_ball_eventually_in_endpoint_neighborhood",
    "ConcentrationAware.selected_cusp_ball_actual_hessian_rate",
)
normalized = re.sub(r"\s+", " ", text)
expected_axioms = "depends on axioms: [propext, Classical.choice, Quot.sound]"
printed = re.findall(r"'([^']+)' depends on axioms:", normalized)
if (
    "error:" in text
    or "sorryAx" in text
    or tuple(printed) != declarations
    or normalized.count(expected_axioms) != len(declarations)
):
    raise SystemExit("Lean compile or axiom audit did not pass")
result = {
    "status": "PASS",
    "scope": "Pinned Lean elaboration and axiom audit of Euclidean-ball coordinate bounds, non-vacuous margin/radius choice, local germ equality throughout a shrinking cusp ball, uniform entry of the entire moving ball into endpoint neighborhoods, and transfer of the upstream full-spacetime Hessian rate onto that ball.",
    "upstream_repository": "https://github.com/openai/NavierStokesAndEuler",
    "upstream_commit": "f9e8bc5b38b6e212696e8a30e3e91517af887bbd",
    "mathlib_commit": "85e3a25e006c35636f0e53b0e9296caca2685bc0",
    "lean": "4.34.0-rc2",
    "checker_image_id": image,
    "source_sha256": sha(source),
    "lean_log_sha256": sha(log),
    "declarations": list(declarations),
    "permitted_axioms": ["propext", "Classical.choice", "Quot.sound"],
    "limitations": [
        "For every fixed eta in (-1,1), an admissible positive radius and eta margin exist; the terminal-time interval remains existential and parameter-dependent.",
        "The Hessian result is a full-spacetime jet bound with existential constants/terminal interval; it does not establish a finite-size packet comparison or a theorem at the singular endpoint.",
        "The result does not imply particle alignment, a phase transition, molecular determinism, or reduced viscosity.",
        "It is not a particle ensemble, molecular model, numerical solver validation, or independent review of the upstream construction."
    ],
}
(out / "manifest.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
PY
