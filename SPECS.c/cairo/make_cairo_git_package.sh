#!/bin/bash
git clone git://anongit.freedesktop.org/git/cairo
./autogen.sh --enable-gtk-doc --enable-test-surfaces --enable-full-testing
make -j4
make dist
mv cairo-1.13.1.tar.xz cairo-1.13.1-`git rev-parse --short HEAD`.tar.xz
