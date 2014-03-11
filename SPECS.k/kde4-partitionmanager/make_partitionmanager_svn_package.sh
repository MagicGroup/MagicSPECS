#!/bin/bash
svn co svn://anonsvn.kde.org/home/kde/trunk/extragear/sysadmin/partitionmanager/ || exit 1
mv partitionmanager $1-svn$2
tar --remove-files -cJvf $1-svn$2.tar.xz $1-svn$2
