# Tools to build Sensorgnome Images and Packages

## Package Building

Run build.py to create output packages.

### build.py switches:

- `-c`/`--c-compiler`: Optionally set non-standard C compiler, useful for cross-compilation.
- `-x`/`--cpp-compiler`: Optionally set non-standard C++ compiler, useful for cross-compilation.
- `-s`/`--strip`: Optionally set non-standard strip binary, useful for cross-compilation.
- `-t`/`--temp`: Temp directory to store build files and artifacts in.
- `-o`/`--output`:  Directory to output finished debian pagkages.

### Dependencies

Note that the `build-essential` Debian package needs to be installed to build all of the packages. Same with Python, Debian package `python3`.

The `gitpython` Python package is also used in all build scripts.

### build_vamp_alsa_host.py

Source repo at https://github.com/sensorgnome-org/vamp-alsa-host

#### Build Dependendcies:

- Debian:
  - libfftw3-3
  - libfftw3-dev
  - vamp-plugin-sdk
  - libboost-all-dev
  - libasound2-dev

### build_vamp_plugins.py

Source repo at https://github.com/sensorgnome-org/vamp-plugins

#### Build Dependendcies:

- Debian:
  - libfftw3-3
  - libfftw3-dev
  - vamp-plugin-sdk
  - libboost-all-dev
  - libasound2-dev

### build_sensorgnome_control.py

Source repo at https://github.com/sensorgnome-org/sensorgnome-control.git

#### Build Dependendcies:

No additional.

### build_sensorgnome_support.py

Source repo at https://github.com/sensorgnome-org/sensorgnome-support.git

#### Build Dependendcies:

No additional.

### build_openssh_portable.py

Source repo at https://github.com/sensorgnome-org/sensorgnome-openssh-portable.git

Builds that patched version of OpenSSH portable that SensorGnome currently uses.

#### Build Dependendcies:

- Debian:
  - libssl-dev
  - autoconf
  - zlib1g
  - zlib1g-dev

#### Notes

This version of OpenSSH is very, very out of date.

### build_sensorgnome_librtlsdr.py

Source repo at https://github.com/sensorgnome-org/sensorgnome-librtlsdr.git

Builds the patched version of librtlsdr that SensorGnome currently uses.

#### Build Dependendcies:

- Debian:
  - libusb-1.0-0
  - libusb-1.0-0-dev
  - autoconf
  - libtool

### build_fcd.py

Source repo at https://github.com/sensorgnome-org/fcd.git


#### Build Dependendcies:

No additional.

### build_find_tags.py

Source repo at https://github.com/sensorgnome-org/find_tags.git

Builds the `find_tags_unifile` branch for running on the SensorGnome.

#### Build Dependendcies:

- Debian:
  - libsqlite3-dev
