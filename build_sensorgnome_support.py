import git
import time
import subprocess
import sys
from os import mkdir, chdir, getcwd, makedirs, path, chmod
from shutil import copyfile, copytree
from helpers import timestamp, bcolors

PROJECT = "sensorgnome-support"
REPO = "https://github.com/sensorgnome-org/sensorgnome-support.git"


def build(temp_dir, build_output_dir, version):
    base_dir = getcwd()
    print(f"[{timestamp()}]: Starting build of {PROJECT}.")

    print(f"[{timestamp()}]: Git clone from {REPO}.")
    git.Git(path.join(base_dir, temp_dir)).clone(REPO)

    # print(f"[{timestamp()}]: Starting make.")
    # build_dir = path.join(base_dir, temp_dir, PROJECT, "overlays")
    # chdir(build_dir)
    # make_process = subprocess.Popen("make all;", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # # Wait for make to finish. Maybe change to use poll()
    # while make_process.stdout.readline() or make_process.stderr.readline():
    #     pass
    # # Strip binary files.
    # _ = subprocess.Popen(["strip", "lotek-plugins.so"])
    # chdir(base_dir)

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
        "Depends": "perl, awk, python, bash",
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
        "scripts/": [build_dir, path.join(temp_package_dir, "home", "pi", "proj", "sensorgnome"), None],
        "udev-rules/usb-hub-devices.rules": [build_dir, path.join(temp_package_dir, "etc", "udev", "rules.d"), None],
        "root/etc/": [build_dir, path.join(temp_package_dir, "etc"), None],
        # "root/dev/sdcard/uboot/network.txt": [build_dir, path.join(temp_package_dir, "boot"), None],
        # todo: Handle overlays.
        # todo: Handle GESTURES.TXT too.
        }
    for file_name, file_paths in files.items():
        split_name = path.split(file_name)[-1]
        dest_name = file_name
        if split_name != '':
            dest_name = split_name
        source = path.join(file_paths[0], file_name)
        destination = path.join(file_paths[1], dest_name)
        permissions = file_paths[2]
        try:
            makedirs(file_paths[1])
        except FileExistsError:
            pass  # Directory was already created in a previous batch.
        # Handle copy of single file differently than copy of a directory + contents.
        try:
            copyfile(source, destination)
        except IsADirectoryError:
            copytree(source, destination)
        if permissions is not None:  # Permissions are not supported for multiple files right now.
            chmod(destination, permissions)
    # Note: There may need to be a post-install trigger to run "udevadm control --reload-rules".
    # However, udev should detect that the rules have been changed and reload them itself.  

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