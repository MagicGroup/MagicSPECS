#!/bin/bash
svn co https://multiget.svn.sourceforge.net/svnroot/multiget multiget-svn$1 || exit 1
pushd multiget-svn$1
find . -name .svn|xargs rm -rf
popd
tar --remove-files -cJvf multiget-svn$1.tar.xz multiget-svn$1


