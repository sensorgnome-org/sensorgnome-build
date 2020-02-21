from helpers import timestamp, bcolors
from pathlib import Path
import os
import subprocess

"""
The purpose of this script is the overall runner to builid that packages to be installed on a sensorgnome,
    to generate a system image and to put them and any other supporting files together for a complete sensorgnome image.
"""

def docker_package_setup(dockerfile_location, dockcross_image):
    """
    Sets everything up needed to get the package building in docker.
    Args:
        dockerfile_location (Path): Path to the dockerfile to run.
        dockcross_image (str): Name of the dockcross image to use.
    Returns:
        Path object containing the dockcross executable script.
    """
    dockcross_exec_path = dockerfile_location / dockcross_image
    print(f"[{timestamp()}]: Creating dock-cross image.")
    build = subprocess.Popen(["docker", "build", "-t", f"{dockcross_image}", f"{dockerfile_location}"])
    exit_code = build.wait()
    if exit_code != 0:
        print(f"[{timestamp()}]: {bcolors.RED}Docker build failed.{bcolors.ENDC}")
        return False
    print(f"[{timestamp()}]: Creating dock-cross executable at: {dockcross_exec_path}")
    try:
        result = subprocess.run(["docker", "run", f"{dockcross_image}"], stdout=subprocess.PIPE)
        with open(dockcross_exec_path, 'wb') as f:
            f.write(result.stdout)
    except subprocess.CalledProcessError:
        print(f"[{timestamp()}]: {bcolors.RED}Docker run failed.{bcolors.ENDC}")

    _ = subprocess.Popen(["chmod", "+x", f"{dockcross_exec_path}"])

    return dockcross_exec_path

def docker_build_packages(dockcross_exec):
    """
    Use a created docker container to cross-compile and build the .deb packages.
    Runs build_packages/build_packages.py with (for now) hard-coded commands.
    Args:
        dockcross_exec (Path): Path to the dockcross executable script to use for cross-compiling.
    Returns:
        bool: True if the command completed successfully, False if it didn't.
    """
    cmd = [f"./{dockcross_exec} bash -c 'cd build_packages && python3.6 build_packages.py -t build-temp -o output -c $CC -p $CXX -s $STRIP -x armv7-unknown-linux-gnueabihf'"]
    print(f"command: {cmd}")
    build = subprocess.Popen(cmd, shell=True)
    exit_code = build.wait()
    if exit_code != 0:
        print(f"[{timestamp()}]: {bcolors.RED}Docker build failed.{bcolors.ENDC}")
        return False
    return True


if __name__ == "__main__":
# Start by building packages.
# The first step is to setup the dockcross container being used.
# This assumes that the image exists. See build_packages/Docker.md
    dockerfile_location = Path("build_packages/")
    dockcross_image = "sensorgnome-armv7-hf"
    dockcross_exec = docker_package_setup(dockerfile_location, dockcross_image)
    res = docker_build_packages(dockcross_exec)
    print(res)