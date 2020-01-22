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
    parser.add_argument('-x', '--cpp-compiler', dest="cpp_compiler", help="Path to C++ compiler binary or binary in PATH.", metavar="COMPILER", required=False, default='')
    parser.add_argument('-s', '--strip', dest="strip_bin", help="Path to strip binary or binary in PATH.", metavar="STRIP", required=False, default="strip")
    parser.add_argument('-t', '--temp', dest="temp_dir", help="Path of the temporary work directory.", metavar="PATH", required=True)
    parser.add_argument('-o', '--output', dest="output_dir", help="Path of the package output directory.", metavar="PATH", required=True)
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    options = parse_command_line()
    temp_dir = options.temp_dir
    build_dir = options.output_dir
    c_compiler = options.c_compiler
    cpp_compiler = options.cpp_compiler
    strip_bin = options.strip_bin
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
    vamp_alsa_host_version = "0.5-1"
    vamp_alsa_host.build(temp_dir, build_dir, vamp_alsa_host_version, cpp_compiler, strip_bin)
    vamp_plugins_version = "0.5-1"
    vamp_plugins.build(temp_dir, build_dir, vamp_plugins_version, cpp_compiler, strip_bin)
    sg_control_version = "0.5-1"
    sg_control.build(temp_dir, build_dir, sg_control_version, cpp_compiler, strip_bin)
    sg_support_version = "0.5-1"
    sg_support.build(temp_dir, build_dir, sg_support_version, cpp_compiler, strip_bin)
    openssh_version = "0.5-1"
    openssh.build(temp_dir, build_dir, openssh_version, cpp_compiler, strip_bin)
    sg_librtlsdr_version = "0.5-1"
    sg_librtlsdr.build(temp_dir, build_dir, sg_librtlsdr_version, cpp_compiler, strip_bin)
    fcd_version = "0.5-1"
    fcd.build(temp_dir, build_dir, fcd_version, c_compiler, strip_bin)
    find_tags_version = "0.5-1"
    find_tags.build(temp_dir, build_dir, find_tags_version)
    print(f"[{timestamp()}]: Sensorgnome software packages successfully built.")
