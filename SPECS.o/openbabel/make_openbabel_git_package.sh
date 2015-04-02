#!/bin/bash
git clone git://github.com/openbabel/openbabel.git || exit 1
mv openbabel openbabel-git$1
tar --remove-files -cJvf openbabel-git$1.tar.xz openbabel-git$1
