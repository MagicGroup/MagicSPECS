#!/bin/bash
git clone --depth 1 git://git.videolan.org/ffmpeg.git ffmpeg || exit 1
pushd ffmpeg
find . -name .git|xargs rm -rf
popd
tar --remove-files -cJvf mplayer-ffmpeg.tar.xz ffmpeg


