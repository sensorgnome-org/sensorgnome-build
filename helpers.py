from datetime import datetime
from os import chdir, makedirs, path, chmod
from shutil import copyfile, copytree

"""
The purpose of this file is to contain helper functions used elsewhere.
"""

def timestamp(utc=False, colours=True):
    """
    Returns the current timestamp as a string, using 24-hour clock.
    Args:
        utc (bool, optional): Whether or not to display the time in UTC or localtime. Defaults to False.
        colours (bool, optional): Whether or not to print timestamp color. Defaults to True.
    Returns:
        Current timestamp as a string in the form of "YYYY-mm-dd hh:mm:ss".
    """
    fs = "%Y-%m-%d %H:%M:%S"
    if utc:
        ts = datetime.utcnow()
    else:
        ts = datetime.now()
    if colours:
        return f"{bcolors.BLUE}{datetime.strftime(ts ,fs)}{bcolors.ENDC}"
    else:
        return datetime.strftime(ts ,fs)

class bcolors:
    """
    Do some colouring of text.
    """
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    RED = "\033[31m"
    YELLOW = "\033[33m"
    CYAN = "\033[36m"
    MAGENTA = "\033[35m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    
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
            chmod(destination, permissions)    