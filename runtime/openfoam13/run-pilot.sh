#!/bin/sh
set -eu
# Invoke from repository root; generated case must not already exist.
python3 -m tools.openfoam_case work/of13-pilot
uid=$(id -u)
docker run --rm --entrypoint /bin/bash \
  -v "$PWD/work/of13-pilot:/case" concentration-aware-ns:of13 \
  -c 'useradd -o -u "$1" -m runner && su runner -s /bin/bash -c "source /opt/openfoam13/etc/bashrc && cd /case && blockMesh > log.blockMesh 2>&1 && foamRun > log.foamRun 2>&1"' -- "$uid"
