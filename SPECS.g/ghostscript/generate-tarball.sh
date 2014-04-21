#!/bin/sh

VERSION=$1

rm -rf ghostscript-$VERSION
tar jxvf ghostscript-$VERSION.tar.bz2
rm -r ghostscript-$VERSION/jpegxr
tar jcvf ghostscript-$VERSION-cleaned.tar.bz2 ghostscript-$VERSION
