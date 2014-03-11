#!/bin/bash
git clone git://repo.or.cz/tinycc.git || exit 1
pushd tinycc
find . -name .git|xargs rm -rf
popd
mv tinycc $1-git$2
tar --remove-files -cJvf $1-git$2.tar.xz $1-git$2


