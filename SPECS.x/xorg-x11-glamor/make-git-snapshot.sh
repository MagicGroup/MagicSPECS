#!/bin/sh

# Usage: ./make-git-snapshot.sh [COMMIT]
#
# to make a snapshot of the given tag/branch.  Defaults to HEAD.
# Point env var REF to a local glamor repo to reduce clone time.

if [ -z "$1" ] ; then
	echo "Please supply short git commit id"
	exit 1
fi

DIRNAME=xorg-x11-glamor-$( date +%Y%m%d )git$1

echo REF ${REF:+--reference $REF}
echo DIRNAME $DIRNAME
echo HEAD ${1:-HEAD}

rm -rf $DIRNAME

git clone --depth 1 -b master ${REF:+--reference $REF} \
	git://git.freedesktop.org/git/xorg/driver/glamor $DIRNAME

GIT_DIR=$DIRNAME/.git git archive --format=tar --prefix=$DIRNAME/ ${1:-HEAD} \
	| xz > $DIRNAME.tar.xz

# rm -rf $DIRNAME
