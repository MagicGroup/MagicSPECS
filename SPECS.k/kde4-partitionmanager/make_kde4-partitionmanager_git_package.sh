#!/bin/bash
git clone git://anongit.kde.org/partitionmanager.git || exit 1
mv partitionmanager kde4-partitionmanager-git$1
tar --remove-files -cJvf kde4-partitionmanager-git$1.tar.xz kde4-partitionmanager-git$1
