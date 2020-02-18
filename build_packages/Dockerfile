FROM dockcross/linux-armv7-hf

ENV DEFAULT_DOCKCROSS_IMAGE sensorgnome-armv7-hf
# Install Debian Packages.
RUN dpkg --add-architecture armhf && apt-get update \
&& apt-get install --yes \
    libfftw3-3:armhf \
    libfftw3-dev:armhf \
    vamp-plugin-sdk:armhf \
    libasound2-dev:armhf \
    libssl-dev:armhf \
    autoconf:armhf \
    zlib1g:armhf \
    zlib1g-dev:armhf \
    libusb-1.0-0:armhf \
    libusb-1.0-0-dev:armhf \
    libusb-0.1-4:armhf \
    libusb-dev:armhf \
    autoconf:armhf \
    libtool:armhf \
    libsqlite3-dev:armhf \
    libsqlite3-0:armhf \
    libvamp-hostsdk3v5:armhf \
    libhwloc-plugins:armhf \
    libmpdec2 \
    libudev-dev:armhf \
    libudev1:armhf \
    libboost1.67-dev:armhf \
    libboost-thread1.67-dev:armhf \
    libboost-thread1.67.0:armhf \
    libboost-filesystem1.67-dev:armhf \
    libboost-filesystem1.67.0:armhf \
&& apt-get clean --yes
# This is hacky, but the Debian version that Dockcross uses is super old and outdated.
RUN bash -c "wget https://github.com/chriskuehl/python3.6-debian-stretch/releases/download/v3.6.3-1-deb9u1/{python3.6_3.6.3-1.deb9u1_amd64,python3.6-minimal_3.6.3-1.deb9u1_amd64,python3.6-dev_3.6.3-1.deb9u1_amd64,libpython3.6_3.6.3-1.deb9u1_amd64,libpython3.6-minimal_3.6.3-1.deb9u1_amd64,libpython3.6-stdlib_3.6.3-1.deb9u1_amd64,libpython3.6-dev_3.6.3-1.deb9u1_amd64}.deb" \
&& dpkg -i *.deb \
&& rm *python3.6*.deb
# Install pip and Python dependencies.
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py \
&& python3.6 get-pip.py \
&& rm get-pip.py \
&& python3.6 -m pip install gitpython
# After we install the various C/C++ dependencies, we need to symlink them into the crosscompiler.
ADD docker_symlinks.py /work/docker_symlinks.py
RUN python3.6 docker_symlinks.py
