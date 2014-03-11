#!/bin/bash

ROOTDIR_MOUNT='/etc/named /etc/pki/dnssec-keys /etc/named.root.key /etc/named.conf
/etc/named.dnssec.keys /etc/named.rfc1912.zones /etc/rndc.conf /etc/rndc.key
/usr/lib64/bind /usr/lib/bind /etc/named.iscdlv.key /run/named /var/named'

usage()
{
  echo
  echo 'This script setups chroot environment for BIND'
  echo 'Usage: setup-named-chroot.sh ROOTDIR [on|off]'
}

if ! [ "$#" -eq 2 ]; then
  echo 'Wrong number of arguments'
  usage
  exit 1
fi

ROOTDIR="$1"

# Exit if ROOTDIR doesn't exist
if ! [ -d "$ROOTDIR" ]; then
  echo "Root directory $ROOTDIR doesn't exist"
  usage
  exit 1
fi

mount_chroot_conf()
{
  if [ -n "$ROOTDIR" ]; then
    for all in $ROOTDIR_MOUNT; do
      # Skip nonexistant files
      [ -e "$all" ] || continue

      # If mount source is a file
      if ! [ -d "$all" ]; then
        # mount it only if it is not present in chroot or it is empty
        if ! [ -e "$ROOTDIR$all" ] || [ `stat -c'%s' "$ROOTDIR$all"` -eq 0 ]; then
          touch "$ROOTDIR$all"
          mount --bind "$all" "$ROOTDIR$all"
        fi
      else
        # Mount source is a directory. Mount it only if directory in chroot is
        # empty.
        if [ -e "$all" ] && [ `ls -1A $ROOTDIR$all | wc -l` -eq 0 ]; then
          mount --bind --make-private "$all" "$ROOTDIR$all"
        fi
      fi
    done
  fi
}

umount_chroot_conf()
{
  if [ -n "$ROOTDIR" ]; then
    for all in $ROOTDIR_MOUNT; do
      # Check if file is mount target. Do not use /proc/mounts because detecting
      # of modified mounted files can fail.
      if mount | grep -q '.* on '"$ROOTDIR$all"' .*'; then
        umount "$ROOTDIR$all"
        # Remove temporary created files
        [ -f "$all" ] && rm -f "$ROOTDIR$all"
      fi
    done
  fi
}

case "$2" in
  on)
    mount_chroot_conf
    ;;
  off)
    umount_chroot_conf
    ;;
  *)
    echo 'Second argument has to be "on" or "off"'
    usage
    exit 1
esac

exit 0
