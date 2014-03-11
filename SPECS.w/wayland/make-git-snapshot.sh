#!/bin/sh

# Usage: ./make-git-snapshot.sh [COMMIT]
#
# to make a snapshot of the given tag/branch.  Defaults to HEAD.
# Point env var REF to a local repo to reduce clone time.

DIRNAME=wayland-$( date +%Y%m%d )
REPO=wayland

echo REF ${REF:+--reference $REF}
echo DIRNAME $DIRNAME
echo HEAD ${1:-HEAD}

rm -rf $DIRNAME

git clone ${REF:+--reference $REF} \
	git://git.freedesktop.org/git/wayland/${REPO}/ $DIRNAME/${REPO}/
GIT_DIR=$DIRNAME/${REPO}/.git git archive --format=tar --prefix=${REPO}-${DIRNAME#wayland-}/ ${1:-HEAD} \
	| bzip2 > ${REPO}-${DIRNAME#wayland-}.tar.bz2

# rm -rf $DIRNAME
