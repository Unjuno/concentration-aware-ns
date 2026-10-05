#!/bin/sh
set -eu

project_root=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
source_file="$project_root/verification/FinitePacketProbability.lean"
expected_source_sha=3d05e73b1f25b7eaf5e4c0f33f05b374e91d93a692d481bfb7821d5ac631a7da
source_root=${CANS_LEAN_SOURCE_ROOT:-"$project_root/work/lean-verification/independent-source"}

actual_source_sha=$(shasum -a 256 "$source_file" | awk '{print $1}')
if [ "$actual_source_sha" != "$expected_source_sha" ]; then
  echo "FinitePacketProbability.lean hash differs from the audited source" >&2
  exit 1
fi
if [ ! -f "$source_root/lake-manifest.json" ]; then
  echo "prepared pinned Lean project not found: $source_root" >&2
  echo "See runtime/lean-verification/README.md for source and dependency preparation." >&2
  exit 1
fi

tmp=$(mktemp "${TMPDIR:-/tmp}/finite-packet-probability.XXXXXX.lean")
trap 'rm -f "$tmp"' EXIT HUP INT TERM
cat "$source_file" > "$tmp"
printf '\n#print axioms PacketProbability.sublevel_measure_tendsto_zero_atTop\n' >> "$tmp"
(cd "$source_root" && lake env lean "$tmp")
