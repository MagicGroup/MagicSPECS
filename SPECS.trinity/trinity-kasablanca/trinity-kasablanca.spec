#
# spec file for package kasablanca (version R14)
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
%define tde_pkg kasablanca
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
Version:		0.4.0.2
Release:		%{?!preversion:1}%{?preversion:0_%{preversion}}%{?dist}%{?_variant}.1
Summary:		Graphical FTP client for Trinity
Summary(zh_CN.UTF-8): TDE 下的图形 FTP 客户端
Group:			Applications/Internet 
Group(zh_CN.UTF-8): 应用程序/互联网
Url:			http://kasablanca.berlios.de/ 

License:	GPLv2+

#Vendor:		Trinity Desktop
#Packager:	Francois Andriot <francois.andriot@free.fr>

Prefix:			%{_prefix}
BuildRoot:		%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:		%{name}-%{tde_version}%{?preversion:~%{preversion}}.tar.gz
Patch0:			%{tde_pkg}-14.0.0.patch
Patch1:		%{name}-14.0.1-tqt.patch

BuildRequires:	trinity-tdelibs-devel >= %{tde_version}
BuildRequires:	trinity-tdebase-devel >= %{tde_version}
BuildRequires:	desktop-file-utils

BuildRequires:	gettext 

BuildRequires:	autoconf automake libtool m4
BuildRequires:	gcc-c++
BuildRequires:	pkgconfig

# OPENSSL support
BuildRequires:	openssl-devel

# UTEMPTER support
BuildRequires:	libutempter-devel

%description
Kasablanca is an ftp client, among its features are currently: 
* ftps encryption via AUTH TLS
* fxp (direct server to server transfer), supporting alternative mode.
* advanced bookmarking system.
* fast responsive multithreaded engine.
* concurrent connections to multiple hosts.
* interactive transfer queue, movable by drag and drop.
* small nifty features, like a skiplist.

%description -l zh_CN.UTF-8
TDE 下的 FTP 客户端。支持 ftps, fxp 等。

##########

%prep
%setup -q -n %{name}-%{tde_version}%{?preversion:~%{preversion}}
%patch0 -p1 -b .orig
%patch1 -p1

%__cp -f "/usr/share/aclocal/libtool.m4" "admin/libtool.m4.in"
%__cp -f "/usr/share/libtool/config/ltmain.sh" "admin/ltmain.sh" || %__cp -f "/usr/share/libtool/ltmain.sh" "admin/ltmain.sh"
%__make -f "admin/Makefile.common"


%build
unset QTDIR QTINC QTLIB
export PATH="%{tde_bindir}:${PATH}"

## Needed(?) for older/legacy setups, harmless otherwise
if pkg-config openssl ; then
	export CPPFLAGS="$CPPFLAGS $(pkg-config --cflags-only-I openssl)"
fi

%configure \
  --prefix=%{tde_prefix} \
  --exec-prefix=%{tde_prefix} \
  --bindir=%{tde_bindir} \
  --libdir=%{tde_libdir} \
  --includedir=%{tde_tdeincludedir} \
  --datadir=%{tde_datadir} \
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
%__rm -rf $RPM_BUILD_ROOT 
%__make install DESTDIR=$RPM_BUILD_ROOT

magic_rpm_clean.sh
# locale's
%find_lang %{tde_pkg} || :

%clean
%__rm -rf $RPM_BUILD_ROOT 


%post
touch --no-create %{tde_datadir}/icons/hicolor &> /dev/null || :


%postun
if [ $1 -eq 0 ] ; then
  touch --no-create %{_datadir}/icons/hicolor &> /dev/null
  gtk-update-icon-cache %{tde_datadir}/icons/hicolor &> /dev/null || :
fi


%posttrans
gtk-update-icon-cache %{tde_datadir}/icons/hicolor &> /dev/null || :


%files 
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README 
%{tde_bindir}/kasablanca
%{tde_datadir}/apps/kasablanca/
%{tde_datadir}/config.kcfg/kbconfig.kcfg
%{tde_datadir}/icons/hicolor/*/apps/kasablanca.png
%{tde_tdedocdir}/HTML/en/kasablanca/
%{tde_tdeappdir}/kasablanca.desktop


%changelog
* Wed Nov 04 2015 Liu Di <liudidi@gmail.com> - 2:0.4.0.2-1.1
- 为 Magic 3.0 重建

* Fri Jul 05 2013 Francois Andriot <francois.andriot@free.fr> - 2:0.4.0.2-1
- Initial release for TDE 14.0.0
