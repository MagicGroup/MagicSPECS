#
# spec file for package tdelibs (version R14)
#
# Copyright (c) 2014 Trinity Desktop Environment
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.
#
# Please submit bugfixes or comments via http://www.trinitydesktop.org/
#

# BUILD WARNING:
#  Remove qt-devel and qt3-devel and any kde*-devel on your system !
#  Having KDE libraries may cause FTBFS here !

# TDE variables
%define tde_epoch 2
%if "%{?tde_version}" == ""
%define tde_version 14.0.1
%endif
%define tde_pkg tdelibs
%define tde_prefix /opt/trinity
%define tde_bindir %{tde_prefix}/bin
%define tde_confdir %{_sysconfdir}/trinity
%define tde_datadir %{tde_prefix}/share
%define tde_docdir %{tde_datadir}/doc
%define tde_includedir %{tde_prefix}/include
%define tde_libdir %{tde_prefix}/%{_lib}
%define tde_tdeappdir %{tde_datadir}/applications/tde
%define tde_tdedocdir %{tde_docdir}/tde
%define tde_tdeincludedir %{tde_includedir}/tde
%define tde_tdelibdir %{tde_libdir}/trinity

# If TDE is built in a specific prefix (e.g. /opt/trinity), the release will be suffixed with ".opt".
%if "%{?tde_prefix}" != "/usr"
%define _variant .opt
%endif


Name:			trinity-%{tde_pkg}
Version:		%{tde_version}
Release:		%{?!preversion:1}%{?preversion:0_%{preversion}}%{?dist}%{?_variant}.4
Summary:		TDE Libraries
Summary(zh_CN.UTF-8): TDE 基本库
Group:			System/GUI/Other
Group(zh_CN.UTF-8): 系统/GUI/其它
URL:			http://www.trinitydesktop.org/

License:		GPLv2+

#Vendor:			Trinity Desktop
#Packager:		Francois Andriot <francois.andriot@free.fr>

Prefix:			%{tde_prefix}
BuildRoot:		%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:		%{name}-%{version}%{?preversion:~%{preversion}}.tar.gz
Source1:		%{name}-rpmlintrc

Patch0:			tdelibs-14.0.1.patch
Patch1:			trinity-tdelibs-14.0.1-fixper522.patch

#添加农历支持
Patch2:			trinity-tdelibs-add-lunar.patch

Obsoletes:		tdelibs < %{version}-%{release}
Provides:		tdelibs = %{version}-%{release}
Obsoletes:		trinity-kdelibs < %{version}-%{release}
Provides:		trinity-kdelibs = %{version}-%{release}
Obsoletes:		trinity-kdelibs-apidocs < %{version}-%{release}
Provides:		trinity-kdelibs-apidocs = %{version}-%{release}

# Trinity dependencies
BuildRequires:	libtqt4-devel = %{tde_epoch}:4.2.0
BuildRequires:	trinity-arts-devel >= %{tde_epoch}:1.5.10
BuildRequires:	libdbus-tqt-1-devel >= %{tde_epoch}:0.63
BuildRequires:	libdbus-1-tqt-devel >= %{tde_epoch}:0.9
BuildRequires:	trinity-filesystem >= %{tde_version}

Requires:		trinity-arts >= %{tde_epoch}:1.5.10
Requires:		trinity-filesystem >= %{tde_version}
Requires:		fileshareset >= 2.0

BuildRequires:	cmake >= 2.8
BuildRequires:	gcc-c++
BuildRequires:	pkgconfig
BuildRequires:	fdupes

# KRB5 support
BuildRequires:	krb5-devel

# XSLT support
BuildRequires:	libxslt-devel

# ALSA support
BuildRequires:	alsa-lib-devel

# IDN support
BuildRequires:	libidn-devel

# CUPS support
BuildRequires:	cups-devel

# TIFF support
BuildRequires:	libtiff-devel

# OPENSSL support
BuildRequires:	openssl-devel

# ACL support
BuildRequires:	libacl-devel

# GLIB2 support
BuildRequires:	glib2-devel

# LUA support are not ready yet
#BuildRequires:	lua-devel

# LIBART_LGPL support
BuildRequires:	libart_lgpl-devel

# ASPELL support
BuildRequires:	aspell
BuildRequires:	aspell-devel

# GAMIN support
#  Not on openSUSE.
%define with_gamin 1
BuildRequires:	gamin-devel

# PCRE support
%define with_pcre 1
BuildRequires:	pcre-devel

# INOTIFY support
%define with_inotify 1

# BZIP2 support
BuildRequires:	bzip2-devel

# UTEMPTER support
BuildRequires:	libutempter-devel

# HSPELL support
%define with_hspell 1
BuildRequires:	hspell-devel

# JASPER support
%define with_jasper 1
BuildRequires:	jasper-devel

# AVAHI support
%define with_avahi 1
BuildRequires:	avahi-devel
Requires:		avahi

# OPENEXR support
%define with_openexr 1
BuildRequires:	OpenEXR-devel

# LIBTOOL
BuildRequires:	libtool
BuildRequires:	libtool-ltdl-devel

# X11 support
BuildRequires:	xorg-x11-proto-devel

# ICEAUTH
Requires:		xorg-x11-server-utils

# XZ support
%define with_lzma 1
BuildRequires:	xz-devel

# Certificates support
BuildRequires:	ca-certificates
Requires:		ca-certificates
%define	cacert	%{_sysconfdir}/pki/tls/certs/ca-bundle.crt
Requires:		openssl
%if "%{cacert}" != ""
Requires:		%{cacert}
%endif

# XRANDR support
#  On RHEL5, xrandr library is too old.
%define with_xrandr 1

# XCOMPOSITE support
%define xcomposite_devel libXcomposite-devel
%{?xcomposite_devel:BuildRequires: %{xcomposite_devel}}

# XT support
%define xt_devel libXt-devel
%{?xt_devel:BuildRequires: %{xt_devel}}

### New features in TDE R14

# LIBMAGIC support
BuildRequires:	file-devel

# NETWORKMANAGER support
%define with_nm 1
BuildRequires:	NetworkManager-glib-devel

# UDEV support
%define with_tdehwlib 1
BuildRequires:	libudev-devel

# HAL support
%if 0%{?rhel} == 5
%define with_hal 1
%endif

# UDISKS support
%define with_udisks 1
BuildRequires:	udisks-devel
Requires:		udisks

# PMOUNT support
#Requires:		pmount

# UDISKS2 support
%define with_udisks2 1
BuildRequires:	libudisks2-devel
Requires:		udisks2

# DEVICEKIT POWER support
%if 0%{?rhel} == 6
%define with_devkitpower 1
Requires:		DeviceKit-power
%endif

# UPOWER support
%define with_upower 1
Requires:		upower

# SYSTEMD support
%define with_systemd 1


%description
Libraries for the Trinity Desktop Environment:
TDE Libraries included: tdecore (TDE core library), tdeui (user interface),
kfm (file manager), tdehtmlw (HTML widget), tdeio (Input/Output, networking),
kspell (spelling checker), jscript (javascript), kab (addressbook),
kimgio (image manipulation).

%description -l zh_CN.UTF-8
TDE 的基本库。

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING COPYING-DOCS COPYING.LIB README TODO
%{_sysconfdir}/ld.so.conf.d/tde-%{_arch}.conf
%{tde_bindir}/artsmessage
%{tde_bindir}/cupsdconf
%{tde_bindir}/cupsdoprint
%{tde_bindir}/dcop
%{tde_bindir}/dcopclient
%{tde_bindir}/dcopfind
%{tde_bindir}/dcopobject
%{tde_bindir}/dcopquit
%{tde_bindir}/dcopref
%{tde_bindir}/dcopserver
%{tde_bindir}/dcopserver_shutdown
%{tde_bindir}/dcopstart
%{tde_bindir}/imagetops
%{tde_bindir}/tdeab2tdeabc
%{tde_bindir}/kaddprinterwizard
%{tde_bindir}/tdebuildsycoca
%{tde_bindir}/tdecmshell
%{tde_bindir}/tdeconf_update
%{tde_bindir}/kcookiejar
%{tde_bindir}/tde-config
%{tde_bindir}/tde-menu
%{tde_bindir}/kded
%{tde_bindir}/tdeinit
%{tde_bindir}/tdeinit_shutdown
%{tde_bindir}/tdeinit_wrapper
%{tde_bindir}/tdesu_stub
%{tde_bindir}/kdetcompmgr
%{tde_bindir}/kdontchangethehostname
%{tde_bindir}/tdedostartupconfig
%{tde_bindir}/tdefile
%{tde_bindir}/kfmexec
%{tde_bindir}/tdehotnewstuff
%{tde_bindir}/kinstalltheme
%{tde_bindir}/tdeio_http_cache_cleaner
%{tde_bindir}/tdeio_uiserver
%{tde_bindir}/tdeioexec
%{tde_bindir}/tdeioslave
%{tde_bindir}/tdeiso_info
%{tde_bindir}/tdelauncher
%if 0%{?with_elficon}
%{tde_bindir}/tdelfeditor
%endif
%{tde_bindir}/tdemailservice
%{tde_bindir}/tdemimelist
%{tde_bindir}/tdesendbugmail
%{tde_bindir}/kshell
%{tde_bindir}/tdestartupconfig
%{tde_bindir}/tdetelnetservice
%{tde_bindir}/tdetradertest
%{tde_bindir}/kwrapper
%{tde_bindir}/lnusertemp
%{tde_bindir}/make_driver_db_cups
%{tde_bindir}/make_driver_db_lpr
%{tde_bindir}/meinproc
%{tde_bindir}/networkstatustestservice
%{tde_bindir}/start_tdeinit_wrapper
%{tde_bindir}/checkXML
%{tde_bindir}/ksvgtopng
%{tde_bindir}/tdeunittestmodrunner
%{tde_bindir}/preparetips
%{tde_tdelibdir}/*
%{tde_libdir}/lib*.so.*
%{tde_libdir}/libtdeinit_*.la
%{tde_libdir}/libtdeinit_*.so
%{tde_datadir}/applications/tde/*.desktop
%{tde_datadir}/autostart/tdeab2tdeabc.desktop
%{tde_datadir}/applnk/tdeio_iso.desktop
%{tde_datadir}/apps/*
%exclude %{tde_datadir}/apps/ksgmltools2/
%{tde_datadir}/emoticons/*
%{tde_datadir}/icons/crystalsvg/
%{tde_datadir}/icons/default.tde
%{tde_datadir}/icons/hicolor/index.theme
%{tde_datadir}/locale/all_languages
%{tde_datadir}/mimelnk/*/*.desktop
%{tde_datadir}/services/*
%{tde_datadir}/servicetypes/*
%{tde_tdedocdir}/HTML/en/common/*
%{tde_tdedocdir}/HTML/en/tdespell/

# Global Trinity configuration
%config %{tde_confdir}

# Some setuid binaries need special care
%attr(4755,root,root) %{tde_bindir}/kgrantpty
%attr(4755,root,root) %{tde_bindir}/kpac_dhcp_helper
%attr(4711,root,root) %{tde_bindir}/start_tdeinit

%config %{_sysconfdir}/xdg/menus/tde-applications.menu
%config %{_sysconfdir}/xdg/menus/tde-applications.menu-no-kde

# DBUS stuff, related to TDE hwlib
%if 0%{?with_tdehwlib}
%{tde_bindir}/tde_dbus_hardwarecontrol
%config %{_sysconfdir}/dbus-1/system.d/org.trinitydesktop.hardwarecontrol.conf
%{_datadir}/dbus-1/system-services/org.trinitydesktop.hardwarecontrol.service
%endif

%pre
# TDE Bug #1074
if [ -d "%{tde_datadir}/locale/all_languages" ]; then
  rm -rf "%{tde_datadir}/locale/all_languages"
fi

%post
/sbin/ldconfig || :

%postun
/sbin/ldconfig || :

##########

%package devel
Summary:	TDE Libraries (Development files)
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:		Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:	%{name} = %{version}-%{release}

Obsoletes:	tdelibs-devel < %{version}-%{release}
Provides:	tdelibs-devel = %{version}-%{release}
Obsoletes:	trinity-kdelibs-devel < %{version}-%{release}
Provides:	trinity-kdelibs-devel = %{version}-%{release}

Requires:	libtqt3-mt-devel >= 3.5.0
Requires:	libtqt4-devel = %{tde_epoch}:4.2.0
Requires:	trinity-arts-devel >= %{tde_epoch}:1.5.10
Requires:	libart_lgpl-devel
%{?xcomposite_devel:Requires: %{xcomposite_devel}}
%{?xt_devel:Requires: %{xt_devel}}

%description devel
This package includes the header files you will need to compile
applications for TDE.
%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%files devel
%defattr(-,root,root,-)
%{tde_bindir}/dcopidl*
%{tde_bindir}/*config_compiler
%{tde_bindir}/maketdewidgets
%{tde_datadir}/apps/ksgmltools2/
%{tde_tdeincludedir}/*
%{tde_libdir}/*.la
%{tde_libdir}/*.so
%{tde_libdir}/*.a
%exclude %{tde_libdir}/libtdeinit_*.la
%exclude %{tde_libdir}/libtdeinit_*.so
%{tde_datadir}/cmake/tdelibs.cmake
%{tde_libdir}/pkgconfig/tdelibs.pc

%post devel
/sbin/ldconfig || :

%postun devel
/sbin/ldconfig || :

##########

%prep
%setup -q -n %{name}-%{version}%{?preversion:~%{preversion}}
%patch0 -p1 -b .ftbfs
%patch1 -p1
%patch2 -p1

# RHEL 5: remove tdehwlib stuff from include files, to avoid FTBFS in tdebindings
%if 0%{?rhel} == 5
%__sed -i "tdecore/kinstance.h" \
       -i "tdecore/tdeglobal.h" \
       -e "/#ifdef __TDE_HAVE_TDEHWLIB/,/#endif/d"
%endif


%build
unset QTDIR QTINC QTLIB
export PATH="%{tde_bindir}:${PATH}"
export PKG_CONFIG_PATH="%{tde_libdir}/pkgconfig"

if [ -d "/usr/X11R6" ]; then
  export RPM_OPT_FLAGS="${RPM_OPT_FLAGS} -L/usr/X11R6/%{_lib} -I/usr/X11R6/include"
fi

export TDEDIR="%{tde_prefix}"

if ! rpm -E %%cmake|grep -q "cd build"; then
  %__mkdir_p build
  cd build
fi

%cmake \
  -DCMAKE_BUILD_TYPE="RelWithDebInfo" \
  -DCMAKE_C_FLAGS="${RPM_OPT_FLAGS} -DNDEBUG" \
  -DCMAKE_CXX_FLAGS="${RPM_OPT_FLAGS} -DNDEBUG" \
  -DCMAKE_SKIP_RPATH=OFF \
  -DCMAKE_INSTALL_RPATH="%{tde_libdir}" \
  -DCMAKE_NO_BUILTIN_CHRPATH=ON \
  -DCMAKE_VERBOSE_MAKEFILE=ON \
  -DWITH_GCC_VISIBILITY=ON \
  \
  -DCMAKE_INSTALL_PREFIX="%{tde_prefix}" \
  -DBIN_INSTALL_DIR="%{tde_bindir}" \
  -DCONFIG_INSTALL_DIR="%{tde_confdir}" \
  -DDOC_INSTALL_DIR="%{tde_docdir}" \
  -DINCLUDE_INSTALL_DIR="%{tde_tdeincludedir}" \
  -DLIB_INSTALL_DIR="%{tde_libdir}" \
  -DPKGCONFIG_INSTALL_DIR="%{tde_libdir}/pkgconfig" \
  -DSHARE_INSTALL_PREFIX="%{tde_datadir}" \
  \
  -DWITH_ALL_OPTIONS=ON \
  -DWITH_ARTS=ON \
  -DWITH_ALSA=ON \
  -DWITH_LIBART=ON \
  -DWITH_LIBIDN=ON \
  -DWITH_SSL=ON \
  -DWITH_CUPS=ON \
  -DWITH_LUA=OFF \
  -DWITH_TIFF=ON \
  %{?!with_jasper:-DWITH_JASPER=OFF} \
  %{?!with_openexr:-DWITH_OPENEXR=OFF} \
  -DWITH_UTEMPTER=ON \
  %{?!with_elficon:-DWITH_ELFICON=OFF} \
  %{?!with_avahi:-DWITH_AVAHI=OFF} \
  %{?!with_pcre:-DWITH_PCRE=OFF} \
  %{?!with_inotify:-DWITH_INOTIFY=OFF} \
  %{?!with_gamin:-DWITH_GAMIN=OFF} \
  %{?!with_tdehwlib:-DWITH_TDEHWLIB=OFF} \
  %{?!with_tdehwlib:-DWITH_TDEHWLIB_DAEMONS=OFF} \
  %{?with_hal:-DWITH_HAL=ON} \
  %{?with_devkitpower:-DWITH_DEVKITPOWER=ON} \
  %{?with_systemd:-DWITH_LOGINDPOWER=ON} \
  %{?!with_upower:-DWITH_UPOWER=OFF} \
  %{?!with_udisks:-DWITH_UDISKS=OFF} \
  %{?!with_udisks2:-DWITH_UDISKS2=OFF} \
  -DWITH_CONSOLEKIT=ON \
  %{?with_nm:-DWITH_NETWORK_MANAGER_BACKEND=ON} \
  -DWITH_SUDO_TDESU_BACKEND=OFF \
  -DWITH_OLD_XDG_STD=OFF \
  %{?!with_lzma:-DWITH_LZMA=OFF} \
  -DWITH_LIBBFD=OFF \
  %{?!with_xrandr:-DWITH_XRANDR=OFF} \
  -DWITH_XCOMPOSITE=ON \
  -DWITH_KDE4_MENU_SUFFIX=OFF \
  \
  -DWITH_ASPELL=ON \
  %{?!with_hspell:-DWITH_HSPELL=OFF} \
  -DWITH_TDEICONLOADER_DEBUG=OFF \
  ..

%__make %{?_smp_mflags} || %__make


%install
%__rm -rf "%{?buildroot}"
%__make install DESTDIR="%{?buildroot}" -C build

# Use system-wide CA certificates
%if "%{?cacert}" != ""
%__rm -f "%{?buildroot}%{tde_datadir}/apps/kssl/ca-bundle.crt"
%__ln_s "%{cacert}" "%{?buildroot}%{tde_datadir}/apps/kssl/ca-bundle.crt"
%endif

# Symlinks duplicate files (mostly under 'ksgmltools2')
%fdupes -s "%{?buildroot}"

# Remove setuid bit on some binaries.
chmod 0755 "%{?buildroot}%{tde_bindir}/kgrantpty"
chmod 0755 "%{?buildroot}%{tde_bindir}/kpac_dhcp_helper"
chmod 0755 "%{?buildroot}%{tde_bindir}/start_tdeinit"

# fileshareset 2.0 is provided separately.
# Remove integrated fileshareset 1.0 .
%__rm -f "%{?buildroot}%{tde_bindir}/filesharelist"
%__rm -f "%{?buildroot}%{tde_bindir}/fileshareset"

mkdir -p %{buildroot}%{_sysconfdir}/ld.so.conf.d
cat >> %{buildroot}%{_sysconfdir}/ld.so.conf.d/tde-%{_arch}.conf << EOF
/opt/trinity/%{_lib}
EOF

%clean
%__rm -rf "%{?buildroot}"

%changelog
* Thu Nov 05 2015 Liu Di <liudidi@gmail.com> - 14.0.1-1.opt.4
- 为 Magic 3.0 重建

* Tue Oct 13 2015 Liu Di <liudidi@gmail.com> - 14.0.1-1.opt.3
- 为 Magic 3.0 重建

* Tue Oct 13 2015 Liu Di <liudidi@gmail.com> - 14.0.1-1.opt.2
- 为 Magic 3.0 重建

* Tue Oct 06 2015 Liu Di <liudidi@gmail.com> - 14.0.1-1.opt.1
- 为 Magic 3.0 重建

* Tue Jul 21 2015 Francois Andriot <francois.andriot@free.fr> - 14.0.1-1
- Initial release for TDE 14.0.1
