#!/bin/bash
if [ -z "$1" ] ; then
        echo "使用方法：$0 新版本号"
        exit 1
fi
pushd $(dirname $0)
sed -i "s/Version:.*/Version:\t$1/g" gammu.spec
popd
