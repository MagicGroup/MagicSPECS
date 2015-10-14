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
%define tde_pkg krecord
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

%define debug_package %{nil}

Name:			trinity-%{tde_pkg}
Epoch:			%{tde_epoch}
Version:		1.16
Release:		%{?!preversion:1}%{?preversion:0_%{preversion}}%{?dist}%{?_variant}.2
Summary:        Sound recorder for KDE
Summary(zh_CN.UTF-8): KDE 下的录音机

Group:          Applications/Multimedia
Group(zh_CN.UTF-8):     应用程序/多媒体
URL:			http://www.trinitydesktop.org/
License:	GPLv2+

#Vendor:		Trinity Desktop
#Packager:	Francois Andriot <francois.andriot@free.fr>

Prefix:			%{_prefix}
BuildRoot:		%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:		%{name}-%{tde_version}%{?preversion:~%{preversion}}.tar.gz
Source1:	krecord.desktop

BuildRequires:	trinity-tdelibs-devel >= %{tde_version}
BuildRequires:	trinity-tdebase-devel >= %{tde_version}
BuildRequires:	desktop-file-utils

BuildRequires:	autoconf automake libtool m4
BuildRequires:	gcc-c++
BuildRequires:	pkgconfig

%description
A simple KDE interface to record sounds.

%description -l zh_CN.UTF-8
KDE 下的一个简单的录音机。

##########

%prep
%setup -q -n %{name}-%{tde_version}%{?preversion:~%{preversion}}

%build
unset QTDIR QTINC QTLIB
export PATH="%{tde_bindir}:${PATH}"
export QTDIR="/usr"
export TDEDIR=%{tde_prefix}

%__make 


%install
export PATH="%{tde_bindir}:${PATH}"
%__rm -rf %{buildroot}
export TDEDIR=%{tde_prefix}
%__make install DESTDIR=%{buildroot}

install -d $RPM_BUILD_ROOT%{tde_tdeappdir}
install %{SOURCE1} $RPM_BUILD_ROOT%{tde_tdeappdir}
magic_rpm_clean.sh
rm -f $RPM_BUILD_ROOT%{tde_datadir}/applnk/Multimedia/krecord.desktop
rm -f $RPM_BUILD_ROOT%{tde_datadir}/doc/kde/HTML/en/krecord/index.html

%clean
%__rm -rf %{buildroot}


%post
touch --no-create %{tde_datadir}/icons/crystalsvg || :
gtk-update-icon-cache --quiet %{tde_datadir}/icons/crystalsvg || :


%postun
touch --no-create %{tde_datadir}/icons/crystalsvg || :
gtk-update-icon-cache --quiet %{tde_datadir}/icons/crystalsvg || :


%files 
%defattr(-,root,root,-)
%{tde_bindir}/*
%{tde_datadir}/*

%changelog
* Tue Oct 13 2015 Liu Di <liudidi@gmail.com> - 2:1.16-1.2
- 为 Magic 3.0 重建

* Sat Oct 10 2015 Liu Di <liudidi@gmail.com> - 2:3.1.2-1.1
- 为 Magic 3.0 重建

* Fri Jul 05 2013 Francois Andriot <francois.andriot@free.fr> - 2:3.1.2-1
- Initial release for TDE 14.0.0
