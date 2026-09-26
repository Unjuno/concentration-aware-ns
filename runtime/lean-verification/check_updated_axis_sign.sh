#!/bin/sh
# Requires a successful updated assembly build; both volumes are read-only.
set -eu
project_root=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
docker run --rm --name cans-updated-axis-sign --user 501:20 --network none \
  --cpus=2 --memory=4g \
  --mount type=volume,src=cans-lean-updated,dst=/updated,readonly \
  --mount type=volume,src=cans-lean-verification,dst=/verify,readonly \
  --mount "type=bind,src=$project_root/verification,dst=/extension,readonly" \
  -w /updated/source --entrypoint /bin/bash concentration-aware-ns:checker \
  -c 'export PATH=/verify/toolchain/bin:$PATH; export LEAN_NUM_THREADS=2; lake env lean /extension/AxisForceSign.lean'
