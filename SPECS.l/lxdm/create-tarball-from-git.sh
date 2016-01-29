#!/bin/sh

set -e
set -x

CURRENTDIR=$(pwd)

TMPDIR=$(mktemp -d /var/tmp/lxdm-XXXXXX)
pushd $TMPDIR

GITSCM=git://git.lxde.org/lxde/lxdm.git

git clone $GITSCM
pushd lxdm

COMMIT=$(git log | head -n 1 | sed -e 's|^.*[ \t]||')
SHORTCOMMIT=$(echo $COMMIT | cut -c-8)
DATE=$(git show --format=%ci $COMMIT | head -n 1 | sed -e 's|[ \t].*$||')
SHORTDATE=$(echo $DATE | sed -e 's|-||g')
VERSION=$(cat configure.ac | grep AC_INIT | sed -n -e 's|^.*\[\([0-9\.][0-9\.]*\)*\],.*$|\1|p')

echo "VERSION=$VERSION"
echo "COMMIT=$COMMIT"
echo "DATE=$DATE"

echo
popd

TARDIR=lxdm-${VERSION}-D${SHORTDATE}git${SHORTCOMMIT}
ln -sf lxdm $TARDIR
tar cjf ${TARDIR}.tar.bz2 ${TARDIR}/./ 

mv ${TARDIR}.tar.bz2 ${CURRENTDIR}/
popd

rm -rf $TMPDIR

