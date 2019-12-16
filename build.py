from os import mkdir, rmdir
from shutil import rmtree

import build_vamp_alsa_host as vamp_alsa_host




if __name__ == "__main__":
    temp_dir = "build-temp/"
    build_dir = "output/"
    # Create the temporary build dir if it doesn't exist. Remove it (and its contents).
    # That is, always a clean build.
    try:
        mkdir(temp_dir)
    except FileExistsError:
        rmtree(temp_dir)
        mkdir(temp_dir)
    # We don't remove the existing build directory.
    try:
        mkdir(build_dir)
    except FileExistsError:
        pass
    vamp_alsa_host_version = "0.5-1"
    vamp_alsa_host.build(temp_dir, build_dir, vamp_alsa_host_version)