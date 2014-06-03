#!/bin/bash
git clone git://anongit.kde.org/k3b || exit 1
mv k3b kde4-k3b-git$1
tar --remove-files -cJvf kde4-k3b-git$1.tar.xz kde4-k3b-git$1
