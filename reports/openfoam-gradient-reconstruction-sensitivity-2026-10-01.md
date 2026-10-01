# OpenFOAM gradient reconstruction sensitivity — descriptive

This postprocessing audit reopens the six archived high-gradient Foundation 13 cases and checks their archive hashes against the current manifests. It compares the frozen centered-FD2 peak errors with peak errors from the real trigonometric interpolant through the same cell-center velocity samples. The spectral values are counterfactual diagnostics; the frozen gates are unchanged.

| Case | Frozen status | FD2 grad / vort peak error | Pure-mode FD2 attenuation | Trigonometric grad / vort peak error | Counterfactual status |
|---|---|---:|---:|---:|---|
| n16-dt0.001 | PASS / FAIL | 37.0246% / 33.5343% | 36.3380% | 2.7380% / 0.7598% | FAIL |
| n32-dt0.001 | PASS / FAIL | 10.2807% / 9.1799% | 9.9684% | 0.4651% / 0.0447% | PASS |
| n64-dt0.001 | PASS / PASS | 2.6404% / 2.3488% | 2.5505% | 0.1192% / 0.0143% | PASS |
| n128-dt0.001 | PASS / PASS | 0.6631% / 0.5890% | 0.6413% | 0.0284% / 0.0055% | PASS |
| n64-dt0.0005 | PASS / PASS | 2.6417% / 2.3500% | 2.5505% | 0.1206% / 0.0130% | PASS |
| n64-dt0.00025 | PASS / PASS | 2.6424% / 2.3506% | 2.5505% | 0.1213% / 0.0124% | PASS |

The n=32 row changes from frozen local-quality FAIL to counterfactual PASS because velocity, energy and shell-spectrum metrics already pass while both derivative-peak errors fall below 5% under the trigonometric reconstruction. The adequate n=64 and n=128 spatial rows remain PASS under both calculations, so the frozen matrix-level classification is unaffected.

For the MMS's streamwise Fourier wavenumber k=4, periodic centered FD2 has derivative symbol gain sin(kh)/(kh), with h=2π/n. At n=32 this single-mode response is 0.900316, a 9.968% attenuation; the full-vector sampled peak errors are 10.281% (gradient) and 9.180% (vorticity). Across n=16/32/64/128, the pure-mode attenuation decreases monotonically with refinement and is close in scale to the measured peak discrepancies, but it does not exactly predict their maxima because those combine vector components and spatial argmax locations.

A direct reference-only FD2 control separates stencil bias from solver-field differences. At n=32, applying the same FD2 operator to the exact sampled MMS already gives peak floors of 9.862% (gradient) and 9.251% (vorticity); the computed FD2 peaks differ from these FD2 reference peaks by only 0.464% and 0.078%. The FD2 derivative-field L2 differences against the reference FD2 fields are 1.928% and 0.128%. Thus most of the >5% n=32 FD2-vs-analytic peak discrepancy is present even with the exact MMS samples; the residual is small but nonzero and remains an observed solver-field difference.

At n=32, the gradient-field relative L2 error on the sample nodes is 9.533% for FD2 and 1.924% for the trigonometric derivative; the corresponding vorticity-field errors are 9.140% and 0.168%. The sampled gradient-peak index changes FD2 [1, 31, 0] → trigonometric [2, 0, 0], while the analytic-reference sampled maximum is at [25, 0, 31]; vorticity indices are FD2 [2, 0, 0], trigonometric [2, 0, 0], reference [25, 0, 31]. These are discrete argmax locations (possibly among ties), not certified locations of continuous extrema.

This is reconstruction sensitivity, not proof that either derivative is the uniquely correct continuous solver field. Both peak comparisons are finite-node maxima; the exact reference is evaluated at the same cell centers, and no continuous intersample supremum is bounded. The audit does not establish a code defect or physical instability.

Machine-readable values, run archive hashes and limitations are in `evidence/tests/openfoam-gradient-reconstruction-sensitivity-2026-10-01.json`. Reproduce with `python -m tools.audit_openfoam_gradient_reconstruction` after installing the repository verification requirements.

The benchmark's next-gate design follow-up is tracked in [issue #5](https://github.com/Unjuno/concentration-aware-ns/issues/5). It preserves the frozen v2 verdicts and proposes reporting the analytic-reference diagnostic separately from a stencil-matched discrete reference; it does not classify this observation as an OpenFOAM defect.

## Successor diagnostic synthetic controls

The issue #5 acceptance criteria also call for a synthetic control separating
stencil bias from an injected field error. The additive diagnostic-only
protocol `protocols/openfoam-derivative-diagnostics-v3.json` specifies periodic
centered FD2 on uniform cell centers, its exact-sample counterpart, and the
continuous-field limitation. It leaves thresholds unset and does not change
the frozen v2 verdicts or request another solver run.

On `u=(sin(4x),0,0)` sampled at 32 cell centers per axis, the identical FD2
operator gives exactly zero computed-versus-stencil-matched-reference
difference while the reference-only analytic-gradient floor is 9.9684%.
Adding the known perturbation `delta_u=(0.01 sin(2y),0,0)` yields a
0.5411961% discrete gradient difference, matching the closed form
`0.01 sin(2h)/sin(4h)` within floating-point tolerance. This confirms the
diagnostic decomposition on these periodic synthetic modes; it does not
validate reconstruction of the actual finite-volume field or certify
continuous extrema. Reproduce with
`python3 -m tools.check_openfoam_fd2_synthetic_controls`; output and source
hashes are in `evidence/tests/openfoam-fd2-synthetic-controls-v3.json`.
