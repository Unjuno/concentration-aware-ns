#!/bin/sh
# Requires the separately prepared cans-lean-updated source volume.
# Input acquisition and configuration are recorded in evidence/upstream-refresh.
set -eu
if docker inspect cans-updated-build >/dev/null 2>&1; then
    echo 'Existing cans-updated-build container found; inspect it instead of starting a duplicate.' >&2
    exit 1
fi
docker run --rm --name cans-updated-build --user 501:20 --network none \
  --cpus=2 --memory=6g \
  --mount type=volume,src=cans-lean-updated,dst=/updated \
  --mount type=volume,src=cans-lean-verification,dst=/verify,readonly \
  -w /updated/source --entrypoint /bin/bash concentration-aware-ns:checker \
  -c 'export PATH=/verify/toolchain/bin:$PATH; export LEAN_NUM_THREADS=2; lake build NavierStokes.ActualCandidateAssembly'
