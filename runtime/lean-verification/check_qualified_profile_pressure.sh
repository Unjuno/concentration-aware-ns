#!/bin/sh
# Replays the pressure-qualified re-selection through complete profile assembly.
set -eu
project_root=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
docker run --rm --name cans-qualified-profile-pressure --user 501:20 --network none \
  --cpus=2 --memory=4g \
  --mount type=volume,src=cans-lean-verification,dst=/verify,readonly \
  --mount "type=bind,src=$project_root/verification,dst=/extension,readonly" \
  -w /verify/independent-source --entrypoint /bin/bash concentration-aware-ns:checker \
  -c 'export PATH=/verify/toolchain/bin:$PATH; cat /extension/AxisForceSign.lean /extension/QualifiedProfilePressure.lean > /tmp/QualifiedProfilePressure.lean; lake env lean /tmp/QualifiedProfilePressure.lean'
