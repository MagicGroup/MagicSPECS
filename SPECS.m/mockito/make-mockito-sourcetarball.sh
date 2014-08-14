#!/bin/sh
#set -x

VERSION=1.9.0
SRCDIR=mockito-${VERSION}

hg clone https://code.google.com/p/mockito/ ${SRCDIR}
pushd $SRCDIR
hg archive --prefix ${SRCDIR} -t tar -r ${VERSION} ../${SRCDIR}.tar
popd

rm -rf ${SRCDIR}

tar -xf ${SRCDIR}.tar
pushd ${SRCDIR}
rm -rf `find -name *.jar` build.gradle cglib-and-asm doc gradle gradlew gradlew.bat
dos2unix `find -name *.java`
popd

tar -cvJf mockito-${VERSION}.tar.xz ${SRCDIR}
