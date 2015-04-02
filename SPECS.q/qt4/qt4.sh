# Qt initialization script (sh)

qt_prefix=`/usr/bin/pkg-config --variable=prefix QtCore`

if ! echo ${PATH} | /bin/grep -q $qt_prefix/bin ; then
   PATH=$qt_prefix/bin:${PATH}
fi

if [ -z "$QTDIR" ] ; then
	QTDIR="$qt_prefix"
	QTINC="$qt_prefix/include"
	QTLIB="$qt_prefix/lib"
	QMAKE="$qt_prefix/bin/qmake"
fi

export QTDIR QTINC QTLIB PATH QMAKE
