from os import symlink, listdir
from pathlib import Path
import subprocess

if __name__ == "__main__":
    """
    Simple script to create the symlinks needed for building using crosstool-ng in the Docker container.
    """
    # These are the directories (trailing /) or files to symlink.
    include_symlinks = ["vamp-hostsdk/", "vamp-sdk/", "vamp/", "alsa/", "boost/", "fftw3.h", "sqlite3.h", "vamp/vamp.h", "zlib.h", "openssl/", "libusb-1.0/"]
    # These are the libraries we want to match. This is set up this way so that, for example, "libasound" matches "libasound.so" and "libasound.so.1" etc.
    libs_symlinks = ["libfftw3", "libvamp", "libasound", "libboost_", "libusb", "libudev", "libsqlite3", "libz", "libcrypto", "libssl"]

    #include_symlink_dest = "/usr/xcc/armv7-unknown-linux-gnueabihf/lib/gcc/armv7-unknown-linux-gnueabihf/8.3.0/include/"
    include_symlink_dest = "/usr/xcc/armv7-unknown-linux-gnueabi/armv7-unknown-linux-gnueabi/sysroot/usr/include/"
    include_symlink_src = "/usr/include/"

    lib_symlink_dest = "/usr/xcc/armv7-unknown-linux-gnueabi/armv7-unknown-linux-gnueabi/sysroot/usr/lib/"
    lib_symlink_src = "/usr/lib/arm-linux-gnueabihf/"
    lib_symlink_src_2 = "/lib/arm-linux-gnueabihf/"

    for x in include_symlinks:
        # symlink(include_symlink_src + x, include_symlink_dest)
        _ = subprocess.Popen(["ln", "-s", f"{include_symlink_src + x}", f"{include_symlink_dest}"])

    special_handling = [
        [f"/usr/include/arm-linux-gnueabihf/openssl/opensslconf.h", f"{include_symlink_dest}openssl/opensslconf.h"]]
    for e in special_handling:
        x, y = e
        _ = subprocess.Popen(["ln", "-s", x, y])

    ls = listdir(lib_symlink_src)
    to_link = [x for x in ls for y in libs_symlinks if y in x]
    for x in to_link:
        # symlink(lib_symlink_src + x, lib_symlink_dest)
        _ = subprocess.Popen(["ln", "-s", f"{lib_symlink_src + x}", f"{lib_symlink_dest}"])

    ls = listdir(lib_symlink_src_2)
    to_link = [x for x in ls for y in libs_symlinks if y in x]
    for x in to_link:
        _ = subprocess.Popen(["ln", "-s", f"{lib_symlink_src_2 + x}", f"{lib_symlink_dest}"])
