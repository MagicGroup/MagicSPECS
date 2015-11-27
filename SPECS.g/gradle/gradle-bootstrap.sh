#!/bin/sh
# Build Gradle with plain groovyc
#
# Usage: $0 <path-to-module-list> <path-to-module-dependencies>
#
# Author: Mikolaj Izdebski <mizdebsk@redhat.com>

set -e
test $# -eq 2

LANG=en_US.utf8

# External dependencies needed by Gradle.
external_deps="
aether-ant-tasks/aether-ant-tasks
aether/aether-api
aether/aether-connector-basic
aether/aether-impl
aether/aether-spi
aether/aether-transport-classpath
aether/aether-transport-file
aether/aether-transport-http
aether/aether-transport-wagon
aether/aether-util
ant/ant
ant/ant-antlr
ant/ant-junit
ant/ant-launcher
antlr
apache-commons-collections
apache-commons-configuration
apache-commons-lang
apache-ivy/ivy
aqute-bnd/biz.aQute.bndlib
atinject
base64coder
bcpg
bcprov
bea-stax
bea-stax-api
beust-jcommander
bsf
bsh
cglib
commons-cli
commons-codec
commons-io
commons-logging
commons-lang3
dom4j
ecj
extra166y
felix/org.osgi.core
findbugs
geronimo-annotation
geronimo-jms
glassfish-servlet-api
google-gson/gson
google-guice-no_aop
gpars/gpars
groovy/groovy-all
guava
guava-jdk5
hamcrest/core
hawtjni/hawtjni-runtime
httpcomponents/httpclient
httpcomponents/httpcore
isorelax
jansi-native/jansi-native
jansi/jansi
jackson-annotations
jackson-core
jackson-databind
jarjar/jarjar
jatl
javamail/javax.mail
jaxen
jcifs
jcip-annotations
jcsp
jdom
jdom2/jdom2
jettison/jettison
jetty/jetty-annotations
jetty/jetty-jsp
jetty/jetty-plus
jetty/jetty-security
jetty/jetty-server
jetty/jetty-servlet
jetty/jetty-util
jetty/jetty-webapp
jetty/jetty-xml
jline/jline
jna
joda-convert
joda-time
js
jsr-305
jsch
junit
jzlib
kryo
kxml
kxml-min
log4j-1.2.17
maven-wagon/http
maven-wagon/http-shared
maven-wagon/provider-api
maven/maven-aether-provider
maven/maven-artifact
maven/maven-builder-support
maven/maven-compat
maven/maven-core
maven/maven-model
maven/maven-model-builder
maven/maven-plugin-api
maven/maven-repository-metadata
maven/maven-settings
maven/maven-settings-builder
minlog
msv-core
multiverse/multiverse-core
native-platform
nekohtml
netty3-3.9.3
objectweb-asm/asm-all
objenesis/objenesis
org.eclipse.sisu.plexus
org.eclipse.sisu.inject
plexus-classworlds
plexus-containers/plexus-component-annotations
plexus/interpolation
plexus/plexus-cipher
plexus/plexus-sec-dispatcher
plexus/utils
qdox
reflectasm
relaxngDatatype/relaxngDatatype
slf4j/jcl-over-slf4j
slf4j/jul-to-slf4j
slf4j/log4j-over-slf4j
slf4j/slf4j-api
snakeyaml
sonar/sonar-batch
sonar/sonar-batch-bootstrapper
sonar/sonar-core
sonar/sonar-deprecated
sonar/sonar-java-api
sonar/sonar-plugin-api
sonar/sonar-squid
stax2-api
tesla-polyglot/polyglot-common
tesla-polyglot/polyglot-groovy
testng
woodstox-core
xalan-j2
xalan-j2-serializer
xbean/xbean-reflect
xerces-j2
xml-commons-apis
xml-commons-resolver
xom
xsdlib
xstream/xstream
"

# Generate some dummy build properties - they don't need to be 100 % correct.
cat <<EOF >subprojects/core/src/main/resources/org/gradle/build-receipt.properties
buildNumber=none
buildTimestamp=20150101000000+0000
commitId=foo
hostname=localhost
isSnapshot=false
javaVersion=1.8.0
osName=Linux
osVersion=3.1.0
project=gradle
rcNumber=
username=mock
versionBase=2.0
versionNumber=2.0
EOF

rm -rf bootstrap-home
mkdir -p bootstrap-home/lib/plugins

echo "******************************"
echo "*** GRADLE BOOTSTRAP BUILD ***"
echo "******************************"

echo "== finding external dependencies..."
build-jar-repository -s -p bootstrap-home/lib/plugins $external_deps
for old in bootstrap-home/lib/plugins/*; do
    new=${old///*_//lib/plugins/}
    if [ $old != $new ]; then
        mv $old $new
    fi
done
classpath=$(build-classpath $external_deps)

dep_runtime=$(ls bootstrap-home/lib/plugins | xargs | sed s/\ /,/g)

rm -rf bootstrap-classes
mkdir bootstrap-classes

# Process all modules in topological order
for mod in $(cat "$1"); do
    classes_dir=bootstrap-classes/$mod
    resources_dir=subprojects/${mod/gradle-/}/src/main/resources
    mkdir -p $classes_dir $resources_dir

    # Find Java/Groovy sources
    srcdirs=""
    for lang in groovy java; do
	dir=subprojects/${mod/gradle-/}/src/main/$lang
	[[ -d $dir ]] && srcdirs="$srcdirs $dir"
    done

    # Compile sources if there are any (some modules have only
    # resources, but no compilable sources)
    if [[ -n "$srcdirs" ]]; then
	echo "== groovyc $mod..."
	groovyc -cp $classpath -j -J source=1.5 -J target=1.6 -d $classes_dir $(find $srcdirs -name *.java -o -name *.groovy)
    fi

    # Create JAR with classes, but not yet resources
    jar=$PWD/bootstrap-home/lib/$mod.jar
    (cd ./$classes_dir && jar cf $jar .)

    # Generate classpath.properties resource file
    sed -n "/^$mod=/{s//projects=/;p}" "$2" >$resources_dir/$mod-classpath.properties
    echo "runtime=$dep_runtime" >>$resources_dir/$mod-classpath.properties

    # Add resources to JAR
    (cd ./subprojects/${mod/gradle-/}/src/main/resources && jar uf $jar .)
    classpath=$classpath:$jar
done
