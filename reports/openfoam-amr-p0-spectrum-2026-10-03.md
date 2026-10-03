# Analytic continuum spectrum of the declared AMR P0 velocity

Twelve archived N=3 states now have a verified spectrum for their explicitly
cube-constant velocity representation. Cell integrals and a finest-voxel FFT
agree; the global spectral L2 error agrees with the earlier independently
computed spatial P0 error in every state, within 2.04e-15 in relative L2.
No interpolation, new CFD run or solver-quality threshold is introduced.
At n64/postSolve, a finite-cube coefficient error of 0.4814% is accompanied by
6.1608% outside-cube norm, giving 6.1795% global P0 error. These percentages
all use the same integrated continuum reference velocity norm.

The result verifies an available nonuniform **P0** spectral diagnostic.
It does not complete the original AMR peak/spectrum quality gate, define a
smooth numerical velocity reconstruction, or certify a continuous gradient
bound. The earlier frozen mean study and its original UNAVAILABLE spectrum
field are preserved as historical records, with this supplemental result linked
separately. The goal remains active.

## Representation and derivation

The domain is [0,2*pi)^3. Every validated cell is an aligned cube of width
h or h/2, with no overlaps or holes. Write the cell-constant field as
v(x)=sum_K v_K 1_K(x). With normalized Fourier coefficients,

$$c_k=(2\pi)^{-3}\int v(x)e^{-ik\cdot x}\,dx
=\sum_K\frac{|K|}{(2\pi)^3}v_K e^{-ik\cdot C_K}
\prod_{j=1}^3\operatorname{sinc}\!\left(\frac{k_jh_K}{2\pi}\right),$$

where sinc(s)=sin(pi*s)/(pi*s). This direct cube sum requires no interpolated
sample values. For efficient evaluation, repeat each parent constant on the
finest dyadic voxels. This preserves the same P0 function exactly; it does not
infer subcell information. If m=2n and a_i is the voxel value at center
(i+1/2)2*pi/m, its normalized FFT F satisfies

$$c_k=F_{k\bmod m}\,e^{-i\pi(k_1+k_2+k_3)/m}
\prod_{j=1}^3\operatorname{sinc}(k_j/m).$$

The center phase and sinc window are essential. The uncorrected FFT is not the
continuum P0 spectrum. For integer modes beyond Nyquist the same identity uses
the residue and the physical mode's sinc/phase; it does not truncate the
continuum field to a finite spectrum.

The reference is evaluated independently from binomial coefficients of
cos(q/2)^8: g_l=binomial(8,4+l)/256 for |l|<=4. Velocity coefficients are
supported only at kx=+/-3 and |ky|,|kz|<=4. The reference squared norm also
matches the earlier rational Parseval derivation. Independent real-space
Gauss integration tests verify these coefficients.

For B={k:|kj|<=7}, all reference coefficients outside B vanish. Parseval gives

$$T=\langle|v|^2\rangle-\sum_{k\in B}|c_k|^2,
\qquad
\langle|v-u|^2\rangle=\sum_{k\in B}|c_k-\widehat u_k|^2+T.$$

T includes every mode outside the cube, including infinitely many aliases of
the voxel representation. It is a total mass, not a reconstruction of each
outside shell. The stored shells through index 7 are complete integer shells;
higher shells inside the cube are partial. No factor of 1/2 is used in the
reported mean-square norms; kinetic-energy conventions would halve them.

These are analytic identities evaluated in floating point. The implementation
checks geometry coverage, finite values, native-cell versus voxel norms,
selected direct cube integrals, reference Parseval norm and the archived
spatial P0 error. No interval-arithmetic certificate is claimed.

## Archived outcomes

| Final case | Inside-cube coefficient error | Outside-cube norm | Global P0 error |
|---|---:|---:|---:|
| n16-dt0.001 | 7.6825% | 33.3020% | 34.1767% |
| n32-dt0.001 | 1.9298% | 16.6959% | 16.8070% |
| n64-dt0.001 | 0.4814% | 6.1608% | 6.1795% |
| n32-dt0.0005 | 1.9315% | 16.5547% | 16.6670% |

The inside-cube mismatch and outside-cube norm are orthogonal error components;
the total is their root-sum-square, not their arithmetic sum. At n64 the
outside-cube norm dominates this P0 global error, despite representing only
0.3817% of the actual velocity squared norm. The small energy fraction and
its square-root norm percentage are distinct quantities. Much of the P0
error is a representation floor; the earlier cell-mean gate remains separate.
No fixed 5% spectrum-quality rule is applied retrospectively to these norms.

All four preMap/mapped pairs have bit-identical finite-band coefficient arrays
and identical voxel norms. This strengthens the earlier real-space parent-copy
check: repartitioning the same P0 function preserves its spectral content.
Later evolution reduces both finite-band mismatch and outside mass. Resolution
improves the final results substantially; no asymptotic nonconvergence follows.

## Why a P0 derivative spectrum requires care

A P0 velocity is generally discontinuous. Ordinary continuum derivative energy
is not defined as a finite L2 norm solely by its finite native Gauss tensors.
An elementary periodic shear illustrates the distinction: take
v=(0,1_[0,pi)(x),0). For odd nonzero kx its coefficient is
(0,1/(pi*i*kx),0), and even nonzero coefficients vanish. Consequently
kx^2*|c_k|^2=1/pi^2 for every odd kx, so the infinite derivative-weighted
series diverges. The field is bounded and this divergence arises from the
chosen step representation. It is not evidence of a Navier–Stokes blow-up,
physical dissipation becoming infinite, molecular alignment or viscosity change.

This example limits interpretation of P0 spectra. Native Gauss-gradient/curl
quality, a specified smooth reconstruction and physical molecular models need
separate evidence. The new spectral measurement does not substitute for those
remaining goal requirements.

## Publication and replay

Code, protocol, all 12 compressed coefficient arrays, checksums and diagnostic
records are in [`evidence/amr-p0-spectrum-v1`](../evidence/amr-p0-spectrum-v1/README.md).
Raw inputs remain the four original published archives from frozen CFD commit
3566f890; no prior artifact, threshold or original gate result is overwritten.
Local full suite: 281 passed, one skipped and 83 subtests passed. No new upstream
issue is justified by these representation diagnostics alone.
