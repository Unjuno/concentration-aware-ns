FROM ubuntu:24.04@sha256:33ceb71981b602c1a7443a53469e4dba065f7503eab3078a2d7a57a2ab987517

# Same Foundation package as runtime/openfoam13; only acquisition is resumable.
ARG DEBIAN_FRONTEND=noninteractive
COPY fetch_pinned_package.sh /usr/local/bin/fetch-pinned-openfoam-package
RUN test "$(dpkg --print-architecture)" = arm64 \
 && apt-get update \
 && apt-get install -y --no-install-recommends ca-certificates curl \
 && /bin/bash /usr/local/bin/fetch-pinned-openfoam-package \
      https://dl.openfoam.org/ubuntu/dists/noble/main/binary-arm64/openfoam13_20260624_arm64.deb \
      6da0f6460fbc33c8995cbc97caba52c6cb0342f52ed02ff57530d9d62e9ef360 /tmp/openfoam13.deb \
 && apt-get install -y --no-install-recommends /tmp/openfoam13.deb \
 && dpkg-query -W > /opt/package-versions.txt \
 && rm /tmp/openfoam13.deb \
 && find /var/lib/apt/lists -type f -delete

SHELL ["/bin/bash", "-c"]
WORKDIR /case
ENTRYPOINT ["/bin/bash", "-c", "source /opt/openfoam13/etc/bashrc; exec \"$@\"", "--"]
CMD ["foamRun", "-help"]
