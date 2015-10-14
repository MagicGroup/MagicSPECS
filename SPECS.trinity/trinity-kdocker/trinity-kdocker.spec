#
# spec file for package kchmviewer (version R14)
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
%define tde_pkg kdocker
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
Version:		1.3
Release:		%{?!preversion:1}%{?preversion:0_%{preversion}}%{?dist}%{?_variant}.1
Summary: Dock any application in the system tray
Summary(zh_CN): 将任何程序停靠在系统托盘
Group:			Applications/Utilities
Group(zh_CN.UTF-8): 应用程序/工具
URL:			http://www.trinitydesktop.org/
License:	GPLv2+

#Vendor:		Trinity Desktop
#Packager:	Francois Andriot <francois.andriot@free.fr>

Prefix:			%{_prefix}
BuildRoot:		%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:		%{name}-%{tde_version}%{?preversion:~%{preversion}}.tar.bz2

BuildRequires:	trinity-tdelibs-devel >= %{tde_version}
BuildRequires:	trinity-tdebase-devel >= %{tde_version}
BuildRequires:	desktop-file-utils

BuildRequires:	autoconf automake libtool m4
BuildRequires:	gcc-c++
BuildRequires:	pkgconfig

%description
KDocker will help you dock any application in the system tray. This means you
can dock openoffice, xmms, firefox, thunderbolt, eclipse, anything!

KDocker supports the KDE System Tray Protocol and the System Tray Protocol from
freedesktop.org

It works for KDE, GNOME, XFCE, and probably many more.

%description -l zh_CN
KDocker 帮助您停靠任何程序至系统托盘。这意味着您可以停靠 openoffice、xmms、firefox、thunderbolt、eclipse 和任何东西！

KDocker 支持 KDE 系统托盘协议和来自 freedesktop.org 的系统托盘

它能够在 KDE、GNOME、XFCE 桌面下运行，或许更多。

##########

%prep
%setup -q -n %{name}-%{tde_version}%{?preversion:~%{preversion}}

%build
unset QTDIR QTINC QTLIB
export PATH="%{tde_bindir}:${PATH}"

# Specific path for RHEL4
if [ -d /usr/X11R6 ]; then
  export RPM_OPT_FLAGS="${RPM_OPT_FLAGS} -I/usr/X11R6/include -L/usr/X11R6/%{_lib}"
fi

/usr/bin/tqmake

%__make 


%install
export PATH="%{tde_bindir}:${PATH}"
%__rm -rf %{buildroot}
%__make install DESTDIR=%{buildroot}

magic_rpm_clean.sh

# Removes useless files
%__rm -f %{?buildroot}%{tde_libdir}/*.a

%clean
%__rm -rf %{buildroot}


%post

%postun

%files 
%defattr(-,root,root,-)
%{tde_bindir}/*
%{tde_datadir}/*


%changelog
* Sat Oct 10 2015 Liu Di <liudidi@gmail.com> - 2:3.1.2-1.1
- 为 Magic 3.0 重建

* Fri Jul 05 2013 Francois Andriot <francois.andriot@free.fr> - 2:3.1.2-1
- Initial release for TDE 14.0.0
