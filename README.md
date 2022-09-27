# Build Sensorgnome Images and Packages

This repository contains tools to build SensorGnome software packages for the Raspberry Pi
(potentially also BeagleBone) and to build a complete Raspberry Pi OS image with the
SensorGnome software preinstalled.

The build process is designed to run under docker in order to enable building on machines
other than an rPi itself (which has not been tested). There are two main Docker images that are used:
(dockcross)[https://github.com/dockcross/dockcross] and (pi-gen)[https://github.com/RPi-Distro/pi-gen].
Dockcross contains cross-compilation toolchains that allow ARM executables to be produced on an x64
machine. Pi-gen is a collection of scripts and a docker image that allows a bootable Raspberry
Pi OS image to be pre-loaded with software and a final image file to be produced.

The overall steps in the build process are the following:
- customize dockercross to contain all the library prerequisites for building SensorGnome
- use dockercross to cross-compile all the sensorgnome software packages resulting in a collection of `.deb` package files.
- use pi-gen to create a bootable operating system image with the SensorGnome software installed
  and various necessary customizations performed so everything works at boot.

All these steps are orchestrated by the top-level `build.py` script.

## Dockercross customization

Dockercross is a general-purpose docker image to enable cross-compilation for a variety of architectures
and operating system on almost any x64 machine. Unfortunately it is not designed to specifically
support the Raspberry Pi OS and as a result a modified version of dockercross must be used.

As of October 2021 the Raspberry Pi OS uses Debian buster, GCC 8.3, and glibc 2.28.
In order to successfully build packages for the rPi a version of dockercross must be built that
uses (more or less) exactly these software versions. This can be accomplished as follows:
- start with dockercross at commit `12a662e`, which is the last commit that uses buster
- apply (PR 624)[https://github.com/dockcross/dockcross/pull/624], which won't apply cleanly, so
  some tweaking is required (the conflicts are mostly in the github workflow spec, which we don't
  care about)
- create a derivative image with dependencies used by SensorGnome installed using the
  Dockerfile in this repo

The end result is a docker image called `sensorgnome-armv7-hf` and a `sensorgnome-armv7-hf`
script to run a command in that image.

## Package Building

The `build_packages` directory contains all of the scripts required to build the various packages.
See the README there for more information.
The top-level build script lauches a dockercross container to run `build_packages/build_packages.py`.
In principle, this script should also function without docker on an rPi itself.

Packages currently built are:

- fcd
- find-tags
- _openssh-portable_ -- not built for now due to security and maintainability concerns
- sensorgnome-control
- sensorgnome-librtlsdr
- sensorgnome-support
- vamp-alsa-host
- vamp-plugins

## Image Building

The `build_raspbian` directory contains all of the scripts, customization and config files needed to
build a customized Raspbian image tailored for Sensorgnome.

The image build process proceeds in several stages outlined in the pi-gen repository's readme.
For the sensorgnome a "lite" image is produced, which means no GUI and a minimal set of applications.
The main customizations performed are:
- create a 3-partition layout with an ext4 root partition and a fat32 data partition
- install debian packages used by the SG software
- install SG software packages
- install node.js dependencies
- install systemd units to run SG software automatically

The end result is a `.img` image file, which can be flashed to a SD-card in the same way as a
standard Raspberry Pi OS image is flashed.

## Prerequisites

- Install docker
- pip install -r requirements.txt (preferably in a venv)

### Notes

Misc notes.

- Applied patch by Evan Jobling: `patch -f -p1 --binary <evanj.patch` -- ignore that one hunk fails
- To run just the image build step:
  `python -c 'import build; build.create_image(build.image_name())'`
- To build an image using checked-out repositories, check them out (clone) into a sibling dir
  to sensorgnome-build (this repo), then set `SRCDIR` in
  `build_packages/package_sensorgnome_support.py` or
  `build_packages/package_sensorgnome_control.py` and shown in the commented-out statements.
  (TODO: The same `SRCDIR` should be supported for other repos as well.)
  The way this works is that `..` is mounted onto `/mnt` in the docker container
  in `build.py`'s `docker_build_packages`.
