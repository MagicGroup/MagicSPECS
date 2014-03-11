#!/bin/bash

if [ -z "$1" -o $# -ne 1 ]; then
  echo "Usage: $0 <xine-version>"
  exit 2
fi

version=$1
tarball="xine-lib-$version.tar.xz"
dir="xine-lib-$version"
modtarball="xine-lib-$version-pruned.tar.xz"


if [ ! -f $tarball ]; then
  echo "Can't find $tarball !"
  exit 1
fi

echo "Uncompressing $tarball..."
rm -rf $dir
tar -xJf $tarball
cd $dir

rmpluglib()
{
    echo "removing src/$1/$2..."
    rm -rf src/$1/$2
    sed -i -e "s/SUBDIRS = \(.*\)$2\(.*\)/SUBDIRS = \1\2/g" src/$1/Makefile.am
    sed -i -e "/^src\/$1\/$2/d" configure.ac
}

# Main libraries
for remove in libfaad libffmpeg libmad libmpeg2 libmpeg2new dxr3 liba52 libdts; do
    echo "removing src/$remove..."
    rm -rf src/$remove 
    sed -i -e "/$remove/d" src/Makefile.am
    sed -i -e "/^src\/$remove/d" configure.ac
done
# Input plugin libraries
for remove in vcd; do
    rmpluglib input vcd
done
for remove in ffmpeg; do
    rmpluglib combined ffmpeg
done
# Input plugins
for p in dvd vcd mms; do
  echo "removing $p input plugin..."
  # Remove sources
  for sourcefile in `awk '/^xineplug_inp_'$p'_la_SOURCES/ { $1=""; $2=""; print $0}' src/input/Makefile.am`; do
      if [ "`grep -v '^EXTRA_DIST = ' src/input/Makefile.am | grep -c $sourcefile`" -le 1 ]; then # if this file is only used for this plugin
          rm -f src/input/$sourcefile
      fi
  done
  # Remove from Makefile
  sed -i -e "/xineplug_inp_$p/d" src/input/Makefile.am
done
# Demuxers
# These are ok now ( http://bugzilla.redhat.com/213597 )
#for p in mpeg mpeg_block mpeg_ts mpeg_elem mpeg_pes yuv4mpeg2; do
#  echo "removing $p demuxer..."
#  [ -f src/demuxers/demux_$p.c ] && rm -f src/demuxers/demux_$p.c
#  sed -i -e "/xineplug_dmx_$p/d" src/demuxers/Makefile.am
#done
# Postprocessors
echo "removing planar and deinterlace postprocessors..."
sed -i -e 's/deinterlace //g' src/post/Makefile.am # see comments in speedy.c
sed -i -e 's/planar //g' src/post/Makefile.am # requires libpostproc
sed -i -e '/post\/\(deinterlace\|planar\)/d' configure.ac
rm -rf src/post/{deinterlace,planar}
# NSF decoder
echo "removing NSF decoder..."
rm -rf src/libxineadec/{nosefart,nsf.c}
sed -i -e '/^xineplug_decode_nsf_la/,/^\s*$/d' \
       -e /xineplug_decode_nsf/d \
       -e 's/ nosefart//' \
       src/libxineadec/Makefile.am
sed -i -e '/nosefart\/Makefile/d' configure.ac
# Patches for forbidden libraries
rm -fv misc/lib*.patch win32/scripts/*.patch

# All clean !

cd ..
echo "Generating $modtarball..."
tar -cJf $modtarball $dir
rm -rf $dir
