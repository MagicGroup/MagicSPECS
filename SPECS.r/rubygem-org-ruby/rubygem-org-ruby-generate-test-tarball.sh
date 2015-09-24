#!/bin/bash

set -e

VERSION=0.9.12

GITHUBURL=https://github.com/wallyqs/org-ruby/archive/version-${VERSION}.zip

# download zipball
if [[ ! -f org-ruby-$VERSION.zip ]]; then
    curl -o org-ruby-$VERSION.zip -L $GITHUBURL
fi

# extract zipball
[[ -d org-ruby-version-$VERSION ]] && rm -r org-ruby-version-$VERSION
unzip org-ruby-$VERSION.zip

pushd org-ruby-version-$VERSION
  # repack
  tar -cJvf org-ruby-$VERSION-tests.tar.xz spec
  mv org-ruby-$VERSION-tests.tar.xz ..
popd

# Clean up
rm org-ruby-$VERSION.zip
rm -r org-ruby-version-$VERSION
