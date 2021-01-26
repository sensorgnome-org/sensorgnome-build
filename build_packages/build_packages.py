from os import mkdir, rmdir
from shutil import rmtree
import argparse

from package_helpers import bcolors, timestamp
import package_vamp_alsa_host as vamp_alsa_host
import package_vamp_plugins as vamp_plugins
import package_sensorgnome_control as sg_control
import package_sensorgnome_support as sg_support
import package_openssh_portable as openssh
import package_sensorgnome_librtlsdr as sg_librtlsdr
import package_fcd as fcd
import package_find_tags as find_tags

def parse_command_line():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--c-compiler', dest="c_compiler", help="Path to C compiler binary or binary in PATH.", metavar="COMPILER", required=False, default='')
    parser.add_argument('-p', '--cpp-compiler', dest="cpp_compiler", help="Path to C++ compiler binary or binary in PATH.", metavar="COMPILER", required=False, default='')
    parser.add_argument('-s', '--strip', dest="strip_bin", help="Path to strip binary or binary in PATH.", metavar="STRIP", required=False, default="strip")
    parser.add_argument('-t', '--temp', dest="temp_dir", help="Path of the temporary work directory.", metavar="PATH", required=True)
    parser.add_argument('-o', '--output', dest="output_dir", help="Path of the package output directory.", metavar="PATH", required=True)
    parser.add_argument('-x', '--host', dest="xcc_host", help="Cross compiler host name, such as 'armv7-unknown-linux-gnueabihf'.", metavar="HOST_STRING", required=False, default='')
    args = parser.parse_args()
    return args


def build(temp_dir, build_dir, c_compiler=None, cpp_compiler=None, strip_bin=None, xcc_host=None):
    """
    Runner function that handles building all of the Sensorgnome packages.
    Args:
        temp_dir (Path): Path to the temporary directory, that will be used tfor building and temporary build artifacts.
        build_dir (Path): Path to the output directory for finished .deb packages.
        c_compiler (Path, optional): Path to the gcc executable. Default: None.
        cpp_compiler (Path, optional): Path to the g++ executable. Default: None.
        strip_bin (Path, optional): Path to the strip executable. Default: None.
        xcc_host (str, optional): GCC compiler triplet, needed if cross-compiling. Default: None.
"""
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
    if c_compiler:
        print(f"[{timestamp()}]: Overriding C compiler: {c_compiler}.")
    if cpp_compiler:
        print(f"[{timestamp()}]: Overriding C++ compiler: {cpp_compiler}.")
    if strip_bin != "strip":
        print(f"[{timestamp()}]: Overriding strip binary: {strip_bin}.")
    if xcc_host:
        print(f"[{timestamp()}]: Overriding cross-compile host: {xcc_host}.")
    vamp_alsa_host_version = "0.5-1"
    build_success = {}
    build_success["vamp-alsa-host"] = vamp_alsa_host.build(temp_dir, build_dir, vamp_alsa_host_version, cpp_compiler, strip_bin, xcc_host)
    vamp_plugins_version = "0.5-1"
    build_success["vamp-plugins"] = vamp_plugins.build(temp_dir, build_dir, vamp_plugins_version, cpp_compiler, strip_bin, xcc_host)
    sg_control_version = "0.5-1"
    build_success["sensorgnome-control"] = sg_control.build(temp_dir, build_dir, sg_control_version, cpp_compiler, strip_bin, xcc_host)
    sg_support_version = "0.5-1"
    build_success["sensorgnome-support"] = sg_support.build(temp_dir, build_dir, sg_support_version, cpp_compiler, strip_bin, xcc_host)
    openssh_version = "0.5-1"
    build_success["sensorgnome-openssh"] = openssh.build(temp_dir, build_dir, openssh_version, cpp_compiler, strip_bin, xcc_host)
    sg_librtlsdr_version = "0.5-1"
    build_success["sensorgnome-librtlsdr"] = sg_librtlsdr.build(temp_dir, build_dir, sg_librtlsdr_version, cpp_compiler, strip_bin, xcc_host)
    fcd_version = "0.5-1"
    build_success["fcd"] = fcd.build(temp_dir, build_dir, fcd_version, c_compiler, strip_bin, xcc_host)
    find_tags_version = "0.5-1"
    build_success["find_tags"] = find_tags.build(temp_dir, build_dir, find_tags_version, cpp_compiler, strip_bin, xcc_host)

    if all(build_success.values()):
        print(f"[{timestamp()}]: Cleaning up temporary build files.")
        rmtree(temp_dir)
        print(f"[{timestamp()}]: {bcolors.GREEN}Sensorgnome software packages successfully built.{bcolors.ENDC}")
        return True
    else:
        print(f"[{timestamp()}]: {bcolors.RED}Sensorgnome software packages failed build.{bcolors.ENDC}")
        return False


if __name__ == "__main__":
    options = parse_command_line()
    temp_dir = options.temp_dir
    build_dir = options.output_dir
    c_compiler = options.c_compiler
    cpp_compiler = options.cpp_compiler
    strip_bin = options.strip_bin
    xcc_host = options.xcc_host

    _ = build(temp_dir, build_dir, c_compiler=c_compiler, cpp_compiler=cpp_compiler, strip_bin=strip_bin, xcc_host=xcc_host)