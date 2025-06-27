ARG BUILD_FROM
FROM $BUILD_FROM

# Set shell
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Install packages
RUN \
    apk add --no-cache \
        python3=~3.11 \
        py3-pip=~23.1 \
        py3-setuptools=~67.6 \
        py3-wheel=~0.40 \
        python3-dev=~3.11 \
        build-base=~0.5 \
        linux-headers=~6.3 \
        libusb-dev=~1.0 \
        eudev-dev=~3.2

# Install Python packages
RUN pip3 install --no-cache-dir \
    pyserial==3.5 \
    paho-mqtt==1.6.1 \
    mpp-solar==0.15.50

# Copy root filesystem
COPY rootfs /

# Build arguments
ARG BUILD_ARCH
ARG BUILD_DATE
ARG BUILD_DESCRIPTION
ARG BUILD_NAME
ARG BUILD_REF
ARG BUILD_REPOSITORY
ARG BUILD_VERSION

# Labels
LABEL \
    io.hass.name="${BUILD_NAME}" \
    io.hass.description="${BUILD_DESCRIPTION}" \
    io.hass.arch="${BUILD_ARCH}" \
    io.hass.type="addon" \
    io.hass.version=${BUILD_VERSION} \
    maintainer="MPP Solar Community" \
    org.opencontainers.image.title="${BUILD_NAME}" \
    org.opencontainers.image.description="${BUILD_DESCRIPTION}" \
    org.opencontainers.image.vendor="MPP Solar Community" \
    org.opencontainers.image.authors="MPP Solar Community" \
    org.opencontainers.image.licenses="MIT" \
    org.opencontainers.image.url="https://github.com/9991119990/mpp-solar-addon-correct" \
    org.opencontainers.image.source="https://github.com/9991119990/mpp-solar-addon-correct" \
    org.opencontainers.image.documentation="https://github.com/9991119990/mpp-solar-addon-correct/blob/main/README.md" \
    org.opencontainers.image.created=${BUILD_DATE} \
    org.opencontainers.image.revision=${BUILD_REF} \
    org.opencontainers.image.version=${BUILD_VERSION}