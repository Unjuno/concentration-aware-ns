FROM ubuntu:24.04@sha256:33ceb71981b602c1a7443a53469e4dba065f7503eab3078a2d7a57a2ab987517

# Official Foundation binary, distinct from OpenCFD. ARM64 only for this adapter.
ARG DEBIAN_FRONTEND=noninteractive
RUN test "$(dpkg --print-architecture)" = arm64 \
 && apt-get update \
 && apt-get install -y --no-install-recommends ca-certificates curl \
 && curl -fL --retry 3 https://dl.openfoam.org/ubuntu/dists/noble/main/binary-arm64/openfoam13_20260624_arm64.deb -o /tmp/openfoam13.deb \
 && echo '6da0f6460fbc33c8995cbc97caba52c6cb0342f52ed02ff57530d9d62e9ef360  /tmp/openfoam13.deb' | sha256sum -c - \
 && apt-get install -y --no-install-recommends /tmp/openfoam13.deb \
 && dpkg-query -W > /opt/package-versions.txt \
 && rm /tmp/openfoam13.deb \
 && rm -rf /var/lib/apt/lists/*

SHELL ["/bin/bash", "-c"]
WORKDIR /case
ENTRYPOINT ["/bin/bash", "-c", "source /opt/openfoam13/etc/bashrc; exec \"$@\"", "--"]
CMD ["foamRun", "-help"]
