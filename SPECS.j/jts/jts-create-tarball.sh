#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Usage: ./create-sources VERSION"
    exit 1
fi

VERSION=${1}
NAME="jts"
svn checkout http://svn.code.sf.net/p/jts-topo-suite/code/tags/Version_${VERSION}/${NAME}/  ${NAME}-${VERSION}
cd ${NAME}-${VERSION}
wget http://repo1.maven.org/maven2/com/vividsolutions/${NAME}/${VERSION}/${NAME}-${VERSION}.jar
jar -xf ${NAME}-${VERSION}.jar
mv META-INF/maven/com.vividsolutions/jts/pom.xml .
sed -i 's|/Users/michael/coding/jts/jts-topo-suite/tags/Version_1.13/jts|${basedir}|' pom.xml
rm -Rf com META-INF .svn
find . -name "*.jar" -delete
find . -name "*.class" -delete
find . -name "*.bat" -delete
cd ..

tar cJf ${NAME}-${VERSION}.tar.xz ./${NAME}-${VERSION}