from os import chdir, makedirs, path, chmod, walk
from shutil import copyfile, copytree
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
    Todo: support setting owner as ["user", "group"].
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
            recursive_chmod(destination, permissions)
            
def recursive_chmod(base_path, permissions):
    """
    Recursively chmod files and directories from the given base path, including the root.
    Args:
        base_path (path): Path to start chmod from.
        permissions (int): Octal permissions to set.
    """
    for dir_path, _, file_names in walk(base_path):
        chmod(dir_path, permissions)
        for file in file_names:
            chmod(path.join(dir_path, file), permissions)

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
