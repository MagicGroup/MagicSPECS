#!/bin/bash
shopt -s nullglob
exec 2>&1
LANG=C
HR="======"
PREFIX=""
[ -d /usr/lib/pm-utils ] && PREFIX=/usr/lib/pm-utils
[ -d /usr/lib64/pm-utils ] && PREFIX=/usr/lib64/pm-utils
[ -z $PREFIX ] && echo "Unable to find pm-utils installation" 1>&2 && exit 1

if [ "$(id -u)" != "0" ]; then
  echo This utility may only be run by the root user. 1>&2
  exit 1
fi

export STASHNAME=pm-suspend

. $PREFIX/pm-functions

rm -rf "${STORAGEDIR}"
mkdir -p "${STORAGEDIR}"
[ -f "$PARAMETERS" ] || echo '' >"$PARAMETERS"

quirk_db_handler()
{
  . $PREFIX/sleep.d/98video-quirk-db-handler
  echo "location: $PM_QUIRKDB"
  [ $PM_QUIRKDB ] && ls -al $PM_QUIRKDB
  echo $HR
  echo SYS PROPS
  for q in $possible_system_properties
  do
    p=$(canonicalize_dmivar $q) || continue;
    echo "$p: `eval echo \\$$p`"
  done
}

echo SUSPEND LOG
cat /var/log/pm-suspend.log
echo $HR
echo SYS POWER
ls -lA /sys/power
echo $HR
echo SYS POWER STATE
cat /sys/power/state
echo $HR
echo SYS POWER DISK
cat /sys/power/disk
echo $HR
echo QUIRKDB
quirk_db_handler suspend
echo $HR
echo QUIRKS USED
cat $PARAMETERS
echo $HR
echo ETC PM
ls -lAR /etc/pm
for dir in /etc/pm/*
do
    echo DIR ${dir}
    for file in ${dir}/*
    do
        echo FILE $file
        cat ${file}
        echo $HR
    done
    echo $HR
done
echo UNAME
uname -a
echo $HR
echo RPM
rpm --qf '%{name}-%{version}-%{release}\n' -q kernel pm-utils hal hal-info gnome-power-manager vbetool radeontool hdparm
echo $HR
echo FEDORA RELEASE
cat /etc/fedora-release
echo $HR
