import git
import time
import subprocess
import sys
from os import mkdir, chdir, getcwd, path
from shutil import copyfile
from package_helpers import timestamp, bcolors, install_files, create_package, make_subprocess

PROJECT = "sensorgnome-openssh-portable"
REPO = "https://github.com/sensorgnome-org/sensorgnome-openssh-portable.git"


def build(temp_dir, build_output_dir, version, compiler=None, strip_bin="strip"):
    host = "armv7-unknown-linux-gnueabihf"  # ToDo: temporary to get things working, this will break non cross-compile builds.
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
    autoreconf_process = subprocess.Popen("autoreconf", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # Wait for autoreconf to finish running.
    while autoreconf_process.stdout.readline() or autoreconf_process.stderr.readline():
        pass

    if compiler:
        compiler = f"CXX={compiler}"
    # --host is needed for cross-compiling. --disable-strip is needed because there doesn't seem to be a way to override the strip binary.
    # AR= may also be needed for cross-compilation.
    configure_command = f"./configure --host {host} {compiler} --disable-strip"
    success, info = make_subprocess(configure_command, show_debug="no", errors="console")
    if not success and host != "armv7-unknown-linux-gnueabihf":
        print(f"[{timestamp()}]: Configure failed with error: {bcolors.RED}\n{info['error']}{bcolors.ENDC}")
        return False
    elif host == "armv7-unknown-linux-gnueabihf":  # suppress warnings if we're running configure crosscompiling.
        print(f"[{timestamp()}]: {bcolors.YELLOW}Configure had suppressed errors.{bcolors.ENDC} This is normal in a cross-compile.")

    print(f"[{timestamp()}]: Starting make.")
    make_command = f"make clean install-nosysconf DESTDIR={temp_package_dir}"
    success, info = make_subprocess(make_command, show_debug="no", errors="console")
    if not success:
        print(f"[{timestamp()}]: Build failed with error: {bcolors.RED}\n{info['error']}{bcolors.ENDC}")
        return False
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
        "Description": "Patched version of OpenSSH to allow single mapped ports in config files.",
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
