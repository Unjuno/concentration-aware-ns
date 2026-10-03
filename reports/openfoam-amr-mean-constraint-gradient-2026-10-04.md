# Native-mean constraints and continuous gradient accuracy — 2026-10-04

A reconstruction-independent analytic inequality now links archived cell-mean
errors to continuum gradient error. For final n64, its floating evaluation gives
relative gradient L2 lower bound 47.1269% and relative peak-of-gradient-error
lower bound 5.4030%. The inequality holds for every periodic H1 reconstruction
whose exact native-cell averages equal the archived numerical values, interpreted
as nominal finite-volume means. It does not select a particular interpolant.

This is conditional evidence about a defined mean-conservation requirement.
It is not an outward-rounded numerical certificate, an original acceptance-gate
verdict, an OpenFOAM contract violation or a physical singularity claim. The
old finite-band polynomial's 0.5023% gradient L2 error and 0.8353% peak-error
upper formula remain valid for that polynomial, which does not preserve these
native averages. These statements concern different field constraints.

## Reconstruction-independent derivation

Let u be the known smooth periodic MMS, w any periodic H1 velocity with the
prescribed native cube means, and e=w-u. Let P_K be the orthogonal L2 projection
onto constants on the actual native cells. Then a=P_K e is known from the
archived numerical values minus independently integrated exact MMS cell means.
Set a0=a-mean(a). With normalized torus inner products,

    <e,a0> = ||a0||_2^2.

Indeed each native cell integral of e equals its volume times its prescribed
mean error; projection preserves the whole-domain mean. Periodic Fourier
Cauchy–Schwarz, excluding k=0, therefore gives

    ||grad e||_2 >= ||a0||_2^2 / ||a0||_H^-1,
    ||a0||_H^-1^2 = sum_(k!=0) |a_hat_k|^2 / |k|^2.

The native geometry is the validated ideal periodic dyadic partition; floating
archived coordinates and volumes are checked against it. Numerical evaluation
of those coordinates and MMS means is not outward-rounded.

The test field a is P0 and need not be H1; its H^-1 norm is finite. This does
not take an ordinary derivative of the discontinuous test field. Finest-voxel
repetition preserves a for analytic integration only. The unknown error e is
not required to be constant, or to have copied finest-voxel means.

For B_C={k:|k_j|<=C}, analytic native-cube integrals recover all coefficients in
B_C, while Parseval recovers the entire outside L2 mass T_C. Every outside mode
has |k|^2>=(C+1)^2. Thus

    ||a0||_H^-1^2 <= sum_(k in B_C, k!=0) |a_hat_k|^2/|k|^2
                        + T_C/(C+1)^2 = U_C.

The computable lower bound is ||a0||_2^2/sqrt(U_C). Increasing the measured cube
7 -> 31 -> 63 tightens U_C in every state. Modes beyond the voxel Nyquist are
allowed: coefficients are analytic P0 cell integrals with the physical mode's
sinc/phase, not an aliased finite-spectrum interpretation.

Normalize by ||grad u||_2 for the relative L2 lower bound. Since the domain
measure is normalized, sup |grad e|>=||grad e||_2. Dividing the absolute lower
bound by an independent upper bound on sup |grad u| gives a relative
peak-of-error lower bound. The reference upper formula uses its exact finite
Fourier support and a complete 64^3 periodic grid plus the previously verified
Lipschitz covering-radius estimate. Gradient norms are Frobenius norms.
The peak metric is sup |grad(w-u)| / sup |grad u|; it is not the difference
of separate gradient maxima.

If w is also divergence-free, e is divergence-free and periodic, so
||curl e||_2=||grad e||_2. The same absolute L2 lower bound then applies to
curl error. Without that additional assumption it is a gradient bound only.

## Archived native constraints

Final-state bounds below use C=63. All twelve states and all three cutoffs
are saved, including their complete tail masses, H^-1 estimates, constant-mode
removal and reference normalizations.

| Case | Gradient relative L2 lower formula | Gradient relative peak-error lower formula |
|---|---:|---:|
| n16-dt0.001 | 113.5310% | 13.0160% |
| n32-dt0.001 | 112.3721% | 12.8831% |
| n64-dt0.001 | 47.1269% | 5.4030% |
| n32-dt0.0005 | 110.4545% | 12.6633% |

For n64/postSolve, C=7,31,63 gives relative gradient L2 lower formulas
9.2355%, 31.9396%, 47.1269%. For n64/preMap, the C=63 result is only 0.5570%;
immediately after parent copying it is 118.4183%. This does not contradict
unchanged P0 values or spectrum at the map. Splitting a native cell and
interpreting each child value as its exact mean imposes additional constraints
on any H1 field. The projection P_K e and its error constraints change even
when the represented P0 velocity does not. No continuum velocity jump or
physical singularity is inferred.

The final finer-grid result improves substantially. Halving dt at n32 changes
the result modestly. Neither establishes an asymptotic solver convergence
failure. These are fixed archived nominal-mean constraints, not a theorem about
every discretization or every simulation.

## An explicit mean-preserving operator and its independent control

Separately construct R(v) as a real trigonometric polynomial whose finest-voxel
averages equal copied native constants. With m=2n and |k_j|<=m/2,

    r_k = F_(k modulo m) exp(-i*pi*sum(k)/m) / product sinc(k_j/m).

Each Nyquist coordinate contributes an additional factor 1/2 at both signs,
selecting a real symmetric representative. These symmetric modes reconstruct
all imposed voxel means exactly; summing those means preserves every native
cell mean. The extra child means inside unrefined native cells are imposed
constraints, not actual measured subcell values. R is a chosen analysis
operator, not an OpenFOAM interpolation or executed CFD correction.

The complete polynomial spectrum, rather than a low band alone, yields:

| Final case | R velocity L2 error | R gradient L2 error | R curl L2 error | Exact-native-mean control gradient | Control curl |
|---|---:|---:|---:|---:|---:|
| n16-dt0.001 | 38.9878% | 158.7982% | 147.8255% | 0.9432% | 0.8063% |
| n32-dt0.001 | 20.1262% | 175.8965% | 158.6751% | 2.5653% | 2.1325% |
| n64-dt0.001 | 5.9167% | 107.6343% | 97.3415% | 3.8968% | 3.2128% |
| n32-dt0.0005 | 19.8797% | 173.7622% | 157.6391% | 2.5653% | 2.1325% |

The actual polynomial satisfies the reconstruction-independent lower bound in
every state. Mean preservation alone is not enough for derivative consistency:
preMap exact-mean controls have large derivative errors, while post-AMR exact
native means improve their control substantially. At final n64 the exact-mean
control gradient/curl errors are 3.8968% / 3.2128%, versus actual 107.6343% /
97.3415%. The difference is measured in this particular operator; the universal
bound above uses only native constraints and avoids its extra voxel constraints.
All four actual preMap/mapped full coefficient arrays have identical hashes.

## Exact smooth shear counterexample for the repetition operator

Take the periodic smooth shear u=(0,sin x,0). It is divergence-free and can be
a steady manufactured solution with pressure zero and forcing nu*u for any
positive constant nu. Its exact coarse means on n cells are copied to two
fine voxels per cell. Write alpha=pi/(2n). Direct integration gives

    R_n u_y = cos(alpha)^2 sin x + (n-1) sin(alpha)^2 sin((n-1)x).

Both the low and alias terms are necessary for the imposed two child averages;
their coarse average adds back to the original exact mean. Orthogonality gives

    relative velocity L2 error = sin(alpha)^2 sqrt(1+(n-1)^2) -> 0,
    relative derivative L2 error = sin(alpha)^2 sqrt(1+(n-1)^4)
                                  -> pi^2/4 ~= 2.4674.

Thus this chosen sequence converges in velocity L2 while its derivative error
does not vanish. The smooth reference remains bounded; the alias is created
by the imposed repeated child averages. This is a reconstruction-consistency
counterexample, not a theorem that the OpenFOAM solver is nonconvergent.
A different reconstruction of the original coarse means need not have this
limit. Tests verify the full three-dimensional coefficients at n=16,32,64,
independent native cube integrals, Nyquist modes and uniform resolved MMS means.

## Validation, disposition and remaining work

The explicit R audit is frozen at `6819ed429172ce37713ab16a9c17b10a3cc301a7`;
the lower-bound audit at `5abbe08e7d6488f1f23dfea0a83f8d2f34e8fc17`. Input
CFD source remains `3566f890`; all raw archive/member and twenty input source
identities are checked before measurement. A selected `5abbe08` source export replays
both complete analysis JSON files byte-for-byte under Python-level process,
network and Git-open guards. Its reconstruction files match the earlier
`6819ed4` source blobs; no CFD or entire historical replay is claimed. The C=7 n64 pilot preceded the
lower-bound protocol and is disclosed; these are not blind prospective gates.
There is no newly chosen solver threshold. Seven new analytical tests and the
full locked suite pass 292 tests, one skip and 83 subtests. The separate earlier
R-source suite has 289 tests; both logs are preserved with their own source pins.

Maximum voxel-average round-trip difference is 1.67e-16; selected native cube
integrals (up to 2104 cells per state) differ by at most 7.78e-15. Direct curl
and divergence norms independently satisfy the gradient decomposition.
The H^-1 formula tests use a known smooth error and an independent 100001-term
one-dimensional alias series; constant mean removal and refinement monotonicity
are exercised. Detailed hashes, commands and replay status are in
[`mean-preserving evidence`](../evidence/amr-voxel-mean-reconstruction-v1/README.md)
and [`lower-bound evidence`](../evidence/amr-mean-gradient-lower-bound-v1/README.md).

Classification: a chosen-reconstruction limitation, a conditional analytic
obstruction under native-mean preservation, and an evaluation-procedure gap
when filtered/native discrete derivatives are interpreted as a mean-preserving
continuous gradient. No new implementation bug is established. No new upstream
issue is warranted: the construction is our analysis operator, and no inspected
upstream contract guarantees an exact-mean H1 reconstruction with these continuum
errors. Publish the result in the benchmark PR, preserve existing upstream
reports, and require a declared reconstruction/constraint meaning in future gates.

These numerical formulas lack interval-certified rounding and are conditional
on the archived values' nominal-mean interpretation. The necessary-condition
formula is not fed into the original gate as a certified bound. Original full
AMR quality, SU2, PhysicsNeMo, proof/physical interpretation and the overall goal
remain open. No blow-up, molecular ordering, phase transition or viscosity
change follows from these errors.
