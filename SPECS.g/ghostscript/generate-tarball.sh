#!/bin/sh

VERSION="$1"

rm -rf ghostscript-"$VERSION"
tar jxvf ghostscript-"$VERSION".tar.bz2

GS=ghostscript-"$VERSION"

# License unclear (bug #1000387).
rm -r "$GS"/jpegxr

# License unknown (bug #1149617).
## Documentation
rm -f "$GS"/contrib/japanese/doc/djgpp.txt
rm -f "$GS"/contrib/japanese/doc/gdevmag.txt
rm -f "$GS"/contrib/japanese/doc/gs261j.*
## Example code
rm -f "$GS"/examples/chess.ps
## %ram% IODevice
rm -f "$GS"/base/gsioram.c
rm -f "$GS"/base/ramfs.c
rm -f "$GS"/base/ramfs.h
sed -i -e 's, $(GLD)ramfs.dev,,' "$GS"/Makefile.in "$GS"/psi/msvc.mak

tar jcvf ghostscript-"$VERSION"-cleaned-1.tar.bz2 "$GS"
