#!/bin/bash

if [ -z "$1" ] ; then
    echo "Usage: $0 date, eg. 2006-05-10"
    exit 1
fi

tmp=$(mktemp -d)

trap cleanup EXIT
cleanup() {
    [ -z "$tmp" -o ! -d "$tmp" ] || rm -rf "$tmp"
}

unset CDPATH
pwd=$(pwd)
date=$1
tag=sumo-$date
tarball=xemacs-packages-extra-${date//-/}
export CVSROOT=:pserver:cvs@cvs.alioth.debian.org:/cvsroot/xemacs

# For the checkout to work, first "cvs login" with the above CVSROOT (pass:cvs)

cd $tmp

cvs -z3 checkout -r $tag packages
cd packages

cp Local.rules.template Local.rules

# Not useful on Linux
rm -rf xemacs-packages/Sun
sed -i -e 's/Sun //' xemacs-packages/Makefile

# Not built nor included in upstream Sumo, replaced by riece
rm -rf xemacs-packages/liece

# Not included in upstream Sumo
rm -rf xemacs-packages/ess

# Shouldn't ship this
rm -f xemacs-packages/games/tetris.el
sed -i -e 's/ tetris.elc//' xemacs-packages/games/Makefile
sed -i -e 's/ tetris//' -e 's/Tetris, //' xemacs-packages/games/package-info.in

# Clean up
find . -name "*.jar" -o -name "*.class" -delete
find . -name .cvsignore -o -name CVS | xargs rm -rf

cd ..
mv packages $tarball
tar cf $pwd/$tarball.tar $tarball
xz -f $pwd/$tarball.tar

cd $pwd >/dev/null
