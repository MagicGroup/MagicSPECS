#!/bin/bash

set -e

tmp=$(mktemp -d)

trap cleanup EXIT
cleanup() {
    set +e
    [ -z "$tmp" -o ! -d "$tmp" ] || rm -rf "$tmp"
}

unset CDPATH
pwd=$(pwd)
date=$(date +%Y%m%d)
package=libcrystalhd
svn={$date}
svn=HEAD

cd "$tmp"
svn export --force https://xbmc.svn.sourceforge.net/svnroot/xbmc/trunk/lib/libcrystalhd/ ${package}-${date}
tar cJf "$pwd"/${package}-${date}.tar.xz ${package}-${date}
cd - >/dev/null
