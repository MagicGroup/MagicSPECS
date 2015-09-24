#!/bin/bash

set -e

VERSION=1.4.2

GITHUBURL=https://github.com/grosser/rack-openid/archive/v${VERSION}.zip

# download zipball
if [[ ! -f rack-openid-$VERSION.zip ]]; then
    curl -o rack-openid-$VERSION.zip -L $GITHUBURL
fi

# extract zipball
[[ -d rack-openid-$VERSION ]] && rm -r rack-openid-$VERSION
unzip rack-openid-$VERSION.zip

pushd rack-openid-$VERSION
  # repack
  tar -cJvf rack-openid-$VERSION-tests.tar.xz test
  mv rack-openid-$VERSION-tests.tar.xz ..
popd

# Clean up
rm rack-openid-$VERSION.zip
rm -r rack-openid-$VERSION
