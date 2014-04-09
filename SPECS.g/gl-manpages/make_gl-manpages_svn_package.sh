#!/bin/bash
TODAY=$!
DIR=gl-manpages-1.1-$TODAY
mkdir -p $DIR
for MAN in man4 man3 man manglsl ; do
        svn co --username anonymous --password anonymous https://cvs.khronos.org/svn/repos/ogl/trunk/ecosystem/public/sdk/docs/$MAN/ $DIR/$MAN
done
find $DIR -name .svn | xargs rm -rf
tar cJf $DIR.tar.xz $DIR
