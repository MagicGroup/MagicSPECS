#!/bin/bash
git clone http://scm.trinitydesktop.org/scm/git/$1  || exit 1
pushd $1
sed -i 's/system@//g' .gitmodules
git submodule init  || exit 1
git submodule update || exit 1
find . -name .git|xargs rm -rf
popd
mv $1 $1-git$2
tar --remove-files -cJvf $1-git$2.tar.xz $1-git$2


