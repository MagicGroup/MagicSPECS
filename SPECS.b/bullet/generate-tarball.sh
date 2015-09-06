#!/bin/sh

if [ $# -ne 1 ]; then
    echo "Usage: $0 <version>"
    exit 1
fi

VERSION=$1
NAME=bullet

if [ ! -f $NAME-$VERSION.tgz ]; then
    wget "https://bullet.googlecode.com/files/$NAME-$VERSION.tgz"
fi

tar -xzvf $NAME-$VERSION.tgz
rm -f $NAME-$VERSION/*.{DLL,dll}
rm -rf $NAME-$VERSION/Demos
rm -rf $NAME-$VERSION/Extras/{CUDA,khx2dae,software_cache,sph,CDTestFramework}
rm -rf $NAME-$VERSION/Glut
rm -rf $NAME-$VERSION/build

tar -czvf $NAME-$VERSION-free.tar.gz $NAME-$VERSION

