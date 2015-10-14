#
# spec file for package kmplayer (version R14)
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
%define tde_pkg kmplayer
%define tde_prefix /opt/trinity
%define tde_bindir %{tde_prefix}/bin
%define tde_confdir %{_sysconfdir}/trinity
%define tde_datadir %{tde_prefix}/share
%define tde_docdir %{tde_datadir}/doc
%define tde_includedir %{tde_prefix}/include
%define tde_libdir %{tde_prefix}/%{_lib}
%define tde_mandir %{tde_datadir}/man
%define tde_tdeappdir %{tde_datadir}/applications/tde
%define tde_tdedocdir %{tde_docdir}/tde
%define tde_tdeincludedir %{tde_includedir}/tde
%define tde_tdelibdir %{tde_libdir}/trinity


Name:		trinity-%{tde_pkg}
Epoch:		%{tde_epoch}
Version:	0.10.0c
Release:	%{?!preversion:8}%{?preversion:7_%{preversion}}%{?dist}%{?_variant}
Summary:	Media player for Trinity
Summary(zh_CN.UTF-8): TDE 下的媒体播放器
Group:		Applications/Multimedia
Group(zh_CN.UTF-8): 应用程序/多媒体
URL:		http://www.trinitydesktop.org/
#URL:		http://kmplayer.kde.org

License:	GPLv2+

#Vendor:		Trinity Desktop
#Packager:	Francois Andriot <francois.andriot@free.fr>

Prefix:		%{tde_prefix}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:		%{name}-%{tde_version}%{?preversion:~%{preversion}}.tar.gz
Patch1:		trinity-kmplayer-14.0.1-tqt.patch

BuildRequires:	trinity-tdelibs-devel >= %{tde_version}
BuildRequires:	trinity-tdebase-devel >= %{tde_version}
BuildRequires:	desktop-file-utils

BuildRequires:	autoconf automake libtool m4
BuildRequires:	gcc-c++
BuildRequires:	pkgconfig
BuildRequires:	libtool

# DBUS support
BuildRequires:	trinity-dbus-tqt-devel >= %{tde_version}

# GSTREAMER support
BuildRequires:	gstreamer-devel
BuildRequires:	gstreamer-plugins-base-devel

# XINE support
%define with_xine 1
BuildRequires: xine-lib-devel

# X11 stuff
BuildRequires:	libXv-devel

# GTK2 stuff
BuildRequires:	gtk2-devel

# DBUS stuff
BuildRequires:	dbus-glib-devel

Requires:		%{name}-base = %{?epoch:%{epoch}:}%{version}-%{release}


%description
A basic audio/video viewer application for Trinity.

KMPlayer can:
* play DVD (DVDNav only with the Xine player)
* play VCD
* let the backend players play from a pipe (read from stdin)
* play from a TV device (experimental)
* show backend player's console output
* launch ffserver (only 0.4.8 works) when viewing from a v4l device
* DCOP KMediaPlayer interface support
* VDR viewer frontend (with *kxvplayer), configure VDR keys with standard TDE
  shortcut configure window
* Lots of configurable shortcuts. Highly recommended for the VDR keys
  (if you have VDR) and volume increase/decrease

%description -l zh_CN.UTF-8
TDE 下的媒体播放器。

%post
/sbin/ldconfig || :

%postun
/sbin/ldconfig || :

%files -f %{tde_pkg}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog INSTALL README TODO kmplayer.lsm
%{tde_bindir}/kmplayer
%{tde_bindir}/knpplayer
%{tde_bindir}/kxvplayer
%{tde_libdir}/libtdeinit_kmplayer.la
%{tde_libdir}/libtdeinit_kmplayer.so
%{tde_tdelibdir}/kmplayer.la
%{tde_tdelibdir}/kmplayer.so
%{tde_tdeappdir}/kmplayer.desktop
%exclude %{tde_datadir}/apps/kmplayer/bookmarks.xml
%exclude %{tde_datadir}/apps/kmplayer/kmplayerpartui.rc
%exclude %{tde_datadir}/apps/kmplayer/noise.gif
%exclude %{tde_datadir}/apps/kmplayer/pluginsinfo
%{tde_datadir}/apps/kmplayer/

##########

%package base
Group:			Applications/Multimedia
Group(zh_CN.UTF-8): 应用程序/多媒体
Summary:		Base files for KMPlayer [Trinity]
Summary(zh_CN.UTF-8): %{name} 的基本文件

%description base
Core files needed for KMPlayer.
%description base -l zh_CN.UTF-8
%{name} 的基本文件。

%post base
touch --no-create %{tde_datadir}/icons/hicolor || :
gtk-update-icon-cache --quiet %{tde_datadir}/icons/hicolor || :
/sbin/ldconfig || :

%postun base
touch --no-create %{tde_datadir}/icons/hicolor || :
gtk-update-icon-cache --quiet %{tde_datadir}/icons/hicolor || :
/sbin/ldconfig || :

%files base
%defattr(-,root,root,-)
%{tde_libdir}/libkmplayercommon.la
%{tde_libdir}/libkmplayercommon.so
%{tde_bindir}/kgstplayer
%{tde_bindir}/kxineplayer
%{tde_confdir}/kmplayerrc
%{tde_datadir}/apps/kmplayer/bookmarks.xml
%{tde_datadir}/apps/kmplayer/noise.gif
%{tde_datadir}/icons/hicolor/*/apps/kmplayer.png
%{tde_datadir}/icons/hicolor/*/apps/kmplayer.svgz
%{tde_datadir}/mimelnk/application/x-kmplayer.desktop
%{tde_datadir}/mimelnk/video/x-ms-wmp.desktop

##########

%package konq-plugins
Group:			Applications/Multimedia
Group(zh_CN.UTF-8): 应用程序/多媒体
Requires:		%{name}-base = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:		trinity-konqueror >= %{tde_version}
Summary:		KMPlayer plugin for KHTML/Konqueror [Trinity]
Summary(zh_CN.UTF-8): %{name} 的 KTHML/Konqueror 插件

%description konq-plugins
This plugin enables audio/video playback inside konqueror, using Xine (with
*kxineplayer) or GStreamer (with *kgstplayer), such as movie trailers, web
tv or radio. It mimics QuickTime, MS Media Player and RealPlayer plugin
browser plugins.
%description konq-plugins -l zh_CN.UTF-8
%{name} 的 KTHML/Konqueror 插件。

%files konq-plugins
%defattr(-,root,root,-)
%{tde_tdelibdir}/libkmplayerpart.la
%{tde_tdelibdir}/libkmplayerpart.so
%{tde_datadir}/apps/kmplayer/kmplayerpartui.rc
%{tde_datadir}/apps/kmplayer/pluginsinfo
%{tde_datadir}/services/kmplayer_part.desktop

##########

%package doc
Group:			Applications/Multimedia
Group(zh_CN.UTF-8): 应用程序/多媒体
Requires:		%{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Summary:		Handbook for KMPlayer [Trinity]
Summary(zh_CN.UTF-8): KMPlayer 的手册

%description doc
Documention for KMPlayer, a basic audio/video viewer application for TDE.

%description doc -l zh_CN.UTF-8
%{name} 的手册。

%files doc
%defattr(-,root,root,-)
%{tde_tdedocdir}/HTML/*/kmplayer

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
export PKG_CONFIG_PATH="%{tde_libdir}/pkgconfig:${PKG_CONFIG_PATH}"
export kde_confdir="%{tde_confdir}"

%configure \
  --prefix=%{tde_prefix} \
  --exec-prefix=%{tde_prefix} \
  --bindir=%{tde_bindir} \
  --datadir=%{tde_datadir} \
  --includedir=%{tde_tdeincludedir} \
  --libdir=%{tde_libdir} \
  --mandir=%{tde_mandir} \
  \
  --disable-dependency-tracking \
  --disable-debug \
  --enable-new-ldflags \
  --enable-final \
  --enable-closure \
  --enable-rpath \
  --disable-gcc-hidden-visibility

%__make %{?_smp_mflags} || %__make


%install
export PATH="%{tde_bindir}:${PATH}"
%__rm -rf %{buildroot}
%__make install DESTDIR=%{buildroot}
magic_rpm_clean.sh
%find_lang %{tde_pkg}

# Removes unwanted files
%__rm -f %{?buildroot}%{tde_datadir}/mimelnk/application/x-mplayer2.desktop

%clean
%__rm -rf %{buildroot}


%changelog
* Fri Jul 05 2013 Francois Andriot <francois.andriot@free.fr> - 2:0.10.0c-1
- Initial release for TDE 14.0.0
