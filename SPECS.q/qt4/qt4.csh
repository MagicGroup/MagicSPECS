# Qt initialization script (csh)

set qt_prefix = `/usr/bin/pkg-config --variable=prefix QtCore`

if ( "${path}" !~ *$qt_prefix/bin* ) then
   set path = ( $qt_prefix/bin $path )
endif

if ( $?QTDIR ) then
   exit
endif

setenv QTDIR $qt_prefix
setenv QTINC $qt_prefix/include
setenv QTLIB $qt_prefix/lib
setenv QMAKE $qt_prefix/bin/qmake
