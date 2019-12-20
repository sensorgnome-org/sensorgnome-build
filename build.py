from os import mkdir, rmdir
from shutil import rmtree

import build_vamp_alsa_host as vamp_alsa_host
import build_vamp_plugins as vamp_plugins
import build_sensorgnome_control as sg_control
import build_sensorgnome_support as sg_support




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
    # vamp_alsa_host_version = "0.5-1"
    # vamp_alsa_host.build(temp_dir, build_dir, vamp_alsa_host_version)
    # vamp_plugins_version = "0.5-1"
    # vamp_plugins.build(temp_dir, build_dir, vamp_plugins_version)
    sg_control_version = "0.5-1"
    sg_control.build(temp_dir, build_dir, sg_control_version)
    sg_support_version = "0.5-1"
    sg_support.build(temp_dir, build_dir, sg_support_version)