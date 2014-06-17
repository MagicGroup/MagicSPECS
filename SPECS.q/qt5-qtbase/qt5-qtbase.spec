# See http://bugzilla.redhat.com/223663
%define multilib_archs x86_64 %{ix86} ppc64 ppc s390x s390 sparc64 sparcv9 ppc64le
%define multilib_basearchs x86_64 ppc64 s390x sparc64 ppc64le

# support qtchooser (adds qtchooser .conf file)
%define qtchooser 1
%global qt_module qtbase

%global rpm_macros_dir %(d=%{_rpmconfigdir}/macros.d; [ -d $d ] || d=%{_sysconfdir}/rpm; echo $d)

# define to build docs, need to undef this for bootstrapping
# where qt5-qttools builds are not yet available
# only primary archs (for now), allow secondary to bootstrap
%ifarch %{arm} %{ix86} x86_64
%define docs 1
%endif

#define pre rc1
#define snap 2013-11-08_141
#define snap_tag 20131108_141

Summary: Qt5 - QtBase components
Name:    qt5-qtbase
Version: 5.3.0
Release: 10%{?dist}

# See LGPL_EXCEPTIONS.txt, LICENSE.GPL3, respectively, for exception details
License: LGPLv2 with exceptions or GPLv3 with exceptions
Url: http://qt-project.org/
%if 0%{?snap:1}
Source0: http://download.qt-project.org/snapshots/qt/5.3/%{version}-%{pre}/%{snap}/submodules/%{qt_module}-opensource-src-%{version}-%{pre}.tar.xz
%else
%if 0%{?pre:1}
Source0: http://download.qt-project.org/development_releases/qt/5.3/%{version}-%{pre}/submodules/%{qt_module}-opensource-src-%{version}-%{pre}.tar.xz
%else
Source0: http://download.qt-project.org/official_releases/qt/5.3/%{version}/submodules/%{qt_module}-opensource-src-%{version}.tar.xz
%endif
%endif

# header file to workaround multilib issue
# https://bugzilla.redhat.com/show_bug.cgi?id=1036956
Source5: qconfig-multilib.h

# xinitrc script to check for OpenGL 1 only drivers and automatically set
# QT_XCB_FORCE_SOFTWARE_OPENGL for them
Source6: 10-qt5-check-opengl2.sh

# drop configure check for xkbcommon-x11
Patch1: qtbase-opensource-src-5.3.0-no_xkbcommon-x11.patch

# support multilib optflags
Patch2: qtbase-multilib_optflags.patch

# fix QTBUG-35459 (too low entityCharacterLimit=1024 for CVE-2013-4549)
Patch4: qt-everywhere-opensource-src-4.8.5-QTBUG-35459.patch

# unconditionally enable freetype lcdfilter support
Patch12: qtbase-opensource-src-5.2.0-enable_ft_lcdfilter.patch

# upstreamable patches
# support poll
# https://bugreports.qt-project.org/browse/QTBUG-27195
# NEEDS REBASE
Patch50: qt5-poll.patch

##upstream patches

# macros
%define _qt5 %{name}
%define _qt5_prefix %{_libdir}/qt5
%define _qt5_archdatadir %{_libdir}/qt5
# -devel bindir items (still) conflict with qt4
# at least until this is all implemented,
# http://lists.qt-project.org/pipermail/development/2012-November/007990.html
#define _qt5_bindir %{_bindir}
%define _qt5_bindir %{_qt5_prefix}/bin
%define _qt5_datadir %{_datadir}/qt5
%define _qt5_docdir %{_docdir}/qt5
%define _qt5_examplesdir %{_qt5_prefix}/examples
%define _qt5_headerdir %{_includedir}/qt5
%define _qt5_importdir %{_qt5_archdatadir}/imports 
%define _qt5_libdir %{_libdir}
%define _qt5_libexecdir %{_qt5_archdatadir}/libexec
%define _qt5_plugindir %{_qt5_archdatadir}/plugins
%define _qt5_settingsdir %{_sysconfdir}/xdg
%define _qt5_sysconfdir %{_qt5_settingsdir} 
%define _qt5_translationdir %{_datadir}/qt5/translations

# for %%check
BuildRequires: cmake
BuildRequires: cups-devel
BuildRequires: desktop-file-utils
BuildRequires: findutils
BuildRequires: libjpeg-devel
BuildRequires: libmng-devel
BuildRequires: libtiff-devel
BuildRequires: pkgconfig(alsa)
BuildRequires: pkgconfig(dbus-1)
BuildRequires: pkgconfig(libdrm)
BuildRequires: pkgconfig(fontconfig)
BuildRequires: pkgconfig(gl)
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(gtk+-2.0)
# xcb-sm
BuildRequires: pkgconfig(ice) pkgconfig(sm)
BuildRequires: pkgconfig(libpng)
BuildRequires: pkgconfig(libudev)
BuildRequires: pkgconfig(NetworkManager)
BuildRequires: pkgconfig(openssl)
BuildRequires: pkgconfig(libpulse) pkgconfig(libpulse-mainloop-glib)
%if 0%{?fedora} > 20
BuildRequires: pkgconfig(xcb-xkb) >= 1.10
%global xkbcommon -system-xkbcommon
BuildRequires: pkgconfig(xkbcommon) >= 0.4.1
BuildRequires: pkgconfig(xkbcommon-x11) >= 0.4.1
## if no xcb-xkb > 1.10 or xkbcommon-x11
## ie, to allow libxkbcommon backport for f19/f20
#global no_xkbcommon_x11 1
%else
Provides: bundled(libxkbcommon) = 0.4.1
%global xkbcommon -qt-xkbcommon
%endif
BuildRequires: pkgconfig(xkeyboard-config)
%if 0%{?fedora} || 0%{?rhel} > 6
%define egl 1
BuildRequires: pkgconfig(atspi-2)
BuildRequires: pkgconfig(egl)
BuildRequires: pkgconfig(gbm)
BuildRequires: pkgconfig(glesv2)
BuildRequires: pkgconfig(sqlite3) >= 3.7
%define sqlite -system-sqlite
BuildRequires: pkgconfig(harfbuzz) >= 0.9.19
%define harfbuzz -system-harfbuzz
BuildRequires: pkgconfig(icu-i18n)
BuildRequires: pkgconfig(libpcre) >= 8.30
%define pcre -system-pcre
%else
BuildRequires: libicu-devel
%define pcre -qt-pcre
%endif
BuildRequires: pkgconfig(xcb) pkgconfig(xcb-glx) pkgconfig(xcb-icccm) pkgconfig(xcb-image) pkgconfig(xcb-keysyms) pkgconfig(xcb-renderutil)
BuildRequires: pkgconfig(zlib)

## Sql drivers
%if 0%{?rhel}
%define ibase -no-sql-ibase
%define tds -no-sql-tds
%endif

%description 
Qt is a software toolkit for developing applications.

This package contains base tools, like string, xml, and network
handling.

%package devel
Summary: Development files for %{name} 
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: %{name}-gui%{?_isa}
# qtsql apparently wants all drivers available at buildtime
%if "%{?ibase}" != "-no-sql-ibase"
Requires: %{name}-ibase%{?_isa}
%endif
Requires: %{name}-mysql%{?_isa}
Requires: %{name}-odbc%{?_isa}
Requires: %{name}-postgresql%{?_isa}
%if "%{?tds}" != "-no-sql-tds"
Requires: %{name}-tds%{?_isa}
%endif
Requires: pkgconfig(gl)
%description devel
%{summary}.

%if 0%{?docs}
%package doc
Summary: API documentation for %{name}
Requires: %{name} = %{version}-%{release}
# for qhelpgenerator
BuildRequires: qt5-qttools-devel
BuildArch: noarch
%description doc
%{summary}.
%endif

%package examples
Summary: Programming examples for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
%description examples
%{summary}.

%package static 
Summary: Static library files for %{name}
Requires: %{name}-devel%{?_isa} = %{version}-%{release}
Requires: pkgconfig(fontconfig)
Requires: pkgconfig(glib-2.0)
Requires: pkgconfig(zlib)
%description static 
%{summary}.

%if "%{?ibase}" != "-no-sql-ibase"
%package ibase
Summary: IBase driver for Qt5's SQL classes
BuildRequires: firebird-devel
Requires: %{name}%{?_isa} = %{version}-%{release}
%description ibase
%{summary}.
%endif

%package mysql
Summary: MySQL driver for Qt5's SQL classes
BuildRequires: mysql-devel
Requires: %{name}%{?_isa} = %{version}-%{release}
%description mysql 
%{summary}.

%package odbc 
Summary: ODBC driver for Qt5's SQL classes
BuildRequires: unixODBC-devel
Requires: %{name}%{?_isa} = %{version}-%{release}
%description odbc 
%{summary}.

%package postgresql 
Summary: PostgreSQL driver for Qt5's SQL classes
BuildRequires: postgresql-devel
Requires: %{name}%{?_isa} = %{version}-%{release}
%description postgresql 
%{summary}.

%if "%{?tds}" != "-no-sql-tds"
%package tds
Summary: TDS driver for Qt5's SQL classes
BuildRequires: freetds-devel
Requires: %{name}%{?_isa} = %{version}-%{release}
%description tds
%{summary}.
%endif

# debating whether to do 1 subpkg per library or not -- rex
%package gui
Summary: Qt5 GUI-related libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
Obsoletes: qt5-qtbase-x11 < 5.2.0
Provides:  qt5-qtbase-x11 = %{version}-%{release}

# for Source6: 10-qt5-check-opengl2.sh:
# directory ownership
Requires: xorg-x11-xinit
# glxinfo
Requires: glx-utils

%description gui
Qt5 libraries used for drawing widgets and OpenGL items.


%prep
%setup -q -n qtbase-opensource-src-%{version}%{?pre:-%{pre}}

%if 0%{?no_xkbcommon_x11}
%patch1 -p1 -b .no_xkbcommon-x11
%endif
%patch2 -p1 -b .multilib_optflags
# drop backup file(s), else they get installed too, http://bugzilla.redhat.com/639463
rm -fv mkspecs/linux-g++*/qmake.conf.multilib-optflags

%patch4 -p1 -b .QTBUG-35459
%patch12 -p1 -b .enable_ft_lcdfilter

#patch50 -p1 -b .poll

# drop -fexceptions from $RPM_OPT_FLAGS
RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed 's|-fexceptions||g'`

%define platform linux-g++
%ifarch %{multilib_archs}
%if "%{?__isa_bits}" == "64"
%define platform linux-g++-64
%endif
%endif

sed -i -e "s|-O2|$RPM_OPT_FLAGS|g" \
  mkspecs/%{platform}/qmake.conf 

sed -i -e "s|^\(QMAKE_LFLAGS_RELEASE.*\)|\1 $RPM_LD_FLAGS|" \
  mkspecs/common/g++-unix.conf

# undefine QMAKE_STRIP (and friends), so we get useful -debuginfo pkgs (#1065636)
sed -i -e 's|^\(QMAKE_STRIP.*=\).*$|\1|g' mkspecs/common/linux.conf

# move some bundled libs to ensure they're not accidentally used
pushd src/3rdparty
mkdir UNUSED
mv freetype libjpeg libpng zlib xcb UNUSED/
%if "%{?sqlite}" == "-system-sqlite"
mv sqlite UNUSED/
%endif
popd


%build

# limit -reduce-relocations to %%ix86 x86_64 archs, https://bugreports.qt-project.org/browse/QTBUG-36129
./configure -v \
  -confirm-license \
  -opensource \
  -prefix %{_qt5_prefix} \
  -archdatadir %{_qt5_archdatadir} \
  -bindir %{_qt5_bindir} \
  -datadir %{_qt5_datadir} \
  -docdir %{_qt5_docdir} \
  -examplesdir %{_qt5_examplesdir} \
  -headerdir %{_qt5_headerdir} \
  -importdir %{_qt5_importdir} \
  -libdir %{_qt5_libdir} \
  -libexecdir %{_qt5_libexecdir} \
  -plugindir %{_qt5_plugindir} \
  -sysconfdir %{_qt5_sysconfdir} \
  -translationdir %{_qt5_translationdir} \
  -platform %{platform} \
  -release \
  -shared \
  -accessibility \
  -dbus-linked \
  -fontconfig \
  -glib \
  -gtkstyle \
  %{?ibase} \
  -iconv \
  -icu \
  -openssl-linked \
  -optimized-qmake \
  -nomake tests \
  -no-pch \
  -no-rpath \
  -no-separate-debug-info \
%ifarch %{ix86}
  -no-sse2 \
%endif
  -no-strip \
%ifarch %{ix86} x86_64
  -reduce-relocations \
%endif
  %{?harfbuzz} \
  -system-libjpeg \
  -system-libpng \
  %{?pcre} \
  %{?sqlite} \
  %{?tds} \
  %{?xkbcommon} \
  -system-zlib

make %{?_smp_mflags}

%if 0%{?docs}
# wierd but necessary, to force regeration to use just-built qdoc
rm -fv src/corelib/Makefile
make %{?_smp_mflags} docs
%endif


%install
make install INSTALL_ROOT=%{buildroot}

%if 0%{?docs}
make install_docs INSTALL_ROOT=%{buildroot}
%endif

# Qt5.pc
cat >%{buildroot}%{_libdir}/pkgconfig/Qt5.pc<<EOF
prefix=%{_qt5_prefix}
archdatadir=%{_qt5_archdatadir}
bindir=%{_qt5_bindir}
datadir=%{_qt5_datadir}

docdir=%{_qt5_docdir}
examplesdir=%{_qt5_examplesdir}
headerdir=%{_qt5_headerdir}
importdir=%{_qt5_importdir}
libdir=%{_qt5_libdir}
libexecdir=%{_qt5_libexecdir}
moc=%{_qt5_bindir}/moc
plugindir=%{_qt5_plugindir}
qmake=%{_qt5_bindir}/qmake
settingsdir=%{_qt5_settingsdir}
sysconfdir=%{_qt5_sysconfdir}
translationdir=%{_qt5_translationdir}

Name: Qt5
Description: Qt5 Configuration
Version: %{version}
EOF

# rpm macros
mkdir -p %{buildroot}%{rpm_macros_dir}
cat >%{buildroot}%{rpm_macros_dir}/macros.qt5<<EOF
%%_qt5 %{name}
%%_qt5_epoch %{?epoch}%{!?epoch:0}
%%_qt5_version %{version}
%%_qt5_evr %{?epoch:%{epoch:}}%{version}-%{release}
%%_qt5_prefix %%{_libdir}/qt5
%%_qt5_archdatadir %%{_qt5_prefix}
%%_qt5_bindir %%{_qt5_prefix}/bin
%%_qt5_datadir %%{_datadir}/qt5
%%_qt5_docdir %%{_docdir}/qt5
%%_qt5_examplesdir %%{_qt5_prefix}/examples
%%_qt5_headerdir %%{_includedir}/qt5
%%_qt5_importdir %%{_qt5_archdatadir}/imports
%%_qt5_libdir %%{_libdir}
%%_qt5_libexecdir %%{_qt5_archdatadir}/libexec
%%_qt5_plugindir %%{_qt5_archdatadir}/plugins
%%_qt5_qmake %%{_qt5_bindir}/qmake
%%_qt5_settingsdir %%{_sysconfdir}/xdg
%%_qt5_sysconfdir %%{_qt5_settingsdir}
%%_qt5_translationdir %%{_datadir}/qt5/translations
EOF

# create/own dirs
mkdir -p %{buildroot}{%{_qt5_archdatadir}/mkspecs/modules,%{_qt5_importdir},%{_qt5_libexecdir},%{_qt5_plugindir}/iconengines,%{_qt5_translationdir}}

# hardlink files to %{_bindir}, add -qt5 postfix to not conflict
mkdir %{buildroot}%{_bindir}
pushd %{buildroot}%{_qt5_bindir}
for i in * ; do
  case "${i}" in
    moc|qdbuscpp2xml|qdbusxml2cpp|qmake|rcc|syncqt|uic)
      ln -v  ${i} %{buildroot}%{_bindir}/${i}-qt5
      ln -sv ${i} ${i}-qt5
      ;;
    *)
      ln -v  ${i} %{buildroot}%{_bindir}/${i}
      ;;
  esac
done
popd

%ifarch %{multilib_archs}
# multilib: qconfig.h
  mv %{buildroot}%{_qt5_headerdir}/QtCore/qconfig.h %{buildroot}%{_qt5_headerdir}/QtCore/qconfig-%{__isa_bits}.h
  install -p -m644 -D %{SOURCE5} %{buildroot}%{_qt5_headerdir}/QtCore/qconfig.h
%endif

# qtchooser conf
%if 0%{?qtchooser}
  mkdir -p %{buildroot}%{_sysconfdir}/xdg/qtchooser
  pushd    %{buildroot}%{_sysconfdir}/xdg/qtchooser
  echo "%{_qt5_bindir}" >  qt5.conf
  echo "%{_qt5_prefix}" >> qt5.conf
  %ifarch %{multilib_archs}
    mv qt5.conf qt5-%{__isa_bits}.conf
    %ifarch %{multilib_basearchs}
      ln -sv qt5-%{__isa_bits}.conf qt5.conf
    %endif
  %endif
  popd
%endif

## .prl/.la file love
# nuke .prl reference(s) to %%buildroot, excessive (.la-like) libs
pushd %{buildroot}%{_qt5_libdir}
for prl_file in libQt5*.prl ; do
  sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" ${prl_file}
  if [ -f "$(basename ${prl_file} .prl).so" ]; then
    rm -fv "$(basename ${prl_file} .prl).la"
    sed -i -e "/^QMAKE_PRL_LIBS/d" ${prl_file}
  fi
done
popd

install -p -m755 -D %{SOURCE6} %{buildroot}%{_sysconfdir}/X11/xinit/xinitrc.d/10-qt5-check-opengl2.sh


## work-in-progress, doesn't work yet -- rex
%check
export CMAKE_PREFIX_PATH=%{buildroot}%{_prefix}
export CTEST_OUTPUT_ON_FAILURE=1
export PATH=%{buildroot}%{_bindir}:$PATH
export LD_LIBRARY_PATH=%{buildroot}%{_libdir}
mkdir tests/auto/cmake/%{_target_platform}
pushd tests/auto/cmake/%{_target_platform}
cmake .. ||:
ctest --output-on-failure ||:
popd


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc LICENSE.GPL LICENSE.LGPL LGPL_EXCEPTION.txt
%if 0%{?qtchooser}
# not editable config files, so not using %%config here
%dir %{_sysconfdir}/xdg/qtchooser
%{_sysconfdir}/xdg/qtchooser/*.conf
%endif
%{_qt5_libdir}/libQt5Concurrent.so.5*
%{_qt5_libdir}/libQt5Core.so.5*
%{_qt5_libdir}/libQt5DBus.so.5*
%{_qt5_libdir}/libQt5Network.so.5*
%{_qt5_libdir}/libQt5Sql.so.5*
%{_qt5_libdir}/libQt5Test.so.5*
%{_qt5_libdir}/libQt5Xml.so.5*
%dir %{_qt5_docdir}/
%{_qt5_docdir}/global/
%{_qt5_importdir}/
%{_qt5_translationdir}/
%dir %{_qt5_prefix}/
%dir %{_qt5_datadir}/
%dir %{_qt5_libexecdir}/
%dir %{_qt5_plugindir}/
%dir %{_qt5_plugindir}/bearer/
%{_qt5_plugindir}/bearer/libqconnmanbearer.so
%{_qt5_plugindir}/bearer/libqgenericbearer.so
%{_qt5_plugindir}/bearer/libqnmbearer.so
%dir %{_qt5_plugindir}/accessible/
%dir %{_qt5_plugindir}/generic/
%dir %{_qt5_plugindir}/imageformats/
%dir %{_qt5_plugindir}/platforminputcontexts/
%dir %{_qt5_plugindir}/platforms/
%dir %{_qt5_plugindir}/platformthemes/
%dir %{_qt5_plugindir}/printsupport/
%dir %{_qt5_plugindir}/sqldrivers/
%{_qt5_plugindir}/sqldrivers/libqsqlite*.so

%if 0%{?docs}
%files doc
%doc dist/README dist/changes-5.*
%{_qt5_docdir}/*.qch
%{_qt5_docdir}/qdoc/
%{_qt5_docdir}/qmake/
%{_qt5_docdir}/qtconcurrent/
%{_qt5_docdir}/qtcore/
%{_qt5_docdir}/qtdbus/
%{_qt5_docdir}/qtgui/
%{_qt5_docdir}/qtnetwork/
%{_qt5_docdir}/qtopengl/
%{_qt5_docdir}/qtprintsupport/
%{_qt5_docdir}/qtsql/
%{_qt5_docdir}/qttestlib/
%{_qt5_docdir}/qtwidgets/
%{_qt5_docdir}/qtxml/
%endif

%files devel
%{rpm_macros_dir}/macros.qt5
%if "%{_qt5_bindir}" != "%{_bindir}"
%dir %{_qt5_bindir}
%endif
%{_bindir}/moc*
%{_bindir}/qdbuscpp2xml*
%{_bindir}/qdbusxml2cpp*
%{_bindir}/qdoc*
%{_bindir}/qmake*
%{_bindir}/rcc*
%{_bindir}/syncqt*
%{_bindir}/uic*
%{_bindir}/qlalr
%{_qt5_bindir}/moc*
%{_qt5_bindir}/qdbuscpp2xml*
%{_qt5_bindir}/qdbusxml2cpp*
%{_qt5_bindir}/qdoc*
%{_qt5_bindir}/qmake*
%{_qt5_bindir}/rcc*
%{_qt5_bindir}/syncqt*
%{_qt5_bindir}/uic*
%{_qt5_bindir}/qlalr
%if "%{_qt5_headerdir}" != "%{_includedir}"
%dir %{_qt5_headerdir}
%endif
%{_qt5_headerdir}/QtConcurrent/
%{_qt5_headerdir}/QtCore/
%{_qt5_headerdir}/QtDBus/
%{_qt5_headerdir}/QtGui/
%{_qt5_headerdir}/QtNetwork/
%{_qt5_headerdir}/QtOpenGL/
%{_qt5_headerdir}/QtPrintSupport/
%{_qt5_headerdir}/QtSql/
%{_qt5_headerdir}/QtTest/
%{_qt5_headerdir}/QtWidgets/
%{_qt5_headerdir}/QtXml/
%{_qt5_archdatadir}/mkspecs/
%{_qt5_libdir}/libQt5Concurrent.prl
%{_qt5_libdir}/libQt5Concurrent.so
%{_qt5_libdir}/libQt5Core.prl
%{_qt5_libdir}/libQt5Core.so
%{_qt5_libdir}/libQt5DBus.prl
%{_qt5_libdir}/libQt5DBus.so
%{_qt5_libdir}/libQt5Gui.prl
%{_qt5_libdir}/libQt5Gui.so
%{_qt5_libdir}/libQt5Network.prl
%{_qt5_libdir}/libQt5Network.so
%{_qt5_libdir}/libQt5OpenGL.prl
%{_qt5_libdir}/libQt5OpenGL.so
%{_qt5_libdir}/libQt5PrintSupport.prl
%{_qt5_libdir}/libQt5PrintSupport.so
%{_qt5_libdir}/libQt5Sql.prl
%{_qt5_libdir}/libQt5Sql.so
%{_qt5_libdir}/libQt5Test.prl
%{_qt5_libdir}/libQt5Test.so
%{_qt5_libdir}/libQt5Widgets.prl
%{_qt5_libdir}/libQt5Widgets.so
%{_qt5_libdir}/libQt5Xml.prl
%{_qt5_libdir}/libQt5Xml.so
%dir %{_qt5_libdir}/cmake/
%{_qt5_libdir}/cmake/Qt5/
%{_qt5_libdir}/cmake/Qt5Concurrent/
%{_qt5_libdir}/cmake/Qt5Core/
%{_qt5_libdir}/cmake/Qt5DBus/
%{_qt5_libdir}/cmake/Qt5Gui/
%{_qt5_libdir}/cmake/Qt5Network/
%{_qt5_libdir}/cmake/Qt5OpenGL/
%{_qt5_libdir}/cmake/Qt5PrintSupport/
%{_qt5_libdir}/cmake/Qt5Sql/
%{_qt5_libdir}/cmake/Qt5Test/
%{_qt5_libdir}/cmake/Qt5Widgets/
%{_qt5_libdir}/cmake/Qt5Xml/
%{_qt5_libdir}/pkgconfig/Qt5.pc
%{_qt5_libdir}/pkgconfig/Qt5Concurrent.pc
%{_qt5_libdir}/pkgconfig/Qt5Core.pc
%{_qt5_libdir}/pkgconfig/Qt5DBus.pc
%{_qt5_libdir}/pkgconfig/Qt5Gui.pc
%{_qt5_libdir}/pkgconfig/Qt5Network.pc
%{_qt5_libdir}/pkgconfig/Qt5OpenGL.pc
%{_qt5_libdir}/pkgconfig/Qt5PrintSupport.pc
%{_qt5_libdir}/pkgconfig/Qt5Sql.pc
%{_qt5_libdir}/pkgconfig/Qt5Test.pc
%{_qt5_libdir}/pkgconfig/Qt5Widgets.pc
%{_qt5_libdir}/pkgconfig/Qt5Xml.pc

%files static
%{_qt5_libdir}/libQt5Bootstrap.*a
%{_qt5_libdir}/libQt5Bootstrap.prl
%{_qt5_libdir}/pkgconfig/Qt5Bootstrap.pc
%{_qt5_headerdir}/QtOpenGLExtensions/
%{_qt5_libdir}/libQt5OpenGLExtensions.*a
%{_qt5_libdir}/libQt5OpenGLExtensions.prl
%{_qt5_libdir}/cmake/Qt5OpenGLExtensions/
%{_qt5_libdir}/pkgconfig/Qt5OpenGLExtensions.pc
%{_qt5_headerdir}/QtPlatformSupport/
%{_qt5_libdir}/libQt5PlatformSupport.*a
%{_qt5_libdir}/libQt5PlatformSupport.prl
%{_qt5_libdir}/pkgconfig/Qt5PlatformSupport.pc

%files examples
%{_qt5_examplesdir}/

%if "%{?ibase}" != "-no-sql-ibase"
%files ibase
%{_qt5_plugindir}/sqldrivers/libqsqlibase.so
%endif

%files mysql
%{_qt5_plugindir}/sqldrivers/libqsqlmysql.so

%files odbc 
%{_qt5_plugindir}/sqldrivers/libqsqlodbc.so

%files postgresql 
%{_qt5_plugindir}/sqldrivers/libqsqlpsql.so

%if "%{?tds}" != "-no-sql-tds"
%files tds
%{_qt5_plugindir}/sqldrivers/libqsqltds.so
%endif

%post gui -p /sbin/ldconfig
%postun gui -p /sbin/ldconfig

%files gui
%{_sysconfdir}/X11/xinit/xinitrc.d/10-qt5-check-opengl2.sh
%{_qt5_libdir}/libQt5Gui.so.5*
%{_qt5_libdir}/libQt5OpenGL.so.5*
%{_qt5_libdir}/libQt5PrintSupport.so.5*
%{_qt5_libdir}/libQt5Widgets.so.5*
%{_qt5_plugindir}/accessible/libqtaccessiblewidgets.so
%{_qt5_plugindir}/generic/libqevdevkeyboardplugin.so
%{_qt5_plugindir}/generic/libqevdevmouseplugin.so
%{_qt5_plugindir}/generic/libqevdevtabletplugin.so
%{_qt5_plugindir}/generic/libqevdevtouchplugin.so
%{_qt5_plugindir}/imageformats/libqgif.so
%{_qt5_plugindir}/imageformats/libqico.so
%{_qt5_plugindir}/imageformats/libqjpeg.so
%{_qt5_plugindir}/platforminputcontexts/libcomposeplatforminputcontextplugin.so
%{_qt5_plugindir}/platforminputcontexts/libibusplatforminputcontextplugin.so
%if 0%{?egl}
%{_qt5_plugindir}/platforms/libqeglfs.so
%{_qt5_plugindir}/platforms/libqkms.so
%{_qt5_plugindir}/platforms/libqminimalegl.so
%endif
%{_qt5_plugindir}/platforms/libqdirectfb.so
%{_qt5_plugindir}/platforms/libqlinuxfb.so
%{_qt5_plugindir}/platforms/libqminimal.so
%{_qt5_plugindir}/platforms/libqoffscreen.so
%{_qt5_plugindir}/platforms/libqxcb.so
%{_qt5_plugindir}/platformthemes/libqgtk2.so
%{_qt5_plugindir}/printsupport/libcupsprintersupport.so


%changelog
* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 5.3.0-10
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 5.3.0-9
- 为 Magic 3.0 重建

* Thu Jun 12 2014 Liu Di <liudidi@gmail.com> - 5.3.0-8
- 为 Magic 3.0 重建

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 30 2014 Rex Dieter <rdieter@fedoraproject.org> 5.3.0-6
- %%ix86: build -no-sse2 (#1103185)

* Tue May 27 2014 Rex Dieter <rdieter@fedoraproject.org> 5.3.0-5
- BR: pkgconfig(xcb-xkb) > 1.10 (f21+)
- allow possibility for libxkbcommon-0.4.x only

* Fri May 23 2014 Rex Dieter <rdieter@fedoraproject.org> 5.3.0-4
- -system-libxkbcommon (f21+)

* Thu May 22 2014 Rex Dieter <rdieter@fedoraproject.org> 5.3.0-3
- qt5-qtbase-5.3.0-2.fc21 breaks keyboard input (#1100213)

* Wed May 21 2014 Rex Dieter <rdieter@fedoraproject.org> 5.3.0-2
- limit -reduce-relocations to %%ix86 x86_64 archs (QTBUG-36129)

* Wed May 21 2014 Jan Grulich <jgrulich@redhat.com> 5.3.0-1
- 5.3.0

* Thu Apr 24 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2.1-8
- DoS vulnerability in the GIF image handler (QTBUG-38367)

* Wed Mar 26 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2.1-7
- support ppc64le multilib (#1080629)

* Wed Mar 12 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> 5.2.1-6
- reenable documentation

* Sat Mar 08 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> 5.2.1-5
- make the QMAKE_STRIP sed not sensitive to whitespace (see #1074041 in Qt 4)

* Tue Feb 18 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2.1-4
- undefine QMAKE_STRIP (and friends), so we get useful -debuginfo pkgs (#1065636)

* Wed Feb 12 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2.1-3
- bootstrap for libicu bump

* Wed Feb 05 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2.1-2
- qconfig.pri: +alsa +kms +pulseaudio +xcb-sm

* Wed Feb 05 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2.1-1
- 5.2.1

* Sat Feb 01 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-11
- better %%rpm_macros_dir handling

* Wed Jan 29 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> - 5.2.0-10
- fix the allow-forcing-llvmpipe patch to patch actual caller of __glXInitialize

* Wed Jan 29 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> - 5.2.0-9
- use software OpenGL (llvmpipe) if the hardware driver doesn't support OpenGL 2

* Tue Jan 28 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-8
- (re)enable -docs

* Mon Jan 27 2014 Rex Dieter <rdieter@fedoraproject.org> - 5.2.0-7
- unconditionally enable freetype lcd_filter
- (temp) disable docs (libxcb bootstrap)

* Sun Jan 26 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-6
- fix %%_qt5_examplesdir macro

* Sat Jan 25 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-5
- -examples subpkg 

* Mon Jan 13 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> - 5.2.0-4
- fix QTBUG-35459 (too low entityCharacterLimit=1024 for CVE-2013-4549)
- fix QTBUG-35460 (error message for CVE-2013-4549 is misspelled)
- reenable docs on Fedora (accidentally disabled)

* Mon Jan 13 2014 Rex Dieter <rdieter@fedoraproject.org> - 5.2.0-3
- move sql build deps into subpkg sections
- macro'ize ibase,tds support (disabled on rhel)

* Thu Jan 02 2014 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-2
- -devel: qtsql apparently wants all drivers available at buildtime

* Thu Dec 12 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-1
- 5.2.0

* Fri Dec 06 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.12.rc1
- qt5-base-devel.x86_64 qt5-base-devel.i686 file conflict qconfig.h (#1036956)

* Thu Dec 05 2013 Rex Dieter <rdieter@fedoraproject.org> - 5.2.0-0.11.rc1
- needs a minimum version on sqlite build dependency (#1038617)
- fix build when doc macro not defined

* Mon Dec 02 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.10.rc1
- 5.2.0-rc1
- revert/omit recent egl packaging changes
- -doc install changes-5.* files here (#989149)

* Tue Nov 26 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.8.beta1.20131108_141
- Install changes-5.x.y file (#989149)

* Mon Nov 25 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.7.beta1.20131108_141
- enable -doc only on primary archs (allow secondary bootstrap)

* Fri Nov 22 2013 Lubomir Rintel <lkundrak@v3.sk> 5.2.0-0.6.beta1.20131108_141
- Enable EGL support

* Sat Nov 09 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.5.beta1.20131108_141
- 2013-11-08_141 snapshot, arm switch qreal double

* Thu Oct 24 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.4.beta1
- 5.2.0-beta1

* Wed Oct 16 2013 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-0.3.alpha
- disable -docs (for ppc bootstrap mostly)

* Wed Oct 16 2013 Lukáš Tinkl <ltinkl@redhat.com> - 5.2.0-0.2.alpha
- Fixes #1005482 - qtbase FTBFS on ppc/ppc64

* Tue Oct 01 2013 Rex Dieter <rdieter@fedoraproject.org> - 5.2.0-0.1.alpha
- 5.2.0-alpha
- -system-harfbuzz
- rename subpkg -x11 => -gui
- move some gui-related plugins base => -gui
- don't use symlinks in %%_qt5_bindir (more qtchooser-friendly)

* Fri Sep 27 2013 Rex Dieter <rdieter@fedoraproject.org> - 5.1.1-6
- -doc subpkg (not enabled)
- enable %%check

* Mon Sep 23 2013 Dan Horák <dan[at]danny.cz> - 5.1.1-5
- fix big endian builds

* Wed Sep 11 2013 Rex Dieter <rdieter@fedoraproject.org> 5.1.1-4
- macros.qt5: use newer location, use unexpanded macros

* Sat Sep 07 2013 Rex Dieter <rdieter@fedoraproject.org> 5.1.1-3
- ExcludeArch: ppc64 ppc (#1005482)

* Fri Sep 06 2013 Rex Dieter <rdieter@fedoraproject.org> 5.1.1-2
- BR: pkgconfig(libudev) pkgconfig(xkbcommon) pkgconfig(xcb-xkb)

* Tue Aug 27 2013 Rex Dieter <rdieter@fedoraproject.org> 5.1.1-1
- 5.1.1

* Sat Aug 03 2013 Petr Pisar <ppisar@redhat.com> - 5.0.2-8
- Perl 5.18 rebuild

* Tue Jul 30 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.2-7
- enable qtchooser support

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 5.0.2-6
- Perl 5.18 rebuild

* Wed May 08 2013 Than Ngo <than@redhat.com> - 5.0.2-5
- add poll support, thanks to fweimer@redhat.com (QTBUG-27195)

* Thu Apr 18 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.2-4
- respin lowmem patch to apply (unconditionally) to gcc-4.7.2 too

* Fri Apr 12 2013 Dan Horák <dan[at]danny.cz> - 5.0.2-3
- rebase the lowmem patch

* Wed Apr 10 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.2-2
- more cmake_path love (#929227)

* Wed Apr 10 2013 Rex Dieter <rdieter@fedoraproject.org> - 5.0.2-1
- 5.0.2
- fix cmake config (#929227)

* Tue Apr 02 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.2-0.1.rc1
- 5.0.2-rc1

* Sat Mar 16 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.1-6
- pull in upstream gcc-4.8.0 buildfix

* Tue Feb 26 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.1-5
- -static subpkg, Requires: fontconfig-devel,glib2-devel,zlib-devel
- -devel: Requires: pkgconfig(gl)

* Mon Feb 25 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.1-4
- create/own %%{_qt5_plugindir}/iconengines
- -devel: create/own %%{_qt5_archdatadir}/mkspecs/modules
- cleanup .prl

* Sat Feb 23 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.1-3
- +%%_qt5_libexecdir

* Sat Feb 23 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.1-2
- macros.qt5: fix %%_qt5_headerdir, %%_qt5_datadir, %%_qt5_plugindir

* Thu Jan 31 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.1-1
- 5.0.1
- lowmem patch for %%arm, s390

* Wed Jan 30 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.0-4
- %%build: -system-pcre, BR: pkgconfig(libpcre)
- use -O1 optimization on lowmem (s390) arch

* Thu Jan 24 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.0-3
- enable (non-conflicting) qtchooser support

* Wed Jan 09 2013 Rex Dieter <rdieter@fedoraproject.org> 5.0.0-2
- add qtchooser support (disabled by default)

* Wed Dec 19 2012 Rex Dieter <rdieter@fedoraproject.org> 5.0.0-1
- 5.0 (final)

* Thu Dec 13 2012 Rex Dieter <rdieter@fedoraproject.org> 5.0.0-0.4.rc2
- 5.0-rc2
- initial try at putting non-conflicting binaries in %%_bindir

* Thu Dec 06 2012 Rex Dieter <rdieter@fedoraproject.org> 5.0.0-0.3.rc1 
- 5.0-rc1

* Wed Nov 28 2012 Rex Dieter <rdieter@fedoraproject.org> 5.0.0-0.2.beta2
- qtbase --> qt5-qtbase

* Mon Nov 19 2012 Rex Dieter <rdieter@fedoraproject.org> 5.0.0-0.1.beta2
- %%build: -accessibility
- macros.qt5: +%%_qt5_archdatadir +%%_qt5_settingsdir
- pull in a couple more configure-related upstream patches 

* Wed Nov 14 2012 Rex Dieter <rdieter@fedoraproject.org> 5.0.0-0.0.beta2
- first try

