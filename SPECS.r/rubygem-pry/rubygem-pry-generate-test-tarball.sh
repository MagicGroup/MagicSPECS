#!/bin/bash

set -e

VERSION=0.10.1

GITHUBURL=https://github.com/pry/pry/archive/v${VERSION}.zip

# download zipball
if [[ ! -f pry-$VERSION.zip ]]; then
    curl -o pry-$VERSION.zip -L $GITHUBURL
fi

# extract zipball
[[ -d pry-$VERSION ]] && rm -r pry-$VERSION
unzip pry-$VERSION.zip

pushd pry-$VERSION
  # repack
  tar -cJvf pry-$VERSION-tests.tar.xz spec
  mv pry-$VERSION-tests.tar.xz ..
popd

# Clean up
rm pry-$VERSION.zip
rm -r pry-$VERSION
