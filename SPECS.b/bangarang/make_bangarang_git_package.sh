#!/bin/bash
git clone https://git.gitorious.org/bangarang/bangarang.git || exit 1
pushd bangarang
sed -i 's/system@//g' .gitmodules
git submodule init  || exit 1
git submodule update || exit 1
find . -name .git|xargs rm -rf
popd
mv bangarang bangarang-git$1
tar --remove-files -cJvf bangarang-git$1.tar.xz bangarang-git$1


