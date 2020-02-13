## Docker Specific Documentation

While everything should be automated, this document serves as a tool to help troubleshooting if something goes wrong.

### Overview

This project uses a patched version of dockcross. While using stock dockcross would be preferable, support for modern versions of GCC doesn't yet exist in the armv7 target. When support for GCC > 8 is added, this part can be easily changed to use a stock container by modifing the Dockerfile.

### Creating armv7-hf target with GCC 8.3.0 using Dockcross

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
