ARG BUILD_FROM
FROM $BUILD_FROM

# Set shell
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Install packages
RUN \
    apk add --no-cache \
        python3 \
        py3-pip \
        py3-setuptools \
        py3-wheel \
        python3-dev \
        build-base \
        linux-headers \
        libusb-dev \
        eudev-dev

# Install Python packages
RUN pip3 install --no-cache-dir \
    pyserial \
    paho-mqtt \
    mpp-solar

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