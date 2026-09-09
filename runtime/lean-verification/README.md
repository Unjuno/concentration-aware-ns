# Independent proof-check environment — preparation in progress

The pinned project's ComparatorChallenges/README.md calls for mathlib cache,
Comparator, landrun, lean4export and nanoda_bin. No successful proof build or
independent check is claimed yet. Preparation is isolated under work/lean-verification.

Source: openai/NavierStokesAndEuler at 8937a8f4cbc7abaab5e9e97d1cc7f5d2319d9538.
Source tar SHA256: e44f67a2bc3c133c14856d73b697f77344b030e3fae2f798254b64dcefbbb772.
Lean: v4.34.0-rc2 Linux aarch64, asset URL/digest in evidence/lean-verification.

The dependency fetcher reads the pinned upstream lake-manifest.json and fetches
all eleven exact revisions as source archives, preserving per-archive hashes.
It creates no Git repositories. Dependencies' own licenses remain applicable.
Lake integration for archive-only packages must be verified before use; this
fetch step does not establish that Lake will build without requesting Git metadata.

`unpack.py` verifies the fixed archive digest before extraction and refuses an
existing destination. Python 3.14 supports the toolchain's Zstandard archive.
Source changes, if any are needed only for package path configuration, must be
recorded separately from the original theorem source. Do not alter proof statements
to obtain a successful check. A Lean build, cache reuse and independent kernel
validation are distinct forms of evidence and must be reported separately.

## Verified archive integration

`use_archive_paths.py` rewrites only the project lake manifest and two direct
requirements in lakefile.toml, preserving upstream backups. Run it after fetching
and unpacking. `check_sources.py` compares every archived Lean source byte with
the extracted copy; evidence/lean-verification/source-byte-check.json records
counts and list hashes. This checks source identity, not theorem validity.

The pinned Lean binary and `lake env lean --version` execute successfully in
the existing SU2 Linux container image. The cache executable also builds.
The initial downstream `lake exe cache get` exits because mathlib compares Git
manifest entries with our path entries. No revision discrepancy is established
by this diagnostic. The dependencies were fetched at their original pins.

Run the built cache from mathlib's own directory under the project's Lake
environment, preserving mathlib's original manifest and cache hash inputs:

```sh
docker run --rm --name cans-lean-cache \
  -e XDG_CACHE_HOME=/verify/cache -e LEAN_NUM_THREADS=2 \
  --entrypoint /bin/bash \
  -v "$PWD/work/lean-verification:/verify" -w /verify/source \
  concentration-aware-ns:su2 \
  -c 'export PATH=/verify/toolchain/bin:$PATH; lake env bash -c "cd /verify/packages/mathlib && .lake/build/bin/cache get"'
```

Upstream Cache/Requests.lean runs the downstream manifest comparison only outside
the mathlib root; Cache/IO.lean identifies that root by its Mathlib directory.
This invocation requires no changes to the cache implementation or Lean sources.
Retrieval and decompression of all 8,747 files completed with exit code zero;
cache-result.json records the log hash. Project type checking and independent
Comparator/kernel checking remain separate outstanding steps. An origin warning is expected for
source archives; the tool reports its official mathlib4 fallback explicitly.

The first project proof build targets `+NavierStokes.ComparatorSolution`, which
imports both R3 and periodic theorem adapters and prints their axioms. It runs
under the same Docker invocation above with `--cpus=2 --memory=10g`, container
name `cans-lean-ns-build`, and final command
`lake build +NavierStokes.ComparatorSolution`. Its log is retained separately
as navier-stokes-build.log. A started build is not a successful check.

## Independent checker preparation

`evidence/lean-verification/checker-archives.json` pins and hashes additional
landrun and nanoda source archives, extracted under work/lean-verification/
checker-sources without Git repositories. Landrun's go.mod requires Go 1.24;
nanoda identifies version 0.4.16 and Apache-2.0 in Cargo.toml. These tools have
not yet been built or executed.

Comparator's pinned README has additional trust preconditions: the challenge
and its imports must be trusted; potentially adversarial solution compilation
must not previously have compromised the checking environment; the process must
not be privileged. The current ordinary proof build is therefore not by itself
an independent Comparator validation environment. Prepare a fresh verified
challenge environment for that stage and record which artifacts are trusted.

The observed OrbStack kernel is 7.0.14-orbstack-00380-ga7e0a2dc9535. Comparator's
README explicitly prescribes restricting AF_UNIX through systemd-run for the
landrun issue it says is fixed in Linux 7.1. A Docker invocation alone does not
establish this condition. Verify an equivalent restriction or the documented
systemd path before claiming the full independent-check guarantees. Do not use
the development fake-landrun wrapper to claim sandboxed validation.

The nanoda release binary built successfully using `cargo build --release
--locked -j 2` in the digest-pinned Rust image recorded in nanoda-build.json.
This is tool compilation only, not a proof check.

The first real landrun filesystem control failed before executing either test:
this pinned landrun requests Landlock ABI v9, but the current kernel provides
ABI v8. Both allowed and denied reads exited at sandbox setup, so this is **not**
a passing denial test. Reproduce with `python3
runtime/lean-verification/check_landrun.py`. Compatibility and AF_UNIX protection
must be resolved before claiming a successful sandboxed Comparator run.

Follow-up: pinned Comparator/Main.lean:81 itself passes `--best-effort` to
landrun. Repeating the filesystem controls with this exact compatibility option
succeeds: the allowed read returns its expected contents and the denied read
fails with Permission denied. Thus the strict-default ABI mismatch is not by
itself a blocker for Comparator's actual invocation. Both results are retained;
run `check_landrun.py --best-effort` to reproduce the compatible control.
This test still does not establish AF_UNIX restrictions or complete isolation.

`no_unix.c` is a Linux aarch64 seccomp launcher for testing denial of AF_UNIX
socket/socketpair syscalls, with no_new_privs inherited across exec. Compile in
the SU2 image with `gcc -Wall -Wextra -Werror -O2 /src/no_unix.c -o /out/no_unix`.
`check_no_unix.py` tests a child process: without the launcher both UNIX socket
operations work; with it both return EPERM, while AF_INET socket creation works.
Results are in no-unix-smoke.json. This is not yet a claim of equivalence to the
Comparator README's systemd restriction: inherited descriptors and alternative
interfaces such as io_uring need consideration before that claim. Keep this
launcher experimental until those conditions and a complete Comparator run have
been checked.

The launcher now closes all inherited descriptors above stderr and rejects socket
stdio. It denies io_uring_setup and pidfd_getfd to limit alternative socket
creation/import paths. Extended positive/negative controls verify that an
explicitly inherited socket is usable without the launcher but closed with it,
and that socket stdin is rejected. The original child socket denial test still
passes. See check_no_unix_extended.py and no-unix-extended.json. These are bounded
controls, not proof against every kernel or sandbox escape.

The first Comparator invocation stopped at `which git` because the SU2 runtime
image does not contain Git. Dockerfile.checker adds that runtime prerequisite;
its build log is retained. Resulting local image ID:
`sha256:0637e54d4b04b0fb3b1eae5829b7616bee43ddb4fa9019628a76219d3466e9de`.
Apt packages are resolved at build time, so this recipe is not a fully pinned
package mirror. No Git repository is created by adding the executable.

`sh runtime/lean-verification/run_comparator.sh` now starts the actual Comparator
challenge build. All sources/dependencies are mounted read-only; only the fresh
project's .lake directory is writable. It runs as UID501, without a network,
under the tested socket-control launcher. Logs distinguish the initial missing
Git failure from the ongoing invocation with Git. A started challenge build is
not a successful comparison or kernel check.

Negative kernel control: copy kernel-smoke/nat.ndjson, parse its JSON lines,
replace the last record's `thm.value` (838) with expression index 0 (Sort 1),
and write nat-invalid.ndjson. Keep the same nanoda configuration except for
export_file_path. The unchanged export checked 52 declarations with zero type
errors; the modified export exits 101 at `src/tc.rs:955` with a failed definitional
 equality assertion. kernel-negative-control.json records the mutation, resulting
file hash and actual stderr. This is rejection of one invalid proof, not a proof
that nanoda has no checker bugs. The crash-style diagnostic is recorded verbatim.

The first with-Git solution build hit `Too many open files` with soft nofile
20,480 (hard 1,048,576). It was explicitly stopped after those errors; its exit
137 must not be interpreted as evidence of an OOM kill. Challenge source hashes
still match the fresh extraction. The runner now requests
`--ulimit nofile=1048576:1048576`; the retry has a separate raised-nofile log.
No theorem rejection or successful kernel verification follows from this failure.
