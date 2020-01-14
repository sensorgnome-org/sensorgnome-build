# Tools to build Sensorgnome Images and Packages

## Package Building

Run build.py to create output packages in a new folder at `output/`.

### build_vamp_alsa_host.py

Source repo at https://github.com/sensorgnome-org/vamp-alsa-host

#### Build Dependendcies:

- Debian:
  - libfftw3-3
  - libfftw3-dev
  - vamp-plugin-sdk
  - libboost-all-dev
  - libasound2-dev
- Python:
  - gitpython

### build_vamp_plugins.py

Source repo at https://github.com/sensorgnome-org/vamp-plugins

#### Build Dependendcies:

- Debian:
  - libfftw3-3
  - libfftw3-dev
  - vamp-plugin-sdk
  - libboost-all-dev
  - libasound2-dev
- Python:
  - gitpython

### build_sensorgnome_control.py

Source repo at https://github.com/sensorgnome-org/sensorgnome-control.git

#### Build Dependendcies:

- Python:
  - gitpython

### build_sensorgnome_support.py

Source repo at https://github.com/sensorgnome-org/sensorgnome-support.git

#### Build Dependendcies:

- Python:
  - gitpython
