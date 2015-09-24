#!/bin/sh
set -x

ORIGDIR=$(pwd)

DIR=$(mktemp -p /tmp -d tmp.XXXXXX)
pushd $DIR
git clone https://github.com/rcairo/rcairo.git
cd rcairo

VERSION=$(gem build cairo.gemspec 2>&1 | sed -n -e 's|^.*Version: ||p')
GITHASH=$(git log | head -n 1 | sed -e 's|^.* \(..........\).*|\1|')
cp -p cairo-$VERSION.gem $ORIGDIR/cairo-$VERSION-$GITHASH.gem

popd
rm -rf $DIR
