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
tarball=xemacs-packages-base-${date//-/}
cvs="cvs -z3 -d:pserver:cvs@cvs.alioth.debian.org:/cvsroot/xemacs"

# For the checkout to work, first "cvs login" with the above CVSROOT (pass:cvs)

cd $tmp

$cvs export -r $tag package-ctlfile
cp packages/Local.rules.template packages/Local.rules
$cvs export -r $tag standard-Makefile mule-Makefile
pushd packages/xemacs-packages >/dev/null

# the meat of xemacs-packages-base:
$cvs export -r $tag efs xemacs-base
cd ../mule-packages
$cvs export -r $tag mule-base

# build dependencies:
cd ../xemacs-packages
$cvs export -r $tag apel dired fsf-compat
sed -i -e 's/ prog-modes//' dired/Makefile

popd >/dev/null
mv packages $tarball
tar cf $pwd/$tarball.tar $tarball
xz -f $pwd/$tarball.tar

cd $pwd
