#!/bin/bash
svn co https://multiget.svn.sourceforge.net/svnroot/multiget $1-svn$2
pushd $1-svn$2
find . -name .svn|xargs rm -rf
popd
tar --remove-files -cJvf $1-svn$2.tar.xz $1-svn$2


