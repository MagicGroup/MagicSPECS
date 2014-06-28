#!/bin/bash
git clone git://git.linphone.org/srtp.git || exit 1
mv srtp srtp-git$1
tar --remove-files -cJvf srtp-git$1.tar.xz srtp-git$1


