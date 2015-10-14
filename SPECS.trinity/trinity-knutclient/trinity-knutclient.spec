#
# spec file for package knutclient (version R14)
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
%define tde_pkg knutclient
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


Name:		trinity-%{tde_pkg}
Epoch:		%{tde_epoch}
Version:	0.9.5
Release:	%{?!preversion:0}%{?preversion:1_%{preversion}}%{?dist}
Summary:	A TDE GUI that displays UPS statistics from NUT's upsd [Trinity]
Summary(zh_CN.UTF-8): 从 NUT 的 upsd 服务中显示 UPS 统计信息的程序
Group:		Applications/Utilities
Group(zh_CN.UTF-8): 应用程序/工具
URL:		http://www.knut.noveradsl.cz/knutclient/

License:	GPLv2+

#Vendor:		Trinity Desktop
#Packager:	Francois Andriot <francois.andriot@free.fr>

Prefix:		%{tde_prefix}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:		%{name}-%{tde_version}%{?preversion:~%{preversion}}.tar.gz
Patch1:		%{name}-14.0.1-tqt.patch

BuildRequires:	trinity-tdelibs-devel >= %{tde_version}
BuildRequires:	trinity-tdebase-devel >= %{tde_version}
BuildRequires:	desktop-file-utils

BuildRequires:	autoconf automake libtool m4
BuildRequires:	gcc-c++
BuildRequires:	pkgconfig
BuildRequires:	fdupes

%description
KNutClient monitors UPS statistics through the NUT (Network UPS Tools,
http://www.networkupstools.org/) framework on Linux and other systems. This
information, presented in a nice visual format, can be invaluable on
stations using an UPS.

%description -l zh_CN.UTF-8
UPS 工具。

##########


%prep
%setup -q -n %{name}-%{tde_version}%{?preversion:~%{preversion}}
%patch1 -p1

# Fix permissions
chmod 644 AUTHORS README TODO COPYING ChangeLog

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
  --datadir=%{tde_datadir} \
  --libdir=%{tde_libdir} \
  --mandir=%{tde_mandir} \
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
magic_rpm_clean.sh
%find_lang %{tde_pkg} || :

# Links duplicate files
%fdupes "%{?buildroot}%{tde_datadir}"


%clean
%__rm -rf %{buildroot}


%post
for f in hicolor locolor; do
  touch --no-create %{tde_datadir}/icons/${f} || :
  gtk-update-icon-cache --quiet %{tde_datadir}/icons/${f} || :
done

%postun
for f in hicolor locolor; do
  touch --no-create %{tde_datadir}/icons/${f} || :
  gtk-update-icon-cache --quiet %{tde_datadir}/icons/${f} || :
done


%files 
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING README
%{tde_bindir}/knutclient
%{tde_datadir}/applnk/Utilities/knutclient.desktop
%{tde_datadir}/apps/knutclient/knutclientui.rc
%{tde_datadir}/apps/knutclient
%{tde_tdedocdir}/HTML/cs/knutclient
%{tde_tdedocdir}/HTML/en/knutclient
%{tde_datadir}/icons/hicolor/*/apps/*.png
%{tde_datadir}/icons/locolor/*/apps/*.png

%changelog
* Fri Jul 05 2013 Francois Andriot <francois.andriot@free.fr> - 2:0.9.5-1
- Initial release for TDE 14.0.0
