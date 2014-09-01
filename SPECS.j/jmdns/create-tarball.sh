#!/bin/bash

version=$(sed -n 's/Version:\s*\(.*\)$/\1/p' *.spec)
echo "Version: $version"

rm -Rf jmdns-${version}
svn checkout https://jmdns.svn.sourceforge.net/svnroot/jmdns/tags/jmdns-${version} jmdns-${version}
pushd jmdns-${version}
find . -name .svn -exec rm -Rf {} +
rm -Rf .classpath clover.license.txt jmdns.* lib/ devdocs/ fulllogging.properties
rm -Rf checkstyle.xml .settings .project src/site/
popd
tar czvf jmdns-${version}.tar.gz jmdns-${version}

