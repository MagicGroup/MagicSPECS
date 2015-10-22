#!/bin/bash -e

if [ "$#" != 2 ]; then
    echo "Usage: $0 date revision, eg. 2014-06-30 832449bdc11b"
    exit 1
fi

tmp=$(mktemp -d)

trap cleanup EXIT
cleanup() {
    [ -z "$tmp" -o ! -d "$tmp" ] || rm -rf "$tmp"
}

unset CDPATH
pwd=$PWD
date=$1
tag=$2
tarball=xemacs-packages-extra-${date//-/}

pushd $tmp > /dev/null
hg clone https://bitbucket.org/xemacs/xemacs-packages
cd xemacs-packages
cp -p Local.rules.template Local.rules

# Not useful on Linux
rm -rf xemacs-packages/Sun
sed -i -e 's/Sun //' xemacs-packages/Makefile
sed -i -e '/Sun/d' package-compile.el

# Not built nor included in upstream Sumo, replaced by riece
rm -rf xemacs-packages/liece

# Not included in upstream Sumo
rm -rf xemacs-packages/ess

# Shouldn't ship this for trademark reasons
rm -f xemacs-packages/games/tetris.el
sed -i -e 's/ tetris.elc//' xemacs-packages/games/Makefile
sed -i -e 's/ tetris//' -e 's/Tetris, //' xemacs-packages/games/package-info.in

# Clean up
find . -name "*.jar" -o -name "*.class" -delete
find . -name .hg\* | xargs rm -fr

# Make the tarball
cd ..
mv xemacs-packages $tarball
tar cf $pwd/$tarball.tar $tarball
xz -9f $pwd/$tarball.tar
popd > /dev/null
