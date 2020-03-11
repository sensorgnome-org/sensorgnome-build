#!/bin/sh -e
# copy packages into /tmp/ for installation.

mkdir -p "${ROOTFS_DIR}"/tmp/sg/
cp fcd_0.5-1.deb "${ROOTFS_DIR}"/tmp/sg/fcd_0.5-1.deb
cp find_tags_0.5-1.deb "${ROOTFS_DIR}"/tmp/sg/find_tags_0.5-1.deb
cp sensorgnome-control_0.5-1.deb "${ROOTFS_DIR}"/tmp/sg/sensorgnome-control_0.5-1.deb
cp sensorgnome-librtlsdr_0.5-1.deb "${ROOTFS_DIR}"/tmp/sg/sensorgnome-librtlsdr_0.5-1.deb
cp sensorgnome-openssh-portable_0.5-1.deb "${ROOTFS_DIR}"/tmp/sg/sensorgnome-openssh-portable_0.5-1.deb
cp sensorgnome-support_0.5-1.deb "${ROOTFS_DIR}"/tmp/sg/sensorgnome-support_0.5-1.deb
cp vamp-alsa-host_0.5-1.deb "${ROOTFS_DIR}"/tmp/sg/vamp-alsa-host_0.5-1.deb
cp vamp-plugins_0.5-1.deb "${ROOTFS_DIR}"/tmp/sg/vamp-plugins_0.5-1.deb
