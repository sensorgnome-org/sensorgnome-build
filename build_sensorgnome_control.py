import git
import time
import subprocess
import sys
from os import mkdir, chdir, getcwd, makedirs, path, chmod
from shutil import copyfile, copytree
from helpers import timestamp, bcolors

PROJECT = "sensorgnome-control"
REPO = "https://github.com/sensorgnome-org/sensorgnome-control.git"


def build(temp_dir, build_output_dir, version):
    base_dir = getcwd()
    print(f"[{timestamp()}]: Starting build of {PROJECT}.")

    print(f"[{timestamp()}]: Git clone from {REPO}.")
    git.Git(path.join(base_dir, temp_dir)).clone(REPO)

    build_dir = path.join(base_dir, temp_dir, PROJECT)    
    output_package_name = f"{PROJECT}_{version}.deb"
    print(f"[{timestamp()}]: Creating debian package at \"{path.join(build_output_dir, output_package_name)}\".")
    # Create temporary packaging directory.
    temp_package_dir = path.join(base_dir, temp_dir, f"{PROJECT}_{version}")
    mkdir(temp_package_dir)
    deb_metadata_dir = path.join(build_dir, temp_package_dir, "DEBIAN")
    mkdir(deb_metadata_dir)
    # Create control file, metadata needed for each .deb package.
    template = {
        "Package": PROJECT,
        "Version": version,
        "Architecture": "armhf",
        "Essential": "yes",
        "Depends": "nodejs, sensorgnome-support",
        "Maintainer": "Dale Floer <dalefloer@gmail.com>",
        "Description": "Sensorgnome master control process.",
        }
    output = '\n'.join([f"{k}: {v}" for k, v in template.items()])
    output += '\n'  # Final newline needed at end of file.
    with open(deb_metadata_dir + "/control", 'w') as f:
        for x in output:
            f.write(x)
    # Copy files to where they should go.
    # Dictionary of the form {"filename": ["source_path", "destination_path", "permissions"]}
    # Where source path is the path from build artifacts.
    # The destination path is the _absolute_ path to where we want the file to go.
    # Permissions are the permissions that file should have, in octal form as in Linux.
    # Todo: support owners.
    files = {
        "master/": [build_dir, path.join(temp_package_dir, "home", "pi", "proj", "sensorgnome"), None],
        }
    for file_name, file_paths in files.items():
        source = path.join(file_paths[0], file_name)
        destination = path.join(file_paths[1], file_name)
        permissions = file_paths[2]
        makedirs(file_paths[1])
        copytree(source, destination)
        if permissions is not None:  # Permissions are not supported for multiple files right now.
            chmod(destination, permissions)
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
    src = path.join(temp_dir, output_package_name)
    dest = path.join(base_dir, build_output_dir, output_package_name)
    copyfile(src, dest)
    print(f"[{timestamp()}]: {bcolors.GREEN}{PROJECT} version: {version} built.{bcolors.ENDC}")