#!/bin/sh
# Independent comparator run for the separately prepared updated source volume.
set -eu
docker run --rm --name cans-updated-comparator-euler --user 501:20 --network none \
  --cpus=2 --memory=8g --ulimit nofile=1048576:1048576 -e LEAN_NUM_THREADS=2 \
  -e COMPARATOR_LANDRUN=/verify/checker-bin/landrun \
  -e COMPARATOR_LEAN4EXPORT=/verify/packages/lean4export/.lake/build/bin/lean4export \
  -e COMPARATOR_NANODA=/verify/checker-sources/nanoda/target/release/nanoda_bin \
  --entrypoint /verify/checker-bin/no_unix \
  --mount type=volume,src=cans-lean-verification,dst=/verify,readonly \
  --mount type=volume,src=cans-lean-updated,dst=/updated,readonly \
  --mount type=volume,src=cans-lean-updated,dst=/updated/source/.lake,volume-subpath=source/.lake \
  -w /updated/source concentration-aware-ns:checker /bin/bash -c \
  'export PATH=/verify/toolchain/checker-wrappers:/verify/toolchain/bin:$PATH; lake env /verify/packages/Comparator/.lake/build/bin/comparator ComparatorChallenges/Euler.json'
