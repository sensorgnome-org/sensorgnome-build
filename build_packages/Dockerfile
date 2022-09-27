# Raspberry Pi OS used in this build is based on Debian buster. We need to use a version of
# dockcross that is also based on buster so it uses the same compiler version and the same
# shared library versions as will be found on the rPi.
# We end up using the changes made for linux-armv7-lts applied to the last dockcross buster image
# which was commit 12a662e
FROM dockcross/linux-armv7-lts

ENV DEFAULT_DOCKCROSS_IMAGE sensorgnome-armv7-hf

# Dockcross pulls from official debian repos. Seems to work OK. The following
# causes arm packages to be pulled from the raspberry-pi repos using the debian multiarch
# feature instead. Commented out but kept in case that becomes necessary someday.
#RUN sed -i -e 's/^deb/deb [arch=amd64,i386]/' /etc/apt/sources.list &&\
#    echo 'deb [arch=armhf] http://raspbian.raspberrypi.org/raspbian/ buster main contrib non-free rpi' >>/etc/apt/sources.list
# Add the following line after the dpkg --add-architecture:
#    wget https://archive.raspbian.org/raspbian.public.key -O - | apt-key add - &&\

# Install Raspberry PI packages needed to build our apps using the dpkg/apt multi-arch feature:
# https://wiki.debian.org/Multiarch/HOWTO
RUN dpkg --add-architecture armhf &&\
    apt-get update &&\
    apt-get install --yes \
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
        libmpdec-dev \
        libudev-dev:armhf \
        libudev1:armhf \
        libboost-dev:armhf \
        libboost-thread-dev:armhf \
        libboost-filesystem-dev:armhf \
        python3-minimal \
        python3-dev \
        libpython3-dev \
        libpython3-stdlib \
        python3-pip &&\
    apt-get clean --yes

# Install pip and Python dependencies.
RUN pip3 install gitpython pytz filehash

# After we install the various C/C++ dependencies, we need to symlink them into the crosscompiler.
ADD docker_symlinks.py /work/docker_symlinks.py
RUN python3 docker_symlinks.py
