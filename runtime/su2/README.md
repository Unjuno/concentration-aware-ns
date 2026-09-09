# SU2 transient MMS adapter — pilot executed

Pinned upstream: v8.5.0 / 12eb826f049ef7f67df974dfcb44cf36ee07c0f8.
The source, Eigen and MEL archives are checksum-verified, with Meson pinned to 1.8.2.
Ubuntu transitive packages are not snapshot-pinned; preserve built image identity.

`docker build --platform linux/arm64 -t concentration-aware-ns:su2 runtime/su2`

mms.patch modifies SU2's USER_DEFINED_SOLUTION extension for our periodic 3D
reference with sigma=0.5, nondimensional rho=1 and nu=0.01. The patch retains
SU2's LGPL-2.1-or-later licensing; it is not covered by the root MIT license.
Source is retained inside the image. No second Git repository is created.

Build completed and both pilots exited successfully. The 1000-inner-iteration
pilot reached all four residual thresholds at every step. The mapping between
MMS time, history time and the updated solution remains unresolved; no local
quality verdict is assigned. See docs/progress.md and evidence/su2.
This adapter is our experiment, not an upstream SU2 change or proven bug fix.
