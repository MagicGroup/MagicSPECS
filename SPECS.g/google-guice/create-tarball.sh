#!/bin/sh
set -e -x
test $# -eq 1
test ! -d sisu-guice
git clone git://github.com/sonatype/sisu-guice.git
cd ./sisu-guice
git checkout sisu-guice-${1}
git branch unbundled-guice-${1}
git checkout unbundled-guice-${1}
rm -rf $(ls . | grep -E -v 'core|extensions|pom|COPYING')
find . -name "*.jar" -delete
find . -name "*.class" -delete
git commit -a -m "Remove unneeded stuff"
git tag unbundled-${1}
git archive --format=tar --prefix=google-guice-${1}/ unbundled-${1} \
    | xz >../google-guice-${1}.tar.xz
