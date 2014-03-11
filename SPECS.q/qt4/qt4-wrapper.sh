#!/bin/bash

if [ -z "$QT4DIR" ] ; then
  # rpm is more correct multilib-wise, provided /etc/rpm/platform doesn't get in the way.
  QT4DIR="$(/bin/rpm --eval "%{_libdir}/qt4" 2>/dev/null || /usr/bin/pkg-config --variable=prefix QtCore )"
  export QT4DIR
fi

if ! echo ${PATH} | /bin/grep -q $QT4DIR/bin ; then
 PATH=${QT4DIR}/bin:${PATH}
 export PATH
fi

exec $QT4DIR/bin/`basename $0` ${1+"$@"}

