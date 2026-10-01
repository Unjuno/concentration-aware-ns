# OpenFOAM Foundation 14 comparison runtime

This runtime is a local Docker recipe for the official Foundation package, not
an official OpenFOAM image. It targets Linux/arm64 on the pinned Ubuntu 24.04
base and downloads the Foundation `openfoam14` package `20260724`. The package
SHA-256 is checked during the build. The Foundation package's source tag is
`20260724` at commit `7b05503f98a85be88af930df48623b4d152bfc35`.

Build and inspect it from the repository root:

```sh
docker build --platform linux/arm64 -t concentration-aware-ns:of14-20260724 -f runtime/openfoam14/Dockerfile runtime/openfoam14
docker image inspect concentration-aware-ns:of14-20260724 --format '{{.Id}} {{.Os}}/{{.Architecture}}'
docker run --rm --entrypoint cat concentration-aware-ns:of14-20260724 /opt/package-versions.txt
```

The captured image ID, full installed package inventory, build log, and the
single-case compatibility probe are in
`evidence/of14-high-gradient-v1/`. The apt dependency index is not snapshot
pinned, so a future build can have a different image ID or dependency set even
when the OpenFOAM package checksum still matches. Compare the recorded image
ID and package inventory before claiming an exact runtime reproduction.

The archived probe uses the unchanged mathematical case and thresholds from
`protocols/high-gradient-of13-v2.json`, but it is one Foundation 14 case only.
It does not establish a full v14 resolution/time-step matrix or solver-wide
behavior. The recorded case uses `incompressibleFluid`; v14 release-note
improvements to `isothermalFluid` were therefore not exercised by this probe.
