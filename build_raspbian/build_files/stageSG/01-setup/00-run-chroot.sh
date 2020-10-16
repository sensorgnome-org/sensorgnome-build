#!/bin/sh -e

# Enable other needed services.
on_chroot << EOF
systemctl enable gpsd
systemctl enable chrony
systemctl enable sensorgnome-boot
systemctl enable sensorgnome-control
EOF
