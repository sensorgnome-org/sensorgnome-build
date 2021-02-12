#!/bin/sh -e

# Install the previously copied packages in the chroot.
on_chroot << EOF
echo "Installing Sensorgnome Packages."
apt install -y /tmp/sg/fcd_0.5-1.deb
apt install -y /tmp/sg/find_tags_0.5-1.deb
apt install -y /tmp/sg/sensorgnome-support_0.5-1.deb
apt install -y /tmp/sg/sensorgnome-control_0.5-1.deb
apt install -y /tmp/sg/sensorgnome-librtlsdr_0.5-1.deb
apt install -y /tmp/sg/sensorgnome-openssh-portable_0.5-1.deb
apt install -y /tmp/sg/vamp-alsa-host_0.5-1.deb
apt install -y /tmp/sg/vamp-plugins_0.5-1.deb
EOF
