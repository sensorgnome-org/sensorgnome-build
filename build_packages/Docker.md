## Docker Specific Documentation

While everything should be automated, this document serves as a tool to help troubleshooting if something goes wrong.

The docker builds use [dockcross](https://github.com/dockcross/dockcross) to build ARM binaries on an x64 machine. WHile dockcross is great, it has its trickky aspects. Specifically, the GCC toolchain used by dockcross must match what's installed on the target rPi and other libraries that are pulled into dockcross to be able to compile applications also need to have the same version as the ones ultimately installed on the rPi.

### Library compatibility issue

As of October 2021 dockcross uses debian bullseye as a base while the rPi uses debian buster, which is older. Binaries compiled using this dockcross do not work on an rPi because the libraries the applications are compiled against are newer than the ones actually available on the rPi.

#### Fix

Build a dockcross image using debian buster:
- Clone the dockcross repo
- Check out commit `12a662e`
- Build the dockcross image using `make linux-armv7-lts`
- Proceed with building the SG image (`python3 build.py` in the top-level dir)

### GCC compatibility issue

_Note: this issue is resolved as of October 2021, dockcross uses GCC 8.5.0, which is sufficiently close to the 8.3.0 used by the rPi_

This project uses a patched version of dockcross. While using stock dockcross would be preferable, support for modern versions of GCC doesn't yet exist in the armv7 target. When support for GCC > 8 is added, this part can be easily changed to use a stock container by modifing the Dockerfile.

#### Creating armv7-hf target with GCC 8.3.0 using Dockcross

Work in progress. Essential steps are:
- Clone patched dockcross from GitHub: `git clone https://github.com/dockcross/dockcross.git`
- Switch to the `gcc-8.3.0` branch.
- Run `make linux-armv7-hf` to build dockcross/linux-armv7-hf container.
  - This step can take some serious time.
  - If you get an error about being out of space, increase the size of Docker's volumes by adding `{"storage-opts": ["dm.basesize=64G"]}` to `/etc/docker/daemon.json`. GCC is pretty large and needs more than the default 10GB of space. 64GB is way more than needed. **This may delete any existing containers/images.**
- Run `docker build -t dockcross/linux-arm7-hf .` with the Dockerfile included in this project.
- Run `docker run sensorgnome-armv7-hf > linux-armv7-hf` to create an bash script that sets up and runs dockcross.
- Make the script executable `chmod +x ./linux-armv7-hf`.
- Now cross-compiling should be working.
