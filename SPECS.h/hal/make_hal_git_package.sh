#!/bin/bash
git clone git://anongit.freedesktop.org/hal  || exit 1
pushd hal
find . -name .git|xargs rm -rf
popd
mv hal hal-git$1
tar --remove-files -cJvf hal-git$1.tar.xz hal-git$1

