import git
import time
import subprocess
import sys
from os import mkdir, chdir, getcwd, path
from shutil import copyfile
from helpers import timestamp, bcolors, install_files, create_package

PROJECT = "find_tags"
REPO = "https://github.com/sensorgnome-org/find_tags.git"
BRANCH = "find_tags_unifile"


def build(temp_dir, build_output_dir, version, compiler=None, strip_bin="strip"):
    base_dir = getcwd()
    build_dir = path.join(base_dir, temp_dir, PROJECT)
    print(f"[{timestamp()}]: Starting build of {PROJECT}.")

    print(f"[{timestamp()}]: Git clone from {REPO}.")
    git.Git(path.join(base_dir, temp_dir)).clone(REPO)
    print(f"[{timestamp()}]: Git checkout branch {BRANCH}.")
    git.Git(build_dir).checkout(BRANCH)

    print(f"[{timestamp()}]: Starting make.")
    chdir(build_dir)
    if compiler:
        compiler = f"CXX={compiler}"
    make_process = subprocess.Popen(f"make clean all {compiler}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # Wait for make to finish. Maybe change to use poll()
    while make_process.stdout.readline() or make_process.stderr.readline():
        pass
    # Strip binary files.
    _ = subprocess.Popen([f"{strip_bin}", "find_tags_unifile"])
    chdir(base_dir)
    
    output_package_name = f"{PROJECT}_{version}.deb"
    print(f"[{timestamp()}]: Creating debian package at \"{path.join(build_output_dir, output_package_name)}\".")
    # Create temporary packaging directory.
    temp_package_dir = path.join(base_dir, temp_dir, f"{PROJECT}_{version}")
    mkdir(temp_package_dir)
    deb_metadata_dir = path.join(build_dir, temp_package_dir, "DEBIAN")
    mkdir(deb_metadata_dir)
    # Create control file, metadata needed for each .deb package.
    deb_protect_name = PROJECT.replace('_', '-')  # Debian doesn't allow packages with _ in the name.
    template = {
        "Package": deb_protect_name,
        "Version": version,
        "Architecture": "armhf",
        "Essential": "yes",
        "Depends": "",
        "Maintainer": "Dale Floer <dalefloer@gmail.com>",
        "Description": "Sensorgnome software to filter Lotek tags from a raw datastream.",
        }
    output = '\n'.join([f"{k}: {v}" for k, v in template.items()])
    output += '\n'  # Final newline needed at end of file.
    with open(deb_metadata_dir + "/control", 'w') as f:
        for x in output:
            f.write(x)
    # Copy files to where they should go.
    files = {
        "find_tags_unifile": [build_dir, path.join(temp_package_dir, "home", "pi", "proj", "find_tags"), 0o755],
        }
    install_files(files)
    # Finally, package our files.
    error = create_package(output_package_name, base_dir, temp_dir, temp_package_dir, build_output_dir)
    if error:
        print(f"[{timestamp()}]: Build failed with error: {bcolors.RED}{error}{bcolors.ENDC}")
    else:
        print(f"[{timestamp()}]: {bcolors.GREEN}{PROJECT} version: {version} built.{bcolors.ENDC}")
