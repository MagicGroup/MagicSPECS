#!/bin/bash
svn checkout http://libyuv.googlecode.com/svn/trunk/ libyuv || exit 1
mv libyuv libyuv-svn$1
tar --remove-files -cJvf libyuv-svn$1.tar.xz libyuv-svn$1
