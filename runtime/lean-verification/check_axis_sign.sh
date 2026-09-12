#!/bin/sh
# Uses the previously provisioned pinned verification volume and checker image.
set -eu
project_root=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
docker run --rm --name cans-axis-sign --user 501:20 --network none \
  --cpus=2 --memory=4g \
  --mount type=volume,src=cans-lean-verification,dst=/verify,readonly \
  --mount "type=bind,src=$project_root/verification,dst=/extension,readonly" \
  -w /verify/independent-source --entrypoint /bin/bash concentration-aware-ns:checker \
  -c 'export PATH=/verify/toolchain/bin:$PATH; lake env lean /extension/AxisForceSign.lean'
