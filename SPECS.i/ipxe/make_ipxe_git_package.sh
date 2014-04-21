#!/bin/bash
git clone git://git.ipxe.org/ipxe.git || exit 1
pushd ipxe
find . -name .git|xargs rm -rf
popd
mv ipxe ipxe-git$1
tar --remove-files -cJvf ipxe-git$1.tar.xz ipxe-git$1


