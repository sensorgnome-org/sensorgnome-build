import git
import time
import subprocess
import sys
from os import mkdir, chdir, getcwd, path
from shutil import copyfile
from package_helpers import timestamp, bcolors, install_files, create_package

PROJECT = "vamp-alsa-host"
REPO = "https://github.com/sensorgnome-org/vamp-alsa-host"


def build(temp_dir, build_output_dir, version, compiler=None, strip_bin="strip"):
    base_dir = getcwd()
    print(f"[{timestamp()}]: Starting build of {PROJECT}.")

    print(f"[{timestamp()}]: Git clone from {REPO}.")
    git.Git(path.join(base_dir, temp_dir)).clone(REPO)

    print(f"[{timestamp()}]: Starting make.")
    build_dir = path.join(base_dir, temp_dir, PROJECT)
    chdir(build_dir)
    if compiler:
        compiler = f"CXX={compiler}"
    make_process = subprocess.Popen("make clean all {compiler};", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # Wait for make to finish. Maybe change to use poll()
    while make_process.stdout.readline() or make_process.stderr.readline():
        pass
    # Strip binary files.
    _ = subprocess.Popen(["strip", "vamp-alsa-host"])
    chdir(base_dir)
    
    output_package_name = f"{PROJECT}_{version}.deb"
    print(f"[{timestamp()}]: Creating debian package at \"{path.join(build_output_dir, output_package_name)}\".")
    # Create temporary packaging directory.
    temp_package_dir = path.join(base_dir, f"{build_dir}_{version}")
    mkdir(temp_package_dir)
    deb_metadata_dir = path.join(base_dir, temp_package_dir, "DEBIAN")
    mkdir(deb_metadata_dir)
    # Create control file, metadata needed for each .deb package.
    template = {
        "Package": PROJECT,
        "Version": version,
        "Architecture": "armhf",
        "Essential": "yes",
        "Depends": "libboost-filesystem-dev, libboost-system-dev, libboost-thread-dev, libasound2-dev, libvamp-hostsdk3v5, libfftw3-dev",
        "Maintainer": "Dale Floer <dalefloer@gmail.com>",
        "Description": "ALSA support for hosting vamp audio plugins for Sensorgnome.",
        }
    output = '\n'.join([f"{k}: {v}" for k, v in template.items()])
    output += '\n'  # Final newline needed at end of file.
    with open(deb_metadata_dir + "/control", 'w') as f:
        for x in output:
            f.write(x)
    # Copy files to where they should go.
    files = {
        "vamp-alsa-host": [build_dir, path.join(temp_package_dir, "usr", "bin"), 0o755],
        }
    install_files(files)
    # Finally, package our files.
    # Finally, package our files.
    error = create_package(output_package_name, base_dir, temp_dir, temp_package_dir, build_output_dir)
    if error:
        print(f"[{timestamp()}]: Build failed with error: {bcolors.RED}{error}{bcolors.ENDC}")
    else:
        print(f"[{timestamp()}]: {bcolors.GREEN}{PROJECT} version: {version} built.{bcolors.ENDC}")