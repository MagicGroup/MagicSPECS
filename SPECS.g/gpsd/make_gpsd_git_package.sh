#!/bin/bash
git clone git://git.sv.gnu.org/gpsd.git || exit 1
pushd gpsd
find . -name .git|xargs rm -rf
popd
mv gpsd gpsd-git$1
tar --remove-files -cJvf gpsd-git$1.tar.xz gpsd-git$1


