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
tarball=xemacs-packages-base-${date//-/}

pushd $tmp > /dev/null
hg clone https://bitbucket.org/xemacs/xemacs-packages
cd xemacs-packages
cp -p Local.rules.template Local.rules

# Save the only xemacs-packages dirs we want to build
mkdir save
mv xemacs-packages/{Makefile,apel,dired,efs,fsf-compat,xemacs-base} save
rm -fr xemacs-packages
mv save xemacs-packages

# Save the only mule-packages dirs we want to build
mkdir save
mv mule-packages/{Makefile,mule-base} save
rm -fr mule-packages
mv save mule-packages

# Break an unneeded build dependency
sed -i 's/ prog-modes//' xemacs-packages/dired/Makefile

# Remove the mercurial files
find . -name .hg\* | xargs rm -fr

# Make the tarball
cd ..
mv xemacs-packages $tarball
tar cf $pwd/$tarball.tar $tarball
xz -9f $pwd/$tarball.tar
popd > /dev/null
