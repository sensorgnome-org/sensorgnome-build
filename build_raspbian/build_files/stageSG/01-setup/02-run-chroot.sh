#!/bin/sh -e

# Set up data and config directories.
on_chroot << EOF
    mkdir -p /data
    mkdir -p /data/config
    mkdir -p /data/SGdata
    touch /data/config/deployment.txt
EOF
