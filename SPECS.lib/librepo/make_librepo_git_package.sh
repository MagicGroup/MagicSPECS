#!/bin/bash
git clone https://github.com/Tojaj/librepo.git  || exit 1
pushd librepo
git archive --prefix=librepo-$1/ --format=tar HEAD | xz > ../librepo-git$1.tar.xz
popd


