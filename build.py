from os import mkdir, rmdir
from shutil import rmtree

from helpers import bcolors, timestamp
import build_vamp_alsa_host as vamp_alsa_host
import build_vamp_plugins as vamp_plugins
import build_sensorgnome_control as sg_control
import build_sensorgnome_support as sg_support
import build_openssh_portable as openssh
import build_sensorgnome_librtlsdr as sg_librtlsdr


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
    print(f"[{timestamp()}]: Starting build of Sensorgnome software packages.")
    print(f"[{timestamp()}]: Temp dir: {temp_dir}.")
    print(f"[{timestamp()}]: Output dir: {build_dir}.")
    vamp_alsa_host_version = "0.5-1"
    vamp_alsa_host.build(temp_dir, build_dir, vamp_alsa_host_version)
    vamp_plugins_version = "0.5-1"
    vamp_plugins.build(temp_dir, build_dir, vamp_plugins_version)
    sg_control_version = "0.5-1"
    sg_control.build(temp_dir, build_dir, sg_control_version)
    sg_support_version = "0.5-1"
    sg_support.build(temp_dir, build_dir, sg_support_version)
    openssh_version = "0.5-1"
    openssh.build(temp_dir, build_dir, openssh_version)
    sg_librtlsdr_version = "0.5-1"
    sg_librtlsdr.build(temp_dir, build_dir, sg_librtlsdr_version)
    print(f"[{timestamp()}]: Sensorgnome software packages successfully built.")