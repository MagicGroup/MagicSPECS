#!/bin/sh
PCKGDIR=/work/mBuild/SOURCES/
cd  ${PCKGDIR}smplayer/smplayer/trunk/
./get_svn_revision.sh
SVN_REVISION=`cat svn_revision | sed -e 's/SVN-/svn./g'`
SMPVERSION=`cat src/version.cpp | grep "#define VERSION " | sed -e 's/#define VERSION "//g' -e 's/ /_/g' -e 's/"$//g'`
svn export . /tmp/smplayer-${SMPVERSION}.0.${SVN_REVISION} >/dev/null
cd /tmp
tar cjf smplayer-${SMPVERSION}.0.${SVN_REVISION}.tar.bz2 smplayer-${SMPVERSION}.0.${SVN_REVISION}/
rm -r /tmp/smplayer-${SMPVERSION}.0.${SVN_REVISION}
cp /tmp/smplayer-${SMPVERSION}.0.${SVN_REVISION}.tar.bz2 ${PCKGDIR}
echo "Created ${PCKGDIR}smplayer-${SMPVERSION}.0.${SVN_REVISION}.tar.bz2 !"
