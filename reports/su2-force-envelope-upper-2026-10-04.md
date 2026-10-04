# Envelope-aware continuous force displacement

For the executed SU2 reference set S=beta*sum(1-cos(d_i)), beta=1/sigma^2.
Then S>=0, psi_0=exp(-S), and sin^2(d_i)<=2*(1-cos(d_i)) implies
|q|^2<=2*beta*S. Also ||diag(r)||F<=sqrt(3)*beta and s=-q.
Let M(a,c)=(a/(c*e))^a, the maximum of S^a exp(-c*S) on S>=0.
Differentiation gives S^(a-1)exp(-c*S)*(a-c*S), with the unique maximum
a/c and vanishing boundary limits. Independent SymPy differentiation has
zero residual for this identity.

The same triangle and cross-product inequalities as the previous bound give

    B_U = sqrt(14*beta/e)
    B_lap = sqrt(14)*sqrt(2*beta)*[2*beta*M(3/2,1)+(5*beta+1)*M(1/2,1)]
    B_L = B_U+nu*B_lap
    B_Q = 14*sqrt(2*beta)*[2*beta*M(3/2,2)+sqrt(3)*beta*M(1/2,2)].

For B_Q the product of the velocity and gradient retains exp(-2*S),
instead of maximizing those factors independently. The Laplacian bound uses
|q|*(|q|^2+5*beta+1)*exp(-S). These bounds hold at every domain point.
Insert B_L,B_Q into the previous temporal identity to obtain the same
continuous-domain force-displacement upper bound with tighter constants.

Arb128 proves a strict reduction for all three archived parameter cases:
upper endpoints are approximately .239437,.119659,.059815 for dt
.001,.0005,.00025. The previous endpoints were 9.69284,4.84400,2.42140.
Corrected floating sample maxima .085052,.042505,.021247 remain smaller,
but samples are diagnostics and not the justification for the bound.
Use the rational upper endpoints, not rounded display values, for certificates.

Evidence is `evidence/su2-force-envelope-upper-v1`; source 3fcdc76.
The prior digest-bound receipt supplies archived sigma/nu/time/input identities.
This is an absolute real-reference bound, not a native solver experiment,
relative acceptance result or endpoint PDE-error bound. Floating rounding,
inner solves and discretization are separate. No threshold changes or upstream
issue is justified. The full goal remains active and hosted CI remains pending.

Additive v2 hardens the evidence chain: reference source identity, exactly the
three unique temporal cases, original archive hashes and all sigma/nu/dt/end
parameters are revalidated before computation. The previous coarse bound is
also freshly recomputed instead of trusting a stored lower endpoint to assert
improvement. Six focused tests pass, including five corrupted-input controls.
The three numeric bound records remain identical to v1. Evidence is preserved
under `evidence/su2-force-envelope-upper-v2`, numerical source 0f2b2f8. This
focused result is separate from the earlier 377-test full-suite result and
pending hosted run; no broader validation is claimed.

Guarded source replay at 5aafc291 exports source, the prior coarse receipt and
all three original archives while excluding the envelope output. Python
process/network/Git-open guards are active during fresh input validation and
calculation. The v2 output is byte-identical; origins, export hash, wrapper and
log are preserved. Same-host dependency reuse and Python audit-hook scope
remain explicit. Hosted CI is still queued, and these new local commits are
not inferred to have passed it.
