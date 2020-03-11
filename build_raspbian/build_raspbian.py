from pathlib import Path
from os import getcwd, makedirs, chdir
from shutil import copytree, copyfile, rmtree
from distutils.dir_util import copy_tree
import git
import subprocess

import sys
sys.path.append("../")
from helpers import timestamp, bcolors


def pi_gen_setup(pi_gen_tempdir, package_dir):
    repo = "https://github.com/RPi-Distro/pi-gen.git"
    commit = "8ef3f47d7f0c6fdc722b1c3161d2502c9201bcc1"
    base_dir = getcwd()

    build_dir = pi_gen_tempdir / Path("pi-gen")
    print(f"[{timestamp()}]: Git clone from {repo}, commit: {commit[:8]}.")
    git.Git(pi_gen_tempdir).clone(repo)
    git.Git(build_dir).checkout(commit)

    print(f"[{timestamp()}]: Copying debian pacakges from `build_packages'.")
    sg_stage = build_dir / Path("stageSG")
    install_packages = sg_stage / Path("00-packages/")
    _ = copytree(package_dir, install_packages)

    print(f"[{timestamp()}]: Copying other build files.")
    build_files = Path("build_files/")
    copyfile(build_files / Path("Dockerfile"), build_dir / Path("Dockerfile"))
    copyfile(build_files / Path("config"), build_dir / Path("config"))
    _ = copytree(build_files / Path("stageSG/"), sg_stage, dirs_exist_ok=True)

    print(f"[{timestamp()}]: Changing default mirrors.")
    _ = copy_tree(str(build_files / Path("stage0/")), str(build_dir / Path("stage0")))


    print(f"[{timestamp()}]: Generating Raspbian image. This may take a while.")

    cmd = [f"./build-docker.sh"]
    chdir(build_dir)
    run = subprocess.Popen(cmd)
    exit_code = run.wait()
    if exit_code != 0:
        print(f"[{timestamp()}]: {bcolors.RED}Pi-gen build failed.{bcolors.ENDC}")
        return False
    chdir(base_dir)


if __name__ == "__main__":
    base_dir = Path(getcwd())
    temp_dir = base_dir / Path("pi-gen-temp")
    # Start from a clean slate, remove any existing build dirs.
    rmtree(temp_dir, ignore_errors=True)
    makedirs(temp_dir)

    pi_gen_setup(temp_dir, Path("../build_packages/output/"))