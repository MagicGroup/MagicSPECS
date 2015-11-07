#
# spec file for package ktorrent (version R14)
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
%define tde_pkg ktorrent
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
Version:	2.2.8
Release:	%{?!preversion:1}%{?preversion:0_%{preversion}}%{?dist}.1
Summary:	BitTorrent client for Trinity
Summary(zh_CN.UTF-8): TDE 下的 BT 客户端
Group:		Applications/Utilities
Group(zh_CN.UTF-8): 应用程序/模拟器
URL:		http://ktorrent.org

License:	GPLv2+

#Vendor:		Trinity Desktop
#Packager:	Francois Andriot <francois.andriot@free.fr>

Prefix:		%{tde_prefix}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:		%{name}-%{tde_version}%{?preversion:~%{preversion}}.tar.gz
Patch1:		%{name}-14.0.1-tqt.patch
Patch2:		%{name}-14.0.1-cjk.patch

BuildRequires:	trinity-tdelibs-devel >= %{tde_version}
BuildRequires:	trinity-tdebase-devel >= %{tde_version}
BuildRequires:	desktop-file-utils
BuildRequires:	gettext

BuildRequires:	autoconf automake libtool m4
BuildRequires:	gcc-c++
BuildRequires:	pkgconfig
BuildRequires:	fdupes

# GMP support
BuildRequires:	gmp-devel

# AVAHI support
#  Disabled on RHEL4 and RHEL5
%define with_avahi 1
BuildRequires:	trinity-avahi-tqt-devel
Requires:		trinity-avahi-tqt
BuildRequires:	avahi-devel
Requires:		avahi


%description
KTorrent is a BitTorrent program for Trinity. Its features include speed capping
(both down and up), integrated searching, UDP tracker support, preview of
certain file types (video and audio) and integration into the TDE Panel
enabling background downloading.
 
%description -l zh_CN.UTF-8
TDE 下的 BT 客户端。

##########

%prep
%setup -q -n %{name}-%{tde_version}%{?preversion:~%{preversion}}
%patch1 -p1
%patch2 -p1

%__cp -f "/usr/share/aclocal/libtool.m4" "admin/libtool.m4.in"
%__cp -f "/usr/share/libtool/config/ltmain.sh" "admin/ltmain.sh" || %__cp -f "/usr/share/libtool/ltmain.sh" "admin/ltmain.sh"
%__make -f "admin/Makefile.common"


%build
unset QTDIR QTINC QTLIB
export PATH="%{tde_bindir}:${PATH}"

%configure \
  --prefix="%{tde_prefix}" \
  --exec-prefix="%{tde_prefix}" \
  --bindir="%{tde_bindir}" \
  --datadir="%{tde_datadir}" \
  --libdir="%{tde_libdir}" \
  --mandir="%{tde_mandir}" \
  --includedir="%{tde_tdeincludedir}" \
  \
  --disable-dependency-tracking \
  --disable-debug \
  --enable-final \
  --enable-new-ldflags \
  --enable-closure \
  --enable-rpath \
  --disable-gcc-hidden-visibility \
  \
  %{?!with_avahi:--without-avahi}


# Not SMP safe !
%__make


%install
export PATH="%{tde_bindir}:${PATH}"
%__rm -rf "%{buildroot}"
%__make install DESTDIR="%{buildroot}"
magic_rpm_clean.sh
%find_lang %{tde_pkg} || :

# Unwanted files
%__rm -f "%{?buildroot}%{tde_libdir}/libktorrent.so"


%clean
%__rm -rf "%{buildroot}"


%post
update-desktop-database %{tde_tdeappdir} > /dev/null
touch --no-create %{tde_datadir}/icons/hicolor || :
gtk-update-icon-cache --quiet %{tde_datadir}/icons/hicolor || :
/sbin/ldconfig || :

%postun
update-desktop-database %{tde_tdeappdir} > /dev/null
touch --no-create %{tde_datadir}/icons/hicolor || :
gtk-update-icon-cache --quiet %{tde_datadir}/icons/hicolor || :
/sbin/ldconfig || :


%files -f %{tde_pkg}.lang
%defattr(-,root,root,-)
%{tde_bindir}/ktcachecheck
%{tde_bindir}/ktorrent
%{tde_bindir}/ktshell
%{tde_bindir}/kttorinfo
%{tde_bindir}/ktupnptest
%{tde_libdir}/libktorrent-%{version}.so
%{tde_libdir}/libktorrent.la
%{tde_tdelibdir}/ktinfowidgetplugin.la
%{tde_tdelibdir}/ktinfowidgetplugin.so
%{tde_tdelibdir}/ktipfilterplugin.la
%{tde_tdelibdir}/ktipfilterplugin.so
%{tde_tdelibdir}/ktlogviewerplugin.la
%{tde_tdelibdir}/ktlogviewerplugin.so
%{tde_tdelibdir}/ktpartfileimportplugin.la
%{tde_tdelibdir}/ktpartfileimportplugin.so
%{tde_tdelibdir}/ktrssfeedplugin.la
%{tde_tdelibdir}/ktrssfeedplugin.so
%{tde_tdelibdir}/ktscanfolderplugin.la
%{tde_tdelibdir}/ktscanfolderplugin.so
%{tde_tdelibdir}/ktschedulerplugin.la
%{tde_tdelibdir}/ktschedulerplugin.so
%{tde_tdelibdir}/ktsearchplugin.la
%{tde_tdelibdir}/ktsearchplugin.so
%{tde_tdelibdir}/ktstatsplugin.la
%{tde_tdelibdir}/ktstatsplugin.so
%{tde_tdelibdir}/ktupnpplugin.la
%{tde_tdelibdir}/ktupnpplugin.so
%{tde_tdelibdir}/ktwebinterfaceplugin.la
%{tde_tdelibdir}/ktwebinterfaceplugin.so
%{tde_tdeappdir}/ktorrent.desktop
%{tde_datadir}/apps/ktorrent/
%{tde_datadir}/config.kcfg/*.kcfg
%{tde_datadir}/icons/hicolor/*/*/*.png
%{tde_datadir}/icons/hicolor/*/*/*.svgz
%{tde_datadir}/services/*.desktop
%{tde_datadir}/servicetypes/ktorrentplugin.desktop
%{tde_tdedocdir}/HTML/en/ktorrent/

%if 0%{?with_avahi}
%{tde_tdelibdir}/ktzeroconfplugin.la
%{tde_tdelibdir}/ktzeroconfplugin.so
%endif


%changelog
* Thu Nov 05 2015 Liu Di <liudidi@gmail.com> - 2:2.2.8-1.1
- 为 Magic 3.0 重建

* Fri Jul 05 2013 Francois Andriot <francois.andriot@free.fr> - 2:2.2.8-1
- Initial release for TDE 14.0.0
