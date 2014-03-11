#!/bin/bash
git clone git://github.com/Pulse-Eight/libcec.git  || exit 1
pushd $1
git archive --prefix=libcec-$2/ --format=tar HEAD | xz > ../$1-$2.tar.xz
popd


