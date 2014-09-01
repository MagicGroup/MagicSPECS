#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Usage: ./create-tarball.sh VERSION"
    exit 1
fi

VERSION=${1}
NAME="cobertura"

wget http://downloads.sourceforge.net/${NAME}/${NAME}-${VERSION}-src.tar.bz2
tar xvf ${NAME}-${VERSION}-src.tar.bz2
rm ${NAME}-${VERSION}-src.tar.bz2
# remove unneeded stuff
find ./${NAME}-${VERSION}/lib/ -type f -delete
find ./${NAME}-${VERSION}/antLibrary/common -type f -delete
# this directory contains some files under non-free license (#850481)
# these files are probably not copyrightable, but since we don't need them,
# we can remove them
find ./${NAME}-${VERSION}/etc/dtds/ -type f -delete

tar czvf ${NAME}-${VERSION}-clean.tar.gz ./${NAME}-${VERSION}

