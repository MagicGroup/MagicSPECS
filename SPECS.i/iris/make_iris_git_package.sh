#!/bin/bash
git clone http://github.com/psi-im/iris.git  || exit 1
pushd iris
find . -name .git|xargs rm -rf
popd
mv iris iris-git$1
tar --remove-files -cJvf iris-git$1.tar.xz iris-git$1


