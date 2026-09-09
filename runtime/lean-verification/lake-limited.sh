#!/bin/sh
export LEAN_NUM_THREADS=2
exec /verify/toolchain/bin/lake "$@"
