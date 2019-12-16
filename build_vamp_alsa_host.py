import git
import time
import subprocess
import sys
from os import mkdir, chdir, getcwd, makedirs, path
from shutil import copyfile
from helpers import timestamp, bcolors

PROJECT = "vamp-alsa-host"
REPO = "https://github.com/sensorgnome-org/vamp-alsa-host"


def build(temp_dir, build_output_dir, version):
    base_dir = getcwd()
    print(f"[{timestamp()}]: Starting build of {PROJECT}.")

    print(f"[{timestamp()}]: Git clone from {REPO}.")
    git.Git(path.join(base_dir, temp_dir)).clone(REPO)

    print(f"[{timestamp()}]: Starting make.")
    build_dir = path.join(base_dir, temp_dir, PROJECT)
    chdir(build_dir)
    make_process = subprocess.Popen("make clean all;", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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
        "Depends": "libboost-filesystem-dev, libboost-system-dev, libboost-thread-dev, libasound2.dev, libvamp-hostsdk3v5, libfftw3-dev",
        "Maintainer": "Dale Floer <dalefloer@gmail.com>",
        "Description": "ALSA support for hosting vamp audio plugins for Sensorgnome.",
        }
    output = '\n'.join([f"{k}: {v}" for k, v in template.items()])
    output += '\n'  # Final newline needed at end of file.
    with open(deb_metadata_dir + "/control", 'w') as f:
        for x in output:
            f.write(x)
    # Copy files to where they should go.
    # Dictionary of the form {"filename": ["source_path", "destination_path"]}
    # Where source path is the path from build artifacts.
    # And the destination path is the _absolute_ path to where we want the file to go.
    # Todo: support perms and owners.
    files = {
        "vamp-alsa-host": [build_dir, path.join(temp_package_dir, "usr", "bin")],
        }
    for file_name, file_paths in files.items():
        source = path.join(file_paths[0], file_name)
        destination = path.join(file_paths[1], file_name)
        makedirs(file_paths[1])
        copyfile(source, destination)
    # Finally, package our files.
    dpkg_cmd = f"dpkg-deb --build {temp_package_dir}"
    dpkg_process = subprocess.Popen(dpkg_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # Wait for make to finish.
    while True:
        line = dpkg_process.stdout.readline()
        err =  dpkg_process.stderr.readline()
        if err:
            print(f"[{timestamp()}]: {bcolors.RED}{err.decode('ascii')}{bcolors.ENDC}")
            break
             # Should probably raise an exception here.
        elif line == b'' and err == b'':
            break
    # Finally, copy the finished package to the output dir.
    src = path.join(base_dir, temp_dir, output_package_name)
    dest = path.join(base_dir, build_output_dir, output_package_name)
    copyfile(src, dest)
    print(f"[{timestamp()}]: {bcolors.GREEN}{PROJECT} version: {version} built.{bcolors.ENDC}")