FROM ubuntu:24.04@sha256:33ceb71981b602c1a7443a53469e4dba065f7503eab3078a2d7a57a2ab987517
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends build-essential ca-certificates curl python3 python3-venv ninja-build pkg-config patch && rm -rf /var/lib/apt/lists/*
RUN python3 -m venv /opt/build-env && /opt/build-env/bin/pip install meson==1.8.2
RUN curl -fL --retry 3 https://codeload.github.com/su2code/SU2/tar.gz/12eb826f049ef7f67df974dfcb44cf36ee07c0f8 -o /tmp/su2.tar.gz \
 && echo '316552bdf987a9254093f1179addc2afa2c396c8fe97fbeeae06250dccaea7e4  /tmp/su2.tar.gz' | sha256sum -c - \
 && mkdir /opt/SU2 && tar -xzf /tmp/su2.tar.gz --strip-components=1 -C /opt/SU2 \
 && curl -fL --retry 3 https://gitlab.com/libeigen/eigen/-/archive/d71c30c47858effcbd39967097a2d99ee48db464/eigen-d71c30c47858effcbd39967097a2d99ee48db464.tar.gz -o /tmp/eigen.tar.gz \
 && echo 'f1d28c2205d015490a685b1e5a171c434da87f757746724de3cb85e69621dec2  /tmp/eigen.tar.gz' | sha256sum -c - \
 && tar -xzf /tmp/eigen.tar.gz --strip-components=1 -C /opt/SU2/externals/eigen
RUN curl -fL --retry 3 https://codeload.github.com/pcarruscag/MEL/tar.gz/46205ab019e5224559091375a6d71aabae6bc5b9 -o /tmp/mel.tar.gz \
 && echo 'e0f7f95ab80d098a2c2bafceefb52e958378302c2150ef7cb9fe2bf4aa81177b  /tmp/mel.tar.gz' | sha256sum -c - \
 && tar -xzf /tmp/mel.tar.gz --strip-components=1 -C /opt/SU2/externals/mel
WORKDIR /opt/SU2
RUN python3 preconfigure.py --no-codi --no-medi --no-opdi --no-mpp --no-coolprop --no-mel --no-fado --no-mlpcpp --no-eigen
COPY mms.patch /tmp/mms.patch
RUN patch -p1 < /tmp/mms.patch \
 && /opt/build-env/bin/meson setup build --prefix=/opt/su2-install -Dwith-mpi=disabled -Denable-cgns=false -Denable-tecio=false -Dcpu-arch=armv8-a \
 && ninja -C build -j2 install \
 && dpkg-query -W > /opt/package-versions.txt
ENV PATH="/opt/su2-install/bin:${PATH}"
WORKDIR /case
CMD ["SU2_CFD", "--help"]
