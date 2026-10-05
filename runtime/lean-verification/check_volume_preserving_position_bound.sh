#!/bin/sh
set -eu

project_root=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
source_file="$project_root/verification/VolumePreservingPositionBound.lean"
source_root=${CANS_LEAN_SOURCE_ROOT:-"$project_root/work/lean-verification/independent-source"}
if [ ! -f "$source_root/lake-manifest.json" ]; then
  echo "prepared pinned Lean project not found: $source_root" >&2
  echo "See runtime/lean-verification/README.md for source and dependency preparation." >&2
  exit 1
fi
(cd "$source_root" && lake env lean "$source_file")
