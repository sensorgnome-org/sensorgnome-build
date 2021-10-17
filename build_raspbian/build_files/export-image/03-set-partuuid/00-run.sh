#!/bin/bash -e

IMG_FILE="${STAGE_WORK_DIR}/${IMG_FILENAME}${IMG_SUFFIX}.img"

IMGID="$(dd if="${IMG_FILE}" skip=440 bs=1 count=4 2>/dev/null | xxd -e | cut -f 2 -d' ')"

BOOT_PARTUUID="${IMGID}-01"
ROOT_PARTUUID="${IMGID}-02"
DATA_PARTUUID="${IMGID}-03"

sed -i "s/BOOTDEV/PARTUUID=${BOOT_PARTUUID}/" "${ROOTFS_DIR}/etc/fstab"
sed -i "s/ROOTDEV/PARTUUID=${ROOT_PARTUUID}/" "${ROOTFS_DIR}/etc/fstab"

# Need to add this manually.
echo "Adding /data mount to fstab."
echo "PARTUUID=${DATA_PARTUUID}  /data           vfat    defaults          0       2" >> "${ROOTFS_DIR}/etc/fstab"

sed -i "s/ROOTDEV/PARTUUID=${ROOT_PARTUUID}/" "${ROOTFS_DIR}/boot/cmdline.txt"

# Commented out in favor of using symlinks (simpler)
# Bind mount so that this behaves the same as the existing SG.
# This behaviour will go away.
#
#echo "# Temporary /boot bind mounts for compatibility." >> "${ROOTFS_DIR}/etc/fstab"
#echo "/data/SGdata    /boot/SGdata    none    bind" >> "${ROOTFS_DIR}/etc/fstab"
#echo "/data/config    /boot/uboot    none    bind" >> "${ROOTFS_DIR}/etc/fstab"
