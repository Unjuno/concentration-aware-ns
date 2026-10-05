# Analytic checks for the high-gradient MMS

This note records exact continuum identities for the periodic stress field in
`docs/protocol.md`. It is not a solver validation and does not claim a singular
limit, material-particle alignment, or a molecular-scale implication.

Let

```text
chi(y,z) = ((1+cos(y))/2)^4 ((1+cos(z))/2)^4
psi      = exp(-t) chi(y,z) sin(N x)/N^2
u        = curl((0,0,psi)) = (psi_y, -psi_x, 0)
```

For any positive integer `N`, `div u=0` identically. With `p=0` and
`nu=1/100`, define
`f = partial_t u + (u dot grad)u - nu Delta u`; substitution then gives the
forced incompressible Navier--Stokes equation exactly. The hand-coded Fourier
evaluator and direct symbolic differentiation are separately implemented in
`tools/high_gradient_reference.py` and `tools/check_high_gradient_reference.py`.

Since `0 <= chi <= 1` and `|chi_y| <= 2`,

```text
||u||_infinity <= exp(-t) (1/N + 2/N^2).
```

This is a bound, not the exact velocity supremum. At
`(x,y,z)=(pi/(2N),0,0)`, one has `chi=1`, `chi_y=chi_z=0`, and
`chi_yy=chi_zz=-2`. Therefore

```text
|du_y/dx| = exp(-t),
||grad u||_F = exp(-t) sqrt(1 + 4/N^4),
|curl u| = exp(-t) (1 + 2/N^2).
```

The component equality proves `||grad u||_F >= exp(-t)` everywhere as a
continuous-supremum lower bound; the two norm formulas at the selected point
similarly give lower bounds on their continuous suprema. The checker does not
prove these norm lower bounds are sharp global maxima. Thus this family
rigorously separates a velocity upper bound tending to zero from a fixed
positive local derivative lower bound at fixed time, without asserting anything
about a solver or an infinite-`N` physical limit.

Reproduce the symbolic identities and regenerate
`evidence/tests/high-gradient-mms.json` with:

```sh
uv run --with-requirements requirements-verification.txt -- python -m tools.check_high_gradient_mms
```

Cross-check the formula implementation against direct SymPy derivatives and
regenerate `evidence/tests/high-gradient-reference.json` with:

```sh
uv run --with-requirements requirements-verification.txt -- python -m tools.check_high_gradient_reference
```

The saved seeded comparison evaluates `N=4,8,16` at 65 points per case,
including the selected point, and compares velocity, full gradient, vorticity
and forcing. It verifies implementation agreement to the stated floating-point
tolerance; it does not certify compiled solver forcing or any CFD acceptance
gate. For the shared `N=4` case, a separate exact-rational certificate proves
that the selected-point derivative values are the continuous global maxima:
`max |grad u|_F = sqrt(65)/8 * exp(-t)` and
`max |curl u| = 9/8 * exp(-t)`. It reduces the trigonometric expressions to
four bivariate polynomial gaps and verifies that all tensor-Bernstein
coefficients on `[0,1]^2` are nonnegative. This sharpening is specific to
`N=4`; the selected-point values remain only lower bounds for other `N`. See
the [full derivation and coefficient receipt](../reports/high-gradient-global-peaks-analytic-certificate-2026-10-04.md).
