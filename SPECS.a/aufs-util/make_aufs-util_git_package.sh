#!/bin/bash
rm -rf aufs-util.git
git clone git://aufs.git.sourceforge.net/gitroot/aufs/aufs-util.git \
	aufs-util.git || exit 1
pushd aufs-util.git
git checkout origin/aufs3.2
popd
pushd aufs-util.git
find . -name .git|xargs rm -rf
popd
mv aufs-util.git aufs-util-git$1
tar --remove-files -cJvf aufs-util-git$1.tar.xz aufs-util-git$1


