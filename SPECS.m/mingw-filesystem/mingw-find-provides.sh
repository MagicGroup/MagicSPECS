#!/bin/bash

# This script reads filenames from STDIN and outputs any relevant provides
# information that needs to be included in the package.

targets=$@
if [ -z "$targets" ] ; then
    echo "Usage: $0 [ mingw32 ] [ mingw64 ]"
    exit 1
fi

filelist=`sed "s/['\"]/\\\&/g"`

dlls=$(echo $filelist | tr [:blank:] '\n' | grep '\.dll$')

for f in $dlls; do
    basename=`basename $f | tr [:upper:] [:lower:]`
    for target in $targets; do
        host_triplet=`rpm --eval "%{${target}_target}"`
        [[ $f =~ .*$host_triplet.* ]] && echo "$target($basename)"
    done
done

exit 0
