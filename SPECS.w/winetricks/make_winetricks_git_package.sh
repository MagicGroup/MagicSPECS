#!/bin/bash
git clone https://github.com/hillwoodroc/winetricks-zh.git || exit 1
mv winetricks-zh winetricks-git$1
tar --remove-files -cJvf winetricks-git$1.tar.xz winetricks-git$1
