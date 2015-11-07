#
# spec file for package kaffeine (version R14)
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

# TDE variables
%define tde_epoch 2
%if "%{?tde_version}" == ""
%define tde_version 14.0.1
%endif
%define tde_pkg kaffeine
%define tde_prefix /opt/trinity
%define tde_appdir %{tde_datadir}/applications
%define tde_bindir %{tde_prefix}/bin
%define tde_datadir %{tde_prefix}/share
%define tde_docdir %{tde_datadir}/doc
%define tde_includedir %{tde_prefix}/include
%define tde_libdir %{tde_prefix}/%{_lib}
%define tde_mandir %{tde_datadir}/man
%define tde_tdeappdir %{tde_datadir}/applications/tde
%define tde_tdedocdir %{tde_docdir}/tde
%define tde_tdeincludedir %{tde_includedir}/tde
%define tde_tdelibdir %{tde_libdir}/trinity


Name:			trinity-%{tde_pkg}
Epoch:			%{tde_epoch}
Version:		0.8.8
Release:		%{?!preversion:1}%{?preversion:0_%{preversion}}%{?dist}%{?_variant}.1
Summary:		Xine-based media player
Summary(zh_CN.UTF-8): 基于 Xine 的媒体播放器
Group:			Applications/Multimedia
Group(zh_CN.UTF-8): 应用程序/多媒体
URL:			http://kaffeine.sourceforge.net/

License:	GPLv2+

#Vendor:		Trinity Desktop
#Packager:	Francois Andriot <francois.andriot@free.fr>

Prefix:			%{_prefix}
BuildRoot:		%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:		%{name}-%{tde_version}%{?preversion:~%{preversion}}.tar.gz

Patch1:		%{name}-14.0.1-tqt.patch

Source2:        kaffeine.desktop
Source3:        kaffeine_part.desktop
Source4:        kaffeine.zh_CN.po
Source5:        kaffeine.zh_TW.po
Source6:        mms.protocol
Source7:        rtsp.protocol

BuildRequires:	trinity-tdelibs-devel >= %{tde_version}
BuildRequires:	trinity-tdebase-devel >= %{tde_version}
BuildRequires:	desktop-file-utils

BuildRequires:	gettext

BuildRequires:	autoconf automake libtool m4
BuildRequires:	gcc-c++
BuildRequires:	pkgconfig

# VORBIS support
BuildRequires:	libvorbis-devel

# CDDA support
BuildRequires:	libcdio-devel
BuildRequires:	cdparanoia
BuildRequires:	cdparanoia-devel

# X11 stuff
BuildRequires:	libXext-devel 
BuildRequires:	libXtst-devel
BuildRequires:	libXinerama-devel
BuildRequires: libxcb-devel

# GSTREAMER support
%define with_gstreamer 1
BuildRequires:	gstreamer-plugins-base-devel >= 0.10

# XINE support
%define with_xine 1
BuildRequires: xine-lib-devel

# LAME support
%define with_lame 1
BuildRequires:	lame-devel

# WTF support
BuildRequires:	glibc-kernheaders 

Requires: %{name}-libs = %{?epoch:%{epoch}:}%{version}-%{release}

%description
Kaffeine is a xine-based media player for TDE.  It plays back CDs,
and VCDs, and can decode all (local or streamed) multimedia formats 
supported by xine-lib.
Additionally, Kaffeine is fully integrated in TDE, it supports drag
and drop and provides an editable playlist, a bookmark system, a
Konqueror plugin, OSD and much more.

%description -l zh_CN.UTF-8
TDE 下基于 Xine 的媒体播放器。

%files -f %{tde_pkg}.lang
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING README TODO
%{tde_bindir}/kaffeine
%{tde_libdir}/libkaffeinepart.so
%{tde_tdelibdir}/lib*.*
%{tde_datadir}/appl*/*/*.desktop
%if 0%{?with_gstreamer}
%{tde_datadir}/apps/gstreamerpart/
%endif
%{tde_datadir}/apps/kaffeine/
%{tde_datadir}/apps/konqueror/servicemenus/*.desktop
%{tde_datadir}/apps/profiles/
%{tde_datadir}/icons/hicolor/*/*/*
%{tde_datadir}/mimelnk/*/*.desktop
%{tde_datadir}/service*/*.desktop
%{tde_tdedocdir}/HTML/en/kaffeine/

%post
touch --no-create %{tde_datadir}/icons/hicolor ||:
gtk-update-icon-cache -q %{tde_datadir}/icons/hicolor 2> /dev/null ||:
update-desktop-database >& /dev/null ||:
/sbin/ldconfig || :

%postun
touch --no-create %{_datadir}/icons/hicolor ||:
gtk-update-icon-cache -q %{_datadir}/icons/hicolor 2> /dev/null ||:
update-desktop-database >& /dev/null ||:
/sbin/ldconfig || :

##########

%package devel
Summary:		Development files for %{name}
Summary(zh_CN.UTF-8): %{name} 的开发包
Group:			Development/Libraries
Group(zh_CN.UTF-8): 开发/库
Requires:		%{name}-libs = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:		trinity-tdelibs-devel

%description devel
%{summary}.

%description devel -l zh_CN.UTF-8
%{name} 的开发包。

%files devel
%defattr(-,root,root,-)
%{tde_tdeincludedir}/kaffeine/
%{tde_libdir}/lib*.so
%exclude %{tde_libdir}/libkaffeinepart.so

%post devel
/sbin/ldconfig || :

%postun devel
/sbin/ldconfig || :

##########

%package libs
Summary:		%{name} runtime libraries
Summary(zh_CN.UTF-8): %{name} 的运行库
Group:			System Environment/Libraries
Group(zh_CN.UTF-8): 系统环境/库
# include to be paranoid, installing libs-only is still mostly untested -- Rex
Requires:		%{name} = %{?epoch:%{epoch}:}%{version}-%{release}

%description libs
%{summary}.
%description libs -l zh_CN.UTF-8
%{name} 的运行库。

%files libs
%defattr(-,root,root,-)
%{tde_libdir}/lib*.so.*

%post libs
/sbin/ldconfig || :

%postun libs
/sbin/ldconfig || :

##########

%prep
%setup -q -n %{name}-%{tde_version}%{?preversion:~%{preversion}}
%patch1 -p1

%__cp "/usr/share/aclocal/libtool.m4" "admin/libtool.m4.in"
%__cp "/usr/share/libtool/config/ltmain.sh" "admin/ltmain.sh" || %__cp "/usr/share/libtool/ltmain.sh" "admin/ltmain.sh"
%__make -f "admin/Makefile.common"


%build
unset QTDIR QTINC QTLIB
export PATH="%{tde_bindir}:${PATH}"

%configure \
  --prefix=%{tde_prefix} \
  --exec-prefix=%{tde_prefix} \
  --bindir=%{tde_bindir} \
  --libdir=%{tde_libdir} \
  --datadir=%{tde_datadir} \
  --includedir=%{tde_tdeincludedir} \
  --mandir=%{tde_mandir} \
  \
  --disable-dependency-tracking \
  --disable-debug \
  --enable-new-ldflags \
  --enable-final \
  --enable-closure \
  --enable-rpath \
  --disable-gcc-hidden-visibility \
  \
  --with-xinerama \
  --with-gstreamer \
  --with-lame \
%if 0%{?rhel} > 0 && 0%{?rhel} <= 5
  --without-dvb \
%endif
  

%__make %{?_smp_mflags}


%install
export PATH="%{tde_bindir}:${PATH}"
%__rm -rf $RPM_BUILD_ROOT
%__make install DESTDIR=$RPM_BUILD_ROOT


%{__rm} -f %{buildroot}%{tde_datadir}/applications/kde/kaffeine.desktop
install -D -m 644 %{SOURCE2} %{buildroot}%{tde_datadir}/applications/kde/kaffeine.desktop
install -D -m 644 %{SOURCE3} %{buildroot}%{tde_datadir}/apps/kaffeine/kaffeine_part.desktop

msgfmt %{SOURCE4} -o %{buildroot}%{tde_datadir}/locale/zh_CN/LC_MESSAGES/kaffeine.mo

magic_rpm_clean.sh
## File lists
# locale's
%find_lang %{tde_pkg}

# Unpackaged files
rm -f $RPM_BUILD_ROOT%{tde_libdir}/lib*.la
rm -f $RPM_BUILD_ROOT%{tde_datadir}/mimelnk/application/x-mplayer2.desktop


%clean
rm -rf $RPM_BUILD_ROOT


%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 2:0.8.8-1.1
- 为 Magic 3.0 重建

* Fri Jul 05 2013 Francois Andriot <francois.andriot@free.fr> - 2:0.8.8-1
- Initial release for TDE 14.0.0
