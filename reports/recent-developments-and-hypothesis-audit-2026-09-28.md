# Navier–Stokes developments and hypothesis audit

Initial research date: 2026-09-28; refreshed: 2026-10-01. This note records public-source changes since the OpenAI announcement and relates them to the concentration-aware benchmark. The preprints below are active scholarly work, not settled consensus or a substitute for an independent proof review.

## What OpenAI published

OpenAI's 8 September 2026 announcement and the linked paper describe an analytical construction, accompanied by Lean formalization, for every positive viscosity: a smooth, compactly supported external force and initially resting 3D incompressible flow with bounded kinetic energy but unbounded velocity as a finite time is approached. The repository says this addresses Clay alternatives C and D. It is an existence result for an engineered smooth forcing and a continuum PDE; it is not a numerical CFD solver result, a generic prediction for ordinary flows, or a molecular dynamics calculation. OpenAI says it does not intend to claim the Clay prize. Sources: [announcement](https://openai.com/index/navier-stokes-solution/), [paper](https://cdn.openai.com/pdf/32d9f210-8b73-45e0-91bc-82a30aef8a9a/navier-stokes.pdf), [Lean repository](https://github.com/openai/NavierStokesAndEuler).

The paper's physical sketch is an axisymmetric vortex core with inward swirl and axial outflow, anisotropic contraction, and oscillatory pulses whose momentum flux cancels singular residual terms so that the external force remains smooth. Its continuum equations track velocity and pressure fields, not individual molecules. The paper explicitly says that if the continuum model's velocity becomes infinite, real-fluid modeling must then track particles individually; that is a warning about the continuum model's breakdown, not a particle configuration or molecular probability result supplied by the proof. A continuum singularity does not itself specify how molecules arrange or determine a real fluid's post-cutoff constitutive law. The public repository also documents a separate Comparator challenge workflow for independent checking; a Lean build or proof certificate should be reported with its exact theorem and checker scope, rather than treated as verification of physical interpretation. Sources: [OpenAI announcement, problem description and formalization links](https://openai.com/index/navier-stokes-solution/), [OpenAI formalization repository and Comparator instructions](https://github.com/openai/NavierStokesAndEuler).

## Related forced-Euler result and the local-gradient implication

The same announcement links a separate OpenAI paper proving finite-time breakdown for the **unforced incompressible 3D Euler** equations from smooth compactly supported divergence-free data. Its construction iteratively adds localized oscillatory packets along particle trajectories. In the displayed leading packet, the velocity increment has a factor proportional to `1/k`, while differentiating its phase contributes `k`, leaving a gradient increment of order `alpha` rather than `alpha/k`. Thus small velocity-amplitude error alone cannot certify small gradient error; this gives an analytic, source-specific reason to keep local derivatives as independent benchmark observables. The argument concerns the staged Euler construction, not a claim that arbitrary CFD solutions hide a defect, and it says nothing about Newtonian viscosity or molecular alignment. Sources: [OpenAI Euler paper, §§1–2](https://cdn.openai.com/pdf/315b36cd-ec98-4023-8342-93345194ece1/euler.pdf), [formalization repository](https://github.com/openai/NavierStokesAndEuler).

This related result must not be merged with the forced Navier–Stokes claim: the equations and forcing assumptions differ, and Euler has no viscous stress term. In particular, Euler particle-map volume preservation (`det F=1`) supports only the continuum kinematics in that proof; it is not evidence for molecular ordering, probability concentration, or a viscosity transition. The benchmark remains anchored to its independent manufactured solution rather than attempting to reproduce either singular construction.

## New work after the announcement

- **A numerical/physical follow-up appeared 15 September.** Ramani Duraiswami's preprint recasts the leading-order similarity equations, constructs and verifies a related porous-wall profile solver, and estimates when a real fluid would leave the continuum regime. For its illustrative water scaling it estimates cavitation around a 0.6–1 mm core, far before molecular lengths; in air it estimates compressibility/shock before rarefaction reaches molecular scales. It explicitly says the forced construction does not establish a mechanism reachable in flows normally computed or built, and leaves the unforced engineering equations unchanged. This is a useful physical cutoff analysis, but it is a single preprint with stated approximations: it does not numerically integrate the complete forced Navier–Stokes construction, including the oscillatory stress-realizing annulus and higher-order corrections. The paper marks its inception numbers as order-of-magnitude estimates, dependent on annulus content. Source: [arXiv:2609.17642](https://arxiv.org/abs/2609.17642), [HTML, especially §8](https://arxiv.org/html/2609.17642v1).
- **A conditional regularity theorem appeared 17 September.** Constantin, Ignatova, and Vicol show regularity at the proposed singular point under the construction's stated anisotropic Type-II bounds and an exactly axisymmetric collapsing core, if the force is real analytic in space; they conclude forces for that setup cannot be analytic (or vanish near the singular point under their stated conditions). This narrows a regularity boundary; it does not contradict a merely smooth compactly supported, non-analytic force. Source: [arXiv:2609.20803](https://arxiv.org/abs/2609.20803).
- **A force-density result appeared 9 September and has a revised public version.** The current arXiv v4 for Cao, Chi, and Nie says smooth blow-up-producing forces are dense in the relative time-integrated spatial `H^s` topology for `s < 1/2` on both the torus and whole space, under its stated fixed-viscosity and initial-state assumptions. Their construction starts from OpenAI's example and uses a localized vector potential/cutoff to avoid nonlinear interaction. The earlier separate whole-space record, [arXiv:2609.10269](https://arxiv.org/abs/2609.10269), is marked withdrawn; the authors say it was combined into v3/v4 of [arXiv:2609.10262](https://arxiv.org/abs/2609.10262). Density in a specified topology is not a probability, physical typicality, or smallness in a norm controlling pointwise derivatives. It remains a preprint and is downstream of the OpenAI construction, not an independent physical validation.
- **A new weak-solution search target appeared 20 September.** Petrillo and Glimm formulate positive energy defect on a finite time window for unforced periodic Leray–Hopf solutions and reduce it to a time-averaged lower bound on fine Littlewood–Paley energy flux. They explicitly state that a finite pseudo-spectral computation cannot establish the required Galerkin-uniform ceiling; their 128³/256³ runs are exploratory and fail the scale requirement at the Kolmogorov wavenumber. This is a distinct unforced problem, not a validation of the forced construction or evidence about molecular positions. Source: [arXiv:2609.23868](https://arxiv.org/abs/2609.23868).
- **The physical cutoff study itself reports numerical scope limits.** Duraiswami's preprint computes a leading-order profile and a related porous-wall model, but says it does not integrate the full forced evolution, pulse annulus, or higher-order corrections. It also reports non-converged branches/spectra in parts of its parameter sweep. Its order-of-magnitude water/air estimates therefore inform likely continuum cutoffs, rather than independently validating the entire singular construction. Source: [arXiv:2609.17642](https://arxiv.org/abs/2609.17642), especially §§5–9.
- **A 23 September essay addresses proof legibility, not fluid dynamics.** Alexander Gamburd's arXiv essay discusses how the community should interpret and scrutinize a large machine-produced formal proof. It is a perspective piece; it does not independently audit the Lean development or add a theorem about Navier–Stokes. It reinforces why a certificate, source closure, human-readable argument and physical interpretation need separate evidence. Source: [arXiv:2609.28591](https://arxiv.org/abs/2609.28591).

## Audit of the user's molecular/particle hypothesis

The hypothesis that the continuum alignment result implies molecular alignment, more deterministic particle positions, or a sudden reduction in material viscosity is **not established by the OpenAI theorem or these follow-ups**. The theorem's variables have no molecular positions or probability law. The physical follow-up estimates that cavitation in liquid or compressibility in gas interrupts the continuum regime well before molecular scales in its example. That estimate argues against directly reading particle ordering out of the singular limit. Any molecular claim needs a separate kinetic/statistical model, a justified continuum-to-kinetic matching rule, and independently checked material parameters and observables. The current CFD benchmark cannot infer these from its solver fields.

There is a genuine, narrower alignment result in our analytic work on the selected OpenAI axis trajectory. The checked variational matrix has singular values `Q^(C/2), Q^(C/2), Q^(-C)` with determinant one (`Q=(1-t)/(1-t0)`, `C>0`). Thus an infinitesimal material separation that is not exactly transverse becomes more axial: its transverse-to-axial ratio is multiplied by `Q^(3C/2)`. Under an explicitly imposed isotropic distribution of initial infinitesimal directions, the probability of being within any fixed nonzero angle of the axis tends to one. The variational algebra is Lean-checked and its identification with the nonlinear flow derivative has a classical local proof for each fixed `T<1`; no common finite-packet radius through `t=1` is established. See [`docs/axis-flow-derivative.md`](../docs/axis-flow-derivative.md), [`docs/particle-position-probability.md`](../docs/particle-position-probability.md), and [`docs/axis-packet-bound.md`](../docs/axis-packet-bound.md).

This is a result about **directions of infinitesimal continuum separations**, not molecular orientation or absolute particle positions. Volume is preserved (`det=1`); in the corresponding global affine Gaussian comparison, transverse mass enters a fixed-radius infinite tube while mass in a fixed finite cylinder tends to zero, and peak density stays constant. That Gaussian result is explicitly a linear-model comparison, not a finite-packet theorem for the constructed PDE. Duraiswami's observation that a material particle turns through only a fraction of a revolution per decade concerns its trajectory's angular motion; it neither proves nor refutes the distinct deformation-gradient alignment above. The physical preprint remains a reduced leading-order model, not a simulation of the complete forced construction.

The announcement's continuum equations are also **not a molecular probability model**: a blow-up means a field norm becomes unbounded within the stipulated PDE model. It does not mean the probability of a molecule occupying a location tends to one, nor that an infinite value means particle diameters shrink or particles line up. Such interpretations require new equations and a limiting argument. Separately, the particular physical-cutoff estimates in the porous-wall preprint say water cavitation and air compressibility occur while the similarity correction is still modest, well before the illustrative molecular scale. That cuts against extrapolating its continuum profile to molecular arrangement; it remains a model-dependent estimate and not a measurement of the OpenAI construction.

The 17 September conditional-regularity result has one useful sharper consequence for reading the construction: it identifies spatial analyticity of the forcing as a decisive added hypothesis, and its authors state that compactly supported cutoffs in the OpenAI force violate that hypothesis. Thus smoothness of forcing alone cannot be silently upgraded to analyticity; the paper narrows the theorem's hypothesis boundary without contradicting the announced example. Source: [Constantin, Ignatova and Vicol, arXiv:2609.20803](https://arxiv.org/abs/2609.20803).

## Additional progress: a real but separate molecular-rheology connection

The proposed link from flow organization to changing viscosity has a legitimate
nearby research area, but it is narrower than the singularity hypothesis.
Jadhao and Robbins' published nonequilibrium-molecular-dynamics study of
squalane under elastohydrodynamic lubrication conditions spans shear rates
`10^5–10^10 s^-1`, pressures `0.1 MPa–1.2 GPa`, and temperatures
`150–373 K`. It finds molecular alignment along the flow, but that order
saturates after viscosity has fallen by only about a factor of three; viscosity
then keeps falling, in some regimes by many orders of magnitude, with little
further change in alignment. Their interpretation emphasizes thermally
activated rearrangements in the high-viscosity Eyring regime. This is positive
evidence that molecular structure and apparent viscosity can covary in a
specified complex fluid, and equally useful evidence that alignment alone is
not a universal explanation for a viscosity collapse. [Jadhao and Robbins,
*Tribology Letters* 67, 66 (2019)](https://doi.org/10.1007/s11249-019-1178-3);
[author manuscript](https://arxiv.org/abs/1903.03996).

That observation does not transfer directly to the OpenAI construction. Its
equations prescribe a constant Newtonian viscosity; they contain no molecular
orientation variable, kinetic distribution, temperature equation, or
rate-dependent constitutive law. Also, `||u||_infinity -> infinity` alone is
not a statement that the symmetric strain-rate tensor, local shear rate, or a
material's apparent viscosity follows a particular limit. The quantity to
connect is the deformation history generated by `D=(grad u + grad u^T)/2`
and a separately justified constitutive or molecular model.

A testable successor hypothesis is therefore: *for a specified material and
thermodynamic path, does the local strain-history from a resolved continuum
flow predict changes in molecular orientation statistics and stress-derived
apparent viscosity before the continuum model reaches its physical cutoff?*
The minimum observables would be an orientation order parameter, pair
separation/deformation statistics, shear stress, apparent viscosity, local
temperature and pressure, plus a continuum-validity measure. The comparison
must use a matched molecular or kinetic model and a fixed-viscosity control.
The OpenAI proof and current CFD benchmark supply none of those molecular
measurements, so this is a new multiscale research direction rather than a
result already found.

## The light-as-fluid idea, with the discreteness correction

The corrected version of the light hypothesis is physically meaningful:
photons are discrete quanta, while an ensemble of photons can still be
described by a distribution function and, after taking moments and supplying
a closure, by radiation-hydrodynamic fields. Which closure is valid depends on
the transport regime and photon-matter interactions; free-streaming radiation
is generally a transport problem, while an optically thick near-equilibrium
regime admits fluid-like moment closures. [Radiation-hydrodynamics derivation
and photon transport equation, Los Alamos National Laboratory](https://www.osti.gov/servlets/purl/1819126).

There is also an established “fluid of light” literature, but it uses specific
optical systems. For example, experiments model laser propagation through a
nonlinear thermo-optical medium as interacting photons; the effective
photon-photon interaction is mediated by that medium's optical nonlinearity.
[Vocke et al., *Optica* 2 (2015)](https://doi.org/10.1364/OPTICA.2.000484).
That is a valid and interesting fluid analogy with experimentally measurable
collective behavior. It does not make freely propagating vacuum light an
ordinary viscous material fluid, and its governing equations and closure are
not automatically the incompressible Navier–Stokes system in the OpenAI proof.

A well-posed next question is whether a concentration or alignment statistic
can be derived for a chosen radiation-transport or photon-fluid model, with
its interaction mechanism, optical-depth regime, closure, and observable
specified. That would be a separate mathematical/physical track; the current
Navier–Stokes proof contains no photon variables and provides no such
derivation.

There is also a narrower experimental connection to the user's “resistance
falls above/below a speed” intuition. Michel et al. directly measured an
optical analogue of obstacle drag in a nonlinear crystal and observed its
suppression in a low-Mach superfluid regime. Their setup is paraxial and
effectively two-dimensional: intensity, phase gradient, and propagation
distance map to density, velocity, and time. The critical behavior depends on
the nonlinear response, obstacle size/strength, healing length and absorption;
their curves did not collapse to a universal function of Mach number alone.
This is a real threshold-like reduction of optical drag, not a finding that
ordinary liquid viscosity vanishes through molecular alignment.
[Michel et al., *Nature Communications* (2018)](https://pmc.ncbi.nlm.nih.gov/articles/PMC5974130/).

Xu et al. later demonstrated optical rarefaction and dispersive-shock waves,
with a critical-velocity transition to a large-contrast nonlinear periodic
wave in a fiber photon fluid. The governing model is a defocusing nonlinear
Schrödinger equation; neglecting its dispersive quantum-pressure term gives a
gas-dynamics Euler analogy, while the full model remains dispersive. This
offers a concrete comparison—full-wave solution versus reduced fluid model,
tracking phase/intensity gradients and drag or cavitation thresholds—but it
is an optical-analogue study with its own exact reference, not a numerical
realization of the OpenAI forced Navier–Stokes construction.
[Xu et al., *Nature Communications* (2022)](https://pmc.ncbi.nlm.nih.gov/articles/PMC9170689/).

As of this review, the Clay Institute's public statement still describes the
claim as “apparently” settled and says its prize-evaluation process is
deliberately unhurried; it is not an independent mathematical endorsement or
award. [Clay Mathematics Institute, 11 September 2026](https://www.claymath.org/news/navier-stokes-announcement/).

The live OpenAI Lean repository still points to
`f9e8bc5b38b6e212696e8a30e3e91517af887bbd` on 28 September; its latest commit
metadata is dated 10 September. This is a source-version check, not new
independent validation. The public Clay page available in this check has no
later Navier–Stokes evaluation statement than 11 September, although its home
page now notes the 23 September Clay Research Conference. A same-day metadata
refresh found no newer default-branch commit for the pinned OpenFOAM Foundation
13 source (9 June), SU2 master (28 April), OpenAI Lean source (10 September) or
PhysicsNeMo main (22 September). The PhysicsNeMo odd-width issue #2007 remains
open and fix PR #2008 remains open; neither has moved past the states recorded
in the inventory. These are repository and page checks, not a claim that all
project activity or independent review has stopped.

The arXiv search also surfaced the 23 September essay above. It is a new
conversation around the announcement, but does not change the benchmark's
mathematical or physical evidence. The light-as-fluid idea remains grounded in
the older, established quantum-fluid-of-light literature under specific
nonlinear optical or cavity conditions, rather than constituting a new
Navier–Stokes consequence.

The more defensible immediate hypothesis is narrower: ordinary convergence or mean-field acceptance criteria may fail to certify local concentration-sensitive quantities in an under-resolved calculation. That claim can be tested with known smooth solutions, independent derivative/forcing checks, and fixed spatial/time refinement. The new preprints make forcing regularity and topology explicit axes for future controlled cases; they do not justify calling the base solver defective.

## Consequence for the current benchmark

1. Keep the manufactured-solution benchmark independent of the OpenAI construction. Treat the proof as motivation and a mathematical source for later study, not as the benchmark's truth oracle.
2. Finish the n=64 pressure-correction dt triple after Docker is stable. The preserved `dt=0.001` case is forensic-only with unknown container exit and cannot explain the temporal order by itself; its report is in `reports/openfoam-pressure-reconstruction.md`.
3. Add a later, separately frozen test matrix for forcing regularity/smoothness and local concentration metrics, only after proving each reference field, forcing, and discrete derivative independently. Track both weak forcing norms and derivative-sensitive norms so an `H^s`-small perturbation is not mislabeled as small in every physically relevant sense.
4. Keep the SU2 discussion about first-order dual-time MMS source-time semantics separate from the OpenAI proof. On 2026-09-28, Discussion #2890 showed a maintainer's substantive 13 September reply and the author's 26 September BDF2 follow-up; GitHub still labels the Q&A “Unanswered” because no accepted answer is marked. This is engagement, not evidence of an upstream solver defect or an accepted fix.
5. Do not file a new upstream defect report based on the molecular interpretation, the partial n=64 run, or these preprints. The current evidence supports a research limitation and a benchmark direction, not a reproduced software defect.
6. A new Foundation 13 source audit traces the generated force sign through `codedFvModel`, `fvModels().source(U)`, matrix equality/subtraction and Euler `ddt`. It confirms that the coded `source -= V*f` yields positive physical `+f` on the assembled RHS and validates the mock's `-source/V` extraction. The solver remains unrun; see `reports/openfoam-source-sign-audit-2026-09-28.md` and its hashed source manifest.

## Source and interpretation limits

The OpenAI blog/paper/repository are primary sources for what OpenAI claims and formalized. The cited arXiv items are primary sources for their authors' newly posted results, but they remain preprints. The porous-wall study is a separate reduced/leading-order computation, not an independent verification of every step of the OpenAI proof. The public [SU2 Discussion #2890](https://github.com/su2code/SU2/discussions/2890) now has a substantive maintainer reply and an author follow-up, while remaining unaccepted as a Q&A answer. The supplied ChatGPT share page exposed a title but no readable conversation body, so no technical claim from it is relied upon here.

## Refresh since the initial 28 September pass

The source pages were rechecked on 1 October. The current [arXiv:2609.10262
v4](https://arxiv.org/abs/2609.10262) combines earlier torus and whole-space
work: its abstract states relative `L¹_t Hˢ_x` density for `s<1/2` on both
domains, and its whole-space Theorem 4.1 gives thresholds `s<2/q-3/2` for
`q=1,2` (including `s<-1/2` for `q=2`). The prior separate whole-space
record [arXiv:2609.10269](https://arxiv.org/abs/2609.10269) is marked
withdrawn. These are force-space density results, distinct from fixed-force
instability and numerical error regularity; density in a topology is not a
probability or a physical likelihood.

A separate 20 September neural-forcing preprint proposes computational
candidate discovery followed by frozen-force replay and a continuum
certification layer. It is a new claim, not validated evidence; assess it only
through its exact hypotheses, public artifacts and independent replay rather
than treating its abstract's certification claim as established. Source:
[arXiv:2609.23934](https://arxiv.org/abs/2609.23934).

Upstream software changes also matter to the independent cross-check plan:
SU2 remains at 8.5.0 in its published release list, while its active PR queue
includes a proposed fix for implicit target-time evaluation (#2857) and
work on aeroacoustic spectrum analysis (#2851). These are not evidence of an
SU2 defect in our MMS; they motivate explicit regression tests for requested
physical-time sampling and spectrum normalization before interpreting a solver
comparison. PhysicsNeMo 26.08 adds mesh calculus and per-point epistemic
uncertainty plus deterministic/closed-form/sampling-based surrogate benchmark
workflows. These can inform future surrogate uncertainty tests, but do not
replace the frozen-force numerical solver matrix. Sources: [SU2 releases](https://github.com/su2code/SU2/releases), [SU2 PR #2857](https://github.com/su2code/SU2/pull/2857), [PhysicsNeMo 26.08 notes](https://docs.nvidia.com/physicsnemo/26.08/release-notes/index.html).

OpenFOAM Foundation 13's pinned container remains the current reproducibility
target. The Foundation's patch notice lists later 13 patch sources, but these
must not be silently substituted into an in-progress run; a future replication
should record and compare the exact tagged source/package while preserving the
current image digest. Do not conflate Foundation OpenFOAM with the distinct
OpenCFD v2606 line. Sources: [Foundation v13 patches](https://openfoam.org/news/v13-patch/), [OpenCFD v2606 release](https://www.openfoam.com/news/main-news/openfoam-v2606).

## Late 28 September literature check: a discrete cascade model

Cheskidov, Dai, and Palasek submitted *Cascade mechanisms for Navier–Stokes
blow-up* on 22 September ([arXiv:2609.26790](https://arxiv.org/abs/2609.26790)).
Its new finite-time result is for a mixed Desnyansky–Novikov–Obukhov dyadic
shell model: finitely supported initial modal amplitudes, no forcing, and a
forward cascade toward higher shells. The paper says the full proof of this
theorem will appear in a companion paper. The authors explicitly distinguish
these shell-model results from the full Navier–Stokes PDE and note that most
negative dyadic results have not transferred to that PDE setting.

This offers a mathematically precise scale-transfer analogy, not evidence that
continuum fluid particles physically align. Shell amplitudes are not molecular
positions or an ensemble probability law. For our benchmark it suggests a
possible later diagnostic—time-resolved energy by spectral band and cumulative
inter-band flux—alongside local gradient and vorticity errors. Such a diagnostic
would need a verified energy/work balance (including external-force work),
resolution controls, and a statement that finite-resolution flux is not a
continuum singularity certificate. It does not change any current solver
verdict or justify an upstream defect report.

## 30 September analytical bridge: finite rigid fibers

Aulnette et al.'s arXiv v2 preprint (submitted 15 July, revised 3 August 2026)
adds a direct, but sharply bounded, result to the particle-orientation question.
It combines microfluidic measurements, Jeffery theory and bead-model simulations
for rigid neutrally buoyant fibers in a stationary Burgers-like cross-slot
vortex. The paper reports aspect ratios 10–100, lengths 40–500 micrometres,
base-flow `Re=40–80` and estimated particle `Re_p=0.05–12`, with local strain
rates around 115–150 s^-1. It observes simultaneous azimuthal precession from
vorticity and polar alignment from extensional strain. Using its reported
mixture density and viscosity gives a Burgers core radius of about 150–171
micrometres, so the measured fiber lengths span approximately `L/r_gamma=0.23–3.33`.
Within the tested range, orientation remains well described by Jeffery theory,
with longer fibers rotating slightly slower and aligning slightly faster than
its local prediction; migration shows clearer finite-size effects. The authors
report that viscous effects dominate orientation in their tested cases, but
their bead simulations assume `Re_p << 1` while the experimental estimate spans
0.05–12; this does not establish general irrelevance of inertia.
The authors warn that a sufficiently long fiber may sample nonuniform gradients
and violate the local-flow assumption, but do not identify a universal
threshold. This is
finite-fiber orientation evidence in a laboratory vortex, not molecular
evidence or an experiment on the OpenAI field. Sources: [arXiv:2607.14298v2](https://arxiv.org/abs/2607.14298v2), [published flexible-fiber study, JFM 1032 A7](https://doi.org/10.1017/jfm.2026.11342).

The idealized connection can be derived exactly. For `E=diag(2 gamma,-gamma,-gamma)`,
Jeffery's equation gives
`d beta/dt=-3 kappa gamma sin(beta)cos(beta)`, so
`tan(beta(t))/tan(beta(t0))=exp(-3 kappa integral(gamma ds))`, with
`kappa=(AR^2-1)/(AR^2+1)`. If one imposes the additional strain history
`gamma(t)=C/(2(1-t))`, this becomes `Q^(3 kappa C/2)`, matching the audited
continuum tangent-map ratio `Q^(3C/2)` in the slender limit `kappa -> 1`.
With an additional isotropic initial-director model, the probability of being
within angle `beta_star` is `1-a/sqrt(a^2+tan(beta_star)^2)`,
`a=Q^(3 kappa C/2)`, and tends to one for `kappa>0` in that ideal strain
history.
For aspect ratios 10 and 100, the cited rigid-fiber paper's shape factor is
`99/101` and `9999/10001`: within about 2% of the slender limit. In this range,
aspect ratio alone weakly changes the ideal local alignment rate; fiber length
can still matter through finite-size sampling, inertia, flexibility and
interactions.

This is a conditional mathematical bridge, not a transfer theorem. A finite
fiber must experience approximately uniform, axisymmetric strain over its
length and obey the Jeffery regime. Our OpenAI-flow result supplies a local
derivative along a trajectory, while fixed-size endpoint tube/Hessian control
remains unestablished. A defensible next research step would be a finite-aspect
director calculation on an explicitly specified pre-endpoint velocity field,
with gradient-variation and particle-scale checks. It would still not predict
molecular orientation, particle-location probability, or viscosity change.
The algebra check and exact assumptions are archived in
[`evidence/tests/jeffery-axisymmetric-bridge.json`](../evidence/tests/jeffery-axisymmetric-bridge.json)
and [`docs/fiber-vortex-literature-audit.md`](../docs/fiber-vortex-literature-audit.md).

## 2026-10-01 singular Burgers-vortex comparison

The shared proposal's reduced model is worth preserving because it has a
clean analytic audit. Assume `Gamma, kappa, nu > 0`. For an axisymmetric
Gaussian-vorticity Burgers profile, `W_z=Gamma/(pi q) exp(-r^2/q)`, in the
prescribed radial strain
`u_r=-a(t)r/2`, the axisymmetric vorticity equation is

    partial_t W_z + u_r partial_r W_z = a W_z + nu Delta_r W_z.

The derivatives are `partial_t W_z/W_z=-q'/q+q' r^2/q^2`,
`u_r partial_r W_z/W_z=a r^2/q`, and
`Delta_r W_z/W_z=-4/q+4r^2/q^2`. Matching the constant and `r^2`
coefficients gives `q'=4 nu-aq`. This is the width equation under an imposed
strain history. The additional proposal
`a=kappa W_peak`, where `W_peak=Gamma/(pi q)`, is a separate closure; it does
not follow from the vorticity equation or from the OpenAI proof. If imposed,
substitution gives `q'=4 nu-kappa Gamma/pi`. If
`kappa Gamma > 4 pi nu`, write
`mu = kappa Gamma/(kappa Gamma - 4 pi nu) > 1`; then
`q = 4 nu (T-t)/(mu-1)`, `a=mu/(T-t)`, and
`W_peak = (mu/kappa)/(T-t)`. This is the published singular Burgers-vortex
family after matching the Gaussian-width and circulation conventions. In the
normalization of Maekawa, Miura and Prange, the axial eigenvalue of their
linear strain is `mu/(T-t)`. For their stated circulation
`alpha_mu=4 pi mu/(mu-1)`, the paper gives `||curl u||_infinity/2 =
mu/[2(T-t)]`; thus the peak-vorticity norm equals the axial strain eigenvalue.
With `kappa=1` and their normalized viscosity convention `nu=1`, the reduced
ansatz matches that family for the stated circulation. This is a parameter
identification along an exact solution with prescribed time-dependent strain;
it is not evidence that the strain is dynamically generated by a local
vorticity-feedback law. The paper describes the relation as the strain behaving
"as if" it depends on the vorticity norm. The solution has spatially growing
linear strain and lies outside the hypotheses
of the standard finite-energy epsilon-regularity and backward-self-similar
nonexistence frameworks. It does not establish blow-up from finite-energy data
or a molecular transition.
Source: [Maekawa, Miura and Prange, arXiv:1807.10341](https://arxiv.org/abs/1807.10341).

The mapping does not transfer automatically to OpenAI's constructed core. Along
its selected axis trajectory the symmetric axial strain rate is
`a_OAI=C/tau`, while the local axial vorticity is
`W_OAI=2 f(0,eta_*) d_*^(h+1) tau^(-(1+h))`. For the *pointwise* closure
`a_OAI=kappa W_OAI`, a nonzero profile value gives
`a_OAI/W_OAI proportional to tau^h`, which cannot be a fixed positive
constant for `h>0`; a zero value also cannot match the positive strain. This
rejects that specific local proportionality along this trajectory. It does not
test a closure using the global `L-infinity` vorticity unless this trajectory is
shown to attain its spatial peak; no such peak-location result is asserted here.
Other closures and finite-time comparisons remain open. The OpenAI proof therefore supplies neither the
Burgers-vortex feedback law nor a discrete-particle interpretation.

The parameter map is also checked by the dependency-free arithmetic regression
`python tools/check_burgers_feedback_mapping.py`; its output is
[`evidence/tests/burgers-feedback-mapping.json`](../evidence/tests/burgers-feedback-mapping.json).
This verifies only the displayed scalar identities at representative parameter
values. It is not a symbolic proof or a Navier–Stokes computation.

## 2026-10-01 live-source recheck

The OpenAI public repository's `main` was checked directly with `git ls-remote`
and remained at `f9e8bc5b38b6e212696e8a30e3e91517af887bbd`, the snapshot already
audited above. The arXiv API reports v2 (updated 29 September) as the current
version of Lei and Ren's Part I. An exact-title API query for their announced
Part II returned only Part I; no Part II record was found as of this check.
This bounds the follow-up-status search, not private work or external review.
The analytic-forcing result and its conditional scope were already recorded
above; no independent application of that theorem to OpenAI's actual force was
performed here.

## 2026-10-01 literature and model-scope refresh

Lei and Ren's version 2 (29 September) of [arXiv:2609.35406](https://arxiv.org/abs/2609.35406) is an explicitly expository reconstruction of the leading-profile portion of OpenAI's manuscript. It describes axisymmetric profiles, a divergence-form stress plus an infinitely flat remainder on fixed similarity sectors, and a new linear model for the inner core. It says the oscillatory-pulse cancellation is deferred to a planned Part II and that the exposition will not be submitted to a journal. This is useful for line-by-line analytic auditing, not an independent end-to-end proof or physical particle model.

Niemi's version 2 (25 September) of [arXiv:2609.24490](https://arxiv.org/abs/2609.24490) uses a smooth flow surrogate with the collapsing core's geometry and scaling to drive a two-component Bose–Einstein-condensate Hopf texture. Its reported fold events are an adjacent quantum-gas analogue, not particles transported by the actual OpenAI solution, not a photon-fluid experiment, and not molecular evidence.

The phrase “light as a fluid” has a precise established analogue in nonlinear optics: medium-induced effective photon–photon interactions let a many-photon system behave collectively as a quantum fluid. This supports a separate model-comparison research track, already recorded in `docs/exploratory-directions.md`, but does not make free-space light an incompressible Newtonian fluid or transfer the OpenAI Navier–Stokes theorem to optical propagation. Any bridge must specify the optical platform and compare its nonlinear-wave equation, dispersive/quantum-pressure term, losses, and boundary conditions against the proposed reduced hydrodynamics. Source: [Carusotto and Ciuti, *Quantum fluids of light*, Reviews of Modern Physics](https://journals.aps.org/rmp/abstract/10.1103/RevModPhys.85.299).

For the user's hypothesis, retain four separate levels: continuum deformation of infinitesimal material directions; finite parcels, needing a nonzero-neighborhood estimate; molecular positions/statistics and viscosity, needing a kinetic/constitutive model; and optical quantum fluids, needing their own effective-wave model. Current proof work reaches the first level conditionally and supplies only a shrinking-packet allowance with non-effective constants for the second. It gives neither absolute-position certainty nor molecular ordering. The determinant-one deformation contracts transversely while expanding axially, and our separate conditional axial viscous-force/material-acceleration ratio does not tend to zero. No constitutive-viscosity drop follows.
