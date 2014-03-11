#!/bin/bash
svn co svn://anonsvn.kde.org/home/kde/branches/trinity/dependencies/arts $1-svn$2
pushd $1-svn$2
find . -name .svn|xargs rm -rf
popd
tar --remove-files -cJvf $1-svn$2.tar.xz $1-svn$2


