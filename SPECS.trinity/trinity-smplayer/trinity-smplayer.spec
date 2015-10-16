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
%define tde_pkg smplayer
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

%define kde_support 1


Name:			trinity-%{tde_pkg}
Epoch:			%{tde_epoch}
Version:		0.8.8
Release:		%{?!preversion:1}%{?preversion:0_%{preversion}}%{?dist}%{?_variant}
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

Source1:        smplayer.desktop

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

Requires:	mplayer

%description
SMPlayer intends to be a complete front-end for MPlayer, from basic features 
like playing videos, DVDs, and VCDs to more advanced features like support 
for Mplayer filters and more. One of the main features is the ability to 
remember the state of a played file, so when you play it later it will resume 
at the same point and with the same settings. smplayer is developed with 
the Qt toolkit, so it's multi-platform.

%description -l zh_CN.UTF-8
SMPlayer 意在成为 MPlayer 的完整前端，从基本的特性，比如播放视频，
DVD，和 VCD 到更多高级特性，像对 MPlayer 过滤器的支持还有更多。
一个主要特性是可以记忆播放文件的位置，这样您就可以以相同的设置
重新在同一位置恢复播放。smplayer 是用 Qt 工具开发的，所以它也是
跨平台的。


##########

%prep
%setup -q -n %{name}-%{tde_version}%{?preversion:~%{preversion}}

sed -i 's!/opt/trinity/lib!/opt/trinity/%{_lib}!g' src/smplayer.pro

%build
unset QTDIR QTINC QTLIB
export PATH="%{tde_bindir}:${PATH}"

%{__make} PREFIX=%{tde_prefix} KDE_SUPPORT=%{kde_support} 

%install
export PATH="%{tde_bindir}:${PATH}"
%__rm -rf $RPM_BUILD_ROOT

%{__make} PREFIX=%{tde_prefix} DESTDIR=%{buildroot} install
%{__rm} -f %{buildroot}%{tde_datadir}/applications/smplayer.desktop
%{__rm} -f %{buildroot}%{tde_datadir}/applications/kde/smplayer.desktop
%{__install} -D -m 644 %{SOURCE1} %{buildroot}%{tde_datadir}/applications/kde/smplayer.desktop

magic_rpm_clean.sh
## File lists
# locale's

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{tde_bindir}/*
%{tde_datadir}/*


%changelog
* Fri Jul 05 2013 Francois Andriot <francois.andriot@free.fr> - 2:0.8.8-1
- Initial release for TDE 14.0.0
