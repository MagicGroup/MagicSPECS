#!/bin/sh

set -e

# Prune content from upstream tarball:
# https://www.redhat.com/archives/fedora-legal-list/2009-February/msg00015.html

date="19991224"
url="http://www.w3.org/TR/1999/REC-html401-$date/html40.tgz"

mkdir html401-dtds
cd html401-dtds

curl -O $url
tar zxf $(basename $url)
rm -r $(find . -maxdepth 1 -mindepth 1 -type d) $(basename $url)

cd ..
tar jcvf html401-dtds-$date.tar.bz2 html401-dtds
rm -r html401-dtds
