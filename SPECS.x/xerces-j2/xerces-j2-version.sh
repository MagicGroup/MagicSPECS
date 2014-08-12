#!/bin/sh
# 
# Xerces-J2 version script
# JPackage Project (http://www.jpackage.org/)
# $Id: xerces-j2-version.sh,v 1.3 2005/05/26 14:21:22 gbenson Exp $

# Source functions library
. /usr/share/java-utils/java-functions

# Configuration
MAIN_CLASS=org.apache.xerces.impl.Version

# Set parameters
set_jvm
export CLASSPATH=$(build-classpath xerces-j2)
set_flags $BASE_FLAGS
set_options $BASE_OPTIONS

# Let's start
run "$@"
