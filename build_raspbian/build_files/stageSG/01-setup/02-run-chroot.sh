#!/bin/sh -e

# Set up data and config directories.
on_chroot << EOF
    echo "Creating data directory"
    mkdir -p /data
    mkdir -p /data/config
    mkdir -p /data/SGdata
    touch /data/config/deployment.txt

    echo "Creating deprecated /boot mount points."
    mkdir -p /boot/uboot
    mkdir -p /boot/SGdata
EOF
