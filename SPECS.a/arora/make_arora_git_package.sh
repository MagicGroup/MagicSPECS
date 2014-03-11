#!/bin/bash
git clone git://github.com/Arora/arora.git || exit 1
mv arora arora-git$1
tar --remove-files -cJvf arora-git$1.tar.xz arora-git$1
