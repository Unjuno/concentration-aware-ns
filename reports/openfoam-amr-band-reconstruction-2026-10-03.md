# Explicit smooth AMR band reconstruction — 2026-10-03

All twelve archived N=3 states now have derivative diagnostics for a named
smooth velocity polynomial. At final n64, gradient/curl relative L2 errors are
0.5023% / 0.4965%. The continuum peak-error enclosure formulas give
0.3974–0.8353% / 0.4182–0.7699%, evaluated in floating point.
This is an explicit reconstruction measurement, not a complete quality verdict
for the original solver field. The projection discards an outside velocity norm
of 6.1608%; the original P0 global error remains 6.1795%.

## Field and metrics

Define B={k: |k_j|<=7} and w(x)=sum_B c_k exp(i k.x), using the previously
verified analytic P0 cell-integral coefficients. This is the orthogonal Fourier
projection P_B v. It is smooth and periodic. It generally does not preserve
original cell averages, and is not an OpenFOAM interpolation or an executed
solver correction. The MMS reference support lies entirely inside B.

Gradient coefficients are i c_k tensor k, with Frobenius norm; curl coefficients
are i k cross c_k, with Euclidean norm. Their relative L2 error follows Parseval
with normalization (2*pi)^-3 integral. Velocity energy has no factor 1/2.
The peak metric is sup |D(w-u)| / sup |D u|. This is the peak of the error
field, not the difference between two separate field maxima.

For a finite vector/tensor polynomial q=sum a_k exp(i k.x),
L=sum |k| |a_k| bounds its global Lipschitz constant, by the triangle inequality
and |exp(i k.x)-exp(i k.y)|<=|k| |x-y| on a shortest torus displacement.
On the complete m^3 periodic grid, every point is within r=sqrt(3)*pi/m of a
grid point. If S is the sampled maximum, then S<=sup |q|<=S+rL.
Apply this separately to error and reference. The relative enclosure is
S_error/(S_ref+r L_ref) through (S_error+r L_error)/S_ref.
All reference sampled peaks here are strictly positive.

The formula is an analytic bound; the numerical endpoints are floating-point
evaluations without certified outward rounding. They are not passed to the
acceptance gate as rigorously rounded error intervals. Both m=32 and m=64
are above twice the maximum coordinate frequency, so discrete spatial mean
squares agree with Parseval without aliasing. All twelve states pass this
independent grid-versus-coefficient norm check.

## Final-state outcomes

The intervals below use m=64; the complete record also retains m=32.

| Case | Gradient L2 | Gradient peak error enclosure | Curl L2 | Curl peak error enclosure | Longitudinal velocity L2 |
|---|---:|---:|---:|---:|---:|
| n16-dt0.001 | 8.0114% | 6.3274–14.0746% | 7.9277% | 6.6768–12.9113% | 1.0543% |
| n32-dt0.001 | 2.0129% | 1.5835–3.3578% | 1.9910% | 1.6714–3.1118% | 0.2806% |
| n64-dt0.001 | 0.5023% | 0.3974–0.8353% | 0.4965% | 0.4182–0.7699% | 0.0725% |
| n32-dt0.0005 | 2.0159% | 1.5833–3.3936% | 1.9932% | 1.6706–3.1325% | 0.2819% |

All four preMap/mapped diagnostic objects are exactly identical, consistent
with the earlier coefficient identity. Repartitioning a P0 field by parent
copy does not change this polynomial either. The finer fixed-time-step result
improves substantially; halving dt at n32 does not remove the spatial error.
No asymptotic nonconvergence or upstream defect is established.

## Solenoidal consistency

For nonzero k define l_k=k(k dot c_k)/|k|^2; set l_0=0. The polynomial with
coefficients c_k-l_k is the L2-nearest divergence-free polynomial in B.
Its correction norm and the remaining reference error satisfy an orthogonal
Pythagorean identity, independently checked in the output. Curl is unchanged
because k cross l_k=0. A longitudinal perturbation test exercises this identity.
At final n64 the required band correction is 0.0725% of the reference velocity
norm. This is a lower bound on the L2 distance of the original P0 field to any
full divergence-free L2 field, because its measured longitudinal band must be
removed. It is not the full distance: outside longitudinal modes are unmeasured.
The nearest-band diagnostic is not actually applied to the CFD solver.

## Evidence and remaining scope

Numerical source is frozen at `21754518dbecefc3fed8c19badb97f28756ccb26`.
[`Protocol`](../protocols/amr-band-reconstruction-v1.json) records the object,
sampling grids, formulas and limits. Input arrays are the hashed outputs of
[`the preceding P0 spectrum audit`](openfoam-amr-p0-spectrum-2026-10-03.md).
[`Evidence`](../evidence/amr-band-reconstruction-v1/README.md) includes all
12 state records, local tests, source/input hashes and a guarded selected-export
replay. The latter reproduces the entire analysis JSON byte-for-byte. Its first
launch lacked a recursively included requirements file and stopped before
analysis; the failure is retained and excluded from successful validation.

Four new analytical tests cover exact shear peaks, independently differentiated
physical polynomials, longitudinal/curl separation and invalid inputs. The full
locked suite passes 285 tests, one skip and 83 subtests on macOS arm64 Python
3.14.5. No configured linter exists; compileall and whitespace checks pass.

No retrospective threshold or upstream issue is introduced. A prospective gate
for this particular reconstruction needs a frozen definition, numerical rounding
budget and reviewed acceptance evidence. The reconstruction has no outside
modes by definition; discarded P0 mass and its derivatives must not be silently
replaced by zero in an original-field claim. Native Gauss tensors, P0 derivative
distributions and this smooth polynomial are three different objects. Original
AMR quality, other targets and the complete goal remain open. These errors
support no singularity, molecular alignment, phase transition or viscosity claim.
