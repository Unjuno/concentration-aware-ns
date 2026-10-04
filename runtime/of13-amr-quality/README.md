# Prospective AMR mean-quality package study

Protocol: `protocols/of13-amr-mean-quality-v1.json`.

Use the frozen official Foundation 13 package recipe under
`runtime/of13-interface-operator/`; the new image is identified after its
fresh build. Fetch the exact Foundation source commit in the protocol and
check every module file hash before instrumenting it. Existing numerical
equations are unchanged. Three callbacks write native gradients and an
independent real-space MMS reference-operator control, all as cell CSVs.
Native tensors are transposed on output to velocity-component-first indexing.

The N=3 extension uses n=16/32/64, plus n=32 at half the time step, to t=0.05.
First mapping occurs at the common physical time t=0.002; maxRefinement is 1.
The n16 case additionally runs the identical compiled module with callbacks
disabled and requires identical final U/p files. Noninterference and source
compatibility are conditions to verify, not existing PASS claims.

The new 2% velocity-mean and 5% gradient/curl-mean tolerances are prospective
engineering accuracy targets. The reference-operator test identifies
underresolution of the declared reconstruction. The P0 projection floor is
reported separately. These gates do not replace the original N=4 peak/spectrum
protocol or certify a continuous numerical field. A gate failure is not an
upstream defect without a separately established contract violation.

Each hosted matrix case uses a fresh owned ARM64 VM, a networking-disabled
solver container and fixed CPU/memory/PID/time limits. The runtime build may
download the same hash-pinned package with bounded resume. Preserve failed
builds, solver logs, snapshot/input hashes, image/module/source identity,
successful raw archives and incomplete outcomes. No unrelated local Docker
or OrbStack resources are changed.

From a clone at the frozen harness commit with the image built and pinned
source present:

```sh
python -m tools.run_amr_mean_quality \
  --case-id n16-dt0.001 --image concentration-aware-ns:of13-amr-mean-v1 \
  --source work/pinned-of13 --work-root work/amr-mean-n16-new \
  --evidence-root evidence/amr-mean-n16-new
python -m tools.analyze_amr_mean_quality --evidence-root evidence/amr-mean-n16-new
```

Both output roots must be new. Exit zero from the analyzer means it completed
the specified analysis; inspect its standard/local/reference gate values.
It can complete successfully while numerical mean quality is FAIL. A missing
run or missing cross-case instrumentation control remains incomplete.

Before any solver run, reproduce the independent uniform reference precheck:
`python -m tools.audit_amr_mean_reference_precheck`. The n32/n64 analytic
reference mean errors pass the prospective gates; n16 is deliberately coarse.
This is neither a native mapped-mesh result nor a solver accuracy claim.

After all four verified analyses, use
`python -m tools.summarize_amr_mean_quality CASE1/analysis.json CASE2/analysis.json CASE3/analysis.json CASE4/analysis.json --output MATRIX.json`.
Missing runs, changed identities, failed instrumentation controls or inadequate
reference reconstruction force UNCERTAIN. Runtime stock library hashes must
match all 167 library payloads independently read from the pinned official deb.
The dynamic loader trace is saved separately from the solver log so its exit
messages cannot be mistaken for missing solver completion.
