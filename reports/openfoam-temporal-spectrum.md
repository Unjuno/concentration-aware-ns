# Fourier localization of the late-time temporal difference

Reproduce with `python3 -m tools.check_openfoam_temporal_spectrum` in the locked
verification environment. This post-hoc diagnostic reads the six previously
validated archives, checks their hashes and uniform periodic cell ordering,
and uses orthonormal 3D FFTs. Radial integer-wave-number bands partition all
modes. Parseval relative defects are at most 2.2e-16.

Let a=U(dt)-U(dt/2), b=U(dt/2)-U(dt/4). The first-order defect is a-2b.
The table gives bandwise log2(||a||/||b||) and the fraction of squared defect
norm in each band, not the fraction of total physical kinetic energy.

| Radial wave number | Baseline order | Control order | Baseline defect fraction | Control defect fraction |
|---|---:|---:|---:|---:|
| 0–4 | 0.9414 | 0.9452 | 1.32% | 1.13% |
| >4–8 | 0.4050 | 0.4194 | 53.03% | 51.97% |
| >8–16 | 0.1913 | 0.1890 | 43.52% | 44.70% |
| >16–32 | -0.3054 | -0.3066 | 2.01% | 2.07% |
| >32 | -0.0689 | -0.0679 | 0.13% | 0.13% |

The middle bands 4<|k|<=16 account for 96.55% of the baseline defect and
96.67% of the projected-initial-field control defect. Low modes are nearer
first-order scaling, whereas the anomaly is not confined to the highest
resolved frequencies. Initial projection leaves this structure largely intact.
This localizes the measured discrepancy; it does not identify a faulty solver
operator, separate temporal from spatial coupling, or prove an asymptotic
order. Negative bandwise orders concern small temporal differences and do not
show instability or blow-up of the physical velocity.

The next mechanism review should examine ongoing pressure/flux correction and
spatial-temporal coupling over these modes, rather than assume the already
suppressed initial impulse or highest-frequency noise is sufficient. Any
operator intervention must retain the original baseline and state whether it
changes the discrete problem. No additional solver run was used here, and all
original acceptance gates remain unchanged.

## Centered-divergence decomposition

Use the verified uniform-grid centered derivative symbol q_j=sin(k_j dx)/dx.
For each nonzero q, split each Fourier vector F into q(q dot F)/|q|² and its
orthogonal complement. Keep the eight all-zero/axis-Nyquist symbol combinations
separate; do not divide by their zero symbol. Squared component norms add to
the original norm within 1e-12 relative, and the transverse symbol divergence
vanishes to roundoff. An independently evaluated real-space centered stencil
agrees with i q dot F within 1e-12 relative for both differences and their
first-order defect. This verifies the array-axis/component correspondence.

| Diagnostic | Original tight baseline | Projected-initial control |
|---|---:|---:|
| Longitudinal fraction of squared first-order defect | 97.4721% | 97.4405% |
| Transverse component observed order | 0.92382 | 0.92552 |
| Longitudinal component observed order | -0.72713 | -0.72490 |

The zero-symbol kernel contributes less than 5e-9 of squared defect norm.
Thus the poor full-vector order is primarily associated with the centered
cell-velocity longitudinal component, while the transverse component is much
closer to first-order scaling. This does not assert failure of face-flux
continuity: the solver's corrected face flux and the centered divergence of
cell velocity are distinct discrete quantities. It motivates analysis of
ongoing pressure/flux correction and cell-velocity reconstruction. Projecting
reported outputs would change the evaluated quantity and cannot retrospectively
turn the original MMS gate into PASS.
