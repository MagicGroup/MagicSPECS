#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Usage: ./create-tarball.sh VERSION"
    exit 1
fi

VERSION=${1}
NAME="junit"

wget https://github.com/${NAME}-team/${NAME}/archive/r${VERSION}.tar.gz
tar xvf r${VERSION}.tar.gz

(
  cd ${NAME}-r${VERSION}
  find . -name "*.jar" -delete
  find . -name "*.class" -delete
)

tar czvf ${NAME}-${VERSION}-clean.tar.gz ${NAME}-r${VERSION}
rm -Rf ${NAME}-${VERSION}.tar.gz

