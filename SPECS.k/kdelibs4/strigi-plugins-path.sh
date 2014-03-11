#!/bin/sh
# since kde4 prefix is different with strigi prefix
# the default strigi can not recognize kde4 strigi plugins
# so we adjust the env to make strigi work properly --- nihui, Sep.9th, 2010
STRIGI_PLUGIN_PATH=${STRIGI_PLUGIN_PATH}:/usr/lib/strigi:/opt/kde4/lib/strigi
export STRIGI_PLUGIN_PATH

