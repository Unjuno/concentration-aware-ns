# Exact global peaks of the manufactured reference field

This is a paper-and-pencil derivation for the benchmark's smooth reference,
not a claim about the OpenAI construction or a machine-checked proof. It sharpens
the previous center-point lower bounds. No CFD or trained-network samples enter
this argument.

Let beta=1/sigma²>0, y=x-(pi,pi,pi), a=(1,2,3), and

    psi(x,t) = exp(-t) exp(beta sum_j(cos(y_j)-1)),
    u = grad(psi) cross a, H = Hessian(psi), m = exp(-t) beta.

We use the Frobenius norm for grad(u) and Euclidean norm for curl(u).

## A nonnegative Fourier representation

The one-dimensional factor has an absolutely convergent Fourier expansion with
nonnegative coefficients. Indeed,

    exp(beta(cos y-1))
      = exp(-beta) exp((beta/2) exp(iy)) exp((beta/2) exp(-iy)).

Expanding both exponentials, the coefficient of exp(iky) is the sum of the
positive terms exp(-beta)(beta/2)^(p+q)/(p!q!) with p-q=k. Their sum is 1 at y=0.
All polynomially weighted sums converge by factorial decay. Taking the product
in three coordinates gives coefficients c_k>=0 and legitimizes differentiating
term by term. Direct differentiation at y=0 gives

    sum_k c_k k k^T = beta I,
    H(y,t) = -exp(-t) sum_k c_k k k^T cos(k dot y).

Thus for every real vector v,

    |v^T H v| <= exp(-t) sum_k c_k (k dot v)^2 = m |v|².

Since H is real symmetric, every eigenvalue lies in [-m,m], so H²<=m² I.
At y=0, H=-m I. These are global bounds for every sigma>0 and finite t.

## Velocity gradient

Let C be the constant linear map v -> v cross a. Then grad(u)=C H.
Since C^T C is positive semidefinite and tr(C^T C)=2|a|²,

    |grad(u)|_F² = tr(C^T C H²) <= 2|a|² m².

Equality holds at y=0. Consequently,

    max_x |grad(u)(x,t)|_F = sqrt(28) exp(-t)/sigma².

## Vorticity

For constant a, curl(grad(psi) cross a)=(H-tr(H) I)a.
If the eigenvalues of H are lambda_1,lambda_2,lambda_3, those of H-tr(H)I
are minus the sums of the other two eigenvalues. Their absolute values are at
most 2m. Hence |curl(u)|<=2m|a|, with equality at y=0, where the matrix is 2m I:

    max_x |curl(u)(x,t)| = sqrt(56) exp(-t)/sigma².

## What this resolves and what it does not

The old center-point bounds are exact global reference maxima for this MMS.
For any reported peak M, its relative discrepancy from the corresponding exact
reference maximum P is |M/P-1|. Evaluating P in ordinary floating point is still
not interval-certified arithmetic.

This removes uncertainty about the *reference* peak location/value. A maximum
over samples of a trained network is still not its continuous maximum; a sampled
finite-difference peak is still a particular numerical diagnostic. This result
does not certify the predicted field between samples, convergence in space/time,
forcing assembly, or optimizer convergence. Existing gate verdicts are not
upgraded automatically. The previously reported one-sided underestimation bounds
remain valid but can be sharpened in a separately regenerated report.
