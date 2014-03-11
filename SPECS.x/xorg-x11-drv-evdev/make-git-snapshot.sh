#!/bin/sh

DIRNAME=xf86-input-evdev-$( date +%Y%m%d )

rm -rf $DIRNAME
git clone git://git.freedesktop.org/git/xorg/driver/xf86-input-evdev $DIRNAME
cd $DIRNAME
if [ -z "$1" ]; then
    git log | head -1
else
    git checkout $1
fi
git log | head -1 | awk '{ print $2 }' > ../commitid
git repack -a -d
cd ..
tar jcf $DIRNAME.tar.bz2 $DIRNAME
rm -rf $DIRNAME
