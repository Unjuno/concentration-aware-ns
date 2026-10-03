# Arb certificate for nominal native-mean continuum error — 2026-10-04

All four archived final states now have ball-arithmetic lower bounds for
continuous gradient error under an explicit mean-conservation interpretation.
For n64 the relative L2 gradient error is at least 46.6290%, and the relative
peak-of-gradient-error is at least 7.4621%. If the reconstruction is also
divergence-free, its relative peak-of-curl-error is at least 6.2651%.
Quoted percentages are rounded down from exact rational lower endpoints.
All four cases exclude a 5% peak-error target in this declared scope.

The scope is exact binary64 values decoded from the archived CSV, interpreted
as nominal means on the validated canonical periodic dyadic partition, and
the exact N=3 MMS at time 1/20. It is not the slightly rounded CSV geometry
interpreted as a new exact tiling, nor a bound on unpublished internal solver
values. It does not establish an upstream exact-average contract or change
an original solver gate. Curl exclusion requires a divergence-free H1 field.
The generic H1 peak norm is an essential supremum, agreeing with the ordinary
supremum for smooth reconstructions.

## Continuum alias bound

As in the preceding [H1/H^-1 derivation](openfoam-amr-mean-constraint-gradient-2026-10-04.md),
a=P_K(w-u) is determined by the prescribed native mean errors and a0=a-mean(a).
Then <w-u,a0>=||a0||_2^2, so

    ||grad(w-u)||_2 >= ||a0||_2^2 / ||a0||_H^-1.

Repeating the P0 test field a on finest voxels preserves this test field; no
additional child-average constraints are placed on w. Let m=2n and F_r be
the normalized discrete Fourier transform of these voxel constants. Continuum
P0 coefficients in the alias class k=r+m*l are F_r times center phase and
cube sinc windows. Each class has total mean-square mass |F_r|^2: apply
Parseval to the corresponding unit-modulus piecewise-constant discrete Fourier
basis function. Thus this statement includes infinitely many continuum aliases,
not just the finite FFT's representative modes.

For r!=0, every physical k in its class has |k|>=|wrap(r)|, where each coordinate
of wrap(r) is chosen in [-m/2,m/2). Consequently

    ||a0||_H^-1^2 <= sum_(r!=0) |F_r|^2 / |wrap(r)|^2 = U.

The r=0 class has only the constant physical coefficient: its other aliases
have a zero sinc factor. Removing the mean therefore removes that entire class.
The bound needs no truncation of the unknown continuum tail. This U differs
from the preceding finite-cube estimate and is a little looser for gradient
L2; its complete ball evaluation supplies an arithmetic enclosure.

## Analytic reference peak bounds

Write g(q)=cos(q/2)^8 and b=cos(q/2)^2 in [0,1]. Then

    g'^2=16 b^7(1-b),    g''=2 b^3(7-8b).

The first polynomial has its nonzero maximum at b=7/8, giving
2*(7/8)^7<1. The second has interior critical point b=21/32, with value
(7/2)*(21/32)^3<2, and endpoint values 0 and -2. Thus |g|<=1,
|g'|<=1 and |g''|<=2, verified using exact rational critical values.

For u_x=e^-t sin(Nx) g'(y)g(z)/N^2 and
u_y=-e^-t cos(Nx) g(y)g(z)/N, the squared Frobenius gradient norm separates
into e^-2t [sin(Nx)^2 A+cos(Nx)^2 B], where A<=1+5/N^4 and B<=3/N^2.
For positive integer N, the former bound is larger. Therefore

    ||grad u||_infinity <= e^-t sqrt(1+5/N^4).

The curl separates similarly, using |g-g''/N^2|<=1+2/N^2:

    ||curl u||_infinity <= e^-t sqrt(1+4/N^2+5/N^4).

Both upper bounds are evaluated outward by Arb. Normalize the absolute error
lower bound using these reference upper bounds. Since normalized L2 error is
no larger than its essential supremum, this yields certified relative peak
lower bounds. For divergence-free periodic w and u, gradient and curl error
L2 norms agree; without that assumption the curl conclusion is unavailable.

## Final-state certificates

| Case | Gradient relative L2 lower | Gradient relative peak-error lower | Curl relative peak-error lower, if solenoidal |
|---|---:|---:|---:|
| n16-dt0.001 | 99.1283% | 15.8636% | 13.3190% |
| n32-dt0.001 | 101.9212% | 16.3105% | 13.6942% |
| n64-dt0.001 | 46.6290% | 7.4621% | 6.2651% |
| n32-dt0.0005 | 100.2689% | 16.0461% | 13.4722% |

The threshold comparison uses exact rational 1/20 and exact rational output
endpoints. Both peak lower bounds exceed it in every final state. This is a
disclosed comparison following the earlier floating pilots, not a blind
prospective threshold or a retroactive upgrade of the original gate.
The previous filtered polynomial's small error is not contradicted: it does
not preserve these nominal native means. Native Gauss tensors are also a
different object from an H1 mean-preserving continuous velocity derivative.

## Arithmetic and independent controls

The numerical source is frozen at `4222bd312c7f70768261c9087b2303dae5a7733a`;
[`protocol`](../protocols/amr-arb-mean-certificate-v1.json) fixes four final
states, exact input interpretation, precision and comparison. Arb at 96 bits
encloses exact canonical MMS cube means, input subtraction, three-axis complex
DFT, norms, normalization and square roots. The rational lower/upper endpoints
are saved, with floating values for display only.

Spatial norm and mean calculations independently intersect their Fourier
counterparts. Direct ball DFT sums and a smooth shear exercise the transform
and alias bound. Cube-average tables are compared with the separate analytic
mean implementation. The full locked local suite passes 295 tests, one skip
and 83 subtests. An initial prototype failed when a generic power of a
zero-centred Fourier ball became nonfinite; explicit products corrected that
path before source freeze and before any accepted archive certificate.

A selected Git-directory-free export replays the full four-case analysis JSON
byte-for-byte under Python-level process/network/Git-open guards. Raw archives
remain external SHA-verified data. The [evidence](../evidence/amr-arb-mean-certificate-v1/README.md)
also includes a standard-library rational checker for the scalar chain, which
rejects four corrupted lower-bound variants. That checker does not prove the
FFT enclosures, input interpretation or analytic inequalities by itself.
Arb enclosures are not a formal proof of the library or this implementation.

## Disposition and remaining scope

This certifies a conditional analytic obstruction for the declared native-mean
preservation target and exposes an evaluation-scope gap. No new implementation
bug or upstream software contract violation is established. Publish in the
benchmark PR; no new upstream issue is warranted for our chosen interpretation
and analysis machinery. No CFD or proof was rerun. Only these four final states
are certified; earlier twelve-state floating records remain separate.
Original full acceptance, SU2/PhysicsNeMo continuous-quality obligations,
mathematical/physical interpretation and the whole goal remain open. No physical
singularity, molecular ordering, phase transition or viscosity change follows.
