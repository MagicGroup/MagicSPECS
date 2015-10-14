#
# spec file for package kcpuload (version R14)
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
%define tde_pkg kcpuload
%define tde_prefix /opt/trinity
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
Version:		2.00
Release:		%{?!preversion:1}%{?preversion:0_%{preversion}}%{?dist}%{?_variant}
Summary:		CPU meter for Kicker [Trinity]
Summary(zh_CN.UTF-8): TDE 下的 CPU 监视器
Group:			Applications/Utilities
Group(zh_CN.UTF-8): 应用程序/工具
URL:			http://www.trinitydesktop.org/

License:	GPLv2+

#Vendor:		Trinity Desktop
#Packager:	Francois Andriot <francois.andriot@free.fr>

Prefix:			%{_prefix}
BuildRoot:		%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:		%{name}-%{tde_version}%{?preversion:~%{preversion}}.tar.gz

Patch1:		%{name}-14.0.1-tqt.patch
BuildRequires:	trinity-tdelibs-devel >= %{tde_version}
BuildRequires:	trinity-tdebase-devel >= %{tde_version}
BuildRequires:	desktop-file-utils

BuildRequires:	gettext

BuildRequires:	autoconf automake libtool m4
BuildRequires:	gcc-c++
BuildRequires:	pkgconfig

%description
KCPULoad is a small program for Kicker (the TDE panel).  It shows a
recent history of CPU usage in the form of one or two configurable
diagrams in the system tray.  These diagrams have settings for colours
and various different styles.

KCPULoad has support for SMP and separate user/system loads.

%description -l zh_CN.UTF-8
TDE 下的 CPU 监视器。

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
  \
  --disable-dependency-tracking \
  --disable-debug \
  --enable-new-ldflags \
  --enable-final \
  --enable-closure \
  --enable-rpath \
  --disable-gcc-hidden-visibility

%__make %{?_smp_mflags}


%install
export PATH="%{tde_bindir}:${PATH}"
%__rm -rf %{buildroot}
%__make install DESTDIR=%{buildroot}

# Fix desktop icon location
%__mkdir_p "%{?buildroot}%{tde_tdeappdir}"
%__mv -f "%{?buildroot}%{tde_datadir}/applnk/System/%{tde_pkg}.desktop" "%{?buildroot}%{tde_tdeappdir}"
magic_rpm_clean.sh

%clean
%__rm -rf %{buildroot}


%post
for f in crystalsvg locolor ; do
  touch --no-create %{tde_datadir}/icons/${f} || :
  gtk-update-icon-cache --quiet %{tde_datadir}/icons/${f} || :
done

%postun
for f in crystalsvg locolor ; do
  touch --no-create %{tde_datadir}/icons/${f} || :
  gtk-update-icon-cache --quiet %{tde_datadir}/icons/${f} || :
done


%files
%defattr(-,root,root,-)
%{tde_bindir}/kcpuload
%{tde_tdeappdir}/kcpuload.desktop
%{tde_datadir}/apps/kcpuload/
%{tde_datadir}/icons/crystalsvg/*/apps/kcpuload.png
%{tde_datadir}/icons/locolor/*/apps/kcpuload.png
%{tde_tdedocdir}/HTML/en/kcpuload/


%changelog
* Fri Jul 05 2013 Francois Andriot <francois.andriot@free.fr> - 2:2.00-1
- Initial release for TDE 14.0.0
