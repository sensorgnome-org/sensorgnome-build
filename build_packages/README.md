# Build Debian Packages of all Sensorgnome Software

## Docker Package Crosscompiling and Package Build

Work in progress. Essential steps are:
- Clone dockcross from GitHub: `git clone https://github.com/dockcross/dockcross.git`
- Patch dockcross files to support modern GCC.
- Run `make linux-armv7-hf` to build dockcross/linux-armv7-hf container.
  - This step can take some serious time.
  - If you get an error about being out of space, increase the size of Docker's volumes by adding `{"storage-opts": ["dm.basesize=64G"]}` to `/etc/docker/daemon.json`. GCC is pretty large and needs more than the default 10GB of space. 64GB is way more than needed. **This may delete any existing containers/images.**
- Run `docker build -t dockcross/linux-arm7-hf .` with the Dockerfile included in this project.
- Run `docker run sensorgnome-armv7-hf > linux-armv7-hf` to create an bash script that sets up and runs dockcross.
- Make the script executable `chmod +x ./linux-armv7-hf`.
- Now cross-compiling should be working. 

## Package Building

Run build_packages.py to create output packages.

### build_packages.py switches:

- `-c`/`--c-compiler`: Optionally set non-standard C compiler, useful for cross-compilation.
- `-x`/`--cpp-compiler`: Optionally set non-standard C++ compiler, useful for cross-compilation.
- `-s`/`--strip`: Optionally set non-standard strip binary, useful for cross-compilation.
- `-t`/`--temp`: Temp directory to store build files and artifacts in.
- `-o`/`--output`:  Directory to output finished debian pagkages.

### Dependencies

Note that the `build-essential` Debian package needs to be installed to build all of the packages. Same with Python, Debian package `python3`, version 3.6 or greater

The `gitpython` Python package is also used in all build scripts.

### package_vamp_alsa_host.py

Source repo at https://github.com/sensorgnome-org/vamp-alsa-host

#### Build Dependendcies:

- Debian:
  - libfftw3-3
  - libfftw3-dev
  - vamp-plugin-sdk
  - libboost-dev
  - libasound2-dev
  - libvamp-hostsdk3v5

### package_vamp_plugins.py

Source repo at https://github.com/sensorgnome-org/vamp-plugins

#### Build Dependendcies:

- Debian:
  - libfftw3-3
  - libfftw3-dev
  - vamp-plugin-sdk
  - libboost-dev
  - libasound2-dev

### package_sensorgnome_control.py

Source repo at https://github.com/sensorgnome-org/sensorgnome-control.git

#### Build Dependendcies:

No additional.

### package_sensorgnome_support.py

Source repo at https://github.com/sensorgnome-org/sensorgnome-support.git

#### Build Dependendcies:

No additional.

### package_openssh_portable.py

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

### package_sensorgnome_librtlsdr.py

Source repo at https://github.com/sensorgnome-org/sensorgnome-librtlsdr.git

Builds the patched version of librtlsdr that SensorGnome currently uses.

#### Build Dependendcies:

- Debian:
  - libusb-1.0-0
  - libusb-1.0-0-dev
  - autoconf
  - libtool

### package_fcd.py

Source repo at https://github.com/sensorgnome-org/fcd.git


#### Build Dependendcies:

No additional.

### package_find_tags.py

Source repo at https://github.com/sensorgnome-org/find_tags.git

Builds the `find_tags_unifile` branch for running on the SensorGnome.

#### Build Dependendcies:

- Debian:
  - libsqlite3-dev
