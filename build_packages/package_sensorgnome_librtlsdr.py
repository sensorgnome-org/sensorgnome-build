import git
import time
import subprocess
import sys
from os import mkdir, chdir, getcwd, path
from shutil import copyfile
from package_helpers import timestamp, bcolors, install_files, create_package, make_subprocess

PROJECT = "sensorgnome-librtlsdr"
REPO = "https://github.com/sensorgnome-org/sensorgnome-librtlsdr.git"


def build(temp_dir, build_output_dir, version, compiler=None, strip_bin="strip", host=''):
    base_dir = getcwd()
    print(f"[{timestamp()}]: Starting build of {PROJECT}.")

    print(f"[{timestamp()}]: Git clone from {REPO}.")
    git.Git(path.join(base_dir, temp_dir)).clone(REPO)

    print(f"[{timestamp()}]: Starting configure.")
    build_dir = path.join(base_dir, temp_dir, PROJECT)
    chdir(build_dir)
    # Create temporary packaging directory.
    temp_package_dir = path.join(base_dir, temp_dir, f"{PROJECT}_{version}")
    mkdir(temp_package_dir)
    autoreconf_command = "autoreconf -i"
    success, info = make_subprocess(autoreconf_command, show_debug="no", errors="console")

    # Workaround for cross-compilation not being able to find libusb unless explicity directed to it.
    configure_flags = ''
    if host == "armv7-unknown-linux-gnueabi":
        configure_flags = "LIBUSB_CFLAGS=-I/usr/xcc/armv7-unknown-linux-gnueabi/armv7-unknown-linux-gnueabi/sysroot/usr/include/libusb-1.0 LIBUSB_LIBS=-L/usr/xcc/armv7-unknown-linux-gnueabi/armv7-unknown-linux-gnueabi/sysroot/usr/lib/ LDFLAGS=-lusb-1.0"

    if host:
        host = f"--host {host}"
    if compiler:
        compiler = f"CXX={compiler}"
    configure_command = f"./configure --build=x86_64-unknown-linux-gnu {host} {compiler} {configure_flags}"
    success, info = make_subprocess(configure_command, show_debug="np", errors="console")
    if not success:
        print(f"[{timestamp()}]: Configure failed with error: {bcolors.RED}\n{info['error']}{bcolors.ENDC}")
        return False
    print(f"[{timestamp()}]: Starting make.")
    make_command = f"make install DESTDIR={temp_package_dir}"
    success, info = make_subprocess(make_command, show_debug="no", errors="console")
    if not success:
        print(f"[{timestamp()}]: Build failed with error: {bcolors.RED}\n{info['error']}{bcolors.ENDC}")
        return False
    libtool_process = subprocess.Popen(f"libtoolize --finish {temp_package_dir}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # Wait for libtool to finish.
    while libtool_process.stdout.readline() or libtool_process.stderr.readline():
        pass
    chdir(base_dir)

    output_package_name = f"{PROJECT}_{version}.deb"
    print(f"[{timestamp()}]: Creating debian package at \"{path.join(build_output_dir, output_package_name)}\".")
    deb_metadata_dir = path.join(build_dir, temp_package_dir, "DEBIAN")
    mkdir(deb_metadata_dir)
    # Create control file, metadata needed for each .deb package.
    template = {
        "Package": PROJECT,
        "Version": version,
        "Architecture": "armhf",
        "Essential": "yes",
        "Depends": "",
        "Maintainer": "Dale Floer <dalefloer@gmail.com>",
        "Description": "Patched version of librtlsdr with SensorGnome enhancements.",
        }
    output = '\n'.join([f"{k}: {v}" for k, v in template.items()])
    output += '\n'  # Final newline needed at end of file.
    with open(deb_metadata_dir + "/control", 'w') as f:
        for x in output:
            f.write(x)
    # Don't need to copy files as they're already done in the makefile for the project.
    # Finally, package our files.
    error = create_package(output_package_name, base_dir, temp_dir, temp_package_dir, build_output_dir)
    if error:
        print(f"[{timestamp()}]: Build failed with error: {bcolors.RED}{error}{bcolors.ENDC}")
        return False
    else:
        print(f"[{timestamp()}]: {bcolors.GREEN}{PROJECT} version: {version} built.{bcolors.ENDC}")
        return True
