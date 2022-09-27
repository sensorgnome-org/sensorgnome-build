# helper functions used in top-level build.py as well as in build_packages

from datetime import datetime
import git
"""
The purpose of this file is to contain helper functions in use with various.
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

def image_name(git_hash=True):
    """
    Returns a name for the image.
    Default is of the form "Sensorgnome_YYYY-mm-dd_git-hash.img". Note that the hash is truncated to the first 8 characters.
    Args:
        git_hash (bool, optional): Include the commit hash. Defaults to True.
    Returns:
        (str) The name for the image.
    """
    repo = git.Repo('.')
    current_hash = str(repo.head.commit)[:8]
    date = datetime.strftime(datetime.utcnow(), '%Y-%m-%d')
    name = ''
    if git_hash:
        name = f"Sensorgnome_{date}_{current_hash}.img"
    else:
        name = f"Sensorgnome_{date}.img"
    return name
