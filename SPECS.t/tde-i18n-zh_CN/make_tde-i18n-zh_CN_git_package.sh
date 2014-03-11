#!/bin/bash
git clone http://scm.trinitydesktop.org/scm/git/tde-i18n  || exit 1
pushd tde-i18n
sed -i 's/system@//g' .gitmodules
git submodule init  || exit 1
git submodule update || exit 1
find . -name .git|xargs rm -rf
popd
cp -rfL tde-i18n/tde-i18n-zh_CN $1-git$2
tar --remove-files -cJvf $1-git$2.tar.xz $1-git$2


