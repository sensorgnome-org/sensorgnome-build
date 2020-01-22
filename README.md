# Tools to build Sensorgnome Images and Packages

These tools are designed to produce a Sensorgnome image ready to be deployed on a Raspberry Pi (or BeagleBone), produce a base image needing some customization or produce the various packages for standalone updates.

## Package Building

The `build_packages` directory contains all of the scripts required to build the various packages. See the README there for more information.

Packages currently built are:

- fcd
- find-tags
- openssh-portable
- sensorgnome-control
- sensorgnome-librtlsdr
- sensorgnome-support
- vamp-alsa-host
- vamp-plugins

## Image Building

### Raspberry Pi

The `build_raspbian` directory contains all of the scripts, customization and config files needed to build an customized Raspbian image tailored for Sensorgnome.

Uses [pi-gen](https://github.com/RPi-Distro/pi-gen).

### Beaglebone

In progress, based on Debian.
