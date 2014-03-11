#!/bin/bash
git clone git://anongit.freedesktop.org/$1  || exit 1
pushd $1
find . -name .git|xargs rm -rf
popd
mv $1 $1-git$2
tar --remove-files -cJvf $1-git$2.tar.xz $1-git$2

