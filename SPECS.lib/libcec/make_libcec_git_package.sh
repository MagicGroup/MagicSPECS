#!/bin/bash
git clone git://github.com/Pulse-Eight/libcec.git  || exit 1
pushd libcec
git archive --prefix=libcec-$1/ --format=tar HEAD | xz > ../libcec-$1.tar.xz
popd


