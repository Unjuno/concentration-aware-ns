# Solid-particle drag branches and viscosity sensitivity — 2026-10-04

The preceding source trace identified carrier interpolation in Foundation 13's `solidParticle` update. Its [pinned implementation](https://github.com/OpenFOAM/OpenFOAM-13/blob/18870c24d21c6b982e2cdec27b2f59738cca5f90/src/lagrangian/solidParticle/solidParticle.C) applies a Reynolds correction only for Re>0.01. This follow-up distinguishes smooth-branch sensitivity from threshold crossing; it is source-linked algebra and Python diagnostics, not an OpenFOAM cloud or trajectory experiment.

## Smooth-branch carrier sensitivity

With fixed positive density/diameter/viscosity, fixed old particle velocity and zero body-force term, write w=Uc-Up, r=|w|, x=dt*Dc and alpha=x/(1+x). The update is Up+alpha*w. On the high-Re branch let z=0.15*Re^p and theta=z/(1+z), where p is the decoded binary64 literal 0.687. The tangential sensitivity is alpha and the radial sensitivity is

    lambda_r = x/(1+x) + p*theta*x/(1+x)^2.

Since 0<p<1 and 0<=theta<=1,

    1-lambda_r = (1+(1-p*theta)*x)/(1+x)^2 > 0.

This extends the earlier frozen-Dc calculation within the stated smooth, body-force-free parameter regime. It is not a global trajectory bound: changing body forces/properties, moving geometry and threshold crossings are separate. Twenty exact rational parameter controls verify the formula and its positive margin.

## Threshold crossing

For the declared synthetic one-dimensional example nu=d=rhoc/rhop=dt=1, Up=0 and gravity=0, the drag coefficient is 18 below the threshold and 18*(1+0.15*Re^p) above it. The decoded-literal real branch limits of the velocity update differ by an Arb128-enclosed **3.14235931376287e-6**. Two adjacent positive Python floats near 0.01 differ by 1.7347e-18 in input and about 3.14236e-6 in output under a source transcription. Continuous-correlation and constant-coefficient negative controls produce changes below 1e-16.

Those two-float quotients are not derivatives: even the constant negative control has a quotient affected by ULP rounding. The result does not show a Navier–Stokes singularity or physical phase transition. It shows that a smooth-branch bound cannot automatically be applied across this piecewise empirical model boundary. No continuity contract has been established or violated, and no source defect is claimed.

An optional standalone C++ transcription failed to compile because Xcode license agreements were not accepted. No license agreement was accepted or privileged command run. Source and failure status are preserved; no native C++/OpenFOAM reproduction is claimed. Python diagnostics and interval algebra remain separate evidence.

## Viscosity is an input, with a conditional drag elasticity

At fixed positive relative speed and geometry in the high-Re branch,

    Dc = C*(nu + 0.15*d^p*r^p*nu^(1-p)),  C=18*rhoc/(d^2*rhop).
    (nu/Dc)*partial_nu Dc = (1+(1-p)*z)/(1+z).

An independent SymPy differentiation gives zero residual for this identity. The relative drag sensitivity lies strictly between 1-p (approximately **0.313**) and 1 for finite positive z, tending toward 1-p as z grows. The low-Re branch has elasticity 1. This is a conditional sensitivity of an existing drag model; it does not derive viscosity from particle positions, lower the supplied nu, or explain molecular alignment. The benchmark's captured gradient/divergence errors do not establish that any simulated particles encounter this branch boundary.

Evidence and decoded-literal/source identities are in `evidence/solid-particle-drag-branches-v1` and the extended `v2` directory. The runnable auditor is `python -m tools.audit_solid_particle_drag_branches --output NEW_DIRECTORY --source-commit ANALYSIS_COMMIT`, numerical source `5d6ec4f`. The full v2 JSON reproduces byte for byte in a selected-source replay with Python process/network/Git-open guards. Environment metadata is explicitly collected before enabling guards because platform discovery invokes a subprocess on macOS; the initial guard rejection is preserved. Scientific calculations are recomputed after the guards are active. This is a same-host replay, not a native sandbox or universal portability claim.

Classification: conditional consumer sensitivity / model-boundary behavior. No new upstream issue is posted because runtime reproduction, novelty and a violated contract are not established. Source-linked formulas, negative controls, Python compilation, exact controls and `git diff --check` pass. Preceding publication 1fc853fa separately passes hosted CI 37156524829 (375 tests, one skip, 89 subtests, v2 analytic equality and scalar recheck), with tested merge/source closure verified. That CI did not execute this new particle-branch auditor. Global consumer/trajectory effects, cross-project transfer and physical constitutive hypotheses remain open; the full goal remains active.
