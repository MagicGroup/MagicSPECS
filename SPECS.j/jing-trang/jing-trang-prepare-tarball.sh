#!/bin/sh

set -e

release=${1:-\
    $(rpm -q --specfile --qf='%{VERSION}\n' jing-trang.spec | head -n 1)}

rm -rf jing-trang-$release
svn export http://jing-trang.googlecode.com/svn/tags/V$release \
    jing-trang-$release
tar cv jing-trang-$release --exclude "*.jar" --exclude gcj \
    --exclude mod/datatype/src/main/org | \
    xz --best > jing-trang-$release.tar.xz
