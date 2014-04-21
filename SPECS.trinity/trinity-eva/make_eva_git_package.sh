#!/bin/bash
git clone git://github.com/MagicGroup/eva.git  || exit 1
mv eva $1-git$2
tar --remove-files -cJvf $1-git$2.tar.xz $1-git$2
