#!/bin/bash

# Wrapper for the %find_lang macro which splits out the various translations in per-target lists

/usr/lib/rpm/find-lang.sh $*
if test $? != 0 ; then
    exit 1
fi

PACKAGE_NAME=$2
targets=`rpm --eval '%{mingw_build_targets}'`
for target in $targets; do
	prefix=`rpm --eval "%{${target}_prefix}"`
	cat $2.lang | grep "$prefix" > ${target}-$PACKAGE_NAME.lang
done

exit 0
