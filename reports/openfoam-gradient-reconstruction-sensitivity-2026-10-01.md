# OpenFOAM gradient reconstruction sensitivity — descriptive

This postprocessing audit reopens the six archived high-gradient Foundation 13 cases and checks their archive hashes against the current manifests. It compares the frozen centered-FD2 peak errors with peak errors from the real trigonometric interpolant through the same cell-center velocity samples. The spectral values are counterfactual diagnostics; the frozen gates are unchanged.

| Case | Frozen status | FD2 grad / vort peak error | Trigonometric grad / vort peak error | Counterfactual status |
|---|---|---:|---:|---|
| n16-dt0.001 | PASS / FAIL | 37.0246% / 33.5343% | 2.7380% / 0.7598% | FAIL |
| n32-dt0.001 | PASS / FAIL | 10.2807% / 9.1799% | 0.4651% / 0.0447% | PASS |
| n64-dt0.001 | PASS / PASS | 2.6404% / 2.3488% | 0.1192% / 0.0143% | PASS |
| n128-dt0.001 | PASS / PASS | 0.6631% / 0.5890% | 0.0284% / 0.0055% | PASS |
| n64-dt0.0005 | PASS / PASS | 2.6417% / 2.3500% | 0.1206% / 0.0130% | PASS |
| n64-dt0.00025 | PASS / PASS | 2.6424% / 2.3506% | 0.1213% / 0.0124% | PASS |

The n=32 row changes from frozen local-quality FAIL to counterfactual PASS because velocity, energy and shell-spectrum metrics already pass while both derivative-peak errors fall below 5% under the trigonometric reconstruction. The adequate n=64 and n=128 spatial rows remain PASS under both calculations, so the frozen matrix-level classification is unaffected.

At n=32, the gradient-field relative L2 error on the sample nodes is 9.533% for FD2 and 1.924% for the trigonometric derivative; the corresponding vorticity-field errors are 9.140% and 0.168%. The sampled gradient-peak index changes FD2 [1, 31, 0] → trigonometric [2, 0, 0], while the analytic-reference sampled maximum is at [25, 0, 31]; vorticity indices are FD2 [2, 0, 0], trigonometric [2, 0, 0], reference [25, 0, 31]. These are discrete argmax locations (possibly among ties), not certified locations of continuous extrema.

This is reconstruction sensitivity, not proof that either derivative is the uniquely correct continuous solver field. Both peak comparisons are finite-node maxima; the exact reference is evaluated at the same cell centers, and no continuous intersample supremum is bounded. The audit does not establish a code defect or physical instability.

Machine-readable values, run archive hashes and limitations are in `evidence/tests/openfoam-gradient-reconstruction-sensitivity-2026-10-01.json`. Reproduce with `python -m tools.audit_openfoam_gradient_reconstruction` after installing the repository verification requirements.
