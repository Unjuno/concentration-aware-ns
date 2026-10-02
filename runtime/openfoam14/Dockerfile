FROM ubuntu:24.04@sha256:33ceb71981b602c1a7443a53469e4dba065f7503eab3078a2d7a57a2ab987517
ARG DEBIAN_FRONTEND=noninteractive
RUN test "$(dpkg --print-architecture)" = arm64 \
 && apt-get update \
 && apt-get install -y --no-install-recommends ca-certificates curl \
 && curl -fL --retry 3 https://dl.openfoam.org/ubuntu/dists/noble/main/binary-arm64/openfoam14_20260724_arm64.deb -o /tmp/openfoam14.deb \
 && echo 'd20102ae6b39377ab3f5e654302ea0d58de166156fe681670f147ac555299a69  /tmp/openfoam14.deb' | sha256sum -c - \
 && apt-get install -y --no-install-recommends /tmp/openfoam14.deb \
 && dpkg-query -W > /opt/package-versions.txt \
 && rm /tmp/openfoam14.deb \
 && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/bash", "-c"]
WORKDIR /case
ENTRYPOINT ["/bin/bash", "-c", "source /opt/openfoam14/etc/bashrc; exec \"$@\"", "--"]
CMD ["foamRun", "-help"]
