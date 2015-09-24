#!/bin/sh

# script to remove files with unclear / non-free licenses from
# the original gem file
#
# usage: VERSION=<version> ./<this_file>

set -x
set -e
umask 0022

VERSION=${VERSION:-0.8.0}
URL=https://rubygems.org/gems

wget -N $URL/opengl-$VERSION.gem
CURRENT_DIR=$(pwd)

TMPDIR=$(mktemp -d /tmp/opengl-XXXXXX)
pushd $TMPDIR

gem unpack $CURRENT_DIR/opengl-$VERSION.gem
cd opengl-$VERSION

gem spec -l --ruby $CURRENT_DIR/opengl-$VERSION.gem > opengl.gemspec

# Cleanup
sed -i \
	-e 's|"examples/NeHe/[^"][^"]*",||g' \
	-e 's|"examples/misc/fbo_test.rb",||' \
	opengl.gemspec
rm -rf examples/NeHe/
rm -f examples/misc/fbo_test.rb

gem build opengl.gemspec
mv opengl-$VERSION.gem $CURRENT_DIR/opengl-$VERSION-clean.gem

popd
rm -rf $TMPDIR
