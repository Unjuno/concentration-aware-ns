# Foundation 13 package interface operator and scalar residual diagnostic

The official ARM64 Foundation 13 package reproduced the preregistered scalar
cyclic-residual prediction on all three grids: a constant-one field with zero
complete matrix residual and physical flux returns native residuals 0.25,
0.125 and 0.0625. The compatible Couette control independently reproduces the
arithmetic-interface FV resistance error and harmonic equilibrium. This is a
stationary scalar operator/diagnostic result, not a full momentum or VoF solve.
The mechanism has public prior discussion; no discovery or universal solver
failure is claimed.

## Frozen run and identity

- Harness/protocol commit: `e6a5b1ad985cdc6ca3c16de5ca8dde650205a8b1`.
- [Hosted ARM64 run 37118442037](https://github.com/Unjuno/concentration-aware-ns/actions/runs/37118442037): build, wmake, all three cases and analysis completed; verified container/process exit zero and all 15 named JSON snapshots.
- Official package: `openfoam13_20260624_arm64.deb`, SHA256 `6da0f6460fbc33c8995cbc97caba52c6cb0342f52ed02ff57530d9d62e9ef360`.
- Fresh image ID: `sha256:2e0f464f40a0b8c73e1d3db0853b85da26c1c87847d6e54b2d1f7384234bf552`. It is distinct from the historic benchmark runtime. Dependency inventory, compiler/build log, actual linked-library paths and hashes are archived.
- Utility binary SHA256: `acb43cd9393705f2a57fcabdc5e32ab2cc1f1ad9ac9d46b843aac44aad4e62c0`.
- Raw archive SHA256: `b3a5cf8e4bc325e77d835d35afd5322e72804bc3f4142f1496a45dcca5bf2cd3`; 106 regular files, 731,442 compressed bytes.

The installed 25 selected source files match both the Debian payload and the
pinned Foundation 13 source. The actually linked `libOpenFOAM.so`,
`libfiniteVolume.so` and `libmeshTools.so` match the three selected payload
hashes. These are byte-identity checks for those files, without reconstructing
how the official libraries were compiled. The image is freshly constructed
from a pinned base/package and recorded apt inventory; an exact future image
rebuild is not claimed.

The previous fixed-commit run `37117700448` stopped during package acquisition
(curl 18, 13,326,066 bytes missing), before compilation/execution. Its raw log
is retained in `evidence/of13-interface-hosted-failure-37117700448/`. The second
recipe resumes bounded partial transfers and checks the same final package
hash. Local containerd blob-read failures remain environment STOP records.
None is classified as a numerical-quality FAIL.

## Model, quantities and observations

The protocol fixes `Nx=16/32/64`, `Ny=Nz=2`, x in [-1,1], unit y/z widths,
mu_left=1, mu_right=100, traction=1, density=1, fixed x walls, translational
cyclic y/z patches, orthogonal Gauss-linear operators and PCG/DIC tolerance
1e-12 with relTol=0. Each coefficient mode starts from the exact nodal shear
`Uy=x/mu_side`. The equation is `-fvm::laplacian(muFace,shear)=0`.
No time advancement, pressure, phase transport or constitutive inference is
included. The continuum traction and numerical coefficients are prescribed.

| Nx | Actual arithmetic flux error to continuum, maximum | Arithmetic PCG final normalized residual | Constant native residual per cell | Constant complete residual / physical flux |
|---|---:|---:|---:|---:|
| 16 | 6.3885539324% | 6.3954e-13 | 0.25 | 0 / 0 |
| 32 | 3.0954012807% | 3.8181e-13 | 0.125 | 0 / 0 |
| 64 | 1.5241119832% | 9.3219e-13 | 0.0625 | 0 / 0 |

The observed arithmetic values match the exact chain within 4.55e-12 in cell
value; complete integrated residuals are below 5.75e-11. Every x-face flux
matches the expected chain within the frozen tolerance. Exact-nodal arithmetic
interface flux is 25.5025 on all grids before the solve; after 13/14/13 PCG
iterations the globally equilibrated flux has the decreasing errors above.
This is the specified arithmetic diffusion coefficient's conditional
interface discretization error, not an automatic implementation defect.
A normalized residual below 1e-12 does not erase that continuum discretization
error.

Harmonic x-face flux differs from continuum traction by at most 4.67e-15.
All three harmonic initial fields already meet the discrete equilibrium and
PCG performs zero iterations. This checks assembled equilibrium and its
unchanged sampled field; it does not demonstrate convergence from a perturbed
initial guess. The independent exact chain/stiffness analysis is in
`reports/incompressible-interface-stress-compatibility-2026-10-03.md`.

Both coefficient modes pass the frozen **specified operator** gate: reference
is the exact discrete chain, and matrix/physical-flux/sign/geometry quantities
agree. This PASS does not mean the arithmetic field has zero continuum error
or that the original smooth 3D/AMR benchmark is complete. The x-normal explicit
transpose correction is zero within its frozen bound and paired divergence
cancels. Individual transverse correction vectors need not be zero; the
estimated kink-adjacent Gauss gradient is not an exact one-sided derivative.

## Native scalar residual and bounded impact

The unit coefficient, constant-one control is assembled without a solve.
The independent full matrix, oriented face balance, saved divergence and
negative-Laplacian matrix flux are exactly zero in the saved numbers. The
native result is exactly `2*h`, h=2/Nx, on every cell. Its difference from
complete `b-Au` equals the sum of saved cyclic boundary coefficients times
neighbour values. The same relation holds before/after both Couette modes to
roundoff, separately from the linear solver's normalized statistics.

Pinned source calls an LDU residual which already includes the cyclic term,
then includes coupled sources again through default `addBoundarySource`.
The scalar solve uses `false` for that source inclusion. The header's short
matrix-residual description does not explicitly define boundary completion;
identifying this diagnostic with the complete system's `b-Au` is the API
interpretation tested here. A maintainer's contract interpretation is not
claimed. Source links/hashes, current 13/14/dev pins, canonical callsite paths
and duplicate search are in
`evidence/upstream-refresh/openfoam-native-residual-source-review-2026-10-03.json`.
Foundation 14 and dev have not been executed by this probe.

The bounded source inventory found no actual no-argument wrapper calls in
8,848 visible local C/H files. Inspected canonical scalar PCG, convergence
control and residual-output paths use their own LDU computation or stored
SolverPerformance. External diagnostic consumers, macros and other paths are
outside that inventory. The result does not establish a defect in their
normal solve or in all simulations.

The [2024 original discussion](https://www.cfd-online.com/Forums/openfoam-programming-development/256831-some-question-about-fvmatrix-residual.html)
already identifies the coupled-source mechanism in OpenFOAM 10 and explicitly
leaves scalar execution untested. Mechanism novelty is therefore not claimed.
No exact official tracker duplicate was identified by bounded searches, but
live Mantis access was incomplete, so absence is unproved. The
[Foundation contribution channel](https://openfoam.org/dev/how-to-contribute/)
uses [Foundation Mantis](https://bugs.openfoam.org/). A possible improvement is to clarify the coupled-source contract and add a
constant-null-mode regression; excluding the duplicate coupled source is a
source-level proposal, without a tested patched-library claim. No new
upstream issue was posted: this report adds the fixed-package scalar reproduction and preserves
its prior-art, contract and tracker-access limits; GitHub is not substituted
for that official channel. Existing two-phase GitHub issue #2 is a separate
full-model observation and was not reproduced here.

## Independent replay and remaining checks

`evidence/of13-interface-operator-v1/` contains the raw archive, process
manifest, original hosted analysis, package/build records, direct face ratios
and archive-only replay. The replayer verifies every archive/source/input
hash, regenerates the frozen three case inputs, checks runtime/payload
identity and independently analyzes all 15 snapshots. It executes no archived
binary or Docker command:

```sh
python -m tools.replay_interface_operator_archive \
  --evidence-root evidence/of13-interface-operator-v1 \
  --source-commit e6a5b1ad985cdc6ca3c16de5ca8dde650205a8b1 \
  --output work/interface-operator-replay-new.json
```

Use the declared Python dependencies and a Git clone with the named commit.
A separate reviewer also checked 106 archive members, 15 snapshots, the
selected payload hashes and complete matrix/face balance independently;
`independent-review.json` records its bounded results.

Linux CPython 3.12 hosted analysis and macOS CPython 3.14 replay have identical
categorical verdicts. Seven derived floating metrics differ, with maximum
absolute difference 1.083e-15; no bitwise numeric equality is claimed across
those platforms. Native constant and source/payload identity results agree.

The e6 Python CI failed three synthetic archive-fixture tests because the
fixture omitted the newly moved recipe's `app/Dockerfile`; the production
archive and its replay succeeded. The fixture has been corrected to include
and check the dynamic recipe. The corrected local suite passes 260 tests, one skip and 57 subtests; its
log/hash are archived. Final hosted CI is a separate publication check. Initial NaN/dimension/shape/before-balance checker gaps were
corrected before production and attacked with hostile controls.

Original AMR-quality, SU2 solver-quality, PhysicsNeMo continuous-field and
actual-profile proof/physical bridges remain open. Nothing here demonstrates
molecular-position certainty, alignment-induced viscosity loss, phase
transition, optical-fluid applicability or continuum blow-up. Goal is active.
