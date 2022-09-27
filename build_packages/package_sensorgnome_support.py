import git
import time
import subprocess
import sys
from os import mkdir, chdir, getcwd, path
from shutil import copyfile
from package_helpers import timestamp, bcolors, install_files, create_package, make_subprocess, copytree2

PROJECT = "sensorgnome-support"
REPO = "https://github.com/sensorgnome-org/sensorgnome-support.git"
BRANCH = "systemd"
# To use a local copy of the repo instead of the remote git repo set SRCDIR
SRCDIR = None # None, abs path, or path relative to build_packages dir
SRCDIR = "/mnt/sensorgnome-support"


def build(temp_dir, build_output_dir, version, compiler=None, strip_bin="strip", host=''):
    base_dir = getcwd()
    build_dir = path.join(base_dir, temp_dir, PROJECT)
    print(f"[{timestamp()}]: Starting build of {PROJECT}.")

    if SRCDIR:
        print(f"[{timestamp()}]: Copying {PROJECT} from {SRCDIR}")
        copytree2(SRCDIR, path.join(base_dir, temp_dir, PROJECT))
    else:
        print(f"[{timestamp()}]: Git clone from {REPO}.")
        git.Git(path.join(base_dir, temp_dir)).clone(REPO)
        print(f"[{timestamp()}]: Git checkout branch {BRANCH}.")
        git.Git(build_dir).checkout(BRANCH)

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
        "Depends": "perl, awk, python, bash, libjson-perl, vsftpd, udhcpc, autossh, hostapd",
        "Maintainer": "Dale Floer <dalefloer@gmail.com>",
        "Description": "Sensorgnome support scripts and services.",
        }
    output = '\n'.join([f"{k}: {v}" for k, v in template.items()])
    output += '\n'  # Final newline needed at end of file.
    with open(deb_metadata_dir + "/control", 'w') as f:
        for x in output:
            f.write(x)
    # Copy files to where they should go.
    files = {
        "scripts/": [build_dir, path.join(temp_package_dir, "home", "pi", "proj", "sensorgnome", "scripts"), 0o755],
        "udev-rules/usb-hub-devices.rules": [build_dir, path.join(temp_package_dir, "etc", "udev", "rules.d"), None],
        "root/etc/": [build_dir, path.join(temp_package_dir, "etc"), None],
        "systemd-services/": [build_dir, path.join(temp_package_dir, "lib", "systemd", "system"), None],
        # "root/dev/sdcard/uboot/network.txt": [build_dir, path.join(temp_package_dir, "boot"), None],
        # todo: Handle overlays.
        # todo: Handle GESTURES.TXT too.
        }
    install_files(files)
    # Note: There may need to be a post-install trigger to run "udevadm control --reload-rules".
    # However, udev should detect that the rules have been changed and reload them itself.

    # Finally, package our files.
    error = create_package(output_package_name, base_dir, temp_dir, temp_package_dir, build_output_dir)
    if error:
        print(f"[{timestamp()}]: Build failed with error: {bcolors.RED}{error}{bcolors.ENDC}")
        return False
    else:
        print(f"[{timestamp()}]: {bcolors.GREEN}{PROJECT} version: {version} built.{bcolors.ENDC}")
        return True
