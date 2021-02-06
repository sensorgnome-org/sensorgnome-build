from os import chdir, makedirs, path, chmod, chown, walk, listdir
from pathlib import Path
from os import environ,getcwd
from shutil import copyfile, copytree, copy2
import subprocess

import sys
sys.path.append("../")
from helpers import *

"""
The purpose of this file is to contain helper functions used elsewhere.
"""


def install_files(files):
    """
    Install files given in the files dict to their locations relative to base_dir.
    Todo: support setting owner as ["user", "group"]. This is hardcoded to 0 and 0.
    Args:
        files (dict): Dictionary of the form {"filename": ["source_path", "destination_path", "permissions"]}
            Note that "filename" can be a file or a directory.
            Source path is the path from build artifacts.
            Destination path is the _absolute_ path to where we want the file to go.
            Permissions are the permissions that file should have, in octal form as in Linux.
    """
    for file_name, file_paths in files.items():
        split_name = path.split(file_name)[-1]
        dest_name = file_name
        if split_name != '':
            dest_name = split_name
        source = path.join(file_paths[0], file_name)
        permissions = file_paths[2]
        try:
            makedirs(file_paths[1])
        except FileExistsError:
            pass  # Directory was already created in a previous batch.
        # Handle copy of single file differently than copy of a directory + contents.
        try:
            destination = path.join(file_paths[1], dest_name)
            copyfile(source, destination)
        except IsADirectoryError:
            destination = file_paths[1]
            copytree2(source, destination)
        if permissions is not None:
            recursive_chmod(destination, permissions)
        # Hardcoded 0:0 (root:root) for now.
        recursive_chown(destination, 0, 0)


def copytree2(source, destination, symlinks=False, ignore=None):
    """
    Copytree that behaves like it has Python 3.8's dirs_exist_ok set.
    Args:
        source (Path): Source path.
        destination (Path): Destination path.
        symlink (bool, optional): As in stock copytree. Defaults to False.
        ignore (calleable, optional): As in stock copytree. Defaults to None.
    """
    for item in listdir(source):
        src = path.join(source, item)
        dst = path.join(destination, item)
        if path.isdir(src):
            copytree(src, dst, symlinks, ignore)
        else:
            copy2(src, dst)


def recursive_chmod(base_path, permissions):
    """
    Recursively chmod files and directories from the given base path, including the root.
    If the base path is a file, then operate on just that file.
    Args:
        base_path (path): Path to start chmod from.
        permissions (int): Octal permissions to set.
    """
    if path.isfile(base_path):
        chmod(base_path, permissions)
    else:
        for dir_path, _, file_names in walk(base_path):
            chmod(dir_path, permissions)
            for file in file_names:
                chmod(path.join(dir_path, file), permissions)


def recursive_chown(base_path, user_id=0, group_id=0):
    """
    Recursively chown files and directories from the given base path, including the root.
    If the base path is a file, then operate on just that file.
    Args:
        base_path (path): Path to start chmod from.
        user_id (int, optional): User ID (uid) to set. Defaults to 0.
        group_id (int, optional): Group ID (gid) to set. Defaults to 0.
    """
    #getUser = lambda: environ["USERNAME"] if "C:" in getcwd() else environ["USER"]
    if path.isfile(base_path):
        chown(base_path, uid=user_id, gid=group_id)
    else:
        for dir_path, _, file_names in walk(base_path):
            chown(dir_path, uid=user_id, gid=group_id)
            for file in file_names:
                chown(path.join(dir_path, file), uid=user_id, gid=group_id)


def create_package(output_package_name, base_dir, temp_dir, temp_package_dir, build_output_dir):
    """
    Create the package from the build artifacts from previous steps.
    Args:
        output_package_name (str): Full name of the output package.
        base_dir (path): The base directory that build.py is run from.
        temp_dir (path): The temporary directory where build artifacts are.
        temp_package_dir (path): The directory where all the files needed for packaging live, in their proper structure for a .deb package.
        build_output_dir (path): The directory where the finished package should be output.
    Returns:
        bool: False if no errors occurred, otherwise an error message. In this case, the error message is straight from dpkg-deb if one occurs.
    """
    dpkg_cmd = f"dpkg-deb --build {temp_package_dir}"
    dpkg_process = subprocess.Popen(dpkg_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # Wait for dpkg-deb to finish.
    while True:
        line = dpkg_process.stdout.readline()
        err =  dpkg_process.stderr.readline()
        if err:
            return err.decode('ascii') # Should probably raise an exception here.
        elif line == b'' and err == b'':
            break
    # Finally, copy the finished package to the output dir.
    src = path.join(temp_dir, output_package_name)
    dest = path.join(base_dir, build_output_dir, output_package_name)
    copyfile(src, dest)
    return False

def make_subprocess(make_command, show_debug="no", errors="console"):
    """
    Runs make in a subprocess given a command. Can optionally show debug info and errors.
    Args:
        make_command (str): Command to pass to make.
        show_debug (str, optional): Whether or not to show debug information. Defaults to no.
            Three possible values, "no" shows no debug into, "console" prints to stdout, and "file" (currently not implememented) writes to a log file.
        errors (str, optional): Wheter ot not to show errors. Defaults to "show".
            Three possible values, "no" effectively ignores errors, "console" prints to stdout and file (not implemented yet) writes to a lot file.
    Returns:
        Tuple, with the first being a bool that's true if no errors happened and the second being a dict of {"debug": str, "error": str} data.
    """
    debug = f"Running '{make_command}'.\n"
    error = ''
    if show_debug == "file" or errors == "file":
        raise NotImplementedError
    elif show_debug == "console":
        print(debug, end='')
    make_process = subprocess.Popen(f"{make_command}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = make_process.communicate()
    exit_code = make_process.wait()
    debug += out.decode("ascii")
    error += err.decode("ascii")
    if show_debug == "console":
        print(debug)
    if errors == "conole":
        print(error)
    res = True
    if exit_code != 0:
        res = False
    return res, {"debug": debug, "error": error}


def create_repo_files(package_dir=Path("output/")):
    """
    Creates the Packages.gz file needed to use the output packages as a repo for installing packages from.
    """
    output_path = package_dir / Path("Packages.gz")
    subprocess.run([f"dpkg-scanpackages {package_dir} /dev/null | gzip > {output_path}"], shell=True)
