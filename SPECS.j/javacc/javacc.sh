#!/bin/sh
# 
# JavaCC script
# JPackage Project <http://www.jpackage.org/>

# Source functions library
if [ -f /usr/share/java-utils/java-functions ] ; then 
  . /usr/share/java-utils/java-functions
else
  echo "Can't find function library, aborting"
  exit 1
fi

# Configuration
MAIN_CLASS=javacc
BASE_JARS="javacc.jar"

# Set parameters
set_jvm
set_classpath $BASE_JARS
set_flags $BASE_FLAGS
set_options $BASE_OPTIONS

# Let's start
run "$@"
