#!/bin/bash
svn co svn://username@openbios.org/openbios/trunk/openbios-devel || exit 1
mv openbios-devel openbios-svn$1
tar --remove-files -cJvf openbios-svn$1.tar.xz openbios-svn$1
