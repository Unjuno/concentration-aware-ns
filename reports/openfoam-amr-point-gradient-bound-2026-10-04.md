# Point-interpolating gradient-error obstruction — 2026-10-04

The four archived final AMR fields now have a reconstruction-independent gradient
error lower bound under a **point interpolation and regularity** condition.
It uses exact decoded cell centres and stored velocity vectors, not a hypothesis
that the finite-volume unknowns are exact cell averages. At n64 the relative
peak-of-gradient-error lower bound is **46.1968%**, rounded down from the exact
rational interval endpoint. This is a conditional continuum result, not an
unconditional solver quality verdict.

## Condition and derivation

Let u be the analytic N=3 reference at exact decimal time 0.05. Let w be any C1
vector field on the convex cube containing the two selected points a,b, with
w(a)=Ua and w(b)=Ub, using the decoded stored point coordinates and velocities.
For e=w-u and d=b-a, the fundamental theorem along the segment gives

```text
e(b)-e(a) = integral_0^1 grad(e)(a+s*d) d ds
||grad(e)||_infinity,F >= ||(Ub-u(b))-(Ua-u(a))||_2 / ||b-a||_2.
```

The same bound applies to a W1-infinity field using its Lipschitz representative.
H1 alone does not supply these point values in three dimensions. No average,
cell-copying, Fourier interpolation or canonical dyadic-coordinate substitution
is imposed. The selected points are inside the reference cube, so their segment
stays inside. Coordinates and velocities are decoded to exact binary rationals;
Arb at 96 bits encloses the analytic point values, numerator and distance. The
ratio divides the numerator lower endpoint by the distance upper endpoint.

The analytic reference peak obeys
`||grad(u)||_infinity,F <= exp(-0.05)*sqrt(86/81)` using the already audited
bounds on the envelope and its first two derivatives. Dividing the absolute
lower endpoint by this peak's upper endpoint gives the relative lower bound.
This denominator may overestimate the actual reference peak, which makes the
result conservative. The independent point formula uses g(q)=cos(q/2)^8 and
g'(q)=-4*cos(q/2)^7*sin(q/2), checked against the Fourier evaluator.

## Results

| Original case | Witness CSV rows | Absolute peak-error lower | Relative peak-error lower |
| --- | --- | ---: | ---: |
| n16, dt=0.001 | 1, 4103 | 0.769199 | 78.4778% |
| n32, dt=0.001 | 116787, 116788 | 0.790197 | 80.6201% |
| n64, dt=0.001 | 868774, 868775 | 0.452797 | 46.1968% |
| n32, dt=0.0005 | 37487, 37488 | 0.778899 | 79.4674% |

All quoted lower numbers are rounded down. Exact rational endpoints and full
point/value witnesses are in [analysis.json](../evidence/amr-point-gradient-bound-v1/analysis.json).
The floating search examines six nearest neighbours for each point and selects
one pair per case. This does not claim the best possible pair or a global
maximum. The enclosure of the chosen pair is independent of the search's
floating slope estimate. The source manifest, twenty frozen input files,
original protocol, archive hashes and every member hash are checked before
reading the final postSolve snapshot.

Each bound exceeds the previously disclosed 5% **peak-of-field-error** comparison
target in this stated interpolation scope. That metric differs from an error
in the numerical peak value alone. The original acceptance gate is unchanged.
In particular, a small stored native Gauss tensor error does not contradict
this bound: that discrete tensor is not established as the derivative of every
continuous field interpolating the stored velocity points.

## Interpretation limits

This complements the [nominal-mean certificate](openfoam-amr-arb-mean-certificate-2026-10-04.md)
with a different condition. The [initialization audit](openfoam-amr-input-representation-2026-10-04.md)
confirmed centre-valued inputs, but does not prove the evolved solver field has
a particular C1 point-interpolating reconstruction. That contract remains
unestablished. These lower bounds therefore do not demonstrate an upstream
implementation defect or transfer automatically to a claimed OpenFOAM continuum
solution. No new issue is justified solely by this result.

A solenoidal assumption does not turn this pointwise gradient lower bound into
a pointwise curl lower bound. The integrated gradient/curl identity used in
other H1 arguments cannot be reused for this infinity-norm conclusion. No curl
certificate is reported. Nor do these results prove asymptotic nonconvergence,
a singularity, molecular alignment, phase transition or viscosity reduction.

## Executed verification and reproduction

Numerical source: `3711beb25d67daff4a04104b5ba983e2b4c98d5b`.
Original CFD source: `3566f89058071910a41bb68010eb258c7bbc3d74`.
Three controls verify the independent point formula, a known linear error's
chord slope and rejection of coincident points. The complete locked benchmark
suite passes **311 tests, 1 skip, 83 subtests**. Compile checks and
`git diff --check` pass.

A selected Git export, without .git, reruns the complete four-case audit with
Python process/network/Git-open guards. All imported tools modules resolve
inside that export and no blocked attempt occurs. The analysis JSON reproduces
byte-for-byte. This uses external SHA-verified raw archives and the same host's
locked dependencies; it is not a separate CFD run or whole-history replay.
Evidence and replay wrapper are in [the package](../evidence/amr-point-gradient-bound-v1/README.md).

Download the original raw archives from the
[release](https://github.com/Unjuno/concentration-aware-ns/releases/tag/of13-amr-mean-quality-v1-3566f89)
and build the four-case JSON archive map. At the numerical source commit run:

```bash
uv run --python /opt/homebrew/bin/python3 --with-requirements requirements-verification-locked.txt \
  python -m tools.audit_amr_point_gradient_bound \
  --raw-map /absolute/path/raw-map.json --output /absolute/path/new-result \
  --source-commit 3711beb25d67daff4a04104b5ba983e2b4c98d5b
```

Next obligations include identifying or validating an upstream-relevant
reconstruction, controlled input/forcing representation comparisons, remaining
solver quality studies and analytic/physical interpretation. The full goal
stays open.
