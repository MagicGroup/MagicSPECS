%define git 1
%define gitdate 20121102

%define qt_dirname tqt-3.4
%define qtdir /opt/trinity/lib/%{qt_dirname}

# define to enable immodule -- Rex
%define immodule 0

# 64bit arch
%define arch64 x86_64 s390x ppc64

# build Motif extention
%define motif_extention 0 

# buildstatic: Build libs for static linking
# TODO: static build broken, don't enable until fixed. -- Rex
%define buildstatic 0 

# Build SQL plugins
%define buildSQL 0
%define buildsqlite 0
%if %{buildsqlite}
%define plugins_sql -enable-sql -plugin-sql-sqlite
%endif

# define to use the dlopen-opengl optimization  -- Rex
%define dlopen_opengl -dlopen-opengl

# Build QT styles into -styles subpkg
%define styleplugins 0 

# visibility
%define enable_hidden_visibility 0

%define debug 0

%define ver 3.4
%define desktop_file 0


Summary: The shared library for the Qt GUI toolkit.
Summary(zh_CN.UTF-8): TQt GUI 工具包的共享库。
Name: 	 tqt3
Version: %{ver}
%if %{git}
Release: 4.git%{gitdate}%{?dist}
%else
Release: 2%{?dist}
%endif
%if %{git}
Source0: tqt3-git%{gitdate}.tar.xz
%else
#地址已经失效，目前使用 tde port 的版本
Source0: ftp://ftp.troll.no/qt/source/qt-x11-free-3.3.8d.tar.xz
%endif
Source2: tqt.sh
Source3: tqt.csh
Source4: tdesigner3.desktop
Source5: tassistant3.desktop
Source6: tlinguist3.desktop
Source7: tqtconfig3.desktop

Prefix:  %{qtdir}
URL: 	 http://www.troll.no/
License: GPL/QPL
Group: 	 System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root


Patch1: qt-3.3.4-print-CJK.patch
Patch2: qt-3.0.5-nodebug.patch
Patch3: qt-3.1.0-makefile.patch
Patch5: qt-x11-free-3.3.8-strip.patch
Patch7: qt-x11-free-3.3.2-quiet.patch
Patch8: qt-x11-free-3.3.8-qembed.patch
Patch12: qt-uic-nostdlib.patch
Patch13: qt-x11-free-3.3.6-qfontdatabase_x11.patch
Patch14: qt-x11-free-3.3.3-gl.patch
Patch16: qt-x11-free-3.3.4-fullscreen.patch
Patch17: qt-x11-free-3.3.4-gcc4.patch
Patch18: qt-x11-free-3.3.4-gcc4-buildkey.patch
Patch19: qt-visibility.patch
Patch20: qt-x11-free-3.3.5-uic.patch

# patches from Fedora
Patch25: qt-x11-free-3.3.7-uic-multilib.patch
Patch27: qt-3.3.6-fontrendering-ml_IN-209097.patch
Patch28: qt-3.3.6-fontrendering-or_IN-209098.patch
Patch29: qt-3.3.6-fontrendering-as_IN-209972.patch
Patch30: qt-3.3.6-fontrendering-bn_IN-209975.patch
Patch31: qt-3.3.6-fontrendering-te_IN-211259.patch
Patch32: qt-3.3.6-fontrendering-as_IN-211436.patch

# immodule patches
Patch50: qt-x11-free-3.3.6-qt-x11-immodule-unified-qt3.3.5-20060318-pre.patch
Patch51: qt-x11-immodule-unified-qt3.3.5-20060318.diff.bz2
Patch52: qt-x11-free-3.3.6-qt-x11-immodule-unified-qt3.3.5-20060318-post.patch
Patch53: qt-x11-immodule-unified-qt3.3.5-20051012-quiet.patch
Patch54: qt-x11-free-3.3.6-fix-key-release-event-with-imm.diff
Patch55: qt-x11-free-3.3.6-qt-x11-immodule-unified-qt3.3.5-20060318-resetinputcontext.patch

# qt-copy patches
Patch100: 0038-dragobject-dont-prefer-unknown.patch
Patch101: 0047-fix-kmenu-width.diff
Patch102: 0048-qclipboard_hack_80072.patch
Patch103: 0056-khotkeys_input_84434.patch
Patch104: 0069-fix-minsize.patch
Patch105: 0070-fix-broken-fonts.patch

#ML patches
Patch10001: xim1.patch
Patch10002: xim2.patch
Patch10003:qt-x11-free-3.3.5-qpsprinter-useFreeType2.patch
Patch10004:qapplication_x11_for_kaffeine.patch
Patch10005:qt-x11-free-3.3.5-scripts-char.patch
Patch10006: xim2-no_immodule.patch
Patch10007: qt-x11-free-3.3.8-xim_fix.patch
Patch10008: qt-x11-free-3.3.6-fakebold.patch
Patch10009: qt3-gcc46.patch

#3.3.8c
Patch99999: http://www.trinitydesktop.org/wiki/pub/Developers/Qt3/qt3_3.3.8c.diff

%define theme %{name}

BuildRequires: libmng-devel
BuildRequires: libjpeg-devel
BuildRequires: libpng-devel
BuildRequires: perl
BuildRequires: sed
BuildRequires: findutils
BuildRequires: cups-devel
BuildRequires: pkgconfig

## gcc version in use? 
BuildRequires: gcc-c++
%define gcc_ver %(rpm -q --qf '%%{version}' gcc-c++ )

%define fc_ver 2.0
BuildRequires: fontconfig-devel >= %{fc_ver}
BuildRequires: libXft-devel >= %{fc_ver}
%define xft_flags %(pkg-config xft >& /dev/null && pkg-config --cflags --libs xft)

# Let rpm auto-detect these -- Rex
#Requires: cups-libs
#Requires: freetype
#Requires: libjpeg
#Requires: libpng
# Requires: libmng

%if %{motif_extention}
BuildRequires: openmotif-devel >= 2.2.2
%else
Obsoletes: qt-Xt < %{version}-%{release}
%endif

%if "%{buildstatic}" == "1"
BuildRequires: libmng-static
%endif

Conflicts: qt2 <= 2.3.1-3
Provides:  libqt.so.3

%if ! %{styleplugins}
Obsoletes: qt-styles < %{version}-%{release}
Provides:  qt-styles = %{version}-%{release}
%endif

%description
Qt is a GUI software toolkit which simplifies the task of writing and
maintaining GUI (Graphical User Interface) applications
for the X Window System.

Qt is written in C++ and is fully object-oriented.

This package contains the shared library needed to run qt
applications, as well as the README files for qt.

%description -l zh_CN.UTF-8
Qt 是一个简化编写和维护用于 X 窗口系统的 GUI (图形化用户界面)程序的 GUI 
软件工具包。 Qt 用 C++ 编写，完全面向对象。 该软件包包括运行 qt 程序所
需的共享库，以及 qt 的 README 文件。

%package config
Summary: Grapical configuration tool for programs using Qt
Summary(zh_CN.UTF-8): 使用Qt程序的图形配置工具
Group:	 User Interface/Desktops
Group(zh_CN.UTF-8): 用户界面/桌面
Requires: %{name} = %{version}-%{release}
%description config
A grapical configuration tool for programs using Qt.

%description config -l zh_CN.UTF-8
使用Qt程序的图形配置工具。

%package devel
Summary: Development files and documentation for the Qt GUI toolkit.
Summary(zh_CN.UTF-8): Qt GUI 工具包的开发文件和文档。
Group: 	 Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Conflicts: qt2-devel <= 2.3.1-3
Requires: %{name} = %{version}-%{release} 
%if ! %{buildstatic}
Obsoletes: qt-static  < %{version}-%{release} 
%endif
Requires: libstdc++-devel
Requires: libpng-devel
Requires: libjpeg-devel
Requires: libmng-devel
%description devel
The qt-devel package contains the files necessary to develop
applications using the Qt GUI toolkit: the header files, the Qt meta
object compiler, the man pages, the HTML documentation and example
programs. See http://www.trolltech.com/products/qt.html for more
information about Qt, or look at
%{qtdir}/html/index.html,
which provides Qt documentation in HTML format.

Install qt-devel if you want to develop GUI applications using the Qt
toolkit.

%description devel -l zh_CN.UTF-8
qt-devel 软件包包括开发使用 Qt GUI 工具包所必需的文件：头文件、Qt 元对
象编译器、man 页、HTML 文档、以及范例程序。 如果你想开发使用 Qt 工具包
的 GUI 应用程序，请安装 qt-devel。

%package Xt
Summary: An Xt (X Toolkit) compatibility add-on for the Qt GUI toolkit.
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release} 
%description Xt
An Xt (X Toolkit) compatibility add-on for the Qt GUI toolkit.

%if %{styleplugins}
%define plugins_style -plugin-style-cde -plugin-style-motifplus -plugin-style-platinum -plugin-style-sgi -plugin-style-windows -plugin-style-compact
%package styles
Summary: Extra styles for the Qt GUI toolkit.
Group: User Interface/Desktops
Requires: %{name} = %{version}-%{release} 
%description styles
Extra styles (themes) for the Qt GUI toolkit.
%else
%define plugins_style -qt-style-cde -qt-style-motifplus -qt-style-platinum -qt-style-sgi -qt-style-windows -qt-style-compact
%endif

%if %{buildSQL}
%define plugins_sql -enable-sql -plugin-sql-mysql -plugin-sql-odbc -plugin-sql-psql
%package ODBC
Summary: ODBC drivers for Qt's SQL classes.
Group: System Environment/Libraries
BuildRequires: unixODBC-devel
Requires: %{name} = %{version}-%{release} 
%description ODBC
ODBC driver for Qt's SQL classes (QSQL)

%package MySQL
Summary: MySQL drivers for Qt's SQL classes.
Group: System Environment/Libraries
BuildRequires:  mysql-devel 
Requires: %{name} = %{version}-%{release} 
%description MySQL
MySQL driver for Qt's SQL classes (QSQL)

%package PostgreSQL
Summary: PostgreSQL drivers for Qt's SQL classes.
Group: System Environment/Libraries
BuildRequires:  postgresql-devel
Requires: %{name} = %{version}-%{release} 
%description PostgreSQL
PostgreSQL driver for Qt's SQL classes (QSQL)
%endif

%if %{buildsqlite}
%package sqlite
Summary: sqlite drivers for Qt's SQL classes.
Group: System Environment/Libraries
BuildRequires:  sqlite-devel
Requires: %{name} = %{version}-%{release}
%description sqlite
sqlite driver for Qt's SQL classes (QSQL)
%endif

%package static
Summary: Version of the Qt GUI toolkit for static linking
Group: Development/Libraries
Requires: %{name}-devel = %{version}-%{release} 
%description static
Version of the Qt library for static linking

%package designer
Summary: Interface designer (IDE) for the Qt toolkit
Summary(zh_CN.UTF-8): Qt GUI 工具包的界面设计程序 (IDE)
Group: Development/Tools
Group(zh_CN.UTF-8): 开发/工具
Requires: %{name}-devel = %{version}-%{release} 
%description designer
Contains a User Interface designer tool for the Qt toolkit.

%description designer -l zh_CN.UTF-8
qt-designer 软件包包括用于 Qt 工具包的用户界面设计工具。

%prep
%if %{git}
%setup -q -n tqt3-git%{gitdate}
%else
%setup -q -n qt-x11-free-3.3.8d
%endif

##redhat patches
#%patch1 -p1 
#%patch2 -p1
#%patch3 -p1
#%patch5 -p1
#%patch7 -p1
#%patch8 -p1
#%patch12 -p1
#%patch13 -p1
#已包含
#%patch14 -p1
#%patch16 -p1 -b .fullscreen

%if %{enable_hidden_visibility}
#%patch19 -p1 -b .hidden_visibility
%endif

#%patch20 -p1 -b .uic

#%patch25 -p1 -b .uic-multilib
#%patch27 -p1 -b .fontrendering-ml_IN-bz#209097
#%patch28 -p1 -b .fontrendering-or_IN-bz#209098
#%patch29 -p1 -b .fontrendering-as_IN-bz#209972
#%patch30 -p1 -b .fontrendering-bn_IN-bz#209975
#%patch31 -p1 -b .fontrendering-te_IN-bz#211259
#%patch32 -p1 -b .fontrendering-as_IN-bz211436

%if %{immodule}
#%patch50 -p1 -b .pre
#%patch51 -p1
#%patch52 -p1 -b .post
#%patch53 -p1 -b .quiet
#%patch54 -p1 -b .fix-key-release-event-with-imm
#%patch55 -p1 -b .resetinputcontext
%endif

## qt-copy patches
#%patch100 -p0 -b .0038-dragobject-dont-prefer-unknown
#%patch101 -p0 -b .0047-fix-kmenu-width
#%patch102 -p0 -b .0048-qclipboard_hack_80072
#%patch103 -p0 -b .0056-khotkeys_input_84434
#%patch104 -p0 -b .0069-fix-minsize
#%patch105 -p0 -b .0070-fix-broken-fonts

## ML patches
#%patch10001 -p1
%if %{immodule}
#%patch10002 -p1 -b .xim2
%else
#%patch10006 -p1 -b .xim2
#变动较大，已不可用
#%patch10007 -p1 -b .xim_fix
%endif
#%patch10003 -p1
#%patch10004 -p1
#%patch10005 -p1
#%patch10008 -p1
#%patch10009 -p1

#%patch99999 -p0

%build
export QTDIR=$(pwd)
export LD_LIBRARY_PATH="$QTDIR/lib:$LD_LIBRARY_PATH"
export PATH="$QTDIR/bin:$PATH"
export QTDEST=%{qtdir}

%if %{immodule}
    sh ./make-symlinks.sh
%endif

# set some default FLAGS
%ifarch ia64
OPTFLAGS="-O0"
%else
OPTFLAGS="$RPM_OPT_FLAGS"
%endif

# don't use rpath
perl -pi -e "s|-Wl,-rpath,| |" mkspecs/*/qmake.conf

# set correct FLAGS
perl -pi -e "s|-O2|$INCLUDES $OPTFLAGS|g" mkspecs/*/qmake.conf

# set correct lib path
if [ "%{_lib}" == "lib64" ] ; then
 perl -pi -e "s,/usr/lib /lib,/usr/%{_lib} /%{_lib},g" config.tests/{unix,x11}/*.test
 perl -pi -e "s,/lib /usr/lib,/%{_lib} /usr/%{_lib},g" config.tests/{unix,x11}/*.test
fi


# build shared, threaded (default) libraries
echo yes | ./configure \
  -prefix $QTDEST \
  -docdir %{_docdir}/qt-devel-%{version}/ \
%if %{_lib} == lib64
  -platform linux-g++-64 \
%else
  -platform linux-g++ \
%endif
%if %{debug}
  -debug \
%else
  -release \
%endif
  -shared \
  %{dlopen_opengl} \
  -largefile \
  -qt-gif \
  -system-zlib \
  -system-libpng \
  -system-libmng \
  -system-libjpeg \
  -no-exceptions \
  -enable-styles \
  -enable-tools \
  -enable-kernel \
  -enable-widgets \
  -enable-dialogs \
  -enable-iconview \
  -enable-workspace \
  -enable-network \
  -enable-canvas \
  -enable-table \
  -enable-xml \
  -enable-opengl \
  -qt-imgfmt-png -qt-imgfmt-jpeg -qt-imgfmt-mng \
  -qt-style-motif \
  %if %{buildSQL}
  %{plugins_sql} \
  %endif
  %{plugins_style} \
  -stl \
  -thread \
  -cups \
  -sm \
  -xkb \
  -ipv6 \
  -xinerama \
  -xrender \
  -xft 

%if %{buildSQL}
# build psql plugin
pushd plugins/src/sqldrivers/psql
tqmake -o Makefile "INCLUDEPATH+=/usr/include/pgsql /usr/include/pgsql/server /usr/include/pgsql/internal" "LIBS+=-lpq" psql.pro
popd

# build mysql plugin
pushd plugins/src/sqldrivers/mysql
tqmake -o Makefile "INCLUDEPATH+=/usr/include/mysql" "LIBS+=-L%{_libdir}/mysql -lmysqlclient" mysql.pro
popd

pushd plugins/src/sqldrivers/odbc
tqmake -o Makefile "LIBS+=-lodbc" odbc.pro
popd
%endif

%if %{buildsqlite}
# build sqlite plugin
pushd plugins/src/sqldrivers/sqlite
tqmake -o Makefile "LIBS+=-lsqlite3" sqlite.pro
popd
%endif

make
#make %{_smp_mflags}


# build Xt/Motif Extention
%if %{motif_extention}
make %{_smp_mflags} -C extensions/motif/src
%endif

# build static libraries, if requested.
%if %{buildstatic}
cp -aR lib lib-bld
cp -aR bin bin-bld
make clean
rm -rf lib bin
mv lib-bld lib
mv bin-bld bin

echo yes | ./configure \
  -prefix $QTDEST \
%if %{debug}
  -debug \
%else
  -release \
%endif
  -largefile \
  %{dlopen_opengl} \
  -static \
  -qt-gif \
  -system-zlib \
  -system-libpng \
  -system-libmng \
  -system-libjpeg \
  -no-exceptions \
  -enable-styles \
  -enable-tools \
  -enable-kernel \
  -enable-widgets \
  -enable-dialogs \
  -enable-iconview \
  -enable-workspace \
  -enable-network \
  -enable-canvas \
  -enable-table \
  -enable-xml \
  -enable-opengl \
  -qt-imgfmt-png -qt-imgfmt-jpeg -qt-imgfmt-mng \
  -qt-style-motif \
  %if %{buildSQL}
  %{plugins_sql} \
  %endif
  %{plugins_style} \
  -stl \
  -thread \
  -cups \
  -sm \
  -xinerama \
  -xft \
  -xrender \
  -xkb 

make %{_smp_mflags}
%endif

%if %{buildsqlite}
# build sqlite plugin
pushd plugins/src/sqldrivers/sqlite
make
popd
%endif

%install
rm -rf $RPM_BUILD_ROOT
export QTDIR=$(pwd)
export PATH=$QTDIR/bin:$PATH
export MANPATH=$QTDIR/doc/man:$MANPATH
export LD_LIBRARY_PATH=$QTDIR/lib:$LD_LIBRARY_PATH
export QTDEST=%{qtdir}

mkdir -p $RPM_BUILD_ROOT{%{_bindir},%{_docdir}/qt{,-devel}-%{version},%{_mandir}/{man1,man3}}
mkdir -p $RPM_BUILD_ROOT%{qtdir}/{bin,include,lib}

make install INSTALL_ROOT=$RPM_BUILD_ROOT/

for i in findtr qt20fix qtrename140 tqlrelease tqlupdate ; do
   install bin/$i %{buildroot}%{qtdir}/bin/
done

# create/fix symlinks, lib64 fixes
/usr/sbin/ldconfig -n $RPM_BUILD_ROOT%{qtdir}/%{_lib}
for link in tqt.so tqt.so.3 ; do
  ln -sf libtqt-mt.so.3.3.8 $RPM_BUILD_ROOT%{qtdir}/%{_lib}/lib${link}
done
pushd mkspecs
rm -rf default
if [ "%_lib" == "lib64" ]; then
   ln -sf linux-g++-64 default
else
   ln -sf linux-g++ default
fi
popd
cp -aR mkspecs %{buildroot}%{qtdir}

# Handle pkgconfig file
mkdir -p $RPM_BUILD_ROOT%{_libdir}/pkgconfig/
cp -lf $RPM_BUILD_ROOT%{qtdir}/lib/pkgconfig/*.pc \
        $RPM_BUILD_ROOT%{_libdir}/pkgconfig/

# install man pages
mkdir -p %{buildroot}%{_mandir}
cp -af doc/man/* %{buildroot}%{_mandir}/
rm -rf doc/man

## Fixup examples/tutorials
# don't include Makefiles of qt examples/tutorials
make -C examples clean
make -C tutorial clean
# Make sure the examples can be built outside the source tree.
# Our binaries fulfill all requirements, so...
perl -pi -e "s,^DEPENDPATH.*,,g;s,^REQUIRES.*,,g" `find examples -name "*.pro"`

# don't include Makefiles of qt examples/tutorials
find examples -name "Makefile" | xargs rm -f
find examples -name "*.obj" | xargs rm -rf
find examples -name "*.moc" | xargs rm -rf
find tutorial -name "Makefile" | xargs rm -f

for a in */*/Makefile ; do
  sed 's|^SYSCONF_MOC.*|SYSCONF_MOC		= %{qtdir}/bin/tqmoc|' < $a > ${a}.2
  mv -v ${a}.2 $a
done


## qt.sh, qt.csh
mkdir -p $RPM_BUILD_ROOT/etc/profile.d
install -m 755 %{SOURCE2} %{SOURCE3} %{buildroot}/etc/profile.d/

mkdir -p %{buildroot}%{_bindir}
install -m 0755 bin/conv2ui %{buildroot}%{qtdir}/bin/conv2ui
#for i in bin/*; do
#  ln -s ../%{_lib}/%{qt_dirname}/bin/`basename $i` $RPM_BUILD_ROOT%{_bindir}/tqt-`basename $i`
#done

# make symbolic link to qt docdir
mv %{buildroot}%{_docdir}/qt-devel-3.4 %{buildroot}%{_docdir}/tqt3-devel-3.4
rm -rf $RPM_BUILD_ROOT%{qtdir}/doc
ln -sf  %{_prefix}/share/doc/%{name}-devel-%{version} $RPM_BUILD_ROOT%{qtdir}/doc

# Add desktop file
%if %{desktop_file}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  --vendor="%{name}" \
  --add-category="X-Magic" \
    %{SOURCE4} %{SOURCE5} %{SOURCE6} %{SOURCE7}
%else
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applnk/Development
install -m 644 %{SOURCE4} %{SOURCE5} %{SOURCE6} %{SOURCE7} $RPM_BUILD_ROOT%{_datadir}/applnk/Development/
%endif

# install icons
mkdir %{buildroot}%{_datadir}/pixmaps
install -m 644 tools/assistant/images/qt.png %{buildroot}%{_datadir}/pixmaps/tqtconfig3.png
install -m 644 tools/assistant/images/designer.png %{buildroot}%{_datadir}/pixmaps/tdesigner3.png
install -m 644 tools/assistant/images/assistant.png %{buildroot}%{_datadir}/pixmaps/tassistant3.png
install -m 644 tools/assistant/images/linguist.png %{buildroot}%{_datadir}/pixmaps/tlinguist3.png

# move into redhat-artwork?  No -- Rex
# Sane default settings
mkdir -p $RPM_BUILD_ROOT%{qtdir}/etc/settings
cat >$RPM_BUILD_ROOT%{qtdir}/etc/settings/tqtrc <<"EOF"
[3.4]
libraryPath=/usr/lib/tqt-3.4/plugins:/usr/lib/trinity/plugins

[General]
XIMInputStyle=Over The Spot
cursorFlashTime=1000
doubleClickInterval=400
embedFonts=true
enableXft=true
font=Tahoma,10,-1,5,48,0,0,0,0,0
fontPath=\0
globalStrut=0^e0^e
resolveSymlinks=true
style=Keramik
useRtlExtensions=false
useXft=true
wheelScrollLines=3

[KDE]
contrast=7
kdeAddedLibraryPaths=~/.kde/lib/trinity/plugins/^e/usr/lib/trinity/plugins/^e

[KWinPalette]
activeBackground=#6b91b8
activeBlend=#6b91b8
activeForeground=#ffffff
activeTitleBtnBg=#7f9ec8
frame=#efefef
inactiveBackground=#9daaba
inactiveBlend=#9daaba
inactiveForeground=#dddddd
inactiveFrame=#efefef
inactiveTitleBtnBg=#a7b5c7

[Palette]
active=#000000^e#e1e3e8^e#ffffff^e#ffffff^e#555555^e#c7c7c7^e#000000^e#ffffff^e#000000^e#ffffff^e#efefef^e#000000^e#678db2^e#ffffff^e#0a5f89^e#890a89^e
disabled=#808080^e#e1e3e8^e#ffffff^e#ffffff^e#555555^e#c7c7c7^e#c7c7c7^e#ffffff^e#808080^e#ffffff^e#efefef^e#000000^e#567594^e#ffffff^e#0a5f89^e#890a89^e
inactive=#000000^e#e1e3e8^e#ffffff^e#ffffff^e#555555^e#c7c7c7^e#000000^e#ffffff^e#000000^e#ffffff^e#efefef^e#000000^e#678db2^e#ffffff^e#0a5f89^e#890a89^e
EOF

# qt-theme
mv      $RPM_BUILD_ROOT%{qtdir}/etc/settings/tqtrc \
        $RPM_BUILD_ROOT%{qtdir}/etc/settings/tqtrc.%{theme}
touch   $RPM_BUILD_ROOT%{qtdir}/etc/settings/tqtrc

# remove some crud
rm -rf $RPM_BUILD_ROOT%{qtdir}/plugins/src \
       $RPM_BUILD_ROOT%{qtdir}/lib/README 
#       $RPM_BUILD_ROOT%{qtdir}/lib/*.prl \
#       $RPM_BUILD_ROOT%{qtdir}/plugins/*.prl 
#       $RPM_BUILD_ROOT%{qtdir}/lib/*.la

# prepare to own possibly-generated config
touch $RPM_BUILD_ROOT%{qtdir}/etc/settings/tqt_plugins_3.4rc

pushd mkspecs
rm -fr default
if [ "%_lib" == "lib64" ]; then
   ln -sf linux-g++-64 default
else
   ln -sf linux-g++ default
fi
popd
cp -aR mkspecs %{buildroot}%{qtdir}

# Patch qmake to use qt-mt unconditionally
perl -pi -e "s,-lqt ,-ltqt-mt ,g;s,-lqt$,-ltqt-mt,g" %{buildroot}%{qtdir}/mkspecs/*/qmake.conf

# remove broken links
rm -f %{buildroot}%{qtdir}/mkspecs/default/linux-g++*
#rm -f %{buildroot}%{qtdir}/lib/*.la
																 
# for newer ld.so's
mkdir -p %{buildroot}/etc/ld.so.conf.d
echo "%{qtdir}/lib" > %{buildroot}/etc/ld.so.conf.d/tqt.conf

magic_rpm_clean.sh

%clean
rm -rf $RPM_BUILD_ROOT


%pre devel
# This *should* be a symlink, otherwise nuke
DIR1=%{qtdir}/doc
[ ! -L "${DIR1}" ] && /bin/rm -rf "${DIR1}"
exit 0


%post
/usr/sbin/ldconfig

%postun
/usr/sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc FAQ LICENSE.QPL README* changes*
/etc/ld.so.conf.d/*
%attr(0755,root,root) %config /etc/profile.d/*
%dir %{qtdir}
%dir %{qtdir}/bin
%dir %{qtdir}/lib
%{qtdir}/lib/lib*.so.*
%dir %{qtdir}/etc
%dir %{qtdir}/etc/settings
# qt-theme
%config(noreplace) %{qtdir}/etc/settings/*rc.%{theme}
%ghost  %{qtdir}/etc/settings/tqtrc
%ghost  %{qtdir}/etc/settings/tqtrc.tqt3
%ghost %verify(not md5 size mtime) %{qtdir}/etc/settings/tqt_plugins_3.4rc
%dir %{qtdir}/plugins
%if %{immodule}
%{qtdir}/plugins/inputmethods
%endif
%if %{desktop_file}
%{_datadir}/applications/*.desktop
%exclude %{_datadir}/applications/qt-designer3.desktop
%else
%{_datadir}/applnk/Development/*.desktop
#%exclude %{_datadir}/applnk/Development/qt-designer3.desktop
%endif
%{_datadir}/pixmaps/*.png
%exclude %{_datadir}/pixmaps/tdesigner3.png

%files config
%defattr(-,root,root,-)
%{qtdir}/bin/tqtconfig
#%{_bindir}/tqt-qtconfig*

%files devel
%defattr(-,root,root,-)
%{qtdir}/bin/tqmoc
%{qtdir}/bin/tquic
%{qtdir}/bin/findtr
%{qtdir}/bin/qt20fix
%{qtdir}/bin/qtrename140
%{qtdir}/bin/conv2ui
%{qtdir}/bin/tqassistant
%{qtdir}/bin/qm2ts
%{qtdir}/bin/tqmake
%{qtdir}/bin/tqembed
%{qtdir}/bin/tqlinguist
%{qtdir}/bin/tqlupdate
%{qtdir}/bin/tqlrelease
#以下需要确定所属包
%{qtdir}/bin/createcw
%{qtdir}/bin/makeqpf
%{qtdir}/bin/mergetr
%{qtdir}/bin/msg2qm
%{qtdir}/plugins/inputmethods/libqimsw-multi.so
%{qtdir}/plugins/inputmethods/libqimsw-none.so
%{qtdir}/plugins/inputmethods/libqsimple.so
%{qtdir}/plugins/inputmethods/libqxim.so
#结束
%{qtdir}/include
%{qtdir}/mkspecs
%{qtdir}/lib/libtqt*.so
%{qtdir}/lib/libtqui.so
%{qtdir}/lib/libtqt-mt.la
%{qtdir}/lib/libeditor.a
%{qtdir}/lib/libdesigner*.a
%{qtdir}/lib/libqassistantclient.a
%{qtdir}/lib/*.prl
%exclude %{_mandir}/*
%{qtdir}/translations
%{qtdir}/phrasebooks
#%{_bindir}/tqt-assistant*
#%{_bindir}/tqt-moc*
#%{_bindir}/tqt-uic*
#%{_bindir}/tqt-findtr*
#%{_bindir}/tqt-qt20fix*
#%{_bindir}/tqt-qtrename140*
#%{_bindir}/tqt-qmake*
#%{_bindir}/tqt-qm2ts*
#%{_bindir}/tqt-linguist
#%{_bindir}/tqt-lrelease
#%{_bindir}/tqt-lupdate
#%{_bindir}/tqt-conv2ui
%{_libdir}/pkgconfig/*
%{qtdir}/lib/pkgconfig
%{qtdir}/doc
%doc doc/html
%doc examples
%doc tutorial

%if %{motif_extention}
%post Xt -p /usr/sbin/ldconfig
%postun Xt -p /usr/sbin/ldconfig

%files Xt
%defattr(-,root,root,-)
%{qtdir}/lib/libqmotif.so*
%endif

%if %{styleplugins}
%files styles
%defattr(-,root,root,-)
%dir %{qtdir}/plugins/styles
%{qtdir}/plugins/styles/*
%endif

%if %{buildSQL}
%files ODBC
%defattr(-,root,root,-)
%{qtdir}/plugins/sqldrivers/libqsqlodbc*

%files PostgreSQL
%defattr(-,root,root,-)
%{qtdir}/plugins/sqldrivers/libqsqlpsql*

%files MySQL
%defattr(-,root,root,-)
%{qtdir}/plugins/sqldrivers/libqsqlmysql*
%endif

%if %{buildsqlite}
%files sqlite
%defattr(-,root,root,-)
%{qtdir}/plugins/sqldrivers/libqsqlite*
%endif

%if %{buildstatic}
%files static
%defattr(-,root,root,-)
%{qtdir}/lib/*.a
%endif

%files designer
%defattr(-,root,root,-)
#%{_bindir}/tqt-designer*
%dir %{qtdir}/plugins/designer
%{qtdir}/templates
%{qtdir}/plugins/designer/*
%{qtdir}/bin/tqdesigner
%if %{desktop_file}
%{_datadir}/applications/qt-designer3.desktop
%else
#%{_datadir}/applnk/Development/qt-designer3.desktop
%endif
%{_datadir}/pixmaps/tdesigner3.png


%changelog
* Sun Dec 09 2012 Liu Di <liudidi@gmail.com> - 3.4-4.git20121102
- 为 Magic 3.0 重建

* Thu Mar 29 2012 Liu Di <liudidi@gmail.com> - 3.4-2
- 为 Magic 3.0 重建

* Mon Oct 30 2006 KanKer <kanker@163.com> -3.3.7-1mgc
- update 3.3.7

* Wed Oct 25 2006 KanKer <kanker@163.com> -3.3.6-10mgc
- update qt-x11-free-3.3.6-qfontdatabase_x11.patch

* Wed Aug 9 2006 KanKer <kanker@163.com>
- rebuild for libXft-2.1.10
- add sqlite plugin build switch,but can't use now

* Thu Mar 7 2006 KanKer <kanker@163.com>
- update to 3.3.6 release

* Sun Jan 15 2006 KanKer <kanker@163.com>
- update xim_fix_patch 

* Thu Jan 10 2006 KanKer <kanker@163.com>
- fix xim_fix.patch bug

* Fri Jan 6 2006 KanKer <kanker@163.com>
- fix xim_fix.patch bug
- disable popup input mode

* Tue Dec 29 2005 KanKer <kanker@163.com>
- remove immodule patches

* Thu Dec 27 2005 KanKer <kanker@163.com>
- update 3.3.6-snapshot

* Tue Dec 13 2005 KanKer <kanker@163.com>
- fix a qlistview bug

* Sun Nov 27 2005 KanKer <kanker@163.com>
- fix a spec bug
- add a patch "qapplication_x11_for_kaffeine.patch" from cjacker

* Tue Nov 10 2005 KanKer <kanker@163.com>
- update update qt-x11-immodule-unified-qt3.3.5-20051018.diff
- update qt-x11-immodule-unified-qt3.3.5-20051012-quiet.patch

* Wed Sep 28 2005 KanKer <kanker@163.com>
- add uic workaround

* Tue Sep 15 2005 KanKer <kanker@163.com>
- update to 3.3.5

* Wed May 18 2005 KanKer <kanker@163.com>
- update immodules patch.

* Thu Apr 19 2005 KanKer <kanker@163.com>
- update to cvs20050419.

* Tue Mar 31 2005 KanKer <kanker@163.com>
- remove immodules patch.

* Sat Mar 19 2005 KanKer <kanker@163.com>
- remove qt-3.1.1-xcursors.patch
- build 3.3.4

* Tue Feb 22 2005 Than Ngo <than@redhat.com> 1:3.3.4-5
- fix application crash when input methode not available (bug #140658)
- remove .moc/.obj
- add qt-copy patch to fix KDE #80072

* Fri Feb 11 2005 Than Ngo <than@redhat.com> 1:3.3.4-4
- update qt-x11-immodule-unified patch

* Thu Feb 10 2005 Than Ngo <than@redhat.com> 1:3.3.4-3 
- fix rpm file conflict

* Wed Feb 02 2005 Than Ngo <than@redhat.com> 1:3.3.4-2
- remove useless doc files #143949
- fix build problem if installman is disable #146311
- add missing html/examples/tutorial symlinks

* Fri Jan 28 2005 Than Ngo <than@redhat.com> 1:3.3.4-1
- update to 3.3.4
- adapt many patches to qt-3.3.4
- drop qt-x11-free-3.3.0-freetype, qt-x11-free-3.3.3-qmake, qt-x11-free-3.3.1-lib64
  qt-x11-free-3.3.3-qimage, which are included in new upstream
  
* Thu Nov 25 2004 KanKer <kanker@163.com>
- remove fakebold patch.

* Wed Oct 27 2004 KanKer <kanker@163.com>
- update fakebold patch from firefly.

* Mon Aug 23 2004 KanKer <kanker@163.com>
- 3.3.3
